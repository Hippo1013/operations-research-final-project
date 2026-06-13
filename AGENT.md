# AGENT.md

> Last updated: 2026-06-12  
> Project: 运筹学期末大作业 / 2026 MCM Problem B：利用太空电梯系统建设月球基地

## Project Purpose

本项目是运筹学课程期末大作业。小组选题为 2026 MCM Problem B，主题是利用 Space Elevator System 与传统火箭运输系统建设并维持一个 100,000 人规模的 Moon Colony。

课程知识背景包括：

- 线性规划
- 单纯形法
- 对偶理论
- 运输问题
- 目标规划
- 整数规划
- 非线性规划
- 动态规划

当前项目重点放在第一阶段：从 2050 年开始，将建设月球基地所需的 100,000,000 公吨材料从地球运输到月球，并比较太空电梯、传统火箭和混合方案。

截至 2026-06-09，项目范围已收敛为只完成第一阶段，不再继续展开原任务拆分中的第二阶段和第三阶段。后续工作转为第一阶段结果的案例分析、解的评估、方法对比和最终报告整理。

2026-06-09 更新：LaTeX 报告 `report/thesis.tex` 中序号 0 标题已改为“题目、作者和摘要”。

2026-06-09 更新：LaTeX 报告第 0 部分已补充三个次级标题“题目”“作者”“摘要”；作者部分使用三列表格列出六位作者的姓名、学号、专业，其中学号暂空，专业均为“机器人工程”。每次修改 LaTeX 报告后均需重新编译 `report/thesis.tex` 并确认 `report/thesis.pdf` 成功生成。

2026-06-09 更新：LaTeX 报告作者表已补全学号：曹航硕 3240101938，吴天昊 3240105556，陈禹成 3240102176，邓凯坤 3240105612，朱奕辰 3240103075，康褀 3240101043。

2026-06-09 更新：LaTeX 报告 `report/thesis.tex` 已写入“前言”部分，包含“选题背景”“研究现状”“研究意义”三个次级标题；开头说明选题改编自 2026 MCM Problem B，并以短文本超链接形式放入 COMAP 原题网页。报告中的中文术语“月球殖民地”已统一改为“月球基地”。

2026-06-09 更新：LaTeX 报告中“建材”已统一改为“材料”，报告题目同步为“面向月球基地建设的材料运输运筹学优化方案”；前言中任务收敛表述改为“我们将原任务收敛为‘探究月球基地建设期的材料运输方案’”。

2026-06-09 更新：删除先前生成的配图 `report/figures/lunar_base_transport_poster.png`。改用用户提供的 `report/figures/ChatGPT Image 2026年6月9日 16_56_07.png`，已插入 LaTeX 报告“前言”部分末尾，宽度设为 `0.68\textwidth`。

2026-06-09 更新：LaTeX 报告 `report/thesis.tex` 已写入“问题描述”部分，包含两个次级标题“实际问题”和“运筹学建模”。“实际问题”部分已补充原题给出的关键任务条件参数，包括三个 Galactic Harbours、单港年运力 179000 公吨、总运力 537000 公吨、10 个火箭发射场和 2050 年 Falcon Heavy 单次 100--150 公吨载荷等信息；“运筹学建模”部分已列出主要参数、基础目标规划模型、非完美运行可用率修正，以及步骤 5 扩展模型中的发射场-年份变量、环境压力存量和技术进步表达。

2026-06-09 更新：LaTeX 报告“运筹学建模”部分已细分为三个次次级标题：“完美工作状态模型”“非完美工作状态模型”“扩展模型”。

2026-06-09 更新：LaTeX 报告“运筹学建模”中三个次次级标题部分末尾均已补充正式数学优化模型：完美工作状态目标规划模型、非完美工作状态可用率修正模型、扩展模型的外层工期选择与内层发射场-年份调度模型。

2026-06-09 更新：LaTeX 报告已继续补写“优化方法”“案例分析”“结论”“参考文献”“附录”“分工与贡献”部分。其中“优化方法”包含模型特点、方法设计和核心算法实现代码框；“案例分析”按 `doc/第一阶段.md` 的逻辑写入具体数据、极端方案、完美/非完美/扩展模型结果、解的评估和方法对比，并插入已有可视化图表；“参考文献”按编号格式列出关键数据和近似公式来源及网址；“附录”补充运输耗电、发射场位置、环境敏感系数和次核心代码。`report/thesis.sty` 中封面硬编码标题也已从“月球殖民地”改为“月球基地”。本轮修改后已重新编译 `report/thesis.tex`，生成 `report/thesis.pdf`。

2026-06-09 更新：LaTeX 报告“扩展模型”部分已扩写，明确说明扩展模型新增考虑的现实条件：不同发射场环境敏感性不同、连续高频发射导致环境影响非线性累积、不同建设阶段材料需求比例不同、火箭技术随时间进步；并新增扩展模型参数/变量解释表。正文已补充对参考文献编号的引用，以及对附录中补充参数、发射场环境敏感系数和次核心代码的交叉引用。用户已明确“不考虑 25 页限制”“不要为了 25 页限制压缩内容排版”，因此恢复正常章节换页排版；当前 `report/thesis.pdf` 重新编译成功，共 26 页。

