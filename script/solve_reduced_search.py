#!/usr/bin/env python3
"""Solve the mixed transport model by one-dimensional integer search.

This script implements the structural simplification described in
the modeling document. Under the current model, a feasible mixed
transport plan can be represented by the total rocket launch count n_R.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from solve_mixed_model import PARAMS, RESULT_DIR, SCENARIOS


def build_search_table() -> pd.DataFrame:
    p = PARAMS
    rocket_launches = np.arange(p.rocket_only_launches + 1, dtype=np.int64)

    x_rocket = np.minimum(
        p.material_demand_mt,
        rocket_launches * p.rocket_payload_mt_per_launch,
    )
    x_elevator = p.material_demand_mt - x_rocket
    time = x_elevator / p.elevator_capacity_mt_per_year
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


def solve_by_search(table: pd.DataFrame, scenario: str, label: str, weights: tuple[float, float, float]) -> dict[str, float | str]:
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
        "elevator_share": float(row["x_elevator_mt"] / p.material_demand_mt),
        "rocket_share": float(row["x_rocket_mt"] / p.material_demand_mt),
        "cost_vs_rocket_only": float(row["cost_trillion_usd"] / p.rocket_only_cost),
        "time_vs_target": float(row["time_year"] / p.target_time_year),
        "emission_vs_rocket_only": float(row["emission_billion_tco2"] / p.rocket_only_emission),
    }


def write_markdown(results: pd.DataFrame, comparison: pd.DataFrame | None) -> None:
    lines = [
        "# 结构化降维搜索求解结果",
        "",
        "求解方法：枚举火箭总发射次数 `n_R=0,...,800000`，由 `x_R=q_R n_R`、`x_E=M-x_R`、`T=x_E/Q_E` 直接计算每个方案的成本、时间、排放和目标函数值。",
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

    if comparison is not None:
        max_abs_diff = comparison["max_abs_metric_diff"].max()
        lines.extend(
            [
                "",
                "## 与 HiGHS MILP 结果对照",
                "",
                f"最大绝对差异：{max_abs_diff:.6g}。若该值接近 0，说明一维整数搜索与 MILP 求解结果一致。",
                "",
            ]
        )

    (RESULT_DIR / "reduced_search_results.md").write_text("\n".join(lines), encoding="utf-8")


def compare_with_milp(search_results: pd.DataFrame) -> pd.DataFrame | None:
    milp_path = RESULT_DIR / "mixed_model_results.csv"
    if not milp_path.exists():
        return None

    metrics = [
        "x_elevator_mt",
        "x_rocket_mt",
        "rocket_launches",
        "time_year",
        "cost_trillion_usd",
        "emission_billion_tco2",
        "objective_value",
    ]
    milp = pd.read_csv(milp_path)
    merged = search_results.merge(milp, on="scenario", suffixes=("_search", "_milp"))

    rows = []
    for row in merged.itertuples(index=False):
        diffs = []
        for metric in metrics:
            search_value = getattr(row, f"{metric}_search")
            milp_value = getattr(row, f"{metric}_milp")
            diffs.append(abs(float(search_value) - float(milp_value)))
        rows.append(
            {
                "scenario": row.scenario,
                "scenario_label": row.scenario_label_search,
                "max_abs_metric_diff": max(diffs),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)

    table = build_search_table()
    results = pd.DataFrame(
        [
            solve_by_search(table, scenario, spec["label"], spec["weights"])
            for scenario, spec in SCENARIOS.items()
        ]
    )

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
    results[result_columns].to_csv(RESULT_DIR / "reduced_search_results.csv", index=False)

    comparison = compare_with_milp(results[result_columns])
    if comparison is not None:
        comparison.to_csv(RESULT_DIR / "reduced_search_vs_milp.csv", index=False)

    write_markdown(results, comparison)

    print(results[result_columns].to_string(index=False))
    if comparison is not None:
        print()
        print("Comparison with MILP:")
        print(comparison.to_string(index=False))
    print()
    print(f"Wrote: {RESULT_DIR / 'reduced_search_results.csv'}")
    print(f"Wrote: {RESULT_DIR / 'reduced_search_results.md'}")
    if comparison is not None:
        print(f"Wrote: {RESULT_DIR / 'reduced_search_vs_milp.csv'}")


if __name__ == "__main__":
    main()
