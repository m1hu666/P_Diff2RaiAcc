# Statistics catalogue

Start with [REPORT.md](REPORT.md) for the full-data versus Django-exclusion comparison.
Detailed definitions and assumptions are in [METHODS.md](../../docs/METHODS.md).
All generated artifacts are grouped by category; the root contains only this index
and the overview. Archived trajectories, patches, labels and human annotations
are unchanged by the analysis.

## Directory map

```text
Statistics results/
  README.md
  REPORT.md
  data/                       Shared attempt/response data and task metadata
  accounting/                 Token definitions, coverage and missingness evidence
  settings/                   Saved parameters, configurations and prompt audit
  full/                       100 tasks, 900 attempts, including Django
    REPORT.md
    analysis_design.json
    resources/                Resource descriptions, paired tests and cost estimates
    outcomes/                 Resolution and three-trial consistency
    failures/                 Catalogue, taxonomy summaries, intervals and tests
    stratified/               Repository and difficulty strata
    repository_sensitivity/   Repository clusters, equal weights, leave-one-out
  without_django/             50 tasks, 450 attempts; same subdirectories as full/
  sensitivity/                Joint Django-exclusion contrasts and multiplicity checks
  audits/                     Extraction, failure provenance and output validation
```

Run the complete offline pipeline from the repository root:

```bash
python3 scripts/run_analysis.py
```

It rebuilds both cohorts, failure summaries, optional-field audits, sensitivity
analyses, Markdown reports, and validation. Defaults are seed 42, 10,000 bootstrap
resamples and 19,999 resource permutations. No model/provider API is called.

## Shared data and evidence

| Directory/file | Meaning |
| --- | --- |
| [data/per_attempt.csv](data/per_attempt.csv) | 900 rows, one model/task/trial each; outcomes, resources, settings and provenance. Repository and archived difficulty are explicit columns. |
| [data/per_response.csv](data/per_response.csv) | 28,479 saved API responses. Optional fields retain numeric/null/missing states. |
| [data/task_metadata.csv](data/task_metadata.csv) | 100 unique tasks with repository and archived human-fix-time difficulty, read from `result/summary.txt` without a network lookup. |
| [accounting/usage_field_coverage.csv](accounting/usage_field_coverage.csv) | Reporting availability for ten token fields by model; numeric zero differs from null/absence. |
| [accounting/MISSINGNESS.md](accounting/MISSINGNESS.md) | Explanation grounded in saved usage objects, with links to source-shape counts and exact examples. |
| [accounting/token_accounting.md](accounting/token_accounting.md) | Fields used by each routed interface. |
| [accounting/output_limit_diagnostics.md](accounting/output_limit_diagnostics.md) | Observed length stops, not reconstructed output-limit settings. |
| [settings/settings.md](settings/settings.md) | Saved client/agent settings, provider reference context and the boundary between requested and effective values. |
| [settings/settings.csv](settings/settings.csv) | Values, serialization status and attempt counts. |
| [settings/configuration_variants.json](settings/configuration_variants.json) | Complete saved configuration variants and their members. |
| [settings/prompt_templates.json](settings/prompt_templates.json) | Exact archived templates. |
| [settings/prompt_consistency.csv](settings/prompt_consistency.csv) | Initial prompt consistency for all nine attempts per task. |

The `accounting/` and `settings/` evidence covers the full archive and is shared by
both cohorts. Availability is not a measure of model quality. The exact historical
native-to-normalized conversion cannot be reconstructed from these saved objects.

## Identical analysis categories in both cohorts

The following relative paths occur under both `full/` and `without_django/`.

