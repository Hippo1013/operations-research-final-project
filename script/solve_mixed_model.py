#!/usr/bin/env python3
"""Solve and visualize the mixed transport goal-programming model.

The model follows the project modeling document:
- no per-launch-site variables or launch-site capacity constraints;
- rocket launch count is the only integer variable.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import Bounds, LinearConstraint, milp


ROOT = Path(__file__).resolve().parents[1]
RESULT_DIR = ROOT / "result"
FIGURE_DIR = ROOT / "report" / "figures"


@dataclass(frozen=True)
class Parameters:
    # Scaled units:
    # material: million metric tons (Mt)
    # cost: trillion USD
    # emissions: billion tCO2
    # time: years
    material_demand_mt: float = 100.0
    elevator_capacity_mt_per_year: float = 0.537
    rocket_payload_mt_per_launch: float = 0.000125
    elevator_cost_trillion_per_mt: float = 0.1
    rocket_cost_trillion_per_launch: float = 0.000178
    elevator_emission_billion_per_mt: float = 0.00408
    rocket_emission_billion_per_launch: float = 0.00000125
    target_time_year: float = 50.0

    @property
    def rocket_only_launches(self) -> int:
        return int(np.ceil(self.material_demand_mt / self.rocket_payload_mt_per_launch))

    @property
    def elevator_only_time(self) -> float:
        return self.material_demand_mt / self.elevator_capacity_mt_per_year

    @property
    def rocket_only_cost(self) -> float:
        return self.rocket_cost_trillion_per_launch * self.rocket_only_launches

    @property
    def rocket_only_emission(self) -> float:
        return self.rocket_emission_billion_per_launch * self.rocket_only_launches

    @property
    def cost_target(self) -> float:
        return 0.8 * self.rocket_only_cost

    @property
    def emission_target(self) -> float:
        return 0.6 * self.rocket_only_emission


PARAMS = Parameters()

SCENARIOS = {
    "cost_schedule_priority": {
        "label": "Cost + Schedule Priority",
        "weights": (0.45, 0.40, 0.15),
    },
    "environment_priority": {
        "label": "Environment Priority",
        "weights": (0.10, 0.05, 0.85),
    },
    "balanced": {
        "label": "Balanced",
        "weights": (0.30, 0.25, 0.45),
    },
}


VAR_NAMES = [
    "x_elevator_mt",
    "x_rocket_mt",
    "rocket_launches",
    "time_year",
    "cost_trillion_usd",
    "emission_billion_tco2",
    "d_cost_plus",
    "d_cost_minus",
    "d_time_plus",
    "d_time_minus",
    "d_emission_plus",
    "d_emission_minus",
]
IDX = {name: i for i, name in enumerate(VAR_NAMES)}


def solve_scenario(name: str, label: str, weights: tuple[float, float, float]) -> dict[str, float | str]:
    p = PARAMS
    n = len(VAR_NAMES)
    w_cost, w_time, w_emission = weights

    objective = np.zeros(n)
    objective[IDX["d_cost_plus"]] = w_cost / p.cost_target
    objective[IDX["d_time_plus"]] = w_time / p.target_time_year
    objective[IDX["d_emission_plus"]] = w_emission / p.emission_target

    lower = np.zeros(n)
    upper = np.full(n, np.inf)
    upper[IDX["x_elevator_mt"]] = p.material_demand_mt
    upper[IDX["x_rocket_mt"]] = p.material_demand_mt
    upper[IDX["rocket_launches"]] = p.rocket_only_launches
    upper[IDX["time_year"]] = p.elevator_only_time
    upper[IDX["cost_trillion_usd"]] = p.rocket_only_cost
    upper[IDX["emission_billion_tco2"]] = p.rocket_only_emission

    integrality = np.zeros(n, dtype=int)
    integrality[IDX["rocket_launches"]] = 1

    rows: list[np.ndarray] = []
    lb: list[float] = []
    ub: list[float] = []

    def add_constraint(coeff: dict[str, float], lower_bound: float, upper_bound: float) -> None:
        row = np.zeros(n)
        for var, value in coeff.items():
            row[IDX[var]] = value
        rows.append(row)
        lb.append(lower_bound)
        ub.append(upper_bound)

    # C = c_E x_E + f_R n_R
    add_constraint(
        {
            "cost_trillion_usd": 1.0,
            "x_elevator_mt": -p.elevator_cost_trillion_per_mt,
            "rocket_launches": -p.rocket_cost_trillion_per_launch,
        },
        0.0,
        0.0,
    )

    # G = g_E x_E + g_R n_R
    add_constraint(
        {
            "emission_billion_tco2": 1.0,
            "x_elevator_mt": -p.elevator_emission_billion_per_mt,
            "rocket_launches": -p.rocket_emission_billion_per_launch,
        },
        0.0,
        0.0,
    )

    # Goal equations.
    add_constraint(
        {"cost_trillion_usd": 1.0, "d_cost_minus": 1.0, "d_cost_plus": -1.0},
        p.cost_target,
        p.cost_target,
    )
    add_constraint(
        {"time_year": 1.0, "d_time_minus": 1.0, "d_time_plus": -1.0},
        p.target_time_year,
        p.target_time_year,
    )
    add_constraint(
        {"emission_billion_tco2": 1.0, "d_emission_minus": 1.0, "d_emission_plus": -1.0},
        p.emission_target,
        p.emission_target,
    )

    # Transport demand and capacity constraints.
    add_constraint({"x_elevator_mt": 1.0, "x_rocket_mt": 1.0}, p.material_demand_mt, np.inf)
    add_constraint({"x_elevator_mt": 1.0, "time_year": -p.elevator_capacity_mt_per_year}, -np.inf, 0.0)
    add_constraint(
        {"x_rocket_mt": 1.0, "rocket_launches": -p.rocket_payload_mt_per_launch},
        -np.inf,
        0.0,
    )

    constraints = LinearConstraint(np.vstack(rows), np.array(lb), np.array(ub))
    result = milp(
        c=objective,
        integrality=integrality,
        bounds=Bounds(lower, upper),
        constraints=constraints,
        options={"time_limit": 120, "mip_rel_gap": 1e-9},
    )

    if not result.success:
        raise RuntimeError(f"MILP failed for {name}: {result.message}")

    x = result.x
    solved = {var: float(x[i]) for i, var in enumerate(VAR_NAMES)}
    solved["scenario"] = name
    solved["scenario_label"] = label
    solved["w_cost"] = w_cost
    solved["w_time"] = w_time
    solved["w_emission"] = w_emission
    solved["objective_value"] = float(result.fun)
    solved["rocket_launches"] = int(round(solved["rocket_launches"]))
    solved["elevator_share"] = solved["x_elevator_mt"] / p.material_demand_mt
    solved["rocket_share"] = solved["x_rocket_mt"] / p.material_demand_mt
    solved["cost_vs_rocket_only"] = solved["cost_trillion_usd"] / p.rocket_only_cost
    solved["time_vs_target"] = solved["time_year"] / p.target_time_year
    solved["emission_vs_rocket_only"] = solved["emission_billion_tco2"] / p.rocket_only_emission
    return solved


def build_frontier() -> pd.DataFrame:
    p = PARAMS
    launches = np.arange(p.rocket_only_launches + 1, dtype=np.int64)
    rocket_capacity = launches * p.rocket_payload_mt_per_launch
    x_elevator = np.maximum(0.0, p.material_demand_mt - rocket_capacity)
    x_rocket = p.material_demand_mt - x_elevator
    time = x_elevator / p.elevator_capacity_mt_per_year
    cost = p.elevator_cost_trillion_per_mt * x_elevator + p.rocket_cost_trillion_per_launch * launches
    emission = p.elevator_emission_billion_per_mt * x_elevator + p.rocket_emission_billion_per_launch * launches
    return pd.DataFrame(
        {
            "rocket_launches": launches,
            "x_elevator_mt": x_elevator,
            "x_rocket_mt": x_rocket,
            "time_year": time,
            "cost_trillion_usd": cost,
            "emission_billion_tco2": emission,
        }
    )


def write_markdown(results: pd.DataFrame) -> None:
    p = PARAMS
    lines = [
        "# 混合运输模型求解结果",
        "",
        "求解器：SciPy MILP 接口，底层为 HiGHS。模型不设置单个发射场发射次数上限。",
        "",
        "## Benchmark",
        "",
        f"- 电梯-only：时间 {p.elevator_only_time:.2f} 年，成本 {p.elevator_cost_trillion_per_mt * p.material_demand_mt:.2f} trillion USD，排放 {p.elevator_emission_billion_per_mt * p.material_demand_mt:.3f} billion tCO2。",
        f"- 火箭-only：发射 {p.rocket_only_launches:,} 次，成本 {p.rocket_only_cost:.2f} trillion USD，排放 {p.rocket_only_emission:.3f} billion tCO2。",
        "",
        "## 三种权重情景",
        "",
        "| 情景 | 电梯运输 Mt | 火箭运输 Mt | 火箭发射次数 | 时间 年 | 成本 trillion USD | 排放 billion tCO2 | 目标函数值 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in results.itertuples(index=False):
        lines.append(
            f"| {row.scenario_label} | {row.x_elevator_mt:.3f} | {row.x_rocket_mt:.3f} | "
            f"{int(row.rocket_launches):,} | {row.time_year:.2f} | "
            f"{row.cost_trillion_usd:.3f} | {row.emission_billion_tco2:.3f} | {row.objective_value:.6f} |"
        )
    lines.extend(
        [
            "",
            "## 输出图表",
            "",
            "- `report/figures/transport_split.png`：三种权重情景下电梯与火箭运输量分配。",
            "- `report/figures/normalized_metrics.png`：三种方案的成本、时间、排放归一化对比。",
            "- `report/figures/tradeoff_time_emission.png`：运输时间与环境排放的权衡曲线，并标出三种最优解。",
            "",
        ]
    )
    (RESULT_DIR / "mixed_model_results.md").write_text("\n".join(lines), encoding="utf-8")


def plot_results(results: pd.DataFrame, frontier: pd.DataFrame) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    labels = results["scenario_label"].tolist()
    short_labels = ["Cost+Time", "Environment", "Balanced"]
    x = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(x, results["x_elevator_mt"].to_numpy(), label="Space elevator")
    ax.bar(
        x,
        results["x_rocket_mt"].to_numpy(),
        bottom=results["x_elevator_mt"].to_numpy(),
        label="Rocket",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(short_labels)
    ax.set_ylabel("Transported mass (million metric tons)")
    ax.set_title("Transport split")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "transport_split.png", dpi=180)
    plt.close(fig)

    metrics = pd.DataFrame(
        {
            "Cost / rocket-only cost": results["cost_vs_rocket_only"].to_numpy(dtype=float),
            "Time / 50-year target": results["time_vs_target"].to_numpy(dtype=float),
            "Emission / rocket-only emission": results["emission_vs_rocket_only"].to_numpy(dtype=float),
        },
        index=short_labels,
    )
    fig, ax = plt.subplots(figsize=(10, 5.5))
    width = 0.25
    positions = np.arange(len(metrics.index))
    for offset, column in zip([-width, 0, width], metrics.columns):
        bars = ax.bar(
            positions + offset,
            metrics[column].to_numpy(dtype=float),
            width=width,
            label=column,
        )
        ax.bar_label(bars, fmt="%.2f", padding=3, fontsize=8)
    ax.axhline(1.0, color="black", linewidth=1, linestyle="--")
    ax.set_xticks(positions)
    ax.set_xticklabels(metrics.index)
    ax.set_ylabel("Normalized value")
    ax.set_title("Normalized objective indicators")
    ax.set_ylim(0, max(1.05, float(metrics.to_numpy(dtype=float).max()) * 1.18))
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=3, frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "normalized_metrics.png", dpi=180)
    plt.close(fig)

    stride = max(1, len(frontier) // 5000)
    sampled = frontier.iloc[::stride]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(sampled["time_year"], sampled["emission_billion_tco2"], color="#666666", linewidth=1.5)
    colors = {
        "cost_schedule_priority": "#1f77b4",
        "environment_priority": "#2ca02c",
        "balanced": "#ff7f0e",
    }
    for row in results.itertuples(index=False):
        ax.scatter(
            row.time_year,
            row.emission_billion_tco2,
            s=70,
            color=colors[row.scenario],
            zorder=3,
        )

    # The cost+schedule and balanced scenarios can choose the same point.
    # Combine labels at identical coordinates so annotations remain readable.
    grouped: dict[tuple[float, float], list[str]] = {}
    for row in results.itertuples(index=False):
        key = (round(float(row.time_year), 6), round(float(row.emission_billion_tco2), 6))
        grouped.setdefault(key, []).append(row.scenario_label)

    for (time_year, emission), grouped_labels in grouped.items():
        label = " / ".join(
            "Cost+Time" if item == "Cost + Schedule Priority" else item.replace(" Priority", "")
            for item in grouped_labels
        )
        xytext = (14, 12) if time_year <= PARAMS.target_time_year + 1 else (14, 6)
        ax.annotate(
            label,
            (time_year, emission),
            textcoords="offset points",
            xytext=xytext,
            fontsize=9,
            bbox={"boxstyle": "round,pad=0.2", "facecolor": "white", "edgecolor": "none", "alpha": 0.85},
        )
    ax.axvline(PARAMS.target_time_year, color="black", linewidth=1, linestyle="--", label="50-year target")
    ax.axhline(PARAMS.emission_target, color="#777777", linewidth=1, linestyle=":", label="Emission target")
    ax.set_xlabel("Completion time (years)")
    ax.set_ylabel("Emission (billion tCO2)")
    ax.set_title("Time-emission tradeoff frontier")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "tradeoff_time_emission.png", dpi=180)
    plt.close(fig)


def main() -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    solved_rows = [
        solve_scenario(name, spec["label"], spec["weights"])
        for name, spec in SCENARIOS.items()
    ]
    results = pd.DataFrame(solved_rows)
    frontier = build_frontier()

    result_columns = [
        "scenario",
        "scenario_label",
        "w_cost",
        "w_time",
        "w_emission",
        "x_elevator_mt",
        "x_rocket_mt",
        "rocket_launches",
        "time_year",
        "cost_trillion_usd",
        "emission_billion_tco2",
        "objective_value",
        "d_cost_plus",
        "d_time_plus",
        "d_emission_plus",
        "elevator_share",
        "rocket_share",
        "cost_vs_rocket_only",
        "time_vs_target",
        "emission_vs_rocket_only",
    ]
    results[result_columns].to_csv(RESULT_DIR / "mixed_model_results.csv", index=False)
    frontier.iloc[:: max(1, len(frontier) // 10000)].to_csv(
        RESULT_DIR / "tradeoff_frontier_sample.csv",
        index=False,
    )
    write_markdown(results)
    plot_results(results, frontier)

    print(results[result_columns].to_string(index=False))
    print()
    print(f"Wrote: {RESULT_DIR / 'mixed_model_results.csv'}")
    print(f"Wrote: {RESULT_DIR / 'mixed_model_results.md'}")
    print(f"Wrote figures under: {FIGURE_DIR}")


if __name__ == "__main__":
    main()
