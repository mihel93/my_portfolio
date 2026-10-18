"""
util.py - setup, libraries, chart style and helper functions for
hague-energy-labels.ipynb.

The notebook only needs one line:

    from util import *

Everything the analysis uses (libraries, colours, paths, map and
statistics helpers) is defined here, so the notebook cells stay
focused on the analysis itself.

Install once:

    pip install geopandas scikit-learn scipy matplotlib jupyterlab
"""

import warnings
import shutil
from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap
from matplotlib.ticker import FuncFormatter, PercentFormatter

from scipy.stats import spearmanr, mannwhitneyu, kruskal

import sklearn
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples, adjusted_rand_score

from IPython.display import display

try:
    import geopandas as gpd
    import shapely
except ImportError as err:
    raise ImportError(
        "geopandas is missing. Install it in the environment that runs JupyterLab:\n"
        "    pip install geopandas\n"
        "or, with conda:\n"
        "    conda install -c conda-forge geopandas"
    ) from err


# ---------------------------------------------------------------------------
# General settings
# ---------------------------------------------------------------------------

warnings.filterwarnings("ignore")

pd.set_option("display.width", 160)
pd.set_option("display.max_columns", 12)
pd.set_option("display.float_format", "{:,.2f}".format)


# ---------------------------------------------------------------------------
# Palette and chart style
# ---------------------------------------------------------------------------

BLUE = "#2a78d6"
ORANGE = "#eb6834"
AQUA = "#1baf7a"
VIOLET = "#6250d6"

INK = "#0b0b0b"
MUTED = "#52514e"
GRID = "#e5e4df"
SURFACE = "#fcfcfb"
NODATA = "#d9d8d3"
REST_GREY = "#7d7c77"

plt.rcParams.update({
    "figure.dpi": 110,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "axes.edgecolor": GRID,
    "axes.labelcolor": MUTED,
    "axes.titlecolor": INK,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.titlelocation": "left",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": GRID,
    "grid.linewidth": 0.8,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "font.size": 10,
    "legend.frameon": False,
    "lines.linewidth": 2,
    "hatch.color": "#9a9993",
})


# ---------------------------------------------------------------------------
# Energy labels: best to worst, in the colours of Dutch label certificates
# ---------------------------------------------------------------------------

LABELS = ["A++", "A+", "A", "B", "C", "D", "E", "F", "G"]

LABEL_COLORS = ["#00843d", "#2aa13c", "#55b947", "#bed630", "#ffdd00",
                "#fdb913", "#f37021", "#ed1c24", "#b5121b"]

LABEL_SCORE = dict(zip(LABELS, range(9, 0, -1)))        # A++ = 9 ... G = 1

# features used for the K-means clustering (A++, A+ and A merged into one)
FEATURES = ["≥A", "B", "C", "D", "E", "F", "G"]

FEATURE_COLORS = [LABEL_COLORS[2]] + LABEL_COLORS[3:]

NEW_BUILD = "New-build (Leidschenveen-Ypenburg)"
REST = "Rest of the city"

AREA_COLORS = {REST: REST_GREY, NEW_BUILD: AQUA}


# ---------------------------------------------------------------------------
# Paths: data in ./data (or next to the notebook), outputs in ./output
# ---------------------------------------------------------------------------

DATA_DIR = Path("data")

OUT_DIR = Path("output")

FIG_DIR = OUT_DIR / "figures"

FIG_DIR.mkdir(parents=True, exist_ok=True)


def find_file(*patterns):
    """Return the first file that matches one of the patterns, looking in ./data first, then here."""

    for pattern in patterns:

        for base in [DATA_DIR, Path(".")]:

            hits = sorted(base.rglob(pattern)) if base.exists() else []

            if hits:
                return hits[0]

    raise FileNotFoundError(
        f"None of {patterns} found. Put the data files in a folder called 'data' next to the notebook."
    )


# ---------------------------------------------------------------------------
# Numbered figures, saved as PNG
# ---------------------------------------------------------------------------

_FIGURE_NUMBERS = {}


def figure_number(name):
    """Stable figure number per figure name, so re-running a cell keeps its number."""

    if name not in _FIGURE_NUMBERS:
        _FIGURE_NUMBERS[name] = len(_FIGURE_NUMBERS) + 1

    return _FIGURE_NUMBERS[name]


def save_figure(fig, name, title, y=1.0, tight=False):
    """Add the 'Figure N · title' heading, save the figure as PNG and show it."""

    n = figure_number(name)

    if tight:
        fig.tight_layout()

    fig.suptitle(f"Figure {n} · {title}", x=0.01, y=y, ha="left",
                 fontsize=13, fontweight="bold", color=INK)

    fig.savefig(FIG_DIR / f"fig{n:02d}_{name}.png", dpi=150,
                bbox_inches="tight", facecolor=SURFACE)

    plt.show()

    return n


eur = FuncFormatter(lambda v, _: f"€{v / 1000:,.0f}k")

pct = PercentFormatter(100, decimals=0)


# ---------------------------------------------------------------------------
# Map helpers
# ---------------------------------------------------------------------------

def map_axis(ax):
    """Remove the axes around a map and keep the true shape."""

    ax.set_axis_off()

    ax.set_aspect("equal")


def short_name(name):
    """'70 Oostduinen' -> 'Oostduinen'."""

    return name.split(" ", 1)[1]


def classed_colors(values, bins, cmap):
    """Colour each value by the class it falls in (bins = class edges); NaN -> no-data grey."""

    k = len(bins) - 1

    cm = ListedColormap(plt.get_cmap(cmap)(np.linspace(0.2, 0.95, k)))     # skip the near-white end

    classes = np.clip(np.digitize(values, bins[1:-1]), 0, len(bins) - 2)

    colors = [NODATA if pd.isna(v) else cm(c) for v, c in zip(values, classes)]

    return colors, cm


