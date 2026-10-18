# 👥 IBM HR Analytics: Employee Attrition Prevention Strategy

Who leaves, why, how well it can be predicted, and what retention measures would be worth, based on the IBM HR Analytics Employee Attrition & Performance dataset (1,470 employees), using **Python (pandas, SciPy, scikit-learn, seaborn)**.

> Part of my data analytics portfolio. **Mihail Deligrozev**, data analyst (Python · SQL · Power BI)

📌 The dataset is **fictional, created by IBM data scientists** for teaching. It is a single snapshot that shows who left, not when, so all rates are shares of this workforce, not annual turnover.

---

## 📌 Key findings

| | Finding |
|---|---|
| 📉 | **16.1% of employees left** (237 of 1,470). |
| ⏰ | **Overtime is the biggest lever:** 30.5% attrition with overtime vs 10.4% without (2.9x), the largest effect size of all factors tested (Cramér's V 0.24). |
| 🎯 | **Risk is concentrated** in Sales Representatives (39.8%), Laboratory Technicians (23.9%), the first two years of tenure (29.8%), under-25s (35.8%) and the lowest pay band (28.6%). |
| 💰 | **Leavers earn less:** median monthly income $3,202 vs $5,204. Pay, age and tenure move together, so these overlap as signs of being early in a career. |
| 😟 | **Dissatisfaction matters at the bottom of the scale:** the lowest work-life balance score has 31.2% attrition; above the lowest level the differences are small. |
| 🤖 | **Risk can be ranked:** logistic regression reaches **test AUC 0.82** (random forest 0.77). The top 20% of risk scores contain **62% of leavers**. |
| 💼 | **Business case:** a risk score with stay interviews and an early-career programme give the highest net value under the stated assumptions; targeted pay rises don't pay back on replacement cost alone (−41%). |

---

## 🤖 Model results (test set, 441 employees, 71 leavers)

| Model | CV AUC (5-fold) | Test AUC | Avg precision |
|---|---|---|---|
| Baseline: always "stays" | 0.50 | 0.50 | 0.16 |
| Random forest | 0.81 | 0.77 | 0.41 |
| **Logistic regression** | **0.82** | **0.82** | **0.60** |

The baseline is **83.9% accurate** without finding a single leaver, so accuracy is not used to judge the models.

The threshold was chosen on cross-validated training predictions, aiming to catch 60% of leavers. On the test set it flags **74 employees and catches 39 of 71 leavers** (recall 55%, precision 53%, against 16% for a random pick).

---

## 🔍 Approach

1. **Data quality:** one profile of missing values, duplicates, constant columns and IDs.
2. **Segments:** age, income and tenure bands, each validated with a chi-square test and **Cramér's V** as the effect size.
3. **Where and who:** attrition rates by department, role, demographics and satisfaction, with **Wilson 95% confidence intervals**; income and age compared with medians and Mann-Whitney tests, because income is skewed.
4. **Key factors:** ten factors ranked by effect size rather than p-value.
5. **Correlations:** correlation of numeric features with leaving, plus the full correlation matrix, to show which signals overlap.
6. **Model:** a baseline, a random forest and a logistic regression, compared with 5-fold cross-validated AUC on a stratified 70/30 split. Results are shown with ROC, cumulative gains, a confusion matrix at the chosen threshold, permutation importance, and odds multipliers for the direction of each effect.
7. **Business case:** four retention scenarios with every assumption in one parameter cell. Prevented departures come from the data where possible, and the results are shown as net value and ROI, including the one that doesn't pay off.

---

## 🖼️ Selected charts

| | |
|---|---|
| ![Attrition by age, income and tenure band](figures/fig01_attrition_by_band.png) | ![Effect size per factor](figures/fig06_factor_effect_sizes.png) |
| ![Model comparison: ROC and cumulative gains](figures/fig09_model_comparison.png) | ![Business case](figures/fig12_business_case.png) |

All 12 charts are in [`figures/`](figures/).

---

## 📁 Repository contents

| File | What it is |
|---|---|
| `ibm_hr_attrition.ipynb` | The full notebook, with code and outputs |
| `hr_utils.py` | Chart style, note boxes, confidence intervals, Cramér's V, rate charts and model-evaluation helpers |
| `ibm_hr_attrition.html` | Read-only report version with the code hidden |
| `Attrition.csv` | The dataset (1,470 employees × 35 columns) |
| `output/attrition_clean.csv` | Cleaned data with the age, income and tenure bands |
| `output/test_risk_scores.csv` | Risk score and flag for each test-set employee |
| `output/business_case.csv` | The four retention scenarios with their assumptions and results |
| `figures/` | Every chart as a PNG |

---

## ▶️ How to run

```bash
pip install pandas numpy scipy scikit-learn matplotlib seaborn
jupyter notebook ibm_hr_attrition.ipynb
```

Keep `hr_utils.py` and `Attrition.csv` in the same folder as the notebook.

**On Kaggle:** attach the dataset, upload `hr_utils.py` as a dataset (or model), then choose **Run All**. The notebook finds both files in `/kaggle/input` automatically.

To test other business assumptions, change the values in the `# Parameters` cells (cost per leaver, prevention rates, programme costs, target recall) and rerun.

---

## ⚠️ Limitations

- **Fictional data:** the patterns may not hold in a real organisation.
- **Snapshot, no dates:** rates aren't annual, and the model can't say *when* someone will leave.
- **Association, not cause:** overtime, pay and satisfaction go with leaving, but this data can't prove that changing them keeps people.
- **Small groups:** some roles and age bands have fewer than 100 people, so their rates are uncertain.
- **Business case = assumptions:** costs and prevention rates are illustrative inputs, not measured effects, and the scenarios overlap, so their savings aren't additive.
- **Fairness:** a risk score shouldn't drive decisions about individuals without human review; features such as age, gender and marital status need care.

## 🚀 Next steps

- Collect exit dates and model *time to leaving* (survival analysis).
- Pilot retention measures with a comparison group to measure their real effect.
- Check the model's error rates per gender and age group before any use.

---

**Data:** [IBM HR Analytics Employee Attrition & Performance (Kaggle)](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)
