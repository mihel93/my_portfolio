"""Helpers for the IBM HR attrition notebook: chart style, figure saving, coloured note boxes,
small statistics and reusable charts. Kept out of the notebook so it shows analysis, not plumbing."""
import os
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import HTML, display
from scipy.stats import chi2_contingency

# Palette: orange = left (attrition), teal = stayed, blue = neutral series
LEFT, STAYED, BLUE, PURPLE = '#e8833a', '#2a9d8f', '#2a6fdb', '#7b5ea7'
INK, MUTED, GRID, PALE = '#1f2933', '#8a94a3', '#e6e8eb', '#eef1f5'
STATUS_ORDER = ['Stayed', 'Left']
STATUS_COLORS = {'Stayed': STAYED, 'Left': LEFT}

FIG_DIR = '/kaggle/working/figures' if os.path.isdir('/kaggle/working') else 'figures'


def set_style():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', 120)
    pd.set_option('display.float_format', lambda v: f'{v:,.3f}')
    plt.rcParams.update({
        'figure.figsize': (11, 5), 'figure.dpi': 100, 'figure.facecolor': 'white', 'font.size': 10,
        'axes.spines.top': False, 'axes.spines.right': False, 'axes.spines.left': False,
        'axes.edgecolor': MUTED, 'axes.grid': True, 'grid.color': GRID, 'axes.axisbelow': True,
        'axes.titlesize': 12, 'axes.titleweight': 'bold', 'axes.titlelocation': 'left',
        'axes.labelcolor': INK, 'text.color': INK, 'xtick.color': INK, 'ytick.color': INK,
        'xtick.major.size': 0, 'ytick.major.size': 0, 'legend.frameon': False,
    })


def titles(ax, title, sub=None):
    """Bold title stating the conclusion, grey subtitle stating what is plotted."""
    ax.set_title(title, loc='left', fontsize=12.5, fontweight='bold', pad=24 if sub else 8)
    if sub:
        ax.text(0, 1.02, sub, transform=ax.transAxes, fontsize=9.5, color=MUTED, va='bottom')


