#!/usr/bin/env python3
"""
Generate publication-quality figures for the STS Finance Paper.

Reads cross-model experiment results and produces:
  Fig 1: Conceptual model — credence good to search good (3-panel)
  Fig 2: Grouped bar chart — pass rates by model × condition
  Fig 3: Forest plot — Cohen's h effect sizes with CIs
  Fig 4: Box plots — CC and ADF distributions by condition
  Fig 5: Line chart — convergence trajectory (Experiment 7)

Style: Finance-paper conventions (muted colors, serif fonts, minimal gridlines).

Usage:
    uv run python generate_figures.py                          # all figures
    uv run python generate_figures.py --only 2 5               # specific figures
    uv run python generate_figures.py --input path/to/results  # custom input
"""

import argparse
import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT = Path(__file__).parent
RESULTS_FILE = ROOT / "records" / "cross_model_results.json"
FIGURES_DIR = ROOT / "paper" / "figures"

# ---------------------------------------------------------------------------
# Finance-paper style
# ---------------------------------------------------------------------------

def setup_style():
    """Configure matplotlib/seaborn for finance-paper aesthetics."""
    sns.set_theme(style="whitegrid", font_scale=1.1)
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Palatino", "Georgia", "DejaVu Serif"],
        "axes.edgecolor": "0.3",
        "axes.linewidth": 0.8,
        "grid.alpha": 0.3,
        "grid.linewidth": 0.5,
        "axes.grid.axis": "y",  # horizontal gridlines only
        "figure.dpi": 150,
        "savefig.dpi": 600,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "legend.framealpha": 0.9,
        "legend.edgecolor": "0.8",
    })


# Display names
MODEL_NAMES = {
    "claude": "Claude Sonnet 4",
    "gpt4o": "GPT-4o",
    "gemini": "Gemini 2.5 Flash",
}

MODEL_ORDER = ["claude", "gpt4o", "gemini"]
CONDITION_ORDER = ["U", "D", "S"]

CONDITION_LABELS = {
    "U": "Unconstrained",
    "D": "Disclosure",
    "S": "Specification",
}

# Finance-appropriate muted palette
CONDITION_COLORS = {
    "U": "#b0b0b0",   # Gray
    "D": "#5b8db8",   # Steel blue
    "S": "#2c5f8a",   # Navy
}

MODEL_COLORS = {
    "claude": "#2c5f8a",   # Navy
    "gpt4o": "#8b6914",    # Dark goldenrod
    "gemini": "#4a7c59",   # Forest green
}


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_results(filepath: Path) -> list[dict]:
    """Load experiment results, filter out API errors.

    Entries that completed but lack a verdict (truncated/unauditable code)
    are counted as FAIL — they represent genuine production failures.
    """
    with open(filepath) as f:
        raw = json.load(f)
    valid = []
    n_err = 0
    for r in raw:
        if "error" in r and "verdict" not in r:
            n_err += 1  # API-level error, exclude
        elif r.get("verdict") is None:
            r["verdict"] = "H-TIER (FAILED: unauditable)"
            valid.append(r)
        else:
            valid.append(r)
    if n_err:
        print(f"  Filtered {n_err} API error entries, {len(valid)} valid")
    return valid


def group_by(data: list[dict], *keys) -> dict[tuple, list[dict]]:
    """Group data by one or more keys."""
    groups = {}
    for r in data:
        k = tuple(r[key] for key in keys)
        groups.setdefault(k, []).append(r)
    return groups


def pass_rate(entries: list[dict]) -> float:
    """Compute pass rate from a list of result entries."""
    if not entries:
        return 0.0
    return sum(1 for r in entries if "PASSED" in (r.get("verdict") or "")) / len(entries)