2026-06-09 更新：LaTeX 报告图片排版已调整。`report/thesis.sty` 增加 `float` 包，`report/thesis.tex` 中所有 `figure` 环境均改为 `[H]`，强制图片在源码原处排版。案例分析中的第 4 张图和第 5 张图已缩小并收紧 caption 间距，为后文留出更多空间。修改后已重新编译 `report/thesis.pdf`，当前仍为 26 页。

2026-06-09 更新：脚本命名已去除 `phase1` / “第一阶段”元素。`script/solve_phase1_mixed_model.py`、`script/solve_phase1_reduced_search.py`、`script/solve_phase1_nonideal.py`、`script/solve_phase1_step5_extended_model.py` 分别重命名为 `script/solve_mixed_model.py`、`script/solve_reduced_search.py`、`script/solve_nonideal.py`、`script/solve_extended_model.py`。四个脚本内部导入、输出结果文件名、输出图表文件名和 Markdown 标题也已同步改为无 `phase1` 命名，并已按依赖顺序重新运行全部脚本。LaTeX 报告中的脚本名、图表路径和结果索引已同步新命名并重新编译成功。

2026-06-09 更新：LaTeX 报告案例分析部分的 Fig.4 和 Fig.5 已略微放大。Fig.4 两个子图容器由 `0.46\textwidth` 调为 `0.48\textwidth`，图片宽度由 `0.96\textwidth` 调为 `0.98\textwidth`；Fig.5 图片宽度由 `0.62\textwidth` 调为 `0.68\textwidth`。所有图片仍保持 `[H]` 原处排版，修改后已重新编译 `report/thesis.pdf`。

2026-06-09 更新：LaTeX 报告“分工与贡献”部分已补写六人分工表。六位成员均分配到数学建模或代码实现相关工作；数据调查工作分配给曹航硕、吴天昊、陈禹成三人，分别对应太空电梯参数、火箭参数和发射场参数。修改后已重新编译 `report/thesis.pdf`。

2026-06-09 更新：LaTeX 报告“分工与贡献”部分已按用户要求删除表格后的总结句；成员任务描述中不再写“步骤几”，改为“完美工作状态模型”“非完美工作状态模型”“扩展模型”等具体模型中的负责部分。修改后已重新编译 `report/thesis.pdf`。

2026-06-09 更新：LaTeX 报告案例分析中的扩展模型图表再次放大。原 Fig.4 的两个并排子图已拆为上下两个独立 `[H]` figure，分别为“扩展模型候选工期目标函数”和“扩展模型 10/60/30 阶段运输结果”，宽度均为 `0.88\textwidth`；原 Fig.5 “扩展模型中的发射场分配”也放大到 `0.88\textwidth`。修改后已重新编译 `report/thesis.pdf`，当前共 27 页。

2026-06-09 更新：LaTeX 报告第 0 部分“摘要”已按“问题、内容、结论”结构补写，概括月球基地建设期材料运输问题、极端方案 benchmark、目标规划模型、非完美工作状态模型、扩展多时期发射场级模型，以及最终推荐的扩展模型均衡方案。修改后已重新编译 `report/thesis.pdf`，当前共 28 页。

2026-06-09 更新：已重新核验 LaTeX 报告参考文献。报告第 [1]--[15] 条均为真实可访问或可由 DOI/检索页确认的来源，并分别服务于题目条件、太空电梯成本与设计、电力排放因子、Falcon Heavy 参数与合同成本、火箭环境影响、NASA 月球基地/货运背景和多准则决策方法。第 [4] 条已由不稳定的 `472Edwards.pdf` 修正为 NIAC 可访问的 `521Edwards.pdf`，题名同步改为 \textit{The Space Elevator: NIAC Phase II Final Report}。修改后已重新编译 `report/thesis.pdf`，当前共 28 页。

2026-06-09 更新：本机未安装 Homebrew 和 `gh`。已从 GitHub CLI 官方 release 安装 macOS arm64 版 `gh` 2.93.0 到 `/Users/hippo/.local/bin/gh`，并在 `/Users/hippo/.zshrc` 中加入 `~/.local/bin` 到 PATH。新 zsh 登录环境中已验证 `gh --version` 可用，且 `gh auth status` 显示已登录 GitHub 账号 `Hippo1013`。

2026-06-09 更新：项目已初始化为 git 仓库，并创建 GitHub 公开仓库 `operations-research-final-project`（中文含义：运筹学大作业）。远程地址为 `https://github.com/Hippo1013/operations-research-final-project`。已新增 `.gitignore` 和 `README.md`；公开仓库中保留文档、脚本、结果、报告源码和最终 PDF，排除 `.omx/`、`.DS_Store`、Python 缓存、LaTeX 中间文件以及旧 `phase1_*` 生成物。首次提交为 `d845ae2`。

2026-06-12 更新：已在 `slidev-courseware/` 目录内制作 Slidev 网页汇报课件。课件围绕“问题叙述 → 基础模型建模 → 基础模型求解结果 → 非完美工作情况建模 → 非完美工作情况求解 → 扩展模型建模 → 扩展模型求解 → 结论”展开，重点使用文字、表格、标准数学模型和已有可视化图表表达，不展示大段代码。已新增 `slidev-courseware/style.css` 统一视觉风格，复制报告图表到 `slidev-courseware/public/figures/`，并更新 `slidev-courseware/README.md`。已运行 `npm run build` 验证构建成功；`npm run dev` 可在 `http://localhost:3030/` 查看课件。