def show(fig, name):
    """Save the figure as PNG in FIG_DIR, then display it (returns nothing, so no path is printed)."""
    os.makedirs(FIG_DIR, exist_ok=True)
    fig.savefig(os.path.join(FIG_DIR, name + '.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.show()


# Text boxes

_BOXES = {'insight': ('💡 Insight', '#eef4ff', BLUE), 'why': ('🧠 Why this step', '#f4f0fa', PURPLE),
          'caution': ('⚠️ Read with care', '#fff4ea', LEFT), 'result': ('✅ Result', '#eaf6f4', STAYED)}


def callout(text, kind='insight'):
    label, bg, edge = _BOXES[kind]
    body = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text.strip())
    body = re.sub(r'`(.+?)`', r'<code>\1</code>', body).replace('\n\n', '<br><br>').replace('\n', ' ')
    display(HTML(f'<div style="background:{bg};border-left:5px solid {edge};padding:10px 16px;margin:8px 0;'
                 f'border-radius:6px;color:{INK};line-height:1.55"><b style="color:{edge}">{label}</b><br>{body}</div>'))


def pct(x, d=1):
    return f'{x * 100:.{d}f}%'


# Statistics

def wilson(k, n, z=1.96):
    """95% Wilson confidence interval for a rate k/n (works on arrays)."""
    k, n = np.asarray(k, float), np.asarray(n, float)
    p = k / n
    denom = 1 + z**2 / n
    centre = p + z**2 / (2 * n)
    half = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    return (centre - half) / denom, (centre + half) / denom


def rate_table(df, col, target='left'):
    """Attrition rate per level of `col`, with count, leavers and 95% interval."""
    g = df.groupby(col, observed=True)[target].agg(employees='size', left='sum')
    g['rate'] = g['left'] / g['employees']
    g['lo'], g['hi'] = wilson(g['left'], g['employees'])
    return g


def chi2_test(df, col, target='left'):
    """Chi-square test of independence plus Cramér's V (effect size: 0.1 small, 0.3 medium, 0.5 large)."""
    table = pd.crosstab(df[col], df[target])
    chi2, p, dof, _ = chi2_contingency(table)
    v = np.sqrt(chi2 / (table.values.sum() * (min(table.shape) - 1)))
    return {'chi2': chi2, 'p': p, 'dof': dof, 'cramers_v': v}


def fmt_p(p):
    return '< 0.001' if p < 0.001 else f'{p:.3f}'


# Charts

def rate_bars(ax, g, overall, title, sub=None, horizontal=False, label_n=True):
    """Bars = attrition rate per group, whiskers = 95% interval, dashed line = overall rate."""
    vals, lo, hi = g['rate'] * 100, g['lo'] * 100, g['hi'] * 100
    colors = [LEFT if v > overall * 100 else BLUE for v in vals]
    pos = np.arange(len(g))
    labels = [f'{i}\n(n={n:,})' if label_n else str(i) for i, n in zip(g.index, g['employees'])]
    if horizontal:
        ax.barh(pos, vals, color=colors, height=0.65)
        ax.errorbar(vals, pos, xerr=[vals - lo, hi - vals], fmt='none', ecolor=INK, elinewidth=1, capsize=3)
        ax.axvline(overall * 100, color=INK, ls='--', lw=1)
        ax.set_yticks(pos)
        ax.set_yticklabels([l.replace('\n', ' ') for l in labels], fontsize=9)
        ax.invert_yaxis()
        ax.set_xlabel('Attrition rate (%)')
        ax.grid(axis='y', visible=False)
        for p_, v, h in zip(pos, vals, hi):
            ax.text(h + 0.8, p_, f'{v:.1f}%', va='center', fontsize=8.5)
    else:
        ax.bar(pos, vals, color=colors, width=0.65)
        ax.errorbar(pos, vals, yerr=[vals - lo, hi - vals], fmt='none', ecolor=INK, elinewidth=1, capsize=3)
        ax.axhline(overall * 100, color=INK, ls='--', lw=1)
        ax.set_xticks(pos)
        ax.set_xticklabels(labels, fontsize=8.5)
        ax.set_ylabel('Attrition rate (%)')
        ax.grid(axis='x', visible=False)
        for p_, v, h in zip(pos, vals, hi):
            ax.text(p_, h + 0.8, f'{v:.1f}%', ha='center', fontsize=8.5)
    titles(ax, title, sub)


def lollipop(ax, values, center=0, fmt='{:.3f}', colors=None):
    """Horizontal lollipop chart of a Series (index = labels, first row at the top)."""
    values = pd.Series(values)[::-1]
    y = np.arange(len(values))
    colors = colors[::-1] if colors is not None else [BLUE if v >= center else LEFT for v in values]
    ax.hlines(y, center, values, color=colors, lw=2.4)
    ax.scatter(values, y, color=colors, s=70, zorder=3, edgecolor='white', linewidth=1.5)
    span = (max(values.max(), center) - min(values.min(), center)) or 1
    for yi, v in zip(y, values):
        ax.text(v + (0.02 if v >= center else -0.02) * span, yi, fmt.format(v), va='center',
                ha='left' if v >= center else 'right', fontsize=8.5)
    ax.axvline(center, color=INK, lw=1)
    ax.set_yticks(y)
    ax.set_yticklabels(values.index, fontsize=9)
    ax.margins(x=0.15)
    ax.grid(axis='y', visible=False)


# Model helpers

def threshold_for_recall(y_true, proba, target):
    """Highest threshold that still catches at least `target` share of leavers."""
    for t in np.sort(np.unique(proba))[::-1]:
        if ((proba >= t) & (y_true == 1)).sum() / max((y_true == 1).sum(), 1) >= target:
            return t
    return float(np.min(proba))


def metrics_at(y_true, proba, threshold):
    pred = proba >= threshold
    tp = int((pred & (y_true == 1)).sum()); fp = int((pred & (y_true == 0)).sum())
    fn = int((~pred & (y_true == 1)).sum()); tn = int((~pred & (y_true == 0)).sum())
    return {'threshold': threshold, 'flagged': tp + fp, 'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn,
            'precision': tp / max(tp + fp, 1), 'recall': tp / max(tp + fn, 1), 'accuracy': (tp + tn) / len(y_true)}


def gains_curve(y_true, proba):
    """Share of all leavers found when checking employees from highest to lowest risk score."""
    order = np.argsort(-proba)
    found = np.cumsum(np.asarray(y_true)[order]) / max(np.sum(y_true), 1)
    looked = np.arange(1, len(order) + 1) / len(order)
    return looked, found
