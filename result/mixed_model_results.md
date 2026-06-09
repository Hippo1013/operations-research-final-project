# 混合运输模型求解结果

求解器：SciPy MILP 接口，底层为 HiGHS。模型不设置单个发射场发射次数上限。

## Benchmark

- 电梯-only：时间 186.22 年，成本 10.00 trillion USD，排放 0.408 billion tCO2。
- 火箭-only：发射 800,000 次，成本 142.40 trillion USD，排放 1.000 billion tCO2。

## 三种权重情景

| 情景 | 电梯运输 Mt | 火箭运输 Mt | 火箭发射次数 | 时间 年 | 成本 trillion USD | 排放 billion tCO2 | 目标函数值 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Cost + Schedule Priority | 26.850 | 73.150 | 585,200 | 50.00 | 106.851 | 0.841 | 0.060262 |
| Environment Priority | 67.568 | 32.432 | 259,459 | 125.82 | 52.940 | 0.600 | 0.075824 |
| Balanced | 26.850 | 73.150 | 585,200 | 50.00 | 106.851 | 0.841 | 0.180786 |

## 输出图表

- `report/figures/transport_split.png`：三种权重情景下电梯与火箭运输量分配。
- `report/figures/normalized_metrics.png`：三种方案的成本、时间、排放归一化对比。
- `report/figures/tradeoff_time_emission.png`：运输时间与环境排放的权衡曲线，并标出三种最优解。