2026-06-12 更新：Slidev 课件公式渲染已改为 `slidev-courseware/components/Formula.vue` 组件统一调用 KaTeX，避免 raw HTML 中的 Markdown 数学公式不渲染。第 6 页和第 31 页出现的遮挡“污渍”已修复，原因是 `.pipeline div` 等宽泛 CSS 选择器会影响内部嵌套节点；现已收窄为 `.pipeline > div`、`.pipeline > div > span`、`.pipeline > div > p`。已安装 `playwright-chromium` 作为导出核验依赖，并用 `npx slidev export --format png --range 6,31 --output verify-pages` 导出检查两页，确认遮挡层消失；临时 `verify-pages/` 已删除。`npm run build` 构建成功。

2026-06-12 更新：Slidev 课件除封面页外已整体提高内容密度和字号：非封面页页边距收窄，标题、正文、表格、卡片、流程说明和图表说明字号上调，卡片与图表区域相应放大。第 17 页“结构化降维的小技巧”因图表在字号放大后溢出屏幕，已为 `tradeoff_time_emission.png` 添加 `reduction-chart` 局部样式，限制该页图表宽高并保持完整显示。已用 `npm run build` 构建通过，并导出第 17 页 PNG 检查确认不再溢出；临时导出目录已删除。

2026-06-12 更新：Slidev 课件字体层级已增强。`slidev-courseware/style.css` 新增字体角色变量：正文使用无衬线字体，页面标题/章节标题/卡片标题/结论条使用衬线展示字体，编号、权重、关键数字和指标值使用数字/UI 字体并启用更稳定的数字视觉风格。已导出抽查封面、目录、正文卡片页、模型公式页和第 17 页，确认字体变化更明显且没有新溢出；`npm run build` 构建成功，临时导出目录已删除。

2026-06-13 更新：已将 Slidev HTML 网页课件转换为图片版 PPTX。转换流程为 `npx slidev export --format png` 导出全部 42 页 PNG，再将每张 PNG 作为一页 16:9 全屏图片写入 PowerPoint，以保留字体和排版。输出文件为 `slidev-courseware/面向月球基地建设的材料运输优化方案_图片版.pptx`，大小约 42 MB。已通过 `unzip -t` 检查 PPTX 包结构，确认 42 张幻灯片和 42 张图片均存在；并通过 macOS Quick Look 生成缩略图确认文件可被系统识别。临时导出的 PNG 和缩略图目录已删除。

## Source Files

主要题目与任务文件：

- `task/2026_MCM_Problem_B.md`：题目中文翻译与关键数据。
- `task/2026_MCM_Problem_B.pdf`：原题 PDF。
- `task/2026_MCM_Problem_B_translated.pdf`：翻译版 PDF。
- `task/Task_List.md`：小组任务拆分和注解。
- `task/运筹学大作业要求2026夏.pdf`：课程大作业要求 PDF。

当前工作文档：

- `AGENT.md`：项目状态、建模决策与后续任务维护说明。
- `environment.yml`：项目专用 conda 环境定义，环境名为 `operations_research`。
- `doc/第一阶段建模方案.md`：第一阶段建模主方案。
- `doc/第一阶段.md`：第一阶段步骤 1-5 的正式建模文档，包含 benchmark 计算、混合运输目标规划模型、非完美运行求解过程、扩展多时期发射场级模型，以及案例评估与方法对比的开展逻辑。
- `doc/第一阶段数据收集清单.md`：按步骤整理的数据收集任务清单。
- `doc/第一阶段数据.md`：由 `doc/第一阶段调查过程/第一阶段数据调查结果2.md` 复制得到，作为后续查数据和取参数的主数据文档。
- `doc/第一阶段调查过程/第一阶段数据调查结果.md`：第一阶段已有数据调查结果与参数建议。
- `doc/第一阶段调查过程/第一阶段数据调查结果2.md`：从头重新调查得到的第一阶段参数来源与建议值，当前来源核验主要针对该文件。
- `doc/运筹学数学表达写法规范.md`：课程常用数学表达写法参考。

当前脚本与结果文件：

