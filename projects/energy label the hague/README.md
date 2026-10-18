# 🏠 Do Richer Neighbourhoods Live in Greener Homes?

**Household income, energy labels and neighbourhood types across the 114 neighbourhoods of The Hague**

A geographic data-science case study in Python: spatial analysis and hypothesis testing (Part I), then K-means clustering of neighbourhoods by their energy-label mix (Part II).

*Author: Mihail Deligrozev · Based on Assignments 2 and 3 of EPA-1316 Introduction to Urban Data Science, TU Delft*

![Income, A-label share and E–G share by neighbourhood](figures/fig03_maps_side_by_side.png)

---

## Key findings

| | Result |
|---|---|
| **−0.14** | Rank correlation of income with the share of A-label homes across all 106 neighbourhoods (p = 0.16): no clear link |
| **+0.47** | Rank correlation of income with the share of E–G homes outside the new-build district (n = 91, p < 0.001): richer means *worse* labels |
| **71% vs 40%** | Median share of E–G homes in high-income neighbourhoods vs the rest |
| **51% vs 6%** | Median share of A-label homes in Leidschenveen-Ypenburg (built after 1995) vs the rest of the city |
| **0.6** | Moran's I for income and for label shares: both strongly clustered on the map |
| **5 types** | K-means finds five stable neighbourhood types; 13 of the 27 high-income neighbourhoods fall in the **G-dominated** type |

**In short:** the hypothesis that richer neighbourhoods have more energy-efficient homes is rejected. Energy labels follow the **age of the housing**, not income. The best labels are in new-build areas with middle incomes, and the worst are in the wealthy pre-war villa areas along the dunes (Marlot, Duttendel, Nassaubuurt, Vogelwijk), which have 86–94% E–G homes.

---

## Research question and hypothesis

**Question.** Do neighbourhoods in The Hague with higher household incomes have more energy-efficient homes?

**H1.** Neighbourhoods with higher average standardised disposable income have a larger share of homes with good energy labels.

## Data

| File | Source | Contents |
|---|---|---|
| `neighborhoods.csv` | [Den Haag in Cijfers](https://denhaag.incijfers.nl) | Number of homes per energy label (A++ to G) and the average standardised disposable household income, per neighbourhood |
| `neighborhoods.json` (or `.shp` + `.dbf` / `.shx` / `.prj` / `.cpg`) | EPA-1316, TU Delft (prepared by Mikhail Sirenko) | Boundaries of the 114 neighbourhoods (*buurten*), WGS 84 |

The notebook joins the two on the `code + name` field (e.g. `70 Oostduinen`). All 114 neighbourhoods match.

## Methods

**Part I · Income and energy labels**
- Label shares (A-or-better, B–D, E–G) and an average label score (G = 1 … A++ = 9)
- Neighbourhoods with fewer than 100 labelled homes or no income figure excluded (8 near-empty areas, 0.1% of homes)
- Choropleth maps, a bivariate choropleth, and a sorted label-mix strip of all neighbourhoods
- Spearman rank correlations with bootstrap 95% confidence intervals, and Mann-Whitney tests (high income vs the rest)
- Building-age check: old city vs the new-build district of Leidschenveen-Ypenburg
- Global Moran's I with queen contiguity and 999 permutations

**Part II · Neighbourhood types (K-means)**
- Features: share of homes in each of ≥A, B, C, D, E, F and G
- k chosen with three checks: elbow, silhouette score, and stability across 10 random seeds (adjusted Rand index)
- k = 5, giving the types Mostly A, Mostly A and B, Mixed (centred on C), E-dominated and G-dominated
- Evaluation: silhouette per neighbourhood, comparison with each neighbourhood's most common label, a spatial-coherence permutation test, and a Kruskal-Wallis test of income by type

## Repository contents

```
├── the_hague_income_energy_labels.ipynb                  # the analysis notebook (outputs included)
├── utils.py                                              # chart style, map helpers, statistics helpers
├── mihail_deligrozev_the_hague_energy_labels_report.html # report version, no code
├── figures/                                              # 14 numbered PNG figures (also in figures.zip)
└── data/
    ├── neighborhoods.csv
    └── neighborhoods.json                                # or the shapefile set
```

The notebook writes these outputs:
- `the_hague_income_energy_labels_clean.csv`: one row per neighbourhood, with the measures and the K-means type
- `the_hague_income_energy_labels.geojson`: the same data with the boundaries
- `figures/` and `figures.zip`: all charts as PNGs

## How to run

**Locally**

```bash
pip install geopandas scikit-learn scipy matplotlib pandas numpy
```

1. Put `utils.py` next to the notebook and the data files in `data/`.
2. Open the notebook in Jupyter and choose *Run all*.
3. Outputs are written to `output/`.

**On Kaggle**
1. Upload the data files as a dataset and `utils.py` as a model or dataset.
2. Attach both with **Add Input**. Geopandas is pre-installed.
3. Choose *Run all*. Outputs are written to `/kaggle/working/`.

The notebook searches `./data`, `.` and `/kaggle/input` for the files. It only loads a `utils.py` that contains this project's helpers, so a `utils.py` from another project is ignored.

**HTML export**

```bash
jupyter nbconvert --to html the_hague_income_energy_labels.ipynb                 # with code
jupyter nbconvert --to html --no-input the_hague_income_energy_labels.ipynb      # report, no code
```

## Figures

| # | Figure |
|---|---|
| 1 | Areas excluded from the analysis |
| 2 | Full label mix of every neighbourhood, with income |
| 3 | Side-by-side maps: income, % A-or-better, % E–G |
| 4 | Bivariate map: income × A-label share |
| 5 | Scatter of income vs label shares, old city vs new-build |
| 6 | Label mix by income quartile |
| 7 | Forest plot of correlations with 95% CIs |
| 8 | Moran's I permutation tests |
| 9 | Five neighbourhoods: best labels and retrofit candidates |
| 10 | Choosing k: elbow, silhouette, stability |
| 11 | Profiles of the five neighbourhood types |
| 12 | Map of neighbourhood types |
| 13 | Cluster evaluation: silhouettes and most-common-label table |
| 14 | Income by neighbourhood type |

## Limitations

- **Unknown reference year.** The export does not say which year it covers; it is probably 2018–2019.
- **Registered labels only.** Shares are of homes *with* a label. Many older homes carry a provisional label based on building type and year.
- **Ecological data.** Neighbourhood averages say nothing about individual households.
- **No building-age variable.** The new-build flag stands in for construction year.
- **Spatial dependence.** Clustered data makes the ordinary p-values somewhat too small.
- **K-means on shares.** Label shares sum to 100%, so the features are not independent. A log-ratio transform or a Gaussian mixture model would be worth comparing.

## Next steps

Add the average construction year and the share of social housing per neighbourhood from Den Haag in Cijfers. Then fit a spatial lag model of label score on income, building age and tenure.

## Tools

Python · pandas · NumPy · geopandas · shapely · matplotlib · SciPy · scikit-learn
