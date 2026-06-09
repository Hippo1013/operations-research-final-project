#!/usr/bin/env python3
"""Solve the extended multi-period launch-site model.

The extended model is a mixed-integer nonlinear
program. This script implements a transparent computational approximation:

1. enumerate total construction time from T = 50 onward;
2. split each T into 20% / 50% / 30% construction phases;
3. satisfy the 10% / 60% / 30% material delivery proportions exactly;
4. use maximum elevator capacity first in every phase;
5. allocate the required rocket launches over launch sites and years by a
   convex quadratic dispatch approximation for nonlinear environmental
   pressure.

No hard per-launch-site annual launch limits are imposed.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from solve_mixed_model import FIGURE_DIR, PARAMS, RESULT_DIR, SCENARIOS


T_MIN = 50
SEARCH_PATIENCE_YEARS = 30
SEARCH_GUARD_MAX_YEAR = 250
A_E = 0.90
A_R = 0.98
TIME_TARGET_YEAR = 75.0

# Scenario assumptions for 2050+ technology progress.
LAMBDA_COST = 0.005
LAMBDA_EMISSION = 0.003

# Nonlinear environmental pressure model assumptions.
ALPHA_DIRECT = 1.0
BETA_PRESSURE = 2.5e-11

STAGE_RATIOS = (0.10, 0.60, 0.30)
STAGE_TIME_BREAKS = (0.20, 0.70)

SITE_SENSITIVITY = {
    "Alaska": 3.5,
    "California": 4.0,
    "Texas": 5.0,
    "Florida": 4.0,
    "Virginia": 4.0,
    "Kazakhstan": 4.5,
    "French Guiana": 3.5,
    "Satish Dhawan": 4.0,
    "Taiyuan": 4.0,
    "Mahia": 3.5,
}

SITE_LABELS = list(SITE_SENSITIVITY)


@dataclass(frozen=True)
class Step5Targets:
    cost_target_trillion: float
    time_target_year: float
    env_target_billion: float


TARGETS = Step5Targets(
    cost_target_trillion=PARAMS.cost_target,
    time_target_year=TIME_TARGET_YEAR,
    env_target_billion=PARAMS.emission_target,
)


def site_sensitivity_norm() -> np.ndarray:
    values = np.array([SITE_SENSITIVITY[name] for name in SITE_LABELS], dtype=float)
    return values / values.mean()


def site_recovery_rho() -> np.ndarray:
    """Map environmental sensitivity to residual environmental pressure."""

    raw = np.array([SITE_SENSITIVITY[name] for name in SITE_LABELS], dtype=float)
    return 0.50 + 0.08 * (raw - raw.min()) / (raw.max() - raw.min())


def yearly_rocket_cost(T: int) -> np.ndarray:
    years = np.arange(T, dtype=float)
    return PARAMS.rocket_cost_trillion_per_launch * (1.0 - LAMBDA_COST) ** years


def yearly_rocket_emission(T: int) -> np.ndarray:
    years = np.arange(T, dtype=float)
    return PARAMS.rocket_emission_billion_per_launch * (1.0 - LAMBDA_EMISSION) ** years


def stage_years(T: int) -> list[np.ndarray]:
    p1_end = int(np.floor(STAGE_TIME_BREAKS[0] * T))
    p2_end = int(np.floor(STAGE_TIME_BREAKS[1] * T))
    return [
        np.arange(0, p1_end, dtype=int),
        np.arange(p1_end, p2_end, dtype=int),
        np.arange(p2_end, T, dtype=int),
    ]


def allocate_convex_integer(total: int, linear: np.ndarray, quad: np.ndarray) -> np.ndarray:
    """Minimize sum linear*x + quad*x^2 subject to integer x>=0 and sum x=total."""

    if total <= 0:
        return np.zeros_like(linear, dtype=np.int64)

    linear = linear.astype(float)
    quad = np.maximum(quad.astype(float), 1e-18)

    low = float(linear.min())
    high = float((linear + 2.0 * quad * total).max())
    for _ in range(90):
        mu = 0.5 * (low + high)
        x = np.maximum(0.0, (mu - linear) / (2.0 * quad))
        if x.sum() < total:
            low = mu
        else:
            high = mu

    x = np.maximum(0.0, (high - linear) / (2.0 * quad))
    base = np.floor(x).astype(np.int64)
    remainder = int(total - base.sum())

    if remainder > 0:
        marginal_add = linear + quad * (2.0 * base + 1.0)
        candidates = np.argpartition(marginal_add, remainder - 1)[:remainder]
        base[candidates] += 1
    elif remainder < 0:
        removable = np.flatnonzero(base > 0)
        marginal_remove = linear[removable] + quad[removable] * (2.0 * base[removable] - 1.0)
        take = min(-remainder, len(removable))
        candidates = removable[np.argpartition(-marginal_remove, take - 1)[:take]]
        base[candidates] -= 1

    if int(base.sum()) != total:
        raise RuntimeError(f"Integer allocation failed: expected {total}, got {base.sum()}")
    return base


def compute_pressure(launches: np.ndarray, rho: np.ndarray) -> np.ndarray:
    n_sites, T = launches.shape
    pressure = np.zeros((n_sites, T), dtype=float)
    for i in range(n_sites):
        last = 0.0
        for t in range(T):
            last = rho[i] * last + launches[i, t]
            pressure[i, t] = last
    return pressure


def solve_fixed_time(
    T: int,
    scenario: str,
    label: str,
    weights: tuple[float, float, float],
) -> tuple[dict[str, float | int | str], pd.DataFrame, pd.DataFrame]:
    p = PARAMS
    w_cost, w_time, w_env = weights
    sensitivity = site_sensitivity_norm()
    rho = site_recovery_rho()
    rocket_cost = yearly_rocket_cost(T)
    rocket_emission = yearly_rocket_emission(T)
    effective_payload = A_R * p.rocket_payload_mt_per_launch
    elevator_capacity = A_E * p.elevator_capacity_mt_per_year

    launches = np.zeros((len(SITE_LABELS), T), dtype=np.int64)
    y_elevator = np.zeros(T, dtype=float)
    pressure = np.zeros_like(launches, dtype=float)

    stage_rows: list[dict[str, float | int | str]] = []

    for stage_idx, years in enumerate(stage_years(T), start=1):
        demand = STAGE_RATIOS[stage_idx - 1] * p.material_demand_mt
        max_elevator = elevator_capacity * len(years)
        rocket_launches = int(np.ceil(max(0.0, demand - max_elevator) / effective_payload))
        elevator_amount = demand - rocket_launches * effective_payload
        if elevator_amount < -1e-9 or elevator_amount - max_elevator > 1e-9:
            raise RuntimeError(f"Infeasible stage allocation for T={T}, stage={stage_idx}")
        y_elevator[years] = elevator_amount / len(years)

        if rocket_launches > 0:
            slot_years = np.repeat(years, len(SITE_LABELS))
            slot_sites = np.tile(np.arange(len(SITE_LABELS)), len(years))

            linear_cost = w_cost * rocket_cost[slot_years] / TARGETS.cost_target_trillion
            linear_env = (
                w_env
                * sensitivity[slot_sites]
                * ALPHA_DIRECT
                * rocket_emission[slot_years]
                / TARGETS.env_target_billion
            )
            pressure_adjustment = (
                2.0
                * w_env
                * sensitivity[slot_sites]
                * BETA_PRESSURE
                * pressure[slot_sites, slot_years]
                / TARGETS.env_target_billion
            )
            linear = linear_cost + linear_env + pressure_adjustment
            quad = (
                w_env
                * sensitivity[slot_sites]
                * BETA_PRESSURE
                / np.maximum(1.0 - rho[slot_sites] ** 2, 1e-9)
                / TARGETS.env_target_billion
            )

            allocation = allocate_convex_integer(rocket_launches, linear, quad)
            for amount, site, year in zip(allocation, slot_sites, slot_years):
                if amount:
                    launches[site, year] += int(amount)

            pressure = compute_pressure(launches, rho)

        stage_rows.append(
            {
                "scenario": scenario,
                "scenario_label": label,
                "T": T,
                "stage": stage_idx,
                "stage_year_count": len(years),
                "stage_start_year": int(years[0] + 1),
                "stage_end_year": int(years[-1] + 1),
                "stage_demand_mt": demand,
                "stage_elevator_mt": float(y_elevator[years].sum()),
                "stage_rocket_delivery_mt": float(effective_payload * launches[:, years].sum()),
                "stage_rocket_launches": int(launches[:, years].sum()),
            }
        )

    pressure = compute_pressure(launches, rho)
    y_rocket = effective_payload * launches.sum(axis=0)

    cost = float(p.elevator_cost_trillion_per_mt * y_elevator.sum() + (launches.sum(axis=0) * rocket_cost).sum())
    physical_emission = float(p.elevator_emission_billion_per_mt * y_elevator.sum() + (launches.sum(axis=0) * rocket_emission).sum())
    direct_site_env = float(
        (
            sensitivity[:, None]
            * ALPHA_DIRECT
            * launches
            * rocket_emission[None, :]
        ).sum()
    )
    nonlinear_env = float((sensitivity[:, None] * BETA_PRESSURE * pressure**2).sum())
    env_damage = float(p.elevator_emission_billion_per_mt * y_elevator.sum() + direct_site_env + nonlinear_env)

    d_cost_plus = max(cost - TARGETS.cost_target_trillion, 0.0)
    d_time_plus = max(T - TARGETS.time_target_year, 0.0)
    d_env_plus = max(env_damage - TARGETS.env_target_billion, 0.0)
    objective = (
        w_cost * d_cost_plus / TARGETS.cost_target_trillion
        + w_time * d_time_plus / TARGETS.time_target_year
        + w_env * d_env_plus / TARGETS.env_target_billion
    )

    result = {
        "scenario": scenario,
        "scenario_label": label,
        "T": T,
        "w_cost": w_cost,
        "w_time": w_time,
        "w_env": w_env,
        "x_elevator_mt": float(y_elevator.sum()),
        "x_rocket_mt": float(y_rocket.sum()),
        "rocket_launches": int(launches.sum()),
        "cost_trillion_usd": cost,
        "physical_emission_billion_tco2": physical_emission,
        "environment_damage_billion": env_damage,
        "direct_site_environment_billion": direct_site_env,
        "nonlinear_environment_billion": nonlinear_env,
        "objective_value": float(objective),
        "d_cost_plus": float(d_cost_plus),
        "d_time_plus": float(d_time_plus),
        "d_environment_plus": float(d_env_plus),
        "lambda_cost": LAMBDA_COST,
        "lambda_emission": LAMBDA_EMISSION,
        "beta_pressure": BETA_PRESSURE,
        "a_e": A_E,
        "a_r": A_R,
    }

    schedule_rows = []
    for i, site in enumerate(SITE_LABELS):
        for t in range(T):
            if launches[i, t] > 0 or pressure[i, t] > 1e-9:
                schedule_rows.append(
                    {
                        "scenario": scenario,
                        "scenario_label": label,
                        "T": T,
                        "site": site,
                        "year": t + 1,
                        "rocket_launches": int(launches[i, t]),
                        "pressure": float(pressure[i, t]),
                        "site_sensitivity": SITE_SENSITIVITY[site],
                        "site_sensitivity_norm": float(sensitivity[i]),
                    }
                )

    return result, pd.DataFrame(stage_rows), pd.DataFrame(schedule_rows)


def solve_scenario(
    scenario: str,
    label: str,
    weights: tuple[float, float, float],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rows = []
    stage_frames = []
    best_schedule = None
    best_objective = np.inf
    stale_years = 0

    for T in range(T_MIN, SEARCH_GUARD_MAX_YEAR + 1):
        result, stages, schedule = solve_fixed_time(T, scenario, label, weights)
        rows.append(result)
        stage_frames.append(stages)
        if result["objective_value"] < best_objective - 1e-12:
            best_objective = float(result["objective_value"])
            stale_years = 0
            best_schedule = schedule
        else:
            stale_years += 1
        if T > TARGETS.time_target_year and stale_years >= SEARCH_PATIENCE_YEARS:
            break

    by_time = pd.DataFrame(rows)
    best_T = int(by_time.loc[by_time["objective_value"].idxmin(), "T"])
    best_stage = pd.concat(stage_frames, ignore_index=True)
    best_stage = best_stage[best_stage["T"] == best_T].copy()
    if best_schedule is None:
        best_schedule = pd.DataFrame()
    return by_time, best_stage, best_schedule


def plot_objective_by_time(by_time: pd.DataFrame) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    for scenario, group in by_time.groupby("scenario", sort=False):
        label = str(group["scenario_label"].iloc[0])
        ax.plot(group["T"], group["objective_value"], marker="o", markersize=2.5, linewidth=1.5, label=label)
        best = group.loc[group["objective_value"].idxmin()]
        ax.scatter([best["T"]], [best["objective_value"]], s=55, zorder=4)
        ax.annotate(
            f"T={int(best['T'])}",
            (best["T"], best["objective_value"]),
            textcoords="offset points",
            xytext=(5, 5),
            fontsize=8,
        )
    ax.axvline(TARGETS.time_target_year, color="gray", linestyle="--", linewidth=1, label="Time target 75y")
    ax.set_xlabel("Candidate construction time T (years)")
    ax.set_ylabel("Step 5 objective value")
    ax.set_title("Step 5 outer enumeration: objective by construction time")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "extended_objective_by_time.png", dpi=180)
    plt.close(fig)


def plot_stage_transport(best_stages: pd.DataFrame) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    labels = []
    elevator = []
    rocket = []
    for row in best_stages.itertuples(index=False):
        labels.append(f"{row.scenario_label}\nP{row.stage}")
        elevator.append(row.stage_elevator_mt)
        rocket.append(row.stage_rocket_delivery_mt)

    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(12, 5.8))
    ax.bar(x, elevator, label="Elevator")
    ax.bar(x, rocket, bottom=elevator, label="Rocket")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.set_ylabel("Delivered material (Mt)")
    ax.set_title("Step 5 best solutions: 10/60/30 stage transport split")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "extended_stage_transport.png", dpi=180)
    plt.close(fig)


def plot_site_launches(site_summary: pd.DataFrame) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    pivot = site_summary.pivot(index="site", columns="scenario_label", values="rocket_launches").fillna(0.0)
    pivot = pivot.reindex(SITE_LABELS, fill_value=0.0)

    fig, ax = plt.subplots(figsize=(10.5, 6))
    pivot.plot(kind="barh", ax=ax)
    ax.set_xlabel("Rocket launches")
    ax.set_ylabel("Launch site")
    ax.set_title("Step 5 best solutions: launch allocation by site")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "extended_site_launches.png", dpi=180)
    plt.close(fig)


def write_markdown(best: pd.DataFrame, by_time: pd.DataFrame, site_summary: pd.DataFrame) -> None:
    lines = [
        "# 扩展多时期发射场级模型求解结果",
        "",
        f"求解方法：外层从 `T={T_MIN}` 年开始逐年枚举，不设置模型意义上的工期上界；当目标函数连续 `{SEARCH_PATIENCE_YEARS}` 年未改善后停止。内层使用凸二次调度近似分配各发射场、各年份的火箭发射次数。模型不设置单个发射场硬性年发射上限。",
        "",
        "## 情景参数",
        "",
        f"- 非完美主情景：`a_E={A_E:.2f}`，`a_R={A_R:.2f}`。",
        f"- 技术进步：火箭发射成本年下降率 `{LAMBDA_COST:.3%}`，火箭单次排放年下降率 `{LAMBDA_EMISSION:.3%}`。",
        f"- 工期目标：`T*=75` 年；成本目标 `C*=0.8C0={TARGETS.cost_target_trillion:.3f}` trillion USD；环境目标 `H*=0.6H0={TARGETS.env_target_billion:.3f}` billion。",
        f"- 环境压力残留：由发射场敏感系数映射到 `{site_recovery_rho().min():.2f}-{site_recovery_rho().max():.2f}`；非线性压力系数 `beta={BETA_PRESSURE:.2e}`。",
        f"- 程序安全保护上限：`T={SEARCH_GUARD_MAX_YEAR}` 年；本次没有触发该保护上限。",
        "",
        "## 最优结果",
        "",
        "| 情景 | 最优 T | 电梯运输 Mt | 火箭运输 Mt | 火箭发射次数 | 成本 trillion USD | CO2 billion tCO2 | 环境损害 H | 目标函数值 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in best.itertuples(index=False):
        lines.append(
            f"| {row.scenario_label} | {int(row.T)} | {row.x_elevator_mt:.3f} | "
            f"{row.x_rocket_mt:.3f} | {int(row.rocket_launches):,} | "
            f"{row.cost_trillion_usd:.3f} | {row.physical_emission_billion_tco2:.3f} | "
            f"{row.environment_damage_billion:.3f} | {row.objective_value:.6f} |"
        )

    lines.extend(
        [
            "",
            "## 发射场分配",
            "",
            "| 情景 | 发射场 | 发射次数 | 占该情景火箭发射比例 | 环境敏感系数 | 最大环境压力 |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for row in site_summary.itertuples(index=False):
        lines.append(
            f"| {row.scenario_label} | {row.site} | {int(row.rocket_launches):,} | "
            f"{row.launch_share:.2%} | {row.site_sensitivity:.1f} | {row.max_pressure:.1f} |"
        )

    lines.extend(
        [
            "",
            "## 输出文件",
            "",
            "- `result/extended_model_results.csv`：三组情景的最优解。",
            "- `result/extended_by_time.csv`：所有候选工期的目标函数与指标。",
            "- `result/extended_stage_results.csv`：最优解的 10/60/30 阶段运输量。",
            "- `result/extended_site_summary.csv`：最优解的发射场分配汇总。",
            "- `result/extended_site_year_schedule.csv`：最优解的发射场-年份调度表。",
            "- `report/figures/extended_objective_by_time.png`：外层工期枚举曲线。",
            "- `report/figures/extended_stage_transport.png`：最优解阶段运输量。",
            "- `report/figures/extended_site_launches.png`：最优解发射场分配。",
            "",
        ]
    )
    (RESULT_DIR / "extended_model_results.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    by_time_frames = []
    stage_frames = []
    schedule_frames = []
    for scenario, spec in SCENARIOS.items():
        by_time, stages, schedule = solve_scenario(scenario, spec["label"], spec["weights"])
        by_time_frames.append(by_time)
        stage_frames.append(stages)
        schedule_frames.append(schedule)

    by_time = pd.concat(by_time_frames, ignore_index=True)
    best_idx = by_time.groupby("scenario")["objective_value"].idxmin()
    best = by_time.loc[best_idx].sort_values("scenario").reset_index(drop=True)
    best_stages = pd.concat(stage_frames, ignore_index=True)
    schedules = pd.concat(schedule_frames, ignore_index=True)

    best_keys = best[["scenario", "T"]]
    best_stages = best_stages.merge(best_keys, on=["scenario", "T"], how="inner")
    schedules = schedules.merge(best_keys, on=["scenario", "T"], how="inner")

    site_summary = (
        schedules.groupby(["scenario", "scenario_label", "site", "site_sensitivity"], as_index=False)
        .agg(rocket_launches=("rocket_launches", "sum"), max_pressure=("pressure", "max"))
        .merge(best[["scenario", "rocket_launches"]], on="scenario", suffixes=("", "_total"))
    )
    site_summary["launch_share"] = site_summary["rocket_launches"] / site_summary["rocket_launches_total"]
    site_summary = site_summary.drop(columns=["rocket_launches_total"])

    by_time.to_csv(RESULT_DIR / "extended_by_time.csv", index=False)
    best.to_csv(RESULT_DIR / "extended_model_results.csv", index=False)
    best_stages.to_csv(RESULT_DIR / "extended_stage_results.csv", index=False)
    schedules.to_csv(RESULT_DIR / "extended_site_year_schedule.csv", index=False)
    site_summary.to_csv(RESULT_DIR / "extended_site_summary.csv", index=False)

    plot_objective_by_time(by_time)
    plot_stage_transport(best_stages)
    plot_site_launches(site_summary)
    write_markdown(best, by_time, site_summary)

    print(best.to_string(index=False))
    print()
    print("Wrote:")
    for path in [
        RESULT_DIR / "extended_model_results.csv",
        RESULT_DIR / "extended_by_time.csv",
        RESULT_DIR / "extended_stage_results.csv",
        RESULT_DIR / "extended_site_summary.csv",
        RESULT_DIR / "extended_site_year_schedule.csv",
        RESULT_DIR / "extended_model_results.md",
        FIGURE_DIR / "extended_objective_by_time.png",
        FIGURE_DIR / "extended_stage_transport.png",
        FIGURE_DIR / "extended_site_launches.png",
    ]:
        print(f"- {path}")


if __name__ == "__main__":
    main()