- `script/solve_mixed_model.py`：混合运输目标规划/整数规划求解脚本。使用 `scipy.optimize.milp` 调用 HiGHS 求解器，分别求解成本+工期优先、环境优先、均衡三组权重。
- `script/solve_reduced_search.py`：结构化降维求解脚本。枚举总火箭发射次数 \(n_R=0,\dots,800000\)，直接计算目标函数并选择最优解，用于快速求解和校验 MILP 结果。
- `script/solve_nonideal.py`：非完美运行求解脚本。使用综合非完美主情景 \(a_E=0.90,a_R=0.98\)，通过一维整数搜索求解并与完美运行结果比较。
- `script/solve_extended_model.py`：扩展多时期发射场级模型求解脚本。外层从 \(T=50\) 年开始自适应枚举，不设置模型意义上的工期上界；内层使用凸二次调度近似分配发射场-年份火箭发射次数。
- `result/mixed_model_results.csv`：三组权重情景的数值结果。
- `result/mixed_model_results.md`：三组权重情景的结果摘要。
- `result/reduced_search_results.csv`：一维整数搜索求解得到的三组权重情景结果。
- `result/reduced_search_results.md`：一维整数搜索结果摘要。
- `result/reduced_search_vs_milp.csv`：一维整数搜索与 HiGHS MILP 结果对照。
- `result/nonideal_results.csv`：综合非完美主情景的三组权重求解结果。
- `result/nonideal_results.md`：非完美运行结果摘要。
- `result/nonideal_vs_ideal.csv`：非完美运行解与完美运行解的逐项对比。
- `result/extended_model_results.md`：扩展模型结果摘要。
- `result/extended_model_results.csv`：扩展模型三组权重情景的最优解。
- `result/extended_by_time.csv`：扩展模型外层所有候选工期的目标函数与指标。
- `result/extended_stage_results.csv`：扩展模型最优解的 10/60/30 阶段运输结果。
- `result/extended_site_summary.csv`：扩展模型最优解的发射场分配汇总。
- `result/extended_site_year_schedule.csv`：扩展模型最优解的发射场-年份调度表。
- `result/tradeoff_frontier_sample.csv`：时间-排放权衡曲线的采样数据。
- `report/figures/transport_split.png`：三组情景下电梯/火箭运输量分配图。
- `report/figures/normalized_metrics.png`：三组情景的成本、时间、排放归一化对比图。
- `report/figures/tradeoff_time_emission.png`：时间-排放权衡曲线图。
- `report/figures/nonideal_change_rates.png`：非完美运行相对完美运行的指标变化率图。
- `report/figures/extended_objective_by_time.png`：扩展模型外层枚举工期目标函数曲线。
- `report/figures/extended_stage_transport.png`：扩展模型最优解阶段运输量图。
- `report/figures/extended_site_launches.png`：扩展模型最优解发射场分配图。
- `report/figures/ChatGPT Image 2026年6月9日 16_56_07.png`：用户提供的 1:1 报告配图，已插入 `report/thesis.tex` 的“前言”部分末尾。
- `report/thesis.tex`：LaTeX 正式报告主文件，当前目录结构已包含“题目、作者和摘要”“前言”“问题描述”“优化方法”“案例分析”“结论”“参考文献”“附录”“分工与贡献”。
- `slidev-courseware/slides.md`：课堂汇报用 Slidev 网页课件主文件，按问题叙述、三层模型建模与求解、结论组织。
- `slidev-courseware/components/Formula.vue`：Slidev 课件公式渲染组件，使用 KaTeX 渲染行内和块级数学公式。
- `slidev-courseware/style.css`：Slidev 课件全局视觉样式，包含封面、章节页、模型框、结果表格、图表页等排版样式。
- `slidev-courseware/public/figures/`：Slidev 课件所需图表副本，包括报告配图、运输分配图、归一化指标图、非完美变化率图、扩展模型图表等。
- `slidev-courseware/README.md`：Slidev 课件运行和构建说明；本地运行命令为 `npm run dev`，构建命令为 `npm run build`。
- `slidev-courseware/面向月球基地建设的材料运输优化方案_图片版.pptx`：由 Slidev 页面逐页导出 PNG 后生成的图片版 PPTX，每页为全屏图片，便于在 PowerPoint 中保持网页字体和排版一致。

## Current Modeling Decisions

第一阶段采用五步推进：

1. 完美运行条件下，计算仅使用 Space Elevator System 的方案。
2. 完美运行条件下，计算仅使用传统火箭的方案。
3. 完美运行条件下，建立目标规划模型，计算电梯 + 火箭混合运输最优方案。
4. 非完美运行条件下，只改变有效运力，不把风险成本加入目标函数，计算解决方案变动程度。
5. 扩展为多时期发射场级模型，同时考虑不同发射场环境敏感系数、连续高频发射的非线性环境累积影响、10/60/30 建设运输节奏和火箭技术随时间进步。

核心建模判断：

- `179,000 公吨/年` 被假设为单个 Galactic Harbour 的年运力。
- Space Elevator System 共有 3 个 Galactic Harbours，因此：

  \[
  Q_E = 3 \times 179000 = 537000
  \]

  单位为公吨/年。

- 总建设材料需求：

  \[
  M = 100000000
  \]

  单位为公吨。

- 火箭单次月球运输载荷按题目给定设为：

  \[
  q_R \in \{100,125,150\}
  \]

  主值通常取 125 公吨/次。

- 仅使用太空电梯时，完成 100,000,000 公吨运输约需：

  \[
  \frac{100000000}{537000} \approx 186.22
  \]

  即约 186 年。

- 仅使用火箭时，如果单次载荷为 100-150 公吨，总发射次数约为 666,667 到 1,000,000 次。

因此，第一阶段最终推荐方案不应是单纯成本最小化，而应是成本、时间、环境影响三目标下的目标规划模型。

当前第一版建模计划已经推进到步骤 1-5：步骤 1、2 不再单独写成完整优化模型，只作为电梯-only 与火箭-only 的 benchmark 计算；步骤 3 写成标准目标规划/混合整数规划模型，用 benchmark 结果标定目标值、归一化基准和方案对比；步骤 4 保持目标函数不变，只设置一个综合非完美主情景，通过 \(a_E=0.90,a_R=0.98\) 修正有效运力并计算解的变动程度；步骤 5 将模型扩展为多时期发射场级调度模型。

步骤 1-5 的第一版正式建模已写入 `doc/第一阶段.md`。步骤 1-4 暂不设置单个发射场发射次数上限，火箭部分先用总发射次数 \(n_R\) 表示；步骤 5 开始引入发射场-年份变量 \(n_{i,t}\)，用于处理发射场环境敏感性和连续发射环境累积影响。

