# Activity 02: organise and analyse ceramic laboratory data

## Aim

Combine the supplied quartz measurement exports into a traceable dataset, check selected results against the published paper and explain what the experiments tell you. Start with data preparation; agree the modelling scope at the first check-in.

The files contain real published experiments. No artificial observations or deliberate data errors have been added.

## Source material

The `data` folder contains the original Excel exports, the published paper, the authors' README files and a source manifest with download links and checksums.

Authors: Vojtech Necina and Willi Pabst, University of Chemistry and Technology, Prague.

- Experimental data: https://doi.org/10.5281/zenodo.18244921
- Paper: *Cold sintering of quartz ceramics and their peculiar effective properties*, Open Ceramics 26 (2026), 100946, https://doi.org/10.5281/zenodo.19251828
- Both records are licensed CC BY 4.0. Retain attribution and source information.

## Setup

Install `uv`, open PowerShell in this folder and run:

```powershell
uv sync --locked
uv run jupyter lab
```

Keep the original `data` files unchanged. Save your scripts and notebooks in this folder and write cleaned tables to a separate `outputs` folder.

## 1. Prepare and check the data

- Inventory the Excel files. Identify the specimen, measurement regime and source of each record.
- Combine the exports with pandas. Preserve the original measurement identifiers and source filenames.
- Create a separate specimen-information table from Table 2 in the paper. Document how you interpret shared table cells and unavailable results.
- Join the measurement and specimen tables. Check keys, repeated readings and unmatched specimens; account for every source row.
- Write a short data dictionary with units and definitions. Distinguish processing temperature from measurement temperature.
- Investigate unusual values and measurement-quality information. Keep a log of corrections, flags and unresolved questions.

At the first check-in, demonstrate the pipeline and discuss any uncertain units or records before excluding data.

## 2. Compare with the publication

- Reproduce selected processing-versus-porosity comparisons from Table 2 and Figure 3.
- Summarise repeat measurements by specimen, including their counts and spread.
- Compare applicable results with the paper's tables or figures. Explain differences and distinguish exact table checks from approximate visual comparisons.

Thermal diffusivity and thermal conductivity are different quantities. Only convert between them when the required quantities, units and assumptions are documented.

## 3. Optional modelling after the check-in

Agree what you intend to predict and which inputs would be available. Reserve the evaluation data before target-led EDA and feature choices. If predicting an unseen specimen, keep its repeated readings together.

Compare a training-mean baseline with one simple regression model on the same validation splits. Report MAE, RMSE and residuals. Explain how the small number of independent specimens limits your conclusions.

## Submit

- A repeatable loading, cleaning and joining script.
- Combined measurement and specimen CSVs, with a data dictionary.
- An audit log explaining decisions and unresolved issues.
- One notebook showing publication cross-checks, EDA and any agreed modelling.

There is no required model score. No raw laser-signal fitting, XRD interpretation or complex model tuning is needed.
