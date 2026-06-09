# 扩展多时期发射场级模型求解结果

求解方法：外层从 `T=50` 年开始逐年枚举，不设置模型意义上的工期上界；当目标函数连续 `30` 年未改善后停止。内层使用凸二次调度近似分配各发射场、各年份的火箭发射次数。模型不设置单个发射场硬性年发射上限。

## 情景参数

- 非完美主情景：`a_E=0.90`，`a_R=0.98`。
- 技术进步：火箭发射成本年下降率 `0.500%`，火箭单次排放年下降率 `0.300%`。
- 工期目标：`T*=75` 年；成本目标 `C*=0.8C0=113.920` trillion USD；环境目标 `H*=0.6H0=0.600` billion。
- 环境压力残留：由发射场敏感系数映射到 `0.50-0.58`；非线性压力系数 `beta=2.50e-11`。
- 程序安全保护上限：`T=250` 年；本次没有触发该保护上限。

## 最优结果

| 情景 | 最优 T | 电梯运输 Mt | 火箭运输 Mt | 火箭发射次数 | 成本 trillion USD | CO2 billion tCO2 | 环境损害 H | 目标函数值 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Balanced | 79 | 38.180 | 61.820 | 504,649 | 74.295 | 0.701 | 0.738 | 0.116826 |
| Cost + Schedule Priority | 75 | 36.247 | 63.753 | 520,430 | 75.786 | 0.708 | 0.785 | 0.046298 |
| Environment Priority | 116 | 54.947 | 45.053 | 367,782 | 50.625 | 0.592 | 0.600 | 0.027798 |

## 发射场分配

| 情景 | 发射场 | 发射次数 | 占该情景火箭发射比例 | 环境敏感系数 | 最大环境压力 |
|---|---|---:|---:|---:|---:|
| Balanced | Alaska | 138,805 | 27.51% | 3.5 | 7891.4 |
| Balanced | California | 17,647 | 3.50% | 4.0 | 2939.9 |
| Balanced | Florida | 17,647 | 3.50% | 4.0 | 2939.9 |
| Balanced | French Guiana | 138,805 | 27.51% | 3.5 | 7891.4 |
| Balanced | Mahia | 138,804 | 27.51% | 3.5 | 7891.4 |
| Balanced | Satish Dhawan | 17,647 | 3.50% | 4.0 | 2939.9 |
| Balanced | Taiyuan | 17,647 | 3.50% | 4.0 | 2939.9 |
| Balanced | Virginia | 17,647 | 3.50% | 4.0 | 2939.9 |
| Cost + Schedule Priority | Alaska | 120,556 | 23.16% | 3.5 | 11329.7 |
| Cost + Schedule Priority | California | 31,168 | 5.99% | 4.0 | 5934.6 |
| Cost + Schedule Priority | Florida | 31,168 | 5.99% | 4.0 | 5934.6 |
| Cost + Schedule Priority | French Guiana | 120,554 | 23.16% | 3.5 | 11329.7 |
| Cost + Schedule Priority | Kazakhstan | 2,925 | 0.56% | 4.5 | 1627.1 |
| Cost + Schedule Priority | Mahia | 120,555 | 23.16% | 3.5 | 11329.7 |
| Cost + Schedule Priority | Satish Dhawan | 31,168 | 5.99% | 4.0 | 5934.6 |
| Cost + Schedule Priority | Taiyuan | 31,168 | 5.99% | 4.0 | 5934.6 |
| Cost + Schedule Priority | Virginia | 31,168 | 5.99% | 4.0 | 5934.6 |
| Environment Priority | Alaska | 114,637 | 31.17% | 3.5 | 5670.8 |
| Environment Priority | California | 4,774 | 1.30% | 4.0 | 1276.5 |
| Environment Priority | Florida | 4,774 | 1.30% | 4.0 | 1276.5 |
| Environment Priority | French Guiana | 114,637 | 31.17% | 3.5 | 5670.8 |
| Environment Priority | Mahia | 114,638 | 31.17% | 3.5 | 5670.8 |
| Environment Priority | Satish Dhawan | 4,774 | 1.30% | 4.0 | 1276.5 |
| Environment Priority | Taiyuan | 4,774 | 1.30% | 4.0 | 1276.5 |
| Environment Priority | Virginia | 4,774 | 1.30% | 4.0 | 1276.5 |

## 输出文件

- `result/extended_model_results.csv`：三组情景的最优解。
- `result/extended_by_time.csv`：所有候选工期的目标函数与指标。
- `result/extended_stage_results.csv`：最优解的 10/60/30 阶段运输量。
- `result/extended_site_summary.csv`：最优解的发射场分配汇总。
- `result/extended_site_year_schedule.csv`：最优解的发射场-年份调度表。
- `report/figures/extended_objective_by_time.png`：外层工期枚举曲线。
- `report/figures/extended_stage_transport.png`：最优解阶段运输量。
- `report/figures/extended_site_launches.png`：最优解发射场分配。