步骤 5 的当前口径：

- 不加入月球基地最大接收能力约束。
- 10/60/30 表示三个建设阶段的运输量比例；步骤 5 保留总工期 \(T\) 的选择，通过外层枚举 \(T\in\{50,51,\dots\}\)，并在每个候选 \(T\) 下按前 20%、中间 50%、后 30% 年份划分 \(P_1(T),P_2(T),P_3(T)\)。脚本使用“目标函数连续 30 年未改善则停止”的自适应搜索规则，并保留 \(T=250\) 年作为防死循环的程序保护上限。
- 用 \(s_i\) 表示发射场环境敏感系数。
- 用 \(S_{i,t}=\rho_iS_{i,t-1}+n_{i,t}\) 表示发射场环境压力存量。
- 用 \(S_{i,t}^2\) 表示连续高频发射的非线性环境累积损害，后续求解时可分段线性化。
- 用 \(f_{R,t}=f_R(1-\lambda_f)^{t-1}\)、\(g_{R,t}=g_R(1-\lambda_g)^{t-1}\) 表示火箭发射成本和排放随技术进步逐年下降。
- 步骤 5 比较不同候选工期时使用 \(T^*=\arg\min_{T\in\mathcal{T}}Z_5^*(T)\)。目标规划中成本目标和环境目标沿用基础模型，工期目标放宽为 \(T^*=75\) 年，并惩罚超过 75 年的正偏差 \(d_T^+/75\)。
- 当前步骤 5 脚本采用可解释近似：每个阶段优先使用太空电梯有效运力，火箭缺口用凸二次调度在发射场-年份之间分配。参数取 \(a_E=0.90,a_R=0.98,\lambda_f=0.005,\lambda_g=0.003,\beta=2.5\times10^{-11}\)。
- 当前步骤 5 仍不引入风险成本。

第一版步骤 1-3 还记录了一个结构化降维求解思路：在不限制单个发射场发射次数时，混合运输方案可由火箭总发射次数 \(n_R\) 唯一刻画。给定 \(n_R\) 后，可由 \(x_R=q_Rn_R\)、\(x_E=M-x_R\)、\(T=x_E/Q_E\) 直接得到成本、时间、排放和目标函数值。因此该目标规划整数模型可降维为一维整数搜索，用于快速求解、绘制 trade-off 曲线，并校验 HiGHS 的 MILP 结果。

步骤 1-3 的目标权重当前分三组：

- 成本+工期优先：\((w_C,w_T,w_G)=(0.45,0.40,0.15)\)，作为真实建设情景。
- 环境优先：\((w_C,w_T,w_G)=(0.10,0.05,0.85)\)，允许建设周期明显变长以降低排放。
- 均衡：\((w_C,w_T,w_G)=(0.30,0.25,0.45)\)。该组权重满足环境权重最高但小于 50%，成本权重次高但小于 40%，工期权重最低但不低于 25%；步骤 5 下最优工期为 79 年，落在 \(75,90\) 开区间内。

当前 Python 运行环境：

- 使用 `/Users/hippo/miniconda3/envs/operations_research`。
- 关键依赖：Python 3.11、NumPy、Pandas、Matplotlib、SciPy、HiGHS (`highspy`)。
- 当前项目后续脚本默认用 `conda activate operations_research` 或 `/Users/hippo/miniconda3/envs/operations_research/bin/python` 运行。

## Current Symbols

当前文档使用偏工程化、可读性较强的符号，而不是完全套用课堂标准形式：

- \(M\)：建设材料总需求量。
- \(Q_E\)：Space Elevator System 年总运力。
- \(x_E\)：通过 Space Elevator System 运输的材料量。
- \(x_R\)：传统火箭运输总量。
- \(x_i\)：第 \(i\) 个火箭发射场运输量。
- \(n_i\)：第 \(i\) 个火箭发射场发射次数。
- \(n_{i,t}\)：第 \(i\) 个火箭发射场第 \(t\) 年发射次数。
- \(y_{E,t}\)：第 \(t\) 年太空电梯有效运输量。
- \(y_{R,t}\)：第 \(t\) 年火箭有效运输量。
- \(S_{i,t}\)：第 \(i\) 个发射场第 \(t\) 年环境压力存量。
- \(T\)：运输总周期。
- \(c_E,c_R,c_i\)：电梯、火箭或发射场单位运输成本。
- \(e_E,e_i\)：电梯和火箭环境影响参数。
- \(a_E,a_i\)：电梯和火箭/发射场可用率。
- \(s_i\)：第 \(i\) 个发射场环境敏感系数。
- \(\rho_i\)：第 \(i\) 个发射场环境压力残留系数。
- \(\lambda_f,\lambda_g\)：火箭发射成本和排放的年下降率。
- \(w_C,w_T,w_G\)：成本、时间、环境权重。

用户曾要求尝试按课堂规范改写符号，后决定改回当前这套符号。后续不要再擅自改成 \(x_0,Q_0,w_1,\alpha_i\) 等课堂版符号，除非用户明确要求。

## Current Documents Status

### `doc/第一阶段建模方案.md`

已完成内容：

