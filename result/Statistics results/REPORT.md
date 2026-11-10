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

Per-cohort paired tests and confidence intervals are in [full](full/REPORT.md) and [without Django](without_django/REPORT.md). The [joint comparison table](sensitivity/model_comparisons_both_cohorts.csv) additionally applies Holm to all 30 resource/outcome tests across both cohorts. Within-cohort global adjustment covers 15 tests. These scopes must not be interchanged.

## Influence on taxonomy

Django contains half of the tasks and contributes 106/242 failures (43.80%). The table distinguishes its contribution to the failure pool from changes in category composition after exclusion.

### Broader stages

| Category | Full n (%) | Without Django n (%) | Change (pp), 95% CI | Django share of category (%) | Rank full -> excluded |
| --- | --- | --- | --- | --- | --- |
| Problem Understanding | 71 (29.34) | 53 (38.97) | +9.63 [-4.35, +23.25] | 25.35 | 2 -> 1 |
| Localization | 17 (7.02) | 3 (2.21) | -4.82 [-12.61, +1.10] | 82.35 | 4 -> 4 |
| Strategy & Logic | 82 (33.88) | 43 (31.62) | -2.27 [-16.14, +12.10] | 47.56 | 1 -> 2 |
| Implementation & Execution | 4 (1.65) | 2 (1.47) | -0.18 [-1.59, +1.50] | 50.00 | 5 -> 5 |
| Validation & Harness Constraints | 68 (28.10) | 35 (25.74) | -2.36 [-15.57, +10.36] | 48.53 | 3 -> 3 |

### Subcategories

| Category | Full n (%) | Without Django n (%) | Change (pp), 95% CI | Django share of category (%) | Rank full -> excluded |
| --- | --- | --- | --- | --- | --- |
| P1 | 44 (18.18) | 35 (25.74) | +7.55 [-4.20, +19.68] | 20.45 | 2 -> 1 |
| P2 | 27 (11.16) | 18 (13.24) | +2.08 [-8.26, +12.50] | 33.33 | 4 -> 4 |
| L1 | 17 (7.02) | 3 (2.21) | -4.82 [-12.61, +1.10] | 82.35 | 7 -> 7 |
| S1 | 53 (21.90) | 31 (22.79) | +0.89 [-11.73, +13.81] | 41.51 | 1 -> 2 |
| S2 | 20 (8.26) | 3 (2.21) | -6.06 [-14.38, +0.13] | 85.00 | 6 -> 7 |
| S3 | 9 (3.72) | 9 (6.62) | +2.90 [+0.00, +9.84] | 0.00 | 8 -> 6 |
| I1 | 4 (1.65) | 2 (1.47) | -0.18 [-1.59, +1.50] | 50.00 | 10 -> 9 |
| V1 | 9 (3.72) | 0 (0.00) | -3.72 [-9.74, +0.00] | 100.00 | 8 -> 10 |
| V2 | 29 (11.98) | 14 (10.29) | -1.69 [-11.11, +7.79] | 51.72 | 3 -> 5 |
| V3 | 27 (11.16) | 21 (15.44) | +4.28 [-4.17, +13.74] | 22.22 | 4 -> 3 |
| V4 | 3 (1.24) | 0 (0.00) | -1.24 [-3.35, +0.00] | 100.00 | 11 -> 10 |

The largest observed subcategory shift is P1: +7.55 percentage points after removing Django. The leading broader stage is Strategy & Logic in the full cohort and Problem Understanding after exclusion. These observed compositions and rankings are sample-dependent and should not be presented as repository-invariant failure distributions.

The [composition-change intervals](sensitivity/django_taxonomy_shift.csv) use a joint task bootstrap stratified by Django status. The same non-Django draws enter both estimates, preserving overlap. They are pointwise descriptive intervals, not a battery of independent full-versus-excluded tests.

Failure [incidence tests](full/failures/category_inference.csv) compare model category counts per all attempts using exact task-block swaps. There are 48 tests per cohort, corrected within cohort and jointly across all 96 taxonomy tests. Taxonomy findings remain exploratory and separate from the resource/outcome family. [Category intervals](full/failures/category_uncertainty.csv) distinguish incidence from composition; zero-event intervals do not bound unseen categories.

## Repository and difficulty sensitivity

Both cohorts contain `stratified/` results by repository and archived difficulty, including task counts, mean resources, outcome rates, failure incidence/composition, and paired estimation intervals. Strata with one task have no confidence interval. Difficulty is the dataset human-fix-time category, not inferred from model outcomes.

Each `repository_sensitivity/` directory contains whole-repository bootstrap intervals, repository-equal summaries, and leave-one-repository-out estimates. Repository resampling retains all tasks, models, and trials and preserves the task-weighted estimand through ratios of sums. Only 11/10 unequal repositories are available, so these intervals are exploratory and have no repository-level significance tests. Repository-equal results deliberately change the weighting and report how many repository-specific failure compositions are defined.

## Optional usage details

Prompt/completion totals are complete. Some optional detail objects are null or contain null/absent fields in the saved responses themselves. [Raw-shape audit](accounting/MISSINGNESS.md) supplies counts and exact examples. The archive cannot establish whether provider reporting, intermediary conversion, or serialization caused each unavailable value; unavailable values are not zero.