def clopper_pearson(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    """Clopper-Pearson exact confidence interval."""
    from scipy.stats import beta
    if n == 0:
        return (0.0, 1.0)
    lo = 0.0 if k == 0 else beta.ppf(alpha / 2, k, n - k + 1)
    hi = 1.0 if k == n else beta.ppf(1 - alpha / 2, k + 1, n - k)
    return (lo, hi)


def cohens_h(p1: float, p2: float) -> float:
    """Cohen's h effect size for two proportions."""
    p1 = max(0.0, min(1.0, p1))
    p2 = max(0.0, min(1.0, p2))
    return 2.0 * math.asin(math.sqrt(p1)) - 2.0 * math.asin(math.sqrt(p2))


# ---------------------------------------------------------------------------
# Figure 1: Conceptual model — From Credence Good to Search Good
# ---------------------------------------------------------------------------

def _draw_box(ax, x, y, w, h, text, facecolor="#ffffff", edgecolor="0.3",
              fontsize=8, fontweight="normal", text_color="0.15", linewidth=1.0):
    """Draw a rounded rectangle with centered text."""
    box = mpatches.FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.05",
        facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth,
        zorder=2,
    )
    ax.add_patch(box)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize,
            fontweight=fontweight, color=text_color, zorder=3, linespacing=1.3)
    return box


def _draw_diamond(ax, x, y, size, text, facecolor="#fff3cc", edgecolor="#b08600",
                  fontsize=7, linewidth=1.5):
    """Draw a diamond shape with centered text."""
    from matplotlib.patches import Polygon
    s = size / 2
    diamond = Polygon(
        [(x, y + s), (x + s, y), (x, y - s), (x - s, y)],
        closed=True, facecolor=facecolor, edgecolor=edgecolor,
        linewidth=linewidth, zorder=2,
    )
    ax.add_patch(diamond)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize,
            color="0.15", zorder=3, linespacing=1.3)


def _arrow(ax, x1, y1, x2, y2, color="0.4", style="-|>", linewidth=1.0,
           linestyle="-"):
    """Draw an arrow between two points."""
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle=style, color=color, lw=linewidth,
                        linestyle=linestyle),
        zorder=1,
    )


