"""Plot current three-trial task consistency from the statistics CSV.

Inputs: <stats-root>/<cohort>/outcomes/success_stability_summary.csv.
Output: <stats-root>/<cohort>/figures/robustness_bar_flat.pdf, or --output.
Only the figure is written; source data are unchanged.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

if __package__:
    from .plot_common import DEFAULT_STATS_ROOT, MODELS, configure_style, output_path, parse_args, read_csv
else:
    from plot_common import DEFAULT_STATS_ROOT, MODELS, configure_style, output_path, parse_args, read_csv


def load_stability_data(stats_root=DEFAULT_STATS_ROOT, cohort="full"):
    rows = read_csv(Path(stats_root) / cohort / "outcomes" / "success_stability_summary.csv")
    by_model = {row["model"]: row for row in rows}
    if len(by_model) != len(rows) or set(by_model) != set(MODELS.values()):
        raise ValueError("Expected one stability-summary row for each model")
    counts = []
    for model in MODELS.values():
        row = by_model[model]
        successes = [int(row[f"tasks_with_{n}_successes"]) for n in range(4)]
        tasks = int(row["n_tasks"])
        if (min(successes) < 0 or sum(successes) != tasks
                or successes[1] + successes[2] != int(row["unstable_tasks"])
                or int(row["attempts"]) != 3 * tasks
                or sum(n * count for n, count in enumerate(successes)) != int(row["resolved_attempts"])):
            raise ValueError(f"Inconsistent three-trial task counts for {model}")
        counts.append((successes[3], successes[1] + successes[2], successes[0]))
    return list(MODELS), np.array(counts).T


def plot_flat_scientific_bar_chart(stats_root=DEFAULT_STATS_ROOT, cohort="full", output=None):
    labels, counts = load_stability_data(stats_root, cohort)
    configure_style()
    x = np.arange(len(labels))
    width = 0.22
    fig, ax = plt.subplots(figsize=(15, 4.5))

    series = [
        ("Consistently Solved (3/3)", "#1D3557"),
        ("Partially Successful (1/3 or 2/3)", "#A8DADC"),
        ("Consistently Failed (0/3)", "#E63946"),
    ]
    for offset, values, (label, color) in zip((-width, 0, width), counts, series):
        rects = ax.bar(x + offset, values, width, label=label, color=color,
                       edgecolor="#333333", linewidth=0.8, alpha=0.85)
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f"{height:.0f}",
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 5), textcoords="offset points",
                        ha="center", va="bottom", fontsize=20, color="black")

    ax.set_ylabel("Number of Tasks", fontsize=22, color="black", labelpad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=24, color="black")
    ax.tick_params(axis="y", labelsize=18)
    ax.set_ylim(0, 85)
    ax.legend(fontsize=20, loc="upper center", bbox_to_anchor=(0.5, 1.25),
              ncol=3, frameon=False, columnspacing=1.5)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#333333")
        ax.spines[side].set_linewidth(1.0)
    ax.yaxis.grid(True, linestyle="--", color="#D3D3D3", alpha=0.7, linewidth=0.8)
    ax.set_axisbelow(True)

    path = output_path(stats_root, cohort, "robustness_bar_flat.pdf", output)
    fig.savefig(path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Robustness chart saved: {path} ({cohort})")
    return path


if __name__ == "__main__":
    args = parse_args(__doc__)
    plot_flat_scientific_bar_chart(args.stats_root, args.cohort, args.output)
