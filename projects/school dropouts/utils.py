"""Helpers for the notebook 'Do Richer Neighbourhoods Live in Greener Homes?'
(The Hague · income, energy labels and K-means neighbourhood types).

Contents
--------
style      chart palette, energy-label colours, matplotlib defaults
paths      find_file, OUT_DIR, FIG_DIR
figures    figure_title, save, eur / pct axis formatters
maps       map_axis, classed_colors, choropleth
stats      fmt_p, spearman_ci, queen_weights, morans_i

Author: Mihail Deligrozev
"""
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, to_hex
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter, PercentFormatter
from scipy.stats import spearmanr

try:
    import shapely
except ImportError:  # pragma: no cover
    raise ImportError("Install geopandas first:  pip install geopandas  (it is pre-installed on Kaggle)")

__all__ = [
    # style
    "BLUE", "ORANGE", "AQUA", "VIOLET", "INK", "MUTED", "GRID", "SURFACE", "NODATA",
    "LABELS", "LABEL_COLORS", "LABEL_SCORE",
    # paths and figures
    "find_file", "OUT_DIR", "FIG_DIR", "figure_title", "save", "eur", "pct",
    # maps
    "map_axis", "classed_colors", "choropleth",
    # stats
    "fmt_p", "spearman_ci", "queen_weights", "morans_i",
]

warnings.filterwarnings("ignore")
pd.set_option("display.width", 160)
pd.set_option("display.max_columns", 12)
pd.set_option("display.float_format", "{:,.2f}".format)

# 🎨 palette and chart style --------------------------------------------------
BLUE, ORANGE, AQUA, VIOLET = "#2a78d6", "#eb6834", "#1baf7a", "#6250d6"
INK, MUTED, GRID, SURFACE, NODATA = "#0b0b0b", "#52514e", "#e5e4df", "#fcfcfb", "#d9d8d3"
plt.rcParams.update({
    "figure.dpi": 110, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "axes.titlecolor": INK,
    "axes.titlesize": 11, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": .8,
    "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 10,
    "legend.frameon": False, "lines.linewidth": 2, "hatch.color": "#9a9993",
})

# 🏷️ energy labels, best to worst, in the colours used on Dutch label certificates
LABELS = ["A++", "A+", "A", "B", "C", "D", "E", "F", "G"]
LABEL_COLORS = ["#00843d", "#2aa13c", "#55b947", "#bed630", "#ffdd00", "#fdb913", "#f37021", "#ed1c24", "#b5121b"]
LABEL_SCORE = dict(zip(LABELS, range(9, 0, -1)))          # A++ = 9 ... G = 1


# 📁 paths --------------------------------------------------------------------
def find_file(*patterns):
    """First file matching any pattern, searched in ./data, . and /kaggle/input (recursively)."""
    for pattern in patterns:
        for base in [Path("data"), Path("."), Path("/kaggle/input")]:
            hits = sorted(base.rglob(pattern)) if base.exists() else []
            if hits:
                return hits[0]
    raise FileNotFoundError(patterns)


OUT_DIR = Path("/kaggle/working") if Path("/kaggle/working").exists() else Path("output")
FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


# 🖼️ numbered figures, saved as PNG ----------------------------------------------
_FIG = {"n": 0}


def figure_title(fig, text, y=1.0):
    """Add 'Figure N · text' as a left-aligned title and advance the figure counter."""
    _FIG["n"] += 1
    fig.suptitle(f"Figure {_FIG['n']} · {text}", x=0.01, y=y, ha="left", fontsize=13, fontweight="bold", color=INK)
    return _FIG["n"]


def save(fig, name):
    """Save the current figure as figNN_name.png in FIG_DIR, then show it."""
    fig.savefig(FIG_DIR / f"fig{_FIG['n']:02d}_{name}.png", dpi=150, bbox_inches="tight", facecolor=SURFACE)
    plt.show()


eur = FuncFormatter(lambda v, _: f"€{v/1000:,.0f}k")
pct = PercentFormatter(100, decimals=0)