def fig1_conceptual_model(output_dir: Path):
    """Three-panel conceptual model: credence good -> search good -> evidence."""
    fig, axes = plt.subplots(1, 3, figsize=(14, 5.5),
                             gridspec_kw={"width_ratios": [1, 1.2, 0.9]})

    # Colors
    c_problem = "#f9e0e0"
    c_solution = "#e0f0e0"
    c_evidence = "#e0e4f9"
    c_pass = "#d4edda"
    c_fail = "#f8d7da"
    c_audit = "#fff3cc"
    c_buyer = "#f0f0f0"

    # ── Panel A: Status Quo ──────────────────────────────────────────────
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis("off")

    # Panel label and title
    ax.text(5, 11.6, "A. Status Quo: Credence Good", ha="center", va="top",
            fontsize=10, fontweight="bold", color="0.15")

    # AI Generator
    _draw_box(ax, 5, 10, 4.5, 1.0, "AI Code Generator",
              facecolor=c_problem, edgecolor="#c44444", fontsize=9, fontweight="bold")

    # Z-Tier and H-Tier
    _draw_box(ax, 2.8, 7.8, 3.2, 1.0, "High Architecture\n(Z-Tier)",
              facecolor=c_problem, edgecolor="#c44444", fontsize=8)
    _draw_box(ax, 7.2, 7.8, 3.2, 1.0, "Low Architecture\n(H-Tier)",
              facecolor=c_problem, edgecolor="#c44444", fontsize=8)

    # Arrows from generator to tiers
    _arrow(ax, 3.8, 9.5, 2.8, 8.3, color="#c44444")
    _arrow(ax, 6.2, 9.5, 7.2, 8.3, color="#c44444")

    # Identical Functionality
    _draw_box(ax, 5, 5.6, 4.5, 1.0, "Identical Functionality",
              facecolor="#f5f5f5", edgecolor="0.5", fontsize=9)

    # Arrows from tiers to functionality
    _arrow(ax, 2.8, 7.3, 4.0, 6.1, color="0.5")
    ax.text(2.2, 6.6, "same\noutput", fontsize=6, color="0.5", ha="center")
    _arrow(ax, 7.2, 7.3, 6.0, 6.1, color="0.5")
    ax.text(7.8, 6.6, "same\noutput", fontsize=6, color="0.5", ha="center")

    # Buyer
    _draw_box(ax, 5, 3.2, 4.5, 1.2, "Buyer\n(observes function only)",
              facecolor=c_buyer, edgecolor="0.5", fontsize=8, linewidth=1.5)

    # Dashed arrow: functionality -> buyer (cannot distinguish)
    _arrow(ax, 5, 5.1, 5, 3.8, color="0.5", linestyle="--", style="-|>")
    ax.text(6.2, 4.45, "cannot\ndistinguish\nquality", fontsize=6.5, color="#c44444",
            ha="center", style="italic")

    # Adverse selection note
    ax.text(5, 1.5, "Adverse Selection\n(H-Tier dominates)", ha="center", va="center",
            fontsize=8, fontweight="bold", color="#c44444", style="italic")

    # ── Panel B: With Search Good Layer ─────────────────────────────────
    ax = axes[1]
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 12)
    ax.axis("off")

    ax.text(6, 11.6, "B. With Search Good Layer", ha="center", va="top",
            fontsize=10, fontweight="bold", color="0.15")

    # AI Generator
    _draw_box(ax, 6, 10, 4.5, 1.0, "AI Code Generator",
              facecolor=c_solution, edgecolor="#4a7c59", fontsize=9, fontweight="bold")

    # Z-Tier and H-Tier
    _draw_box(ax, 3.5, 8, 3.0, 1.0, "High Architecture\n(Z-Tier)",
              facecolor=c_solution, edgecolor="#4a7c59", fontsize=8)
    _draw_box(ax, 8.5, 8, 3.0, 1.0, "Low Architecture\n(H-Tier)",
              facecolor=c_solution, edgecolor="#4a7c59", fontsize=8)

    # Arrows from generator to tiers
    _arrow(ax, 4.8, 9.5, 3.5, 8.5, color="#4a7c59")
    _arrow(ax, 7.2, 9.5, 8.5, 8.5, color="#4a7c59")

    # Audit diamond
    _draw_diamond(ax, 6, 5.8, 2.0, "Architectural\nQuality\nAudit",
                  facecolor=c_audit, edgecolor="#b08600", fontsize=7, linewidth=1.8)

    # Arrows from tiers to audit
    _arrow(ax, 3.5, 7.5, 5.2, 6.5, color="#4a7c59")
    _arrow(ax, 8.5, 7.5, 6.8, 6.5, color="#4a7c59")

    # PASS and FAIL
    _draw_box(ax, 3.5, 3.8, 2.5, 0.9, "PASS",
              facecolor=c_pass, edgecolor="#28a745", fontsize=9, fontweight="bold",
              text_color="#155724")
    _draw_box(ax, 8.5, 3.8, 2.5, 0.9, "FAIL",
              facecolor=c_fail, edgecolor="#dc3545", fontsize=9, fontweight="bold",
              text_color="#721c24")

    # Arrows from audit to verdicts
    _arrow(ax, 5.2, 5.0, 3.5, 4.25, color="#28a745", linewidth=1.2)
    ax.text(3.6, 5.0, "certified", fontsize=6.5, color="#28a745", ha="center")
    _arrow(ax, 6.8, 5.0, 8.5, 4.25, color="#dc3545", linewidth=1.2)
    ax.text(8.4, 5.0, "rejected", fontsize=6.5, color="#dc3545", ha="center")

    # Buyer
    _draw_box(ax, 6, 2.0, 5.0, 1.2, "Buyer\n(observes verdict + function)",
              facecolor=c_buyer, edgecolor="0.5", fontsize=8, linewidth=1.5)

    # Arrows from verdicts to buyer
    _arrow(ax, 3.5, 3.35, 4.5, 2.6, color="0.5")
    _arrow(ax, 8.5, 3.35, 7.5, 2.6, color="0.5")

    # Audit properties annotation (small text box)
    props_text = "Verifiable\nReproducible\nContractible\nLow cost"
    props_box = mpatches.FancyBboxPatch(
        (9.5, 5.0), 2.3, 1.8,
        boxstyle="round,pad=0.1",
        facecolor="#fffbe6", edgecolor="#b08600", linewidth=0.8,
        linestyle="--", zorder=2, alpha=0.9,
    )
    ax.add_patch(props_box)
    ax.text(10.65, 6.5, "Audit Properties:", ha="center", va="center",
            fontsize=6, fontweight="bold", color="#8a6d00", zorder=3)
    ax.text(10.65, 5.85, props_text, ha="center", va="center",
            fontsize=5.5, color="#5a4800", zorder=3, linespacing=1.4,
            family="serif")

    # Quality becomes observable note
    ax.text(6, 0.6, "Quality becomes observable\nProducers shift to Z-Tier",
            ha="center", va="center", fontsize=8, fontweight="bold",
            color="#4a7c59", style="italic")

    # ── Panel C: Experimental Evidence ──────────────────────────────────
    ax = axes[2]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis("off")

    ax.text(5, 11.6, "C. Experimental Evidence", ha="center", va="top",
            fontsize=10, fontweight="bold", color="0.15")

    # Draw three horizontal bars representing pass rates
    bar_colors = {
        "U": "#b0b0b0",
        "D": "#5b8db8",
        "S": "#2c5f8a",
    }
    # Actual pooled pass rates from experiment
    bar_data = [
        ("U", "Unconstrained", 0.133, 9.5),
        ("D", "Disclosure", 0.267, 7.2),
        ("S", "Specification", 1.00, 4.9),
    ]

    max_bar_w = 6.5
    bar_h = 1.3
    bar_left = 1.5

    for cond, label, rate, y_pos in bar_data:
        w = max_bar_w * rate
        bar_rect = mpatches.FancyBboxPatch(
            (bar_left, y_pos - bar_h / 2), w, bar_h,
            boxstyle="round,pad=0.03",
            facecolor=bar_colors[cond], edgecolor="0.4",
            linewidth=0.8, zorder=2, alpha=0.85,
        )
        ax.add_patch(bar_rect)

        # Condition label (left of bar)
        ax.text(bar_left - 0.15, y_pos, f"{cond}", ha="right", va="center",
                fontsize=11, fontweight="bold", color="0.25")

        # Descriptive label and pass rate
        if rate > 0.4:
            # Label fits inside bar; rate goes to the right
            ax.text(bar_left + w / 2, y_pos, label, ha="center", va="center",
                    fontsize=7.5, color="white", fontweight="bold", zorder=3)
            ax.text(bar_left + w + 0.3, y_pos, f"{rate:.0%}",
                    ha="left", va="center", fontsize=9, fontweight="bold",
                    color="0.3", zorder=3)
        else:
            # Bar too narrow — put label and rate to the right of bar
            ax.text(bar_left + w + 0.3, y_pos, f"{rate:.0%}  {label}",
                    ha="left", va="center", fontsize=8, fontweight="bold",
                    color="0.3", zorder=3)

    # Arrows between conditions showing effects
    _arrow(ax, bar_left + max_bar_w * 0.133 + 0.5, 8.85,
           bar_left + max_bar_w * 0.267 * 0.5, 7.85,
           color="#5b8db8", linewidth=1.0)
    ax.text(0.8, 8.3, "disclosure\neffect", fontsize=6, color="#5b8db8",
            ha="center", style="italic")

    _arrow(ax, bar_left + max_bar_w * 0.267 * 0.7, 6.55,
           bar_left + max_bar_w * 1.00 * 0.5, 5.55,
           color="#2c5f8a", linewidth=1.0)
    ax.text(0.8, 6.0, "specification\neffect", fontsize=6, color="#2c5f8a",
            ha="center", style="italic")

    # Model-general note
    note_box = mpatches.FancyBboxPatch(
        (0.8, 2.2), 8.4, 1.5,
        boxstyle="round,pad=0.15",
        facecolor=c_evidence, edgecolor="#4444cc", linewidth=1.0,
        zorder=2, alpha=0.8,
    )
    ax.add_patch(note_box)
    ax.text(5, 2.95, "Effect is model-general", ha="center", va="center",
            fontsize=8.5, fontweight="bold", color="0.15", zorder=3)
    ax.text(5, 2.45, "Claude Sonnet 4  |  GPT-4o  |  Gemini 2.5 Flash", ha="center",
            va="center", fontsize=7, color="0.35", zorder=3)

    # ── Cross-panel flow arrows ─────────────────────────────────────────
    # These use figure-level coordinates
    # Draw "Problem -> Solution -> Evidence" labels between panels
    fig.text(0.34, 0.02, "Problem  -------->  Solution  -------->  Evidence",
             ha="center", va="bottom", fontsize=9, color="0.4",
             fontweight="bold", family="serif")

    # Finishing touches
    fig.tight_layout(rect=[0, 0.05, 1, 1], w_pad=2.0)
    fig.savefig(output_dir / "fig1_conceptual_model.pdf", bbox_inches="tight")
    fig.savefig(output_dir / "fig1_conceptual_model.png", bbox_inches="tight")
    plt.close(fig)
    print("  Fig 1: conceptual model saved")