- 第一阶段问题定位。
- 基本假设。
- 极端方案数量级分析。
- 仅电梯方案模型。
- 仅火箭方案模型。
- 混合运输基础约束系统。
- 完美运行条件下的多目标/目标规划主模型。
- 非完美运行条件下的可用率修正模型。
- 后续扩展目标与约束。
- 数据收集清单。
- 求解步骤和评价指标。

重要修订历史：

- 原先“模型 C：电梯 + 火箭混合方案”被降级为“混合运输基础约束系统”。
- 主模型被明确为“混合运输基础约束系统 + 目标规划”。
- 非完美运输条件下，第四步只修改有效运力约束，不把风险成本加入目标函数。
- 风险成本 \(r_E,r_i\) 当前不进入步骤 1-5。

### `doc/第一阶段数据收集清单.md`

已按五步流程重排：

- 步骤 1-3：完美运行条件下需要的数据。
- 步骤 4：非完美运行条件下需要的数据。
- 步骤 5：扩展多时期发射场级模型需要的数据。

已补充“中文描述 + 符号”的参数：

- 电力来源排放因子 \(\gamma_E\)
- 火箭燃料类型 \(\tau_R\)
- 发射场位置 \(l_i\)
- 发射场延误率 \(\delta_i\)
- 发射场固定使用成本 \(F_i\)
- 发射场环境敏感性 \(s_i\)

发射场位置 \(l_i\) 的定位：

- 不作为前三步的核心硬约束。
- 辅助估计发射场能力 \(N_i\)。
- 为第三阶段环境敏感性 \(s_i\) 提供基础数据。

### `doc/第一阶段调查过程/第一阶段数据调查结果.md`

已有较完整的数据调查结果，包含：

- 数据清单逐项对照表。
- 建议直接采用的主参数表。
- 太空电梯单位成本、运营成本、能耗与电力排放因子。
- 火箭载荷、发射成本、单位运输成本与排放指标。
- 十个发射场的对应场址、位置、条件、能力估计与 \(N_i\) 主值。
- \(T_{\max}\)、\(C_0,T_0,G_0\)、\(w_C,w_T,w_G\)、\(C^*,T^*,G^*\) 建议。
- 非完美运行条件下的 \(a_E\)、\(a_i\)、\(\delta_i\) 估计。
- 可直接放入模型的参数字典。

关键已调查参数包括：

- \(c_E=250000\) USD/公吨，灵敏度 100000/250000/500000 USD/公吨。
- \(Q_E=537000\) 公吨/年。
- \(e_E=50000\) kWh/公吨。
- \(\gamma_E\)：太阳能 0.048、核能 0.012、美国电网 0.350 kgCO2e/kWh。
- \(q_R=125\) 公吨/次，灵敏度 100/125/150。
- \(f_R=178\) million USD/次，采用 NASA Europa Clipper Falcon Heavy launch services 合同作主值；NASA Falcon Heavy 合同敏感性范围取 117/152.5/178/255/256.6 million USD/次。
- \(c_R=1,424,000\) USD/公吨，当 \(q_R=125\)、\(f_R=178M\)。
- Falcon Heavy 估算排放：约 1230-1246 tCO2/次、544 tH2O/次、0.27 tNOx/次。
- 主建设期限 \(T_{\max}=50\) 年，灵敏度 50/75/100。30 年已被认为对 100,000,000 公吨建设材料运输偏激进。
- 当前步骤 1-3 权重分三组：成本+工期优先 \((0.45,0.40,0.15)\)，环境优先 \((0.10,0.05,0.85)\)，均衡 \((0.30,0.25,0.45)\)。
- \(a_E=0.98\)，灵敏度 0.90/0.98/0.999。
- \(a_R=0.98\)。
- 十个发射场 \(N_i\) 主值：
  - Alaska=4
  - California=50
  - Texas=25
  - Florida=90
  - Virginia=12
  - Kazakhstan=15
  - French Guiana=12
  - Satish Dhawan=12
  - Taiyuan=15
  - Mahia=120
- 十个发射场 \(\delta_i\) 主值：
  - Alaska=0.12
  - California=0.12
  - Texas=0.25
  - Florida=0.30
  - Virginia=0.18
  - Kazakhstan=0.08
  - French Guiana=0.18
  - Satish Dhawan=0.20
  - Taiyuan=0.10
  - Mahia=0.18

## What Is Done

已经完成：

