# Generated statistics and audit artifacts

This directory contains quantitative results derived from the archived
trajectories, verified outcomes, patches, and documented analysis inputs. Run
`python3 scripts/run_analysis.py` from the repository root to rebuild the main
quantitative outputs.

## Main outputs

- `REPORT.md` summarizes resource use, API settings, interaction steps,
  approximate cost, success/stability analyses, and statistical design.
- `per_attempt.csv` and `per_response.csv` provide the normalized analysis data.
- `summary_metrics.csv`, `settings.csv`, `parameter_inventory.csv`, and
  `prompt_consistency.csv` support the methodological descriptions.
- `resource_comparisons.csv`, `success_comparisons.csv`,
  `stability_comparisons.csv`, and `estimated_cost_comparisons.csv` contain the
  task-paired inferential results.
- `tables/` contains Markdown and LaTeX versions of publication-ready tables.
- `input_manifest.json`, `audit.json`, and `validation.json` document provenance
  and automated checks.

## Failure analysis and independent audits

- Files prefixed with `failure_` are generated from the final annotations under
  `docs/failure_analysis/` by `python3 scripts/build_failure_analysis.py`.
- `trajectory_audit/` independently checks trajectory completeness and recorded
  token usage.
- `submission_integrity/` compares submitted patches, verified records, and
  evaluation labels.
- `token_usage_stats.txt` is an independent outcome-conditioned token summary.