def choropleth(gdf, col, ax, cmap, k=5, fmt="{:.0f}", title=None, bins=None):
    """Quantile choropleth with a compact class legend; missing values hatched."""

    vals = gdf[col]

    if bins is None:
        bins = np.nanquantile(vals, np.linspace(0, 1, k + 1))
    else:
        bins = np.asarray(bins)

    colors, cm = classed_colors(vals, bins, cmap)

    gdf.plot(ax=ax, color=colors, edgecolor="white", linewidth=0.4)

    missing = gdf[vals.isna()]

    if len(missing):
        missing.plot(ax=ax, color=NODATA, edgecolor="white", linewidth=0.4, hatch="////")

    handles = [Patch(color=cm(i), label=f"{fmt.format(bins[i])} – {fmt.format(bins[i + 1])}")
               for i in range(len(bins) - 1)]

    if len(missing):
        handles.append(Patch(facecolor=NODATA, hatch="////", edgecolor="#9a9993", label="no data"))

    ax.legend(handles=handles, loc="upper left", fontsize=8, title=title,
              title_fontsize=8, handlelength=1.2)

    map_axis(ax)


# ---------------------------------------------------------------------------
# Chart helpers
# ---------------------------------------------------------------------------

def stacked_label_bars(ax, shares, labels, colors, height=0.7, min_text=None, text_dark=()):
    """Horizontal 100% bars, one per row of `shares`, one segment per label."""

    left = np.zeros(len(shares))

    for lab, col in zip(labels, colors):

        ax.barh(range(len(shares)), shares[lab], left=left, color=col, height=height, label=lab)

        if min_text is not None:

            for i, (l, v) in enumerate(zip(left, shares[lab])):

                if v >= min_text:
                    ax.text(l + v / 2, i, f"{v:.0f}%", ha="center", va="center", fontsize=8,
                            fontweight="bold", color=INK if lab in text_dark else "white")

        left += shares[lab].to_numpy()

    ax.set_xlim(0, 100)

    ax.xaxis.set_major_formatter(pct)

    ax.grid(False)


def strip_with_box(ax, groups, colors, labels, seed=1, size=34):
    """Jittered dots per group with the median and the interquartile range drawn on top."""

    rng = np.random.default_rng(seed)

    for i, (values, color) in enumerate(zip(groups, colors)):

        values = pd.Series(values).dropna()

        jitter = rng.uniform(-0.18, 0.18, len(values))

        ax.scatter(i + jitter, values, s=size, color=color, alpha=0.8,
                   edgecolor="white", linewidth=0.5, zorder=2)

        q1, med, q3 = values.quantile([0.25, 0.5, 0.75])

        ax.plot([i, i], [q1, q3], color=INK, lw=7, alpha=0.18, solid_capstyle="round", zorder=1)

        ax.scatter(i, med, marker="_", s=900, color=INK, linewidth=2.5, zorder=3)

    ax.set_xticks(range(len(groups)), labels)

    ax.set_xlim(-0.6, len(groups) - 0.4)

    ax.grid(axis="x", visible=False)


# ---------------------------------------------------------------------------
# Statistics helpers
# ---------------------------------------------------------------------------

def fmt_p(p):
    """p-value as text: '< 0.001' or three decimals."""

    return "< 0.001" if p < 0.001 else f"{p:.3f}"


def spearman_ci(x, y, n_boot=2000, seed=42):
    """Spearman rho with a percentile bootstrap 95% CI."""

    x = np.asarray(x)
    y = np.asarray(y)

    rho, p = spearmanr(x, y)

    rng = np.random.default_rng(seed)

    idx = rng.integers(0, len(x), (n_boot, len(x)))

    boots = [spearmanr(x[i], y[i])[0] for i in idx]

    lo, hi = np.nanpercentile(boots, [2.5, 97.5])

    return rho, p, lo, hi


def queen_weights(gdf, decimals=7):
    """Row-standardised contiguity matrix: two areas are neighbours if they share a boundary point."""

    xy, idx = shapely.get_coordinates(gdf.geometry.to_numpy(), return_index=True)

    groups = pd.Series(idx).groupby([np.round(xy[:, 0], decimals), np.round(xy[:, 1], decimals)]).unique()

    n = len(gdf)

    W = np.zeros((n, n))

    for ids in groups:

        if len(ids) > 1:

            for i in ids:
                W[i, ids] = 1

    np.fill_diagonal(W, 0)

    return W / W.sum(1, keepdims=True).clip(min=1)


def _moran_statistic(z, W):

    return len(z) / W.sum() * (z @ W @ z) / (z @ z)


def morans_i(y, W, n_perm=999, seed=42):
    """Global Moran's I with a one-sided permutation p-value (clustering)."""

    z = np.asarray(y, float) - np.mean(y)

    I = _moran_statistic(z, W)

    rng = np.random.default_rng(seed)

    sims = np.array([_moran_statistic(rng.permutation(z), W) for _ in range(n_perm)])

    p = (1 + (sims >= I).sum()) / (n_perm + 1)

    return I, p, sims


# ---------------------------------------------------------------------------
# Setup summary
# ---------------------------------------------------------------------------

def print_setup():
    """Print library versions and where data is read from and outputs are written to."""

    print("Setup done")

    print(f"  pandas {pd.__version__} · geopandas {gpd.__version__} · scikit-learn {sklearn.__version__} "
          f"· matplotlib {matplotlib.__version__}")

    print(f"  data folder   : {DATA_DIR.resolve()}")

    print(f"  figures go to : {FIG_DIR.resolve()}")
