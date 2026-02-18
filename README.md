# 🧬 CLD Clone Selection Optimization Dashboard

## Overview

A **Streamlit-based Monte Carlo simulation dashboard** for optimizing **Cell Line Development (CLD)** clone selection workflows in biopharmaceutical manufacturing. Upload your assay data, configure screening parameters, and evaluate the probability of selecting top-performing clones under various correlation and workflow configurations.

## Key Features

- **Multi-step workflow simulation** — 2-step or 3-step clone selection pipelines
- **Monte Carlo engine** — configurable repetitions with correlation modeling between assay steps
- **Sensitivity analysis** — parameter impact assessment for `step1_keep`, `step2_keep`, and `top_x_percent`
- **Interactive Plotly visualizations** — success probability curves, distribution comparisons, Sankey flow diagrams, computed parameter interaction heatmaps, efficiency radar charts
- **Criteria-based filtering** — apply quality filters at the initial or final selection step
- **Data quality assessment** — automatic outlier detection, skewness analysis, and recommendations
- **Rule-based assistant** — expert system with data quality analysis, parameter recommendations, results interpretation, and interactive chat
- **Reproducible results** — random seed control for consistent simulations
- **CSV export** — download simulation results and analysis reports

## Expected Input Format

Excel file (`.xlsx`) with:
- **Required:** Column named `Results` containing numeric assay values
- **Optional:** Columns starting with `Criteria` (e.g., `Criteria1`, `Criteria2`) for filtering
- **Multiple sheets** supported with automatic sheet selection

## Project Structure

```
├── app.py               # Main Streamlit application (orchestrator)
├── simulation.py        # Monte Carlo simulation engine
├── loader.py            # Data loading, validation, and preprocessing
├── sidebar.py           # Parameter configuration UI
├── plots.py             # Interactive Plotly visualizations
├── ai_agent.py          # Rule-based expert system assistant
├── requirements.txt     # Python dependencies
└── *.md                 # Documentation files
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Launch the dashboard
streamlit run app.py
```

## Usage

1. **Upload** your Excel file via the sidebar
2. **Configure** simulation parameters (workflow steps, clone counts, correlation range)
3. **Run Simulation** — Monte Carlo analysis across correlation values
4. **Explore tabs** — Sensitivity Analysis, Workflow Comparison, Advanced Plots, Assistant, Results Summary
5. **Export** results as CSV

## Simulation Details

### Correlation Model

Assay correlation between steps is modeled as:

```
assay_step_n = ρ × previous_scores + √(1 − ρ²) × noise
```

where `ρ` is the correlation coefficient and `noise` is independently sampled from the fitted distribution.

### Distribution Methods

| Method | Description |
|--------|-------------|
| **Lognormal** | Parametric fit via `scipy.stats.lognorm` — best for moderately skewed data |
| **KDE** | Non-parametric kernel density estimation — best for highly skewed or multimodal data |

### Success Metric

A simulation trial is "successful" when **all** final selected clones fall within the **top X%** of the original data distribution. The dashboard reports success probability based on effective (non-skipped) Monte Carlo iterations.

## Dependencies

```
streamlit>=1.30,<2.0
pandas>=1.5.0,<3.0
numpy>=1.23.0,<2.0
scipy>=1.10.0,<2.0
plotly>=5.15.0,<6.0
openpyxl>=3.1.0,<4.0
```

Requires **Python 3.8+**.

## Tabs Overview

| Tab | Contents |
|-----|----------|
| 🎯 Main Simulation | Run Monte Carlo, view success probability vs correlation, distribution comparison |
| 📊 Sensitivity Analysis | One-at-a-time parameter sweeps with summary table |
| 🔄 Workflow Comparison | Side-by-side 2-step vs 3-step probability comparison |
| 📈 Advanced Plots | Parameter interaction heatmap, Sankey flow diagram, efficiency radar chart |
| 🤖 Assistant | Rule-based expert system: data quality, recommendations, results analysis, chat |
| 📋 Results Summary | Key findings, performance recommendations, CSV export |