- 题目文件和任务拆分已整理在 `task/`。
- 第一阶段建模路线已确定。
- 已将 `doc/第一阶段调查过程/第一阶段数据调查结果2.md` 复制为 `doc/第一阶段数据.md`，后续作为主数据文档使用。
- 已创建 `doc/第一阶段.md`，完成步骤 1-3 的正式建模：电梯-only benchmark、火箭-only benchmark、混合运输目标规划/整数规划模型。
- 已在 `doc/第一阶段.md` 中追加步骤 4 的非完美运行求解过程：使用综合非完美主情景 \(a_E=0.90,a_R=0.98\) 修正 \(x_E\le a_EQ_ET\)、\(x_R\le a_Rq_Rn_R\)，保持目标函数不变，并给出与步骤 3 完美运行结果对比的解变化评价指标。
- 已在 `doc/第一阶段.md` 中追加步骤 5 的扩展多时期发射场级模型：引入 \(n_{i,t}\)、\(y_{E,t}\)、\(S_{i,t}\)、发射场环境敏感系数 \(s_i\)、非线性环境累积项 \(S_{i,t}^2\)、10/60/30 建设运输节奏，以及随时间变化的 \(f_{R,t},g_{R,t}\)。
- 已将步骤 5 修改为方案 A：外层从 \(T=50\) 开始自适应枚举，内层求解该 \(T\) 下的发射场级调度模型，最后比较 \(Z_5^*(T)\) 选择最优工期和对应方案。`doc/第一阶段建模方案.md` 也已同步该口径。
- 已将步骤 5 的目标函数改为与基础目标规划一致的偏差变量形式：成本目标和环境目标沿用基础模型，工期目标改为 \(T^*=75\) 年。
- 已新增并运行 `script/solve_phase1_step5_extended_model.py`。当前步骤 5 求解结果：成本+工期优先选择 \(T=75\) 年，电梯 36.247 Mt、火箭 63.753 Mt、火箭发射 520,430 次、成本约 75.786 trillion USD、CO2 约 0.708 billion tCO2；环境优先选择 \(T=116\) 年，电梯 54.947 Mt、火箭 45.053 Mt、火箭发射 367,782 次、成本约 50.625 trillion USD、CO2 约 0.592 billion tCO2；均衡选择 \(T=79\) 年，电梯 38.180 Mt、火箭 61.820 Mt、火箭发射 504,649 次、成本约 74.295 trillion USD、CO2 约 0.701 billion tCO2。
- 已将步骤 5 数值结果写入 `doc/第一阶段.md` 的 6.12 节，并生成 `result/phase1_step5_results.md` 与三张步骤 5 可视化图。
- 已对步骤 5 权重做临时敏感性测试。若保持 \(w_C=w_T\) 并逐步提高环境权重，约在 \((w_C,w_T,w_H)=(0.275,0.275,0.450)\) 时最优工期从 75 年变为 76 年；若固定 \(w_C=0.45\)，则约在 \(w_T=0.20,w_H=0.35\) 时最优工期变为 76 年。
- 已根据用户要求把均衡情景改为 \((0.30,0.25,0.45)\)，并重新运行步骤 3、步骤 3 降维校验、步骤 4、步骤 5 的全部脚本；`doc/第一阶段.md`、`doc/第一阶段建模方案.md`、`doc/第一阶段数据.md` 已同步新权重和结果。
- 已将原先较细的均衡权重改成更整齐的 \((0.30,0.25,0.45)\)，该设置下步骤 5 均衡情景最优工期为 79 年；`doc/第一阶段调查过程/第一阶段数据调查结果1.md` 和 `doc/第一阶段调查过程/第一阶段数据调查结果2.md` 也已同步该口径。
- 已再次重新运行第一阶段全部求解脚本，并同步清理 `doc/第一阶段数据收集清单.md` 与 `doc/第一阶段调查过程/第一阶段数据调查结果1.md` 中残留的旧权重口径，当前统一为三组情景：成本+工期优先、环境优先、均衡。
- 已确定本大作业只继续完成第一阶段，不再展开第二阶段和第三阶段；后续任务转入第一阶段案例评估、方法对比和最终报告写作。
- 已在 `doc/第一阶段.md` 新增第 7 节“案例评估与方法对比的开展逻辑”，整理评价目标、评价指标、极端方案评估、混合运输方案评估、非完美运行评估、扩展模型评估、方法对比和推荐方案形成逻辑。
- 已创建 `operations_research` conda 环境，并安装 SciPy/HiGHS 作为专门运筹学 MILP 求解器。
- 已编写并运行 `script/solve_phase1_mixed_model.py`，完成三组权重情景求解和可视化输出。
- 已将步骤 1-3 的主目标工期从 30 年调整为 50 年，并重新运行求解脚本。50 年口径下：成本+工期优先和均衡方案均为电梯 26.85 Mt、火箭 73.15 Mt、火箭发射 585,200 次、总工期 50 年、成本约 106.851 trillion USD、排放约 0.841 billion tCO2；环境优先方案为电梯 67.568 Mt、火箭 32.432 Mt、火箭发射 259,459 次、总工期约 125.82 年、成本约 52.940 trillion USD、排放约 0.600 billion tCO2。
- 已修复 `script/solve_phase1_mixed_model.py` 的可视化问题：`phase1_normalized_metrics.png` 由于 Pandas index 自动对齐导致柱状数据变成 NaN，已改为显式使用 numpy 数组；`phase1_tradeoff_time_emission.png` 中成本+工期优先和均衡解重合导致文字重叠，已改为合并标注。
- 已在 `doc/第一阶段.md` 新增 4.9“结构化降维求解思路”，说明当前第一版模型可由总火箭发射次数 \(n_R\) 降维为一维整数搜索。
- 已统一清理项目文档和脚本中的旧成本项表述。后续电梯金钱成本只通过单位运输成本 \(c_E\) 表达。
- 已新增并运行 `script/solve_phase1_reduced_search.py`，用一维整数搜索求解三组权重情景。该脚本与 HiGHS MILP 结果最大绝对差异约为 \(1.56\times10^{-13}\)，可视为浮点误差内一致。
- 已新增并运行 `script/solve_phase1_nonideal.py`，求解步骤 4 综合非完美主情景 \(a_E=0.90,a_R=0.98\)。成本+工期优先方案相对完美运行：火箭发射次数约增加 5.79%，成本约增加 5.39%，排放约增加 3.73%，工期基本保持 50 年；环境优先方案相对完美运行：工期约增加 12.89%，成本约下降 0.98%，排放基本不变。
- 已将步骤 1-4 的求解数值结果直接记录进 `doc/第一阶段.md`：2.1 记录电梯-only benchmark，3.1 记录火箭-only benchmark，4.10 记录完美运行混合模型三组权重结果，5.8 记录综合非完美主情景结果及相对完美运行的变化率。
- 第一阶段主模型从单一成本模型调整为目标规划模型。
- 单个 Galactic Harbour 年运力口径已统一为 179,000 公吨/年。
- 数据收集清单已按步骤重排。
- 关键数据调查已经形成一版完整结果。
- 符号系统已定为 \(M,Q_E,x_E,x_R,q_R,c_E,w_C\) 等工程可读风格。
- 已创建 `AGENT.md` 作为项目状态和后续任务维护说明。
- 已对 `doc/第一阶段调查过程/第一阶段数据调查结果2.md` 做来源真实性核验和断网链接复查。多数链接真实可访问；太空电梯成本、Falcon Heavy 推进剂、NASA Falcon Heavy 发射服务合同、Rocket Lab 场址能力、NASA 月面货运能力、FAA 保险费率等关键来源可支撑对应判断。
- 已将 `doc/第一阶段调查过程/第一阶段数据调查结果2.md` 中 \(f_R\) 从 97M 历史商业报价改为 178M NASA Europa Clipper 合同主值，并同步更新 \(c_R\) 与 \(C_0\)。