# 🗺️ maps ----------------------------------------------------------------------
def map_axis(ax):
    ax.set_axis_off()
    ax.set_aspect("equal")


def classed_colors(values, bins, cmap):
    """Hex colour per value by the class it falls in (bins = class edges); NaN -> no-data grey.

    Every entry is a hex string: geopandas converts the list to a NumPy array,
    which fails if strings and RGBA tuples are mixed.
    """
    k = len(bins) - 1
    cm = ListedColormap(plt.get_cmap(cmap)(np.linspace(0.2, 0.95, k)))   # skip the near-white end
    cls = np.clip(np.digitize(values, bins[1:-1]), 0, k - 1)
    return [NODATA if pd.isna(v) else to_hex(cm(c)) for v, c in zip(values, cls)], cm


def choropleth(gdf, col, ax, cmap, k=5, fmt="{:.0f}", title=None, bins=None):
    """Quantile choropleth with a compact class legend; missing values hatched."""
    vals = gdf[col]
    bins = np.nanquantile(vals, np.linspace(0, 1, k + 1)) if bins is None else np.asarray(bins)
    colors, cm = classed_colors(vals, bins, cmap)
    gdf.plot(ax=ax, color=colors, edgecolor="white", linewidth=0.4)
    miss = gdf[vals.isna()]
    if len(miss):
        miss.plot(ax=ax, color=NODATA, edgecolor="white", linewidth=0.4, hatch="////")
    handles = [Patch(color=cm(i), label=f"{fmt.format(bins[i])} – {fmt.format(bins[i+1])}") for i in range(len(bins) - 1)]
    if len(miss):
        handles.append(Patch(facecolor=NODATA, hatch="////", edgecolor="#9a9993", label="no data"))
    ax.legend(handles=handles, loc="upper left", fontsize=8, title=title, title_fontsize=8, handlelength=1.2)
    map_axis(ax)


# 📐 statistics ----------------------------------------------------------------
def fmt_p(p):
    return "< 0.001" if p < 0.001 else f"{p:.3f}"


def spearman_ci(x, y, n_boot=2000, seed=42):
    """Spearman rho, p-value and a percentile bootstrap 95% CI."""
    x, y = np.asarray(x), np.asarray(y)
    rho, p = spearmanr(x, y)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(x), (n_boot, len(x)))
    boots = [spearmanr(x[i], y[i])[0] for i in idx]
    lo, hi = np.nanpercentile(boots, [2.5, 97.5])
    return rho, p, lo, hi


def queen_weights(gdf, decimals=7):
    """Row-standardised contiguity matrix: two areas are neighbours if they share a boundary point.

    Built from shared polygon vertices with NumPy, so PySAL is not needed.
    Use on the unprojected (lon/lat) GeoDataFrame; row order follows gdf.
    """
    xy, idx = shapely.get_coordinates(gdf.geometry.to_numpy(), return_index=True)
    key = pd.Series(idx).groupby([np.round(xy[:, 0], decimals), np.round(xy[:, 1], decimals)]).unique()
    n = len(gdf)
    W = np.zeros((n, n))
    for ids in key:
        if len(ids) > 1:
            for i in ids:
                W[i, ids] = 1
    np.fill_diagonal(W, 0)
    return W / W.sum(1, keepdims=True).clip(min=1)


def morans_i(y, W, n_perm=999, seed=42):
    """Global Moran's I with a one-sided permutation p-value (test for clustering).

    Returns (I, p, simulated I values under random shuffling).
    """
    z = np.asarray(y, float) - np.mean(y)
    S0 = W.sum()
    stat = lambda v: len(v) / S0 * (v @ W @ v) / (v @ v)
    I = stat(z)
    rng = np.random.default_rng(seed)
    sims = np.array([stat(rng.permutation(z)) for _ in range(n_perm)])
    p = (1 + (sims >= I).sum()) / (n_perm + 1)
    return I, p, sims
