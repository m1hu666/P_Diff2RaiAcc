"""Plot observed failure-category counts from the statistics CSV.

Inputs: <stats-root>/<cohort>/failures/failure_taxonomy_summary.csv.
Output: <stats-root>/<cohort>/figures/workflow_taxonomy_compact.pdf,
or --output, sized at 3.4 inches wide for a single publication column.
Categories with zero assigned trials in the full reconciled corpus
are omitted from every cohort figure; the source tables and codebook remain
unchanged. Only the figure is written.
"""

from itertools import groupby
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

if __package__:
    from .plot_common import DEFAULT_STATS_ROOT, MODELS, configure_style, output_path, parse_args, read_csv
else:
    from plot_common import DEFAULT_STATS_ROOT, MODELS, configure_style, output_path, parse_args, read_csv


def load_heatmap_data(stats_root=DEFAULT_STATS_ROOT, cohort="full"):
    stats_root = Path(stats_root)

    def validated_rows(cohort_name):
        cohort_rows = read_csv(
            stats_root / cohort_name / "failures" / "failure_taxonomy_summary.csv"
        )
        codes = [row["primary_category"] for row in cohort_rows]
        if len(set(codes)) != len(codes):
            raise ValueError("Duplicate failure categories")
        cohort_data = np.array(
            [[int(row[f"{model}_count"]) for row in cohort_rows] for model in MODELS]
        )
        totals = np.array([int(row["assigned_trials"]) for row in cohort_rows])
        if np.any(cohort_data < 0) or not np.array_equal(cohort_data.sum(axis=0), totals):
            raise ValueError("Failure-category counts disagree with assigned trial totals")
        return cohort_rows, cohort_data, totals

    rows, data, totals = validated_rows(cohort)
    full_rows, full_totals = rows, totals
    if cohort != "full":
        full_rows, _, full_totals = validated_rows("full")
    observed_codes = {
        row["primary_category"]
        for row, total in zip(full_rows, full_totals)
        if total > 0
    }
    observed = np.array([row["primary_category"] in observed_codes for row in rows])
    if not np.any(observed):
        raise ValueError("No observed failure categories")
    rows = [row for row, keep in zip(rows, observed) if keep]
    data = data[:, observed]
    codes = [row["primary_category"] for row in rows]
    stages = []
    start = 0
    for name, entries in groupby(rows, key=lambda row: row["stage"]):
        end = start + len(list(entries))
        stages.append((name, start, end))
        start = end
    return codes, list(MODELS), data, stages


def plot_heatmap_like_image(stats_root=DEFAULT_STATS_ROOT, cohort="full", output=None):
    x_labels, y_labels, data, _ = load_heatmap_data(stats_root, cohort)
    configure_style()
    if plt.rcParams["font.serif"][0] == "DejaVu Serif":
        plt.rcParams["font.serif"] = ["STIXGeneral", "DejaVu Serif"]

    # Set typography at the final print size instead of shrinking a wide figure.
    fig = plt.figure(figsize=(3.4, 1.1), dpi=300)
    ax_hm = fig.add_axes([0.14, 0.23, 0.79, 0.70])
    cbar_ax = fig.add_axes([0.941, 0.23, 0.016, 0.70])

    sns.heatmap(data, cmap="Reds", annot=True, fmt="d", linewidths=0,
                cbar=True, cbar_ax=cbar_ax, ax=ax_hm, vmin=0, vmax=25,
                cbar_kws={"ticks": [0, 5, 10, 15, 20, 25]},
                annot_kws={"size": 8})
    for text in ax_hm.texts:
        text.set_color("white" if int(text.get_text()) > 20 else "#222222")

    ax_hm.set_xticks(np.arange(len(x_labels)) + 0.5)
    ax_hm.set_xticklabels(x_labels, rotation=0, fontsize=7.5)
    ax_hm.set_yticks(np.arange(len(y_labels)) + 0.5)
    ax_hm.set_yticklabels(y_labels, rotation=0, fontsize=8, fontweight="bold")
    ax_hm.tick_params(axis="both", which="both", length=0, pad=3)
    for spine in ax_hm.spines.values():
        spine.set_visible(False)
    cbar_ax.tick_params(labelsize=6, length=1.5, width=0.4, pad=2)
    cbar_ax.set_yticks([0, 5, 10, 15, 20, 25], labels=["0", "5", "10", "15", "20", "25"])

    path = output_path(stats_root, cohort, "workflow_taxonomy_compact.pdf", output)
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print(f"Heatmap saved: {path} ({cohort}; {data.sum()} failed trials)")
    return path


if __name__ == "__main__":
    args = parse_args(__doc__)
    plot_heatmap_like_image(args.stats_root, args.cohort, args.output)
