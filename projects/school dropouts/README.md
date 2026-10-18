# 🎒 Do richer countries keep more children in school?

How national wealth and public spending relate to out-of-school rates across **217 economies, 2000–2025**, using World Bank World Development Indicators, with **Python (pandas, SciPy, matplotlib)**.

> Part of my data analytics portfolio. **Mihail Deligrozev**, data analyst (Python · SQL · Power BI)
> Originally Assignment 1 (Data Collection and Wrangling) of EPA-1316 Introduction to Urban Data Science, TU Delft, rebuilt as a standalone case study on a fresh WDI export (last updated 8 October 2026).

---

## 📌 Key findings

| | Result |
|---|---|
| **−0.59** | Rank correlation between GDP per capita and adolescents out of school in 2015 (n = 62) |
| **20×** | Median out-of-school rate for adolescents in the poorest vs the richest quarter of countries (20.3% vs 1.0%) |
| **≈ 0** | Link between spending effort and out-of-school rates once GDP is held constant |
| **35% → 42%** | Adolescents out of school in low-income countries, 2013 to 2024 |

**H1, "Richer countries have lower out-of-school rates": ✅ supported.** It holds for both age groups in every year from 2008 to 2016, in 2015 (rho = −0.53 for children and −0.59 for adolescents, n = 62), and in 2021 with a much larger sample (rho = −0.45 and −0.71, n = 136). The pattern looks like a threshold: rates are high below about $2,000 per capita and close to zero above $20,000.

**H2, "Countries that spend less per student have higher out-of-school rates": ❌ not supported.** Spending per student as a share of GDP per capita shows at most a weak raw link, and no link at all once wealth is held constant. That holds both in 2015 (n = 62) and with the latest 2014–2018 values (n = 103). Spending in dollars per student is almost the same variable as GDP per capita (rho = 0.97), so it can't separate money from wealth.

**The problem is concentrated and, for adolescents, getting worse:** in low-income countries the share of adolescents out of school rose from 35.5% in 2013 to 42% in 2024.

---

## 🔍 Approach

1. **Load and profile:** read the DataBank export and deal with its quirks: `..` for missing values, footer lines, 5 regional/income aggregates mixed in with the 217 economies, and a "metadata" file that repeats the data before its definitions block (verified to be identical).
2. **The bigger picture:** out-of-school trends by income group, 2000–2024.
3. **Hypotheses and year choice:** the cross-section year is picked by a stated rule (the most recent year with at least 60 economies reporting all five indicators, giving **2015**), not by eye.
4. **Missing data and selection bias:** measure what listwise deletion costs. Countries that report everything are about three times richer than those that don't.
5. **Testing:** Spearman rank correlations with bootstrap 95% confidence intervals, a GDP-quartile comparison, and partial rank correlation to hold wealth constant.
6. **Recent data:** retest H1 in 2021, the best-covered recent year (n = 136).
7. **Robustness:** rerun the tests for every year and with a latest-value window (2014–2018).

### Indicators used

| Role | Indicator | Code |
|---|---|---|
| Outcome | Children out of school (% of primary school age) | `SE.PRM.UNER.ZS` |
| Outcome | Adolescents out of school (% of lower secondary school age) | `SE.SEC.UNER.LO.ZS` |
| Explanatory | Government expenditure per student, primary (% of GDP per capita) | `SE.XPD.PRIM.PC.ZS` |
| Explanatory | Government expenditure per student, secondary (% of GDP per capita) | `SE.XPD.SECO.PC.ZS` |
| Explanatory | GDP per capita (current US$) | `NY.GDP.PCAP.CD` |

---

## 🖼️ Selected charts

| | |
|---|---|
| ![Out-of-school trends by income group](figures/fig02_income_group_trends.png) | ![Spearman correlations with confidence intervals](figures/fig04_forest_spearman.png) |
| ![Out-of-school rates by GDP quartile](figures/fig06_gdp_quartiles.png) | ![H1 with 2021 data](figures/fig07_recent_h1.png) |

All 8 charts are in [`figures/`](figures/).

---

## 📁 Repository contents

| File | What it is |
|---|---|
| `world_bank_school_dropout_analysis.ipynb` | The full notebook, with code and outputs |
| `world_bank_school_dropout_analysis.html` | Read-only report version with the code hidden |
| `5798c482-…_Data.csv` | Raw World Bank DataBank export (5 indicators × 222 countries and aggregates, 1960–2025) |
| `5798c482-…_Series - Metadata.csv` | The same export with indicator definitions |
| `output/school_dropout_2015_clean.csv` | Cleaned 2015 cross-section, 62 economies with all indicators, plus spending per student in US$ and GDP quartile |
| `output/school_dropout_2021_h1.csv` | 2021 sample for H1: 136 economies with GDP per capita and both out-of-school rates |
| `figures/` | Every chart as a PNG |

---

## ▶️ How to run

```bash
pip install pandas numpy scipy matplotlib
jupyter notebook world_bank_school_dropout_analysis.ipynb
```

Keep the two World Bank CSV files in the same folder as the notebook; it finds them by name pattern (`*_Data.csv`, `*Metadata.csv`). Cleaned tables and charts are written to `output/`.

To use a newer export, download the same five indicators from the [World Bank DataBank](https://databank.worldbank.org/source/world-development-indicators) as CSV and replace the two files. The year choice and sample sizes update automatically.

---

## ⚠️ Limitations

- **Selection bias:** the poorest countries are under-represented in the joint tests, because they report less complete data.
- **No recent spending data:** this export has no spending per student after 2018, so H2 can't be tested on recent years.
- **Correlation, not causation:** wealth also goes with health, governance, conflict and geography, none of which are controlled for.
- **Effort is a ratio:** spending per student divided by GDP per capita also depends on how many students there are, so a country can look generous because few children are enrolled.
- **Data revisions:** the WDI is revised every year. On an earlier export the same 2015 test had 55 countries and rho = −0.70; on this one it has 62 and rho between −0.53 and −0.59. The direction and conclusions didn't change.

## 🚀 Next steps

- Add income group and region from the WDI country metadata and compare within groups.
- Build a 2008–2018 panel with a regression on log GDP per capita, spending effort and region fixed effects.
- Add conflict and fragility indicators to separate poverty from instability in the Sahel cases.

---

**Data:** World Bank, [World Development Indicators](https://databank.worldbank.org/source/world-development-indicators), DataBank export last updated 8 October 2026.
