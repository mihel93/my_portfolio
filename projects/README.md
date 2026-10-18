# 📊 Data Analytics Portfolio · Mihail Deligrozev

Data analyst based in the Netherlands, working with **Python, SQL and Power BI**. I hold an MSc in Engineering and Policy Analysis from TU Delft and the Microsoft PL-300 Power BI Data Analyst certification, and I've been doing freelance analytics in gaming, real estate and HR tech since 2023.

Each project below goes from raw data to conclusions: data checks, clear definitions, honest statistics and a readable report.

🔗 **Kaggle:** [kaggle.com/mihaildeligrozev](https://www.kaggle.com/mihaildeligrozev)

---

## 🗂️ Projects at a glance

| Project | Question | Main tools | Notebook |
|---|---|---|---|
| 🎮 [Steam game success](#-what-makes-a-steam-game-successful) | What makes a game successful, and can it be predicted at launch? | Python, SQL (DuckDB), scikit-learn | [Kaggle](https://www.kaggle.com/code/mihaildeligrozev/steam-game-success) |
| 👥 [IBM HR attrition](#-ibm-hr-analytics-employee-attrition) | Who leaves, why, and what would retention measures be worth? | Python, SciPy, scikit-learn | [Kaggle](https://www.kaggle.com/code/mihaildeligrozev/ibm-hr) |
| 🎒 [World Bank school dropout](#-do-richer-countries-keep-more-children-in-school) | Do wealth and public spending keep children in school? | Python, pandas, SciPy | *link to add* |
| 🏠 [Dutch housing market](#-dutch-housing-market-price-trends) | How have house prices developed across the Netherlands? | Python, CBS StatLine API, geopandas | *link to add* |
| 🏙️ [The Hague Airbnb](#️-the-hague-airbnb-eda) | What does the short-stay market in The Hague look like? | Python, matplotlib, seaborn | *link to add* |
| 🚌 [Sofia public transport](#-sofia-public-transport-gtfs) | How is Sofia's transit network structured and served? | Power BI, DAX | *link to add* |

---

## 🎮 What makes a Steam game successful?

An analysis of **125,855 Steam games**: defining success fairly, testing which launch-time features go with it, and predicting which new games become hits.

**Highlights:**
- **Concentrated success:** the top 1% of games hold 80% of all reviews (Gini 0.98).
- **Reach vs quality:** reach and quality are separate kinds of success (Spearman 0.00).
- **Prediction:** the model reaches AUC 0.80 on newer games, and its top 10% of predictions contain 43% of the actual hits.

**Skills:**
- **Data cleaning:** fixing a broken CSV header that shifted every column; parsing list-like text fields
- **SQL (DuckDB):** a relational data model, joins, CTEs and window functions (`ROW_NUMBER`, `NTILE`, `RANGE` frames for developer track records)
- **Storage optimisation:** lossless type changes (149 MB → 53 MB in memory); CSV vs Parquet vs DuckDB (40 MB → 10 MB on disk)
- **Statistics:** AUC as an effect size, Wilson confidence intervals, lift, Spearman correlation, Lorenz curve and Gini
- **Problem framing:** four success definitions, with a per-year cutoff that removes age bias
- **Machine learning:** gradient boosting with a time-based split and no leakage; ablation, permutation importance, SHAP, an ordinal model and TF-IDF text features
- **Visualisation:** ridgeline, Lorenz curve, waffle, dumbbell and forest plots, cumulative gains and calibration curves

---

## 👥 IBM HR Analytics: Employee Attrition

Who leaves, why, how well it can be predicted, and what retention measures would be worth, based on the IBM HR sample dataset (1,470 employees, fictional data created by IBM).

**Highlights:**
- **Overtime:** employees working overtime leave at 2.9x the rate of others (30.5% vs 10.4%).
- **Prediction:** a logistic regression reaches test AUC 0.82, and its top 20% of risk scores contain 62% of leavers.
- **Honest evaluation:** the model is compared against an 83.9%-accurate "everyone stays" baseline.

**Skills:**
- **Segmentation:** age, income and tenure bands validated with chi-square tests and Cramér's V
- **Statistics:** Wilson confidence intervals, Mann-Whitney tests for skewed pay data, effect sizes over p-values
- **Imbalanced classification:** baseline comparison, 5-fold cross-validation, a threshold chosen without touching the test set, precision/recall trade-off
- **Model explanation:** permutation importance, odds multipliers, and a check on misleading tree importance
- **Business case:** retention scenarios with explicit, adjustable assumptions, net value and ROI, including the option that doesn't pay off
- **Communication:** findings, roadmap, KPIs and limits, including fairness

---

## 🎒 Do richer countries keep more children in school?

Wealth, public spending and out-of-school rates across **217 economies, 2000–2025**, using World Bank World Development Indicators. It started as a TU Delft assignment and was rebuilt as a standalone case study.

**Highlights:**
- **Wealth:** GDP per capita is strongly linked to keeping children in school (rho −0.59 for adolescents; 20x higher out-of-school rates in the poorest vs richest quarter of countries).
- **Spending:** spending effort shows no link once wealth is held constant.

**Skills:**
- **Data wrangling:** handling a raw World Bank DataBank export (missing-value codes, footer rows, aggregates mixed with countries, metadata file checks)
- **Reproducible choices:** the analysis year is picked by a stated rule, not by eye
- **Bias awareness:** measuring the selection bias caused by dropping incomplete countries
- **Statistics:** Spearman correlation with bootstrap confidence intervals, partial rank correlation, quartile comparisons, robustness across years
- **Hypothesis testing:** clear verdicts on H1 and H2, with limitations

---

## 🏠 Dutch housing market price trends

House price trends in the Netherlands using official CBS data.

**Skills:**
- **APIs:** retrieving data from the CBS StatLine API
- **pandas:** time-series wrangling
- **Geospatial:** analysis and maps with geopandas

---

## 🏙️ The Hague Airbnb EDA

An exploratory analysis of Airbnb listings in The Hague.

**Skills:**
- **EDA:** exploratory data analysis
- **Visualisation:** charts with matplotlib and seaborn
- **Geospatial:** spatial analysis of listings

---

## 🚌 Sofia public transport (GTFS)

An analysis of Sofia's public transport network from GTFS timetable data.

**Skills:**
- **Power BI:** a data model built from GTFS tables, report design
- **DAX:** custom measures

---

## 🧰 Skills overview

| Area | Tools and methods |
|---|---|
| **Languages** | Python, SQL, DAX |
| **Data** | pandas, NumPy, DuckDB, Parquet, APIs (CBS StatLine, World Bank), GTFS |
| **Statistics** | Confidence intervals, effect sizes (AUC, Cramér's V), Spearman, Mann-Whitney, chi-square, bootstrap, Gini |
| **Machine learning** | scikit-learn, gradient boosting, random forest, logistic regression, cross-validation, SHAP, permutation importance |
| **Visualisation** | matplotlib, seaborn, Power BI, geopandas |
| **Practice** | Leakage-free evaluation, reproducible parameters, data-quality checks, clear write-ups with stated limitations |

---

📫 **Contact:** *add your LinkedIn, email or portfolio site here*