| Relative path | Contents and interpretation |
| --- | --- |
| `resources/summary_metrics.csv` | All/success/failure distributions of steps, prompt tokens, completion tokens and estimated USD; means, medians, quartiles and counts. Outcome splits are descriptive. |
| `resources/resource_comparisons.csv` | Nine task-paired model comparisons: steps/input/output, mean differences and ratios, pointwise 95% intervals and adjusted p-values. |
| `resources/estimated_cost_comparisons.csv` | Three exploratory paired cost comparisons, without cost hypothesis tests. |
| `outcomes/success_stability_summary.csv` | Resolution, 0/3 through 3/3 success counts, instability and task-bootstrap intervals. Consistency includes persistent failure. |
| `outcomes/success_comparisons.csv` | Three paired success-fraction comparisons with exact task-block-swap tests. |
| `outcomes/stability_comparisons.csv` | Three exact paired McNemar comparisons of task instability. |
| `failures/failure_trial_catalog.csv` | Every failed attempt in that cohort, with retained human category, diagnosis, evidence locations and hashes. |
| `failures/failure_model_summary.csv` | Failure counts/rates and distinct failed tasks per model. |
| `failures/failure_stage_summary.csv` | Five stage counts, composition percentages, model incidence and task coverage. |
| `failures/failure_taxonomy_summary.csv` | The same measures for eleven subcategories. |
| `failures/failure_task_summary.csv` | Three outcomes and per-trial failure categories for each task with a failure. |
| `failures/category_uncertainty.csv` | Task-bootstrap intervals for category incidence and composition, per model and pooled across models. Ratios are recomputed per draw. |
| `failures/category_inference.csv` | 48 exploratory exact task-paired incidence comparisons: 16 category/stage outcomes times three model pairs. |
| `stratified/stratum_sizes.csv` | Task/attempt denominators by repository and difficulty. |
| `stratified/resource_summary.csv` | Mean resource use and task-cluster intervals by stratum/model. |
| `stratified/outcome_summary.csv` | Resolution and instability estimates/intervals by stratum/model. |
| `stratified/failure_summary.csv` | Category incidence/composition with task-cluster intervals by stratum/model, including pooled `All` rows. |
| `stratified/paired_comparisons.csv` | Paired differences and intervals within strata; no post-hoc stratum significance tests. |
| `repository_sensitivity/cluster_summary.csv` | Whole-repository-bootstrap intervals for resources, outcomes and taxonomy. |
| `repository_sensitivity/paired_comparisons.csv` | Paired model differences from the same repository draws, without p-values. |
| `repository_sensitivity/repository_equal_summary.csv` | Means of repository-specific estimates, deliberately changing the weighting. Defined repository counts are reported. |
| `repository_sensitivity/leave_one_repository_out.csv` | Descriptive estimates after excluding each repository in turn. |

Markdown display tables sit beside the CSVs in `resources/` and `outcomes/`.
The full qualitative case report remains [result/analyse.md](../analyse.md).
Annotations awaiting verification retain their categories and evidence limitations;
these statistics do not independently establish their causal attribution.

## Cross-cohort sensitivity

| File | Meaning |
| --- | --- |
| [sensitivity/django_taxonomy_shift.csv](sensitivity/django_taxonomy_shift.csv) | Full, Django-only and non-Django counts; failure composition; category rankings; Django contribution; exclusion-minus-full percentage-point changes and joint intervals. |
| [sensitivity/model_comparisons_both_cohorts.csv](sensitivity/model_comparisons_both_cohorts.csv) | All 30 resource/outcome tests with additional joint Holm correction. |
| [sensitivity/analysis_design.json](sensitivity/analysis_design.json) | Cohort sizes, seed, resampling, estimands, multiplicity scopes and input hashes. |

The full and non-Django estimates overlap. Django composition-change intervals use
a joint bootstrap stratified by Django status, reusing the same non-Django draw in
both estimates. They do not use an independent-groups test.

## Statistical interpretation

- Main resource/outcome inference first averages the three trials within each
  model/task and preserves pairing across models. Task resampling assumes tasks
  are suitable independent clusters conditional on the benchmark mix.
- Whole-repository bootstrap sensitivity retains all tasks/models/trials within a
  selected repository. Only 11 full-data and 10 non-Django repositories are
  available, with unequal sizes. These exploratory intervals do not establish
  precise transfer to a population of new repositories.
- `incidence_percent` is category failures divided by all attempts;
  `composition_percent` is category failures divided by observed failures.
  In pooled `All` rows there are nine attempts per task; per-model rows have three.
- Optional details and zero-denominator compositions stay undefined. Bootstrap
  files report valid draw counts. Singleton strata have blank intervals. A
  zero-observed bootstrap interval cannot bound an unseen event probability.
- All intervals are pointwise 95% percentile estimates, not simultaneous
  intervals. Non-significance does not establish equivalence.
- Resource/outcome `p_value_holm` covers its outcome family (9/3/3 tests);
  `p_value_holm_global` covers 15 tests within a cohort. The cross-cohort table
  adds `p_value_holm_both_cohorts` over 30 tests.
- Taxonomy `p_value_holm` covers 48 tests within a cohort and
  `p_value_holm_both_cohorts` covers all 96 tests. Taxonomy inference is exploratory
  and a separate family from resource/outcome inference.
- Task-weighted and repository-equal summaries target different averages.
  Difficulty strata use the existing human-fix-time labels and are not
  independent sampling clusters merely because their labels differ.
- Steps count saved assistant/API responses including format retries and the
  submission response. Prompt totals repeatedly count history. Completion totals
  are not necessarily visible prose. USD values are archived framework estimates,
  not reconstructed invoices.

## Audits and provenance

`audits/extraction/` holds the input manifest, extraction audit and anomalies.
`audits/failures/` holds annotation/evidence hashes and exact failure coverage.
[Output validation](audits/validation.json) checks both cohorts, token arithmetic,
raw usage examples, failure counts, stratum denominators and multiplicity.
Independent checks, when run, write to `audits/trajectory/` and
`audits/submissions/`; these are cross-checks, not additional observations.