# ---------------------------------------------------------------------------
# Figure 2: Grouped bar chart — pass rates by model × condition
# ---------------------------------------------------------------------------

def fig2_pass_rates(data: list[dict], output_dir: Path):
    """Grouped bar chart of Z-Tier pass rates by model and condition."""
    groups = group_by(data, "model_name", "condition")

    fig, ax = plt.subplots(figsize=(8, 5))

    bar_width = 0.22
    model_positions = range(len(MODEL_ORDER))

    for i, cond in enumerate(CONDITION_ORDER):
        rates = []
        ci_lo = []
        ci_hi = []
        for model in MODEL_ORDER:
            entries = groups.get((model, cond), [])
            n = len(entries)
            k = sum(1 for r in entries if "PASSED" in (r.get("verdict") or ""))
            rate = k / n if n > 0 else 0
            lo, hi = clopper_pearson(k, n)
            rates.append(rate * 100)
            ci_lo.append((rate - lo) * 100)
            ci_hi.append((hi - rate) * 100)

        x = [p + i * bar_width for p in model_positions]
        bars = ax.bar(
            x, rates, bar_width,
            label=CONDITION_LABELS[cond],
            color=CONDITION_COLORS[cond],
            edgecolor="white",
            linewidth=0.5,
            yerr=[ci_lo, ci_hi],
            capsize=3,
            error_kw={"linewidth": 0.8, "color": "0.3"},
        )

        # Add rate labels on bars
        for bar, rate in zip(bars, rates):
            if rate > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + max(ci_hi) * 0.1 + 2,
                    f"{rate:.0f}%",
                    ha="center", va="bottom",
                    fontsize=8, color="0.3",
                )

    # X-axis
    ax.set_xticks([p + bar_width for p in model_positions])
    ax.set_xticklabels([MODEL_NAMES[m] for m in MODEL_ORDER])
    ax.set_xlabel("")

    # Y-axis
    ax.set_ylabel("Z-Tier Pass Rate (%)")
    ax.set_ylim(0, 115)

    # Legend — place in center-right area to avoid overlap with bar labels
    ax.legend(loc="center right", frameon=True)

    ax.set_title("")  # caption goes in the paper, not the figure

    fig.tight_layout()
    fig.savefig(output_dir / "fig2_pass_rates.pdf", bbox_inches="tight")
    fig.savefig(output_dir / "fig2_pass_rates.png", bbox_inches="tight")
    plt.close(fig)
    print("  Fig 2: pass rates bar chart saved")


