# Plot the current statistics

Run from the repository root after installing `requirements.txt`:

```bash
python scripts/draw/heatmap.py
python scripts/draw/robustness_bar_flat.py
python scripts/draw/plot_rq2_outcome_consistent.py
```

The heatmap and robustness scripts read CSVs under
`result/Statistics results/full/` and write PDFs under that cohort's `figures/`
directory, independently of the working directory. Both retain their original
PDF filenames. The outcome resource plots use the shared attempt data described
below.

To plot the 50-task cohort excluding Django:

```bash
python scripts/draw/heatmap.py --cohort without_django
python scripts/draw/robustness_bar_flat.py --cohort without_django
```

Those PDFs go to `result/Statistics results/without_django/figures/`.
Use `--stats-root PATH` for an alternative statistics directory and
`--output PATH` to select an output filename/format, such as `--output heatmap.png`.
For headless environments, set `MPLBACKEND=Agg`.

| Figure | Source CSV within the selected cohort | Values |
| --- | --- | --- |
| Heatmap | `failures/failure_taxonomy_summary.csv` | `Claude_count`, `Gemini_count`, `GPT_count`, one column per category observed in the full reconciled corpus, in CSV order |
| Robustness bars | `outcomes/success_stability_summary.csv` | 3/3 successes; 1/3 plus 2/3 successes; 0/3 successes |

`plot_rq2_outcome_consistent.py` reads the shared `data/per_attempt.csv` and
`data/task_metadata.csv`. By default it writes step and estimated-cost figures
to `full/figures/` as two PDFs. Each is 3.4 inches wide and 5.3 inches tall,
with roughly 7-point type at single-column publication width. Each figure includes
its panel caption at the bottom: `(a) Interaction steps` or `(b) Estimated API costs`.
Point-value labels and further explanatory caption text are omitted.
The three models share the exact same
horizontal row position. Step axes have major ticks every 25 and minor ticks every
5; USD axes show one decimal, with major ticks every 0.5 and minor ticks every 0.1.
Use `--data-dir PATH` and `--out-dir PATH` to override its directories.
This script currently requires the complete 100-task cohort.

Each point first averages trials with the same outcome within a task/model,
then gives qualifying tasks equal weight within repository/difficulty.
Success and failure can contain overlapping tasks and different task sets
across models. N in the figure is the stratum's total sampled task count;
the raw attempt data retain each point's task/trial membership. These outcome
splits are descriptive and do not include confidence intervals or significance
tests. Embed with `width=\columnwidth` without further shrinking the figure.

Suggested manuscript text (kept outside the figure):

> Each point shows a task-weighted mean within a repository–difficulty stratum.
> Trials with the same outcome are first averaged within each task and model,
> then qualifying tasks receive equal weight. Tasks with mixed outcomes may
> contribute to both panels, and qualifying task sets can differ across models.
> Difficulty follows the archived human-fix-time bins (m: minutes; h: hours).
> Parenthetical counts denote all sampled tasks in the stratum, rather than each
> point's sample size; blank cells indicate no qualifying trials.
> Interaction steps count saved assistant/API responses,
> including format retries and final submission; costs are framework-estimated
> API charges per attempt. The outcome-conditioned comparisons are descriptive.

The heatmap uses the eleven categories in the final reconciled codebook. S3 is
absent because it was retired after all nine of its pre-reconciliation
assignments moved to V5. Categories such as V1 and V4 remain visible as
zeroes in the without-Django figure because they occur in the full corpus. The
colorbar counts failed trials, whereas the bars count tasks.
The heatmap is exported at 3.4 by 1.1 inches for a single publication column,
with model rows, category columns, and annotated failed-trial counts.
The original color scale (0–25) and
bar-chart axis limits (0–85) are retained. Times New Roman is preferred; the
heatmap uses the bundled STIX serif fallback when it is unavailable.

The full-cohort bars currently read **69/15/16** for Claude, **69/7/24** for
Gemini, and **62/14/24** for GPT (solved/partial/failed). Failure totals are
**70/82/90**, respectively. These numbers come from the CSVs, not script constants.
After changing outcomes or annotations, rebuild the statistics with
`python scripts/run_analysis.py` before drawing again.