## What Remains

第一阶段求解任务已结束，后续不再展开第二阶段和第三阶段。当前待完成的是第一阶段成果整理：

1. 将 `doc/第一阶段.md` 第 7 节案例评估逻辑扩写为正式“解的评估与方法对比”文本。
2. 生成或整理最终 `result/phase1_result.md`，记录：
   - 三种完美运行方案的结果。
   - 非完美运行下的解变化。
   - 步骤 5 扩展模型结果。
   - 权重与敏感性分析。
   - 推荐方案和研究结论。
3. 检查并统一 `doc/第一阶段建模方案.md`、`doc/第一阶段数据.md` 和 `doc/第一阶段调查过程/第一阶段数据调查结果*.md` 中的最终参数口径。
4. 根据来源核验结论，最终报告中需要把“来源直接给出”“由来源推算”“建模情景假设”三类参数分开标注。
5. 如篇幅允许，可对步骤 5 的扩展参数 \(s_i,\rho_i,\alpha,\beta,\lambda_f,\lambda_g\) 做简短敏感性说明，但这不是继续求解阶段的必要任务。

最终报告待完成：

- Summary Sheet。
- 目录。
- 完整解决方案。
- 一页致 MCM Agency 推荐信。
- 参考文献。
- AI 使用报告。

## Important Modeling Cautions

- 不要把 `Mahia=120 次/年` 误认为重型月球货运能力。Mahia 是高频小火箭场址；如果模型严格限定 Falcon Heavy-class 月球货运，应设为 0 或作为改造后情景。
- 不要把当前 Falcon Heavy 官方现实能力直接当成题目 2050 年 advanced Falcon Heavy 能力。主模型应服从题目给定的 100-150 公吨/次，当前能力只作现实校验。
- 不要在第四步非完美运行中把风险成本加入目标函数。第四步只通过 \(Q_E^{eff}=a_EQ_E\)、\(q_R^{eff}=a_Rq_R\) 改变有效运力。
- 当前步骤 5 也不引入风险成本，重点是发射场环境敏感性、非线性环境累积、10/60/30 建设运输节奏和技术进步。
- 发射场位置 \(l_i\) 不直接进入前三步核心目标规划，但应保留，因为它服务 \(N_i\)、\(\delta_i\) 和 \(s_i\) 的解释。
- 太空电梯成本、能耗、可用率均无真实运行数据，必须以“来源 + 情景假设 + 灵敏度分析”呈现。
- 当前 SpaceX 官方 PDF 不再直接列 Falcon Heavy 固定价。第一阶段 \(f_R\) 主值应采用更可核验的 NASA Falcon Heavy launch services 合同口径；97M 只能作为历史商业低价背景，不再作为主值。
- \(e_E=85\) kWh/kg、\(a_E\)、\(a_i\)、\(\delta_i\)、大部分 \(F_i\)、\(s_i\)、\(L_t\)、\(D_t\)、\(r_E\)、\(r_i\) 都应标为“推算值或情景假设”，不能写成来源直接实测。
- 发射场 \(N_i,N_i^H\) 的具体上限多数不是官方硬上限。Florida、Texas、Rocket Lab 小火箭场址等有较强直接来源；其他场址多为历史能力或规划能力基础上的条件估计。

## Maintenance Rule For Future Agents

After every substantive task in this project, update this `AGENT.md` before final response.

Minimum update requirements:

1. Update `Last updated`.
2. Add or modify any changed project status under `What Is Done` or `What Remains`.
3. Record any new modeling decision under `Current Modeling Decisions` or `Important Modeling Cautions`.
4. Record any newly created/modified major file under `Source Files` or the relevant status section.
5. If data values or parameter assumptions change, update `Current Documents Status` and the key parameter list.
6. Do not rewrite this file wholesale unless the project structure changes substantially; prefer small, accurate updates.

This file is the project handoff note. Keep it accurate, concise, and synchronized with the actual files.