# ---------------------------------------------------------------------------
# Figure 3: Forest plot — Cohen's h effect sizes with CIs
# ---------------------------------------------------------------------------

def fig3_effect_sizes(data: list[dict], output_dir: Path):
    """Forest plot of Cohen's h effect sizes for U→S and U→D within each model."""
    groups = group_by(data, "model_name", "condition")

    comparisons = []
    for model in MODEL_ORDER:
        for c1, c2, label in [("U", "S", "U → S"), ("U", "D", "U → D"), ("D", "S", "D → S")]:
            e1 = groups.get((model, c1), [])
            e2 = groups.get((model, c2), [])
            n1, n2 = len(e1), len(e2)
            p1 = pass_rate(e1)
            p2 = pass_rate(e2)
            h = cohens_h(p2, p1)  # positive = improvement

            # Bootstrap-style CI approximation for Cohen's h
            # SE(h) ≈ sqrt(1/n1 + 1/n2) for the arcsine transformation
            se = math.sqrt(1 / max(n1, 1) + 1 / max(n2, 1))
            ci_lo = h - 1.96 * se
            ci_hi = h + 1.96 * se

            comparisons.append({
                "model": MODEL_NAMES[model],
                "comparison": label,
                "h": h,
                "ci_lo": ci_lo,
                "ci_hi": ci_hi,
                "label": f"{MODEL_NAMES[model]}\n{label}",
            })

    fig, ax = plt.subplots(figsize=(7, 6))

    y_positions = list(range(len(comparisons) - 1, -1, -1))

    for i, (comp, y) in enumerate(zip(comparisons, y_positions)):
        model_key = [k for k, v in MODEL_NAMES.items() if v == comp["model"]][0]
        color = MODEL_COLORS[model_key]

        ax.plot(comp["h"], y, "o", color=color, markersize=8, zorder=3)
        ax.plot([comp["ci_lo"], comp["ci_hi"]], [y, y], "-", color=color, linewidth=1.5, zorder=2)

    # Reference lines for effect size interpretation
    ax.axvline(0, color="0.5", linewidth=0.8, linestyle="-", zorder=1)
    ax.axvline(0.2, color="0.7", linewidth=0.5, linestyle="--", zorder=1)
    ax.axvline(0.5, color="0.7", linewidth=0.5, linestyle="--", zorder=1)
    ax.axvline(0.8, color="0.7", linewidth=0.5, linestyle="--", zorder=1)

    # Effect size labels — placed directly above the dashed reference lines
    label_y = len(comparisons) + 0.3
    ax.text(0.2, label_y, "Small", ha="center", fontsize=6, color="0.5", rotation=0)
    ax.text(0.5, label_y, "Med.", ha="center", fontsize=6, color="0.5", rotation=0)
    ax.text(0.8, label_y, "Large", ha="center", fontsize=6, color="0.5", rotation=0)

    # Y-axis labels
    ax.set_yticks(y_positions)
    ax.set_yticklabels([c["label"] for c in comparisons], fontsize=9)

    ax.set_xlabel("Cohen's h (effect size)")
    ax.set_xlim(-0.5, max(c["ci_hi"] for c in comparisons) + 0.3)

    # Model legend
    handles = [
        mpatches.Patch(color=MODEL_COLORS[m], label=MODEL_NAMES[m])
        for m in MODEL_ORDER
    ]
    ax.legend(handles=handles, loc="lower right", frameon=True, fontsize=9)

    fig.tight_layout()
    fig.savefig(output_dir / "fig3_effect_sizes.pdf", bbox_inches="tight")
    fig.savefig(output_dir / "fig3_effect_sizes.png", bbox_inches="tight")
    plt.close(fig)
    print("  Fig 3: effect size forest plot saved")


