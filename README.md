# Operations Research Final Project

This repository contains an operations research course final project based on the 2026 MCM Problem B setting. The project focuses on the first-stage problem: optimizing material transportation from Earth to a future Moon base construction site.

## Project Scope

The original task is narrowed to the construction-period material transportation problem. The model compares:

- Space elevator only transportation
- Rocket only transportation
- Mixed space-elevator and rocket transportation
- Non-ideal operating conditions
- An extended multi-period launch-site scheduling model

The optimization considers cost, construction duration, and environmental impact.

## Repository Structure

- `task/`: original problem statement, translated task files, and course requirements
- `doc/`: modeling notes, data collection checklist, investigated data, and first-stage modeling document
- `script/`: Python scripts for optimization and visualization
- `result/`: generated numerical results
- `report/`: LaTeX report source, figures, and compiled PDF
- `environment.yml`: conda environment specification

## Main Output

The final report is available at:

- `report/thesis.pdf`

The main LaTeX source is:

- `report/thesis.tex`

## Reproduce Results

Create the conda environment:

```bash
conda env create -f environment.yml
conda activate or-final-project
```

Run the main scripts:

```bash
python script/solve_mixed_model.py
python script/solve_reduced_search.py
python script/solve_nonideal.py
python script/solve_extended_model.py
```

Build the report:

```bash
cd report
latexmk -xelatex -interaction=nonstopmode thesis.tex
```

## Notes

This is a course project. Several 2050-era engineering parameters are scenario assumptions derived from public sources and documented in `doc/第一阶段数据.md`.
