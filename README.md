# Quartz ceramics data analysis

Analysis of laser-flash thermal diffusivity measurements on cold-sintered quartz ceramics.
The raw Excel exports are combined into a traceable dataset, thermal conductivity is derived
and cross-checked against the published paper, and a simple regression model is compared with
a training-mean baseline.

See [docs/activity-brief.md](docs/activity-brief.md) for the full activity brief.

## Data source

Experimental data and paper by Vojtech Necina and Willi Pabst, University of Chemistry and
Technology, Prague (both CC BY 4.0):

- Data: https://doi.org/10.5281/zenodo.18244921
- Paper: *Cold sintering of quartz ceramics and their peculiar effective properties*,
  Open Ceramics 26 (2026), 100946, https://doi.org/10.5281/zenodo.19251828

## Setup

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12. From the repository root:

```powershell
uv sync --locked
uv run jupyter lab
```

## What to run

Open and run **`notebooks/v1.ipynb`** top to bottom. It:

1. loads and combines the measurement exports from `data/`, preserving source filenames and row numbers;
2. joins them with the specimen table (`data/Sample_table.xlsx`, transcribed from Table 2 of the paper);
3. derives thermal conductivity and cross-checks results against the paper's tables and figures;
4. cleans flagged measurements (with an audit log), runs EDA, and compares a Ridge regression against a training-mean baseline using leave-one-specimen-out validation.

## Repository layout

| Path | Contents |
| --- | --- |
| `notebooks/v1.ipynb` | Main notebook: loading, cleaning, publication cross-checks, EDA and modelling |
| `src/` | Reusable Python modules imported by the notebook |
| `src/thermal_properties.py` | Specific heat, density and thermal conductivity calculations |
| `src/eda.py` | Plotting and summary functions for exploratory analysis |
| `src/model_config.py` | Grouped train/test splitting, Ridge pipeline and model comparison |
| `data/` | Original Zenodo exports (unchanged) plus `Sample_table.xlsx` transcribed from the paper |
| `outputs/` | Generated tables, e.g. the combined measurements export |
| `notes/` | Scratch modelling notes |
| `docs/` | Activity brief |

Keep the original files in `data/` unchanged; write any generated tables to `outputs/`.
