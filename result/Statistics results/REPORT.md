# Full-data and Django-exclusion analysis

Start here for the reviewer-facing sensitivity comparison. See [methods](../../docs/METHODS.md) and the [file catalogue](README.md). All results describe the archived configurations; token counts are normalized reports and costs are framework estimates.

## Cohort sizes

| Cohort | Tasks | Attempts | Failures | Repositories |
| --- | --- | --- | --- | --- |
| full | 100 | 900 | 242 | 11 |
| without_django | 50 | 450 | 136 | 10 |

The exclusion cohort is nested in the full cohort. It is a sensitivity analysis, not an independent replication. The taxonomy and annotations are retained without relabeling.

## Resources and outcomes

| Cohort | Model | Resolution (%) | Mean steps | Input (k) | Output (k) | Estimated USD |
| --- | --- | --- | --- | --- | --- | --- |
| full | Claude | 76.67 | 42.91 | 721.27 | 10.48 | 0.545 |
| full | Gemini | 72.67 | 38.94 | 581.09 | 10.19 | 0.591 |
| full | GPT | 70.00 | 13.08 | 146.98 | 10.47 | 0.238 |
| without_django | Claude | 73.33 | 44.08 | 740.80 | 9.71 | 0.541 |
| without_django | Gemini | 70.67 | 42.06 | 654.77 | 9.89 | 0.628 |
| without_django | GPT | 65.33 | 14.01 | 174.35 | 11.34 | 0.269 |

Per-cohort paired tests and confidence intervals are in [full](full/REPORT.md) and [without Django](without_django/REPORT.md). The [joint comparison table](sensitivity/model_comparisons_both_cohorts.csv) additionally applies Holm to all 18 interaction-step/outcome tests across both cohorts. Within-cohort global adjustment covers nine tests. These scopes must not be interchanged.

## Influence on taxonomy

Django contains half of the tasks and contributes 106/242 failures (43.80%). The table distinguishes its contribution to the failure pool from changes in category composition after exclusion.

### Broader stages

| Category | Full n (%) | Without Django n (%) | Change (pp), 95% CI | Django share of category (%) | Rank full -> excluded |
| --- | --- | --- | --- | --- | --- |
| Problem Understanding | 71 (29.34) | 51 (37.50) | +8.16 [-5.55, +21.48] | 28.17 | 2 -> 1 |
| Localization | 12 (4.96) | 3 (2.21) | -2.75 [-9.01, +1.80] | 75.00 | 4 -> 4 |
| Strategy & Logic | 68 (28.10) | 30 (22.06) | -6.04 [-19.50, +7.15] | 55.88 | 3 -> 3 |
| Implementation & Execution | 8 (3.31) | 3 (2.21) | -1.10 [-4.91, +1.73] | 62.50 | 5 -> 4 |
| Validation & Harness Constraints | 83 (34.30) | 49 (36.03) | +1.73 [-12.01, +15.26] | 40.96 | 1 -> 2 |

### Subcategories

| Category | Full n (%) | Without Django n (%) | Change (pp), 95% CI | Django share of category (%) | Rank full -> excluded |
| --- | --- | --- | --- | --- | --- |
| P1 | 45 (18.60) | 34 (25.00) | +6.40 [-5.26, +18.21] | 24.44 | 2 -> 1 |
| P2 | 26 (10.74) | 17 (12.50) | +1.76 [-8.37, +11.75] | 34.62 | 4 -> 4 |
| L1 | 12 (4.96) | 3 (2.21) | -2.75 [-9.01, +1.80] | 75.00 | 8 -> 7 |
| S1 | 49 (20.25) | 28 (20.59) | +0.34 [-12.22, +12.83] | 42.86 | 1 -> 2 |
| S2 | 19 (7.85) | 2 (1.47) | -6.38 [-14.67, -0.23] | 89.47 | 6 -> 9 |
| I1 | 8 (3.31) | 3 (2.21) | -1.10 [-4.91, +1.73] | 62.50 | 10 -> 7 |
| V1 | 10 (4.13) | 0 (0.00) | -4.13 [-9.58, +0.00] | 100.00 | 9 -> 10 |
| V2 | 30 (12.40) | 15 (11.03) | -1.37 [-10.80, +8.04] | 50.00 | 3 -> 6 |
| V3 | 22 (9.09) | 16 (11.76) | +2.67 [-4.71, +10.81] | 27.27 | 5 -> 5 |
| V4 | 3 (1.24) | 0 (0.00) | -1.24 [-3.35, +0.00] | 100.00 | 11 -> 10 |
| V5 | 18 (7.44) | 18 (13.24) | +5.80 [+0.00, +14.76] | 0.00 | 7 -> 3 |

The largest observed subcategory shift is P1: +6.40 percentage points after removing Django. The leading broader stage is Validation & Harness Constraints in the full cohort and Problem Understanding after exclusion. These observed compositions and rankings are sample-dependent and should not be presented as repository-invariant failure distributions.

The [composition-change intervals](sensitivity/django_taxonomy_shift.csv) use a joint task bootstrap stratified by Django status. The same non-Django draws enter both estimates, preserving overlap. They are pointwise descriptive intervals, not a battery of independent full-versus-excluded tests.

Failure [incidence tests](full/failures/category_inference.csv) compare model category counts per all attempts using exact task-block swaps. There are 48 tests per cohort, corrected within cohort and jointly across all 96 taxonomy tests. Taxonomy findings remain exploratory and separate from the resource/outcome family. V5 counts evaluation-infrastructure blockers, not model repair defects. [Category intervals](full/failures/category_uncertainty.csv) distinguish incidence from composition; zero-event intervals do not bound unseen categories.

## Repository and difficulty sensitivity

Both cohorts contain `stratified/` results by repository and archived difficulty, including task counts, mean resources, outcome rates, failure incidence/composition, and paired estimation intervals. Strata with one task have no confidence interval. Difficulty is the dataset human-fix-time category, not inferred from model outcomes.

Each `repository_sensitivity/` directory contains whole-repository bootstrap intervals, repository-equal summaries, and leave-one-repository-out estimates. Repository resampling retains all tasks, models, and trials and preserves the task-weighted estimand through ratios of sums. Only 11/10 unequal repositories are available, so these intervals are exploratory and have no repository-level significance tests. Repository-equal results deliberately change the weighting and report how many repository-specific failure compositions are defined.

## Optional usage details

Prompt/completion totals are complete. Some optional detail objects are null or contain null/absent fields in the saved responses themselves. [Raw-shape audit](accounting/MISSINGNESS.md) supplies counts and exact examples. The archive cannot establish whether provider reporting, intermediary conversion, or serialization caused each unavailable value; unavailable values are not zero.
