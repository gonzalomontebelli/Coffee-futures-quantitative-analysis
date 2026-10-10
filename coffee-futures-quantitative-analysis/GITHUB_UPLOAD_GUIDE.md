# Publish This Project to GitHub

## Option A — Git CLI (recommended)

1. Extract the ZIP file; **do not upload the ZIP as a single repository file**.
2. On [github.com/new](https://github.com/new), create an **empty public repository** named `coffee-futures-quantitative-analysis`. Leave **Add README**, **Add .gitignore**, and **Add license** disabled: this project already contains those files.
3. Open a terminal **inside the extracted project directory** and run:

```bash
git init
git add .
git commit -m "Initial release: reproducible coffee futures quant case study"
git branch -M main
git remote add origin https://github.com/gonzalomontebelli/coffee-futures-quantitative-analysis.git
git push -u origin main
```

Change the remote URL if your GitHub account or repository name differs. Authenticate using the browser, SSH, or an appropriately configured credential manager.

## Option B — GitHub browser

1. Create the empty repository.
2. Extract the ZIP on your computer.
3. Choose **Add file → Upload files** in the new GitHub repository.
4. Drag the **contents** of the extracted `coffee-futures-quantitative-analysis/` directory, preserving the folder structure. Do not create a redundant parent folder on GitHub.
5. Confirm that `README.md`, `docs/`, `src/`, `data/`, `results/`, `assets/`, `reports/` and `.github/` are at the repository root.
6. Click **Commit changes**. Check that the README renders charts and that the GitHub Actions workflow runs.

**Note:** GitHub's browser upload can be limited for large/many files; use Git CLI if any nested folders are omitted.

## Suggested GitHub settings

**Description:** Reproducible quantitative finance project: coffee futures pricing, options, Monte Carlo, structured products, hedging, and risk management with Python.

**Topics:** `python`, `quantitative-finance`, `derivatives-pricing`, `monte-carlo-simulation`, `risk-management`, `commodities`, `structured-products`, `financial-modeling`.

Set visibility to **Public** if you intend to link this educational project in a CV, LinkedIn profile, or job application.

## Reproducibility check

```bash
python -m pip install -r requirements.txt
python scripts/run_analysis.py
python -m pytest -q
```

## Publication checks

- All public-facing content and plot labels are in English.
- Assumptions and analyst-designed scenarios are clearly distinguished from observed market data.
- The Citi/Forage simulation disclaimer remains visible.
- Never commit credentials, client information, proprietary reports or trading account records.
- Review `.gitignore` and LICENSE before publishing any future additions.
