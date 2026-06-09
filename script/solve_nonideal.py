#!/usr/bin/env python3
"""Solve non-ideal under the single non-ideal transport scenario.

The non-ideal scenario follows the modeling document:
- a_E = 0.90 for the space elevator effective capacity;
- a_R = 0.98 for effective rocket delivery;
- objective functions and weights remain the same as step 3;
- no launch-site-level variables or launch-site capacity constraints.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from solve_mixed_model import FIGURE_DIR, PARAMS, RESULT_DIR, SCENARIOS


A_E_NONIDEAL = 0.90
A_R_NONIDEAL = 0.98


def build_nonideal_search_table(a_e: float, a_r: float) -> pd.DataFrame:
    p = PARAMS
    max_launches = int(np.ceil(p.material_demand_mt / (a_r * p.rocket_payload_mt_per_launch)))
    rocket_launches = np.arange(max_launches + 1, dtype=np.int64)

    x_rocket = np.minimum(
        p.material_demand_mt,
        a_r * p.rocket_payload_mt_per_launch * rocket_launches,
    )
    x_elevator = p.material_demand_mt - x_rocket
    time = x_elevator / (a_e * p.elevator_capacity_mt_per_year)
    cost = p.elevator_cost_trillion_per_mt * x_elevator + p.rocket_cost_trillion_per_launch * rocket_launches
    emission = p.elevator_emission_billion_per_mt * x_elevator + p.rocket_emission_billion_per_launch * rocket_launches

    return pd.DataFrame(
        {
            "rocket_launches": rocket_launches,
            "x_elevator_mt": x_elevator,
            "x_rocket_mt": x_rocket,
            "time_year": time,
            "cost_trillion_usd": cost,
            "emission_billion_tco2": emission,
        }
    )


def solve_nonideal_scenario(
    table: pd.DataFrame,
    scenario: str,
    label: str,
    weights: tuple[float, float, float],
    a_e: float,
    a_r: float,
) -> dict[str, float | str]:
    p = PARAMS
    w_cost, w_time, w_emission = weights

    d_cost_plus = np.maximum(table["cost_trillion_usd"].to_numpy() - p.cost_target, 0.0)
    d_time_plus = np.maximum(table["time_year"].to_numpy() - p.target_time_year, 0.0)
    d_emission_plus = np.maximum(table["emission_billion_tco2"].to_numpy() - p.emission_target, 0.0)
    objective = (
        w_cost * d_cost_plus / p.cost_target
        + w_time * d_time_plus / p.target_time_year
        + w_emission * d_emission_plus / p.emission_target
    )

    best_index = int(np.argmin(objective))
    row = table.iloc[best_index]

    return {
        "scenario": scenario,
        "scenario_label": label,
        "a_e": a_e,
        "a_r": a_r,
        "w_cost": w_cost,
        "w_time": w_time,
        "w_emission": w_emission,
        "x_elevator_mt": float(row["x_elevator_mt"]),
        "x_rocket_mt": float(row["x_rocket_mt"]),
        "rocket_launches": int(row["rocket_launches"]),
        "time_year": float(row["time_year"]),
        "cost_trillion_usd": float(row["cost_trillion_usd"]),
        "emission_billion_tco2": float(row["emission_billion_tco2"]),
        "objective_value": float(objective[best_index]),
        "d_cost_plus": float(d_cost_plus[best_index]),
        "d_time_plus": float(d_time_plus[best_index]),
        "d_emission_plus": float(d_emission_plus[best_index]),
    }


def compare_with_ideal(nonideal: pd.DataFrame) -> pd.DataFrame:
    ideal_path = RESULT_DIR / "mixed_model_results.csv"
    if not ideal_path.exists():
        raise FileNotFoundError(
            f"Missing ideal step-3 results: {ideal_path}. Run script/solve_mixed_model.py first."
        )

    ideal = pd.read_csv(ideal_path)
    merged = nonideal.merge(ideal, on="scenario", suffixes=("_nonideal", "_ideal"))

    metrics = [
        "x_elevator_mt",
        "x_rocket_mt",
        "rocket_launches",
        "time_year",
        "cost_trillion_usd",
        "emission_billion_tco2",
        "objective_value",
    ]
    for metric in metrics:
        ideal_value = merged[f"{metric}_ideal"].astype(float)
        nonideal_value = merged[f"{metric}_nonideal"].astype(float)
        merged[f"{metric}_delta"] = nonideal_value - ideal_value
        merged[f"{metric}_change_rate"] = np.where(
            ideal_value.abs() > 1e-12,
            (nonideal_value - ideal_value) / ideal_value,
            np.nan,
        )
    return merged


def write_markdown(comparison: pd.DataFrame) -> None:
    lines = [
        "# 非完美运行求解结果",
        "",
        f"非完美主情景：\(a_E={A_E_NONIDEAL:.2f}\)，\(a_R={A_R_NONIDEAL:.2f}\)。目标函数、权重和目标值保持步骤 3 不变。",
        "",
        "## 非完美运行最优解",
        "",
        "| 情景 | 电梯运输 Mt | 火箭运输 Mt | 火箭发射次数 | 时间 年 | 成本 trillion USD | 排放 billion tCO2 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in comparison.itertuples(index=False):
        lines.append(
            f"| {row.scenario_label_nonideal} | {row.x_elevator_mt_nonideal:.3f} | "
            f"{row.x_rocket_mt_nonideal:.3f} | {int(row.rocket_launches_nonideal):,} | "
            f"{row.time_year_nonideal:.2f} | {row.cost_trillion_usd_nonideal:.3f} | "
            f"{row.emission_billion_tco2_nonideal:.3f} |"
        )

    lines.extend(
        [
            "",
            "## 相对完美运行的变化率",
            "",
            "| 情景 | 电梯运输量 | 火箭运输量 | 火箭发射次数 | 时间 | 成本 | 排放 |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in comparison.itertuples(index=False):
        lines.append(
            f"| {row.scenario_label_nonideal} | "
            f"{row.x_elevator_mt_change_rate:.2%} | {row.x_rocket_mt_change_rate:.2%} | "
            f"{row.rocket_launches_change_rate:.2%} | {row.time_year_change_rate:.2%} | "
            f"{row.cost_trillion_usd_change_rate:.2%} | {row.emission_billion_tco2_change_rate:.2%} |"
        )

    lines.extend(
        [
            "",
            "## 输出图表",
            "",
            "- `report/figures/nonideal_change_rates.png`：非完美运行相对完美运行的主要指标变化率。",
            "",
        ]
    )
    (RESULT_DIR / "nonideal_results.md").write_text("\n".join(lines), encoding="utf-8")


def plot_change_rates(comparison: pd.DataFrame) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    labels = ["Cost+Time", "Environment", "Balanced"]
    metrics = pd.DataFrame(
        {
            "Launches": comparison["rocket_launches_change_rate"].to_numpy(dtype=float),
            "Time": comparison["time_year_change_rate"].to_numpy(dtype=float),
            "Cost": comparison["cost_trillion_usd_change_rate"].to_numpy(dtype=float),
            "Emission": comparison["emission_billion_tco2_change_rate"].to_numpy(dtype=float),
        },
        index=labels,
    )

    fig, ax = plt.subplots(figsize=(10, 5.5))
    width = 0.2
    positions = np.arange(len(labels))
    offsets = [-1.5 * width, -0.5 * width, 0.5 * width, 1.5 * width]
    for offset, column in zip(offsets, metrics.columns):
        values = metrics[column].to_numpy(dtype=float) * 100
        values[np.abs(values) < 0.05] = 0.0
        bars = ax.bar(positions + offset, values, width=width, label=column)
        ax.bar_label(bars, labels=[f"{value:.1f}%" for value in values], padding=3, fontsize=8)

    ax.axhline(0, color="black", linewidth=1)
    ax.set_xticks(positions)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Change from ideal solution (%)")
    ax.set_title("Step 4 non-ideal transport: change rates")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=4, frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "nonideal_change_rates.png", dpi=180)
    plt.close(fig)


def main() -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    table = build_nonideal_search_table(A_E_NONIDEAL, A_R_NONIDEAL)
    nonideal = pd.DataFrame(
        [
            solve_nonideal_scenario(
                table,
                scenario,
                spec["label"],
                spec["weights"],
                A_E_NONIDEAL,
                A_R_NONIDEAL,
            )
            for scenario, spec in SCENARIOS.items()
        ]
    )

    comparison = compare_with_ideal(nonideal)
    nonideal.to_csv(RESULT_DIR / "nonideal_results.csv", index=False)
    comparison.to_csv(RESULT_DIR / "nonideal_vs_ideal.csv", index=False)
    write_markdown(comparison)
    plot_change_rates(comparison)

    print(nonideal.to_string(index=False))
    print()
    print("Change rates vs ideal:")
    rate_cols = [
        "scenario",
        "rocket_launches_change_rate",
        "time_year_change_rate",
        "cost_trillion_usd_change_rate",
        "emission_billion_tco2_change_rate",
    ]
    print(comparison[rate_cols].to_string(index=False))
    print()
    print(f"Wrote: {RESULT_DIR / 'nonideal_results.csv'}")
    print(f"Wrote: {RESULT_DIR / 'nonideal_vs_ideal.csv'}")
    print(f"Wrote: {RESULT_DIR / 'nonideal_results.md'}")
    print(f"Wrote: {FIGURE_DIR / 'nonideal_change_rates.png'}")


if __name__ == "__main__":
    main()