# ---------------------------------------------------------------------------
# Figure 4: Box plots — CC and ADF distributions by condition
# ---------------------------------------------------------------------------

def fig4_distributions(data: list[dict], output_dir: Path):
    """Side-by-side box plots of CC and ADF by condition, faceted by model."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    for ax, metric, ylabel in [
        (axes[0], "max_cc", "Cyclomatic Complexity (CC)"),
        (axes[1], "adf", "Architectural Drift Fraction (ADF)"),
    ]:
        plot_data = []
        for r in data:
            val = r.get(metric)
            if val is not None:
                plot_data.append({
                    "Model": MODEL_NAMES.get(r["model_name"], r["model_name"]),
                    "Condition": CONDITION_LABELS.get(r["condition"], r["condition"]),
                    "value": val,
                    "cond_order": CONDITION_ORDER.index(r["condition"]),
                })

        if not plot_data:
            ax.text(0.5, 0.5, "No data", ha="center", va="center", transform=ax.transAxes)
            continue

        # Sort for consistent ordering
        plot_data.sort(key=lambda x: x["cond_order"])

        positions = []
        tick_positions = []
        tick_labels = []
        colors = []
        box_data = []

        model_list = [MODEL_NAMES[m] for m in MODEL_ORDER]
        cond_list = [CONDITION_LABELS[c] for c in CONDITION_ORDER]

        pos = 0
        for mi, model in enumerate(model_list):
            for ci, cond in enumerate(cond_list):
                vals = [d["value"] for d in plot_data if d["Model"] == model and d["Condition"] == cond]
                if vals:
                    box_data.append(vals)
                    positions.append(pos)
                    colors.append(CONDITION_COLORS[CONDITION_ORDER[ci]])
                else:
                    box_data.append([0])
                    positions.append(pos)
                    colors.append("#cccccc")
                pos += 1
            # Gap between models
            tick_positions.append(pos - 2)
            tick_labels.append(model)
            pos += 0.5

        bp = ax.boxplot(
            box_data, positions=positions, widths=0.6,
            patch_artist=True, showfliers=True,
            flierprops={"marker": "o", "markersize": 4, "markerfacecolor": "0.6", "markeredgecolor": "0.6"},
            medianprops={"color": "0.2", "linewidth": 1.5},
            whiskerprops={"color": "0.4"},
            capprops={"color": "0.4"},
        )

        for patch, color in zip(bp["boxes"], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
            patch.set_edgecolor("0.4")

        ax.set_xticks(tick_positions)
        ax.set_xticklabels(tick_labels, fontsize=9)
        ax.set_ylabel(ylabel)

        # Add threshold line for ADF
        if metric == "adf":
            ax.axhline(0.05, color="#c44", linewidth=0.8, linestyle="--", alpha=0.7)
            ax.text(positions[-1] + 0.5, 0.052, "Threshold", fontsize=7, color="#c44", va="bottom")

    # Shared condition legend
    handles = [
        mpatches.Patch(color=CONDITION_COLORS[c], label=CONDITION_LABELS[c], alpha=0.7)
        for c in CONDITION_ORDER
    ]
    fig.legend(handles=handles, loc="upper center", ncol=3, frameon=True, fontsize=9,
               bbox_to_anchor=(0.5, 1.02))

    # Panel labels
    axes[0].text(-0.05, 1.05, "(a)", transform=axes[0].transAxes, fontsize=12, fontweight="bold")
    axes[1].text(-0.05, 1.05, "(b)", transform=axes[1].transAxes, fontsize=12, fontweight="bold")

    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(output_dir / "fig4_distributions.pdf", bbox_inches="tight")
    fig.savefig(output_dir / "fig4_distributions.png", bbox_inches="tight")
    plt.close(fig)
    print("  Fig 4: CC and ADF distributions saved")


# ---------------------------------------------------------------------------
# Figure 5: Convergence trajectory (Experiment 7)
# ---------------------------------------------------------------------------

def fig5_trajectory(output_dir: Path):
    """Line chart of paper quality trajectory from Experiment 7."""
    # Hardcoded from version_registry.md — this data is complete
    linear = [
        ("v1", 3.0), ("v2", 3.3), ("v3", 3.5), ("v4", 3.5),
        ("v5", 3.8), ("v6", 3.8), ("v7", 3.75), ("v8", 3.6), ("v9", 3.5),
    ]
    parallel = [
        ("v10a", 3.95, "v9"),   # from v9
        ("v10b", 4.04, "v5"),   # from v5 — BEST
        ("v10c", 3.75, "v5"),   # from v5
        ("v10d", 3.67, "v5"),   # from v5
    ]

    fig, ax = plt.subplots(figsize=(8, 4.5))

    # Linear path
    x_lin = list(range(len(linear)))
    y_lin = [s for _, s in linear]
    labels_lin = [v for v, _ in linear]

    ax.plot(x_lin, y_lin, "o-", color="#2c5f8a", linewidth=1.5, markersize=6, zorder=3, label="Linear path")

    # Annotate phases
    ax.annotate(
        "Optimization\nphase", xy=(2, 3.5), xytext=(1, 3.2),
        fontsize=8, color="0.4", ha="center",
        arrowprops=dict(arrowstyle="->", color="0.5", lw=0.8),
    )
    ax.annotate(
        "Escape phase\n(Goodhart's Law)", xy=(7, 3.6), xytext=(7.5, 3.25),
        fontsize=8, color="#c44", ha="center",
        arrowprops=dict(arrowstyle="->", color="#c44", lw=0.8),
    )

    # Parallel branches
    base_x = {"v9": 8, "v5": 4}
    parallel_colors = {
        "v10a": "#5b8db8",
        "v10b": "#2c5f8a",
        "v10c": "#8b8b8b",
        "v10d": "#c44",
    }

    for i, (name, score, base) in enumerate(parallel):
        bx = base_x[base]
        px = len(linear) + i * 0.3  # spread them out slightly
        color = parallel_colors[name]

        # Dashed line from base to parallel version
        ax.plot([bx, px], [dict(linear)[base], score], "--", color=color, linewidth=0.8, alpha=0.6)
        ax.plot(px, score, "D" if name == "v10b" else "s", color=color, markersize=8 if name == "v10b" else 6, zorder=4)
        ax.annotate(
            f"{name}\n({score:.2f})",
            xy=(px, score),
            xytext=(px + 0.3, score + (0.08 if score > 3.8 else -0.08)),
            fontsize=7, color=color, ha="left",
        )

    # Highlight v10b
    ax.annotate(
        "Best: v10b", xy=(len(linear) + 0.3, 4.04), xytext=(len(linear) + 1.5, 4.15),
        fontsize=9, fontweight="bold", color="#2c5f8a",
        arrowprops=dict(arrowstyle="->", color="#2c5f8a", lw=1.2),
    )

    # X-axis
    all_labels = labels_lin + [""] * 4
    ax.set_xticks(list(range(len(linear))))
    ax.set_xticklabels(labels_lin, fontsize=8, rotation=0)
    ax.set_xlabel("Paper Version")

    # Y-axis
    ax.set_ylabel("Blind Review Score (1–5)")
    ax.set_ylim(2.8, 4.3)

    # Acceptance threshold
    ax.axhline(4.0, color="#4a7c59", linewidth=0.8, linestyle=":", alpha=0.7)
    ax.text(0, 4.02, "Accept threshold", fontsize=7, color="#4a7c59", va="bottom")

    fig.tight_layout()
    fig.savefig(output_dir / "fig5_trajectory.pdf", bbox_inches="tight")
    fig.savefig(output_dir / "fig5_trajectory.png", bbox_inches="tight")
    plt.close(fig)
    print("  Fig 5: convergence trajectory saved")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate paper figures")
    parser.add_argument("--input", type=Path, default=RESULTS_FILE,
                        help="Path to cross_model_results.json")
    parser.add_argument("--output", type=Path, default=FIGURES_DIR,
                        help="Output directory for figures")
    parser.add_argument("--only", nargs="+", type=int, choices=[1, 2, 3, 4, 5],
                        help="Generate only specific figures")
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    setup_style()

    figs_to_run = args.only or [1, 2, 3, 4, 5]

    # Fig 1 and Fig 5 don't need experiment data
    if 1 in figs_to_run:
        fig1_conceptual_model(args.output)
    if 5 in figs_to_run:
        fig5_trajectory(args.output)

    # Fig 2-4 need experiment results
    if any(f in figs_to_run for f in [2, 3, 4]):
        if not args.input.exists():
            print(f"  Results file not found: {args.input}")
            print(f"  Run the experiment first, or use --input to specify a different file.")
            print(f"  (Fig 5 was generated — it doesn't need experiment data)")
            return

        print(f"  Loading results from {args.input}")
        data = load_results(args.input)

        if not data:
            print("  No valid results found. Skipping Fig 2-4.")
            return

        if 2 in figs_to_run:
            fig2_pass_rates(data, args.output)
        if 3 in figs_to_run:
            fig3_effect_sizes(data, args.output)
        if 4 in figs_to_run:
            fig4_distributions(data, args.output)

    print(f"\n  All figures saved to {args.output}/")


if __name__ == "__main__":
    main()
