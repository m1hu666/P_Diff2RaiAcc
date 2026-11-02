# Statistics catalogue and interpretation

This catalogue distinguishes statistical results, normalized analysis data,
experimental settings, and integrity checks. CSV files contain the numeric
results; files under `tables/` display selected columns from those results.
The display tables are Markdown only. LaTeX conversion is deferred until tables
are selected for use.

Start with [REPORT.md](REPORT.md) for a short results overview and
[METHODS.md](../../docs/METHODS.md) for accounting and statistical methods.
The analysis contains 100 tasks, three models and three trials per model/task:
900 attempts, 28,479 saved responses, 658 successful attempts and 242 failed
attempts. Trials are repeated measurements within tasks.

## Statistical results

### Resource use

| File | Contents | Interpretation |
|---|---|---|
| [summary_metrics.csv](summary_metrics.csv) | 108 rows: three cohorts x all/success/failure groups x three models x four measures; count, observed count, mean, median, quartiles, minimum, maximum and sum | Descriptive distributions of steps, input tokens, output tokens and estimated cost. Empty cells in zero-attempt groups are not zero usage. No hypothesis tests or confidence intervals are included here. |
| [resource_comparisons.csv](resource_comparisons.csv) | Nine rows: three model pairs x steps/input/output; means, paired differences, ratios, 95% confidence intervals and raw/adjusted p-values | Main task-paired resource comparisons on all 100 tasks. All step and input-token comparisons survive both Holm adjustments; output-token differences are not statistically established. |
| [estimated_cost_comparisons.csv](estimated_cost_comparisons.csv) | Three model pairs; mean recorded USD, paired differences, ratios and 95% confidence intervals | Exploratory comparisons of archived framework cost estimates. There are no cost hypothesis tests or p-values. Historical bills and unlogged charges are not reconstructed. |

The four resource measures have the following units and limitations:

| Measure | Definition | What it measures |
|---|---|---|
| `steps` | Number of saved assistant/API responses in an attempt | Interaction count, including format retries and the submission response. A response with one valid bash block is a shell action; that block can contain several shell commands. |
| `prompt_tokens` | Sum of reported prompt counts over all responses in an attempt | Cumulative reported input. Conversation history is counted again on each request; this is not unique input or maximum context size. |
| `completion_tokens` | Sum of reported completion counts over all responses in an attempt | Reported output, retaining reasoning when included upstream. It does not isolate visible prose or measure equal computation across providers. |
| `recorded_cost_usd` | Archived `info.model_stats.instance_cost` | The framework's approximate API cost estimate, with provider-specific cache and pricing assumptions. |

Across all 300 attempts per model, the current arithmetic means are:

| Model | Steps | Input tokens (k) | Output tokens (k) | Estimated USD |
|---|---:|---:|---:|---:|
| Claude | 42.91 | 721.27 | 10.48 | 0.545 |
| Gemini | 38.94 | 581.09 | 10.19 | 0.591 |
| GPT | 13.08 | 146.98 | 10.47 | 0.238 |

Here and in the display tables, k = 1,000 tokens. Success/failure splits answer
how resource use is distributed among the observed outcomes. They do not show
that failure causes additional reasoning, because the selected task sets differ.

### Resolution and trial consistency

| File | Contents | Interpretation |
|---|---|---|
| [success_stability_summary.csv](success_stability_summary.csv) | Three model rows; resolved attempts, resolution rate, tasks with 0/3, 1/3, 2/3 or 3/3 successes, instability rate, and bootstrap intervals | Resolution uses 300 attempts per model. Instability uses 100 tasks per model; a task is unstable if one or two of its three attempts succeed. Both 0/3 and 3/3 are consistent, so consistency alone does not imply successful repair. |
| [success_comparisons.csv](success_comparisons.csv) | Three paired resolution comparisons in percentage points, 95% intervals, exact task-swap tests and Holm adjustments | Claude-GPT is +6.67 percentage points, with family-adjusted p = 0.029 but global-adjusted p = 0.087. This is an exploratory difference sensitive to the multiplicity scope. |
| [stability_comparisons.csv](stability_comparisons.csv) | Three paired instability comparisons in percentage points, discordant task counts, 95% intervals, exact McNemar tests and Holm adjustments | No model-pair instability comparison is significant after correction. |

| Model | Resolved attempts | Resolution | 0/3 tasks | 1/3 tasks | 2/3 tasks | 3/3 tasks | Unstable tasks |
|---|---:|---:|---:|---:|---:|---:|---:|
| Claude | 230/300 | 76.67% | 16 | 7 | 8 | 69 | 15/100 |
| Gemini | 218/300 | 72.67% | 24 | 3 | 4 | 69 | 7/100 |
| GPT | 210/300 | 70.00% | 24 | 4 | 10 | 62 | 14/100 |

### Failure frequencies and taxonomy

| File | Contents | Interpretation |
|---|---|---|
| [failure_trial_catalog.csv](failure_trial_catalog.csv) | 242 failed attempts, each with one retained primary category, stage, diagnosis, source paths and hashes | The auditable trial-level table preserves all failed outcomes. Assignments awaiting further verification remain in their categories, with evidence limitations in their diagnoses. Human annotations are inputs; the builder checks and summarizes them rather than automatically diagnosing causes. |
| [failure_model_summary.csv](failure_model_summary.csv) | Three rows; failed attempts, failure rate and tasks containing a failure | Claude: 70/300 failures on 31 tasks; Gemini: 82/300 on 31 tasks; GPT: 90/300 on 38 tasks. |
| [failure_stage_summary.csv](failure_stage_summary.csv) | Five stages, with overall/model counts, percentages and distinct task counts | Overall stage composition and model-specific incidence. These are descriptive counts, without category-level significance tests. |
| [failure_taxonomy_summary.csv](failure_taxonomy_summary.csv) | Eleven subcategories, with the same overall/model breakdown | Fine-grained failure composition. Repeated failures on one task must not be interpreted as independent task evidence. |
| [failure_task_summary.csv](failure_task_summary.csv) | 45 tasks with at least one failed attempt; each model's three outcomes and failure categories | Shows how failures cluster within tasks and repeat across models/trials. |

The stage totals are Problem Understanding 71 (29.34%), Localization 17 (7.02%),
Strategy & Logic 82 (33.88%), Implementation & Execution 4 (1.65%), and
Validation & Harness Constraints 68 (28.10%). These percentages use all 242 failed
attempts as their denominator. Subcategory counts are P1=44, P2=27, L1=17,
S1=53, S2=20, S3=9, I1=4, V1=9, V2=29, V3=27 and V4=3. Definitions are in the
[failure codebook](../../docs/failure_analysis/FAILURE_CODEBOOK.md); the complete
case report is [result/analyse.md](../analyse.md).

Fourteen assignments remain in their original categories pending further
verification: Astropy-8872 (all nine, V3), Django-11532 (Claude/GPT trials 1
and 3, V3), and Sphinx-11510 (Claude trial 2, S2). Their evidence limitations
are stated in the diagnoses and case notes. Retention is not confirmation of
the attribution. All 242 failures remain in the eleven-category totals and
percentage denominators.

The stage and taxonomy CSVs deliberately distinguish these denominators:

| Column | Denominator |
|---|---|
| `share_of_all_failures_percent` | All 242 failed attempts |
| `<Model>_share_of_model_failures_percent` | That model's 70, 82 or 90 failures |
| `<Model>_incidence_per_all_attempts_percent` | All 300 attempts of that model |
| `distinct_tasks` / `<Model>_distinct_tasks` | Count of unique tasks exhibiting that category; not a percentage |

Distinct-task counts can overlap across categories and should not be added.
Task-level category labels are available in the catalogue. Category-level
inferential tests have not been implemented in the current pipeline. The
resource, resolution and instability p-values do not test taxonomy differences.

## How to read the inferential columns

[analysis_design.json](analysis_design.json) records the design, seed and
resampling counts. The three trials are first averaged within each model/task,
then the models are compared on the same 100 tasks. This accounts for the
repeated trials and task pairing; it does not make decoding or orchestration
settings identical or establish causal model effects.

| Column | Meaning |
|---|---|
| `left_mean`, `right_mean` | Mean per-attempt resource use, after averaging within model/task |
| `mean_difference` | Left model mean minus right model mean, in the original measure's units |
| `ratio_of_means` | Left model mean divided by right model mean; not the mean of per-task ratios |
| `difference_percentage_points` | Left rate minus right rate, multiplied by 100; used for resolution and instability |
| `*_ci95_lower`, `*_ci95_upper` | Pointwise 95% percentile bootstrap interval; suffixes `_pp` identify percentage-point units |
| `p_value` | Two-sided test under the relevant paired null hypothesis; not the probability that the null is true |
| `p_value_holm` | Holm adjustment within the outcome family: nine resource, three resolution, or three instability comparisons |
| `p_value_holm_global` | Additional Holm adjustment over all 15 hypothesis tests |

Each of 10,000 bootstrap resamples draws 100 tasks with replacement, carrying
all models and trials for each selected task together. The 2.5th and 97.5th
percentiles form the interval. Resource p-values use 19,999 task-level sign
flips; resolution uses an exact task-swap test; instability uses an exact paired
McNemar test. The seed is 42.

For example, Claude-GPT has a steps difference of 29.83 [27.04, 32.81] and a
ratio of 3.28 [3.06, 3.52]: Claude uses about 30 more model interactions per
attempt on average. Its global-adjusted p-value is below 0.001. This supports a
difference in observed interaction counts under the archived settings.

A non-significant test does not establish equivalence. The confidence intervals
are pointwise, not adjusted for simultaneous coverage of all comparisons, and
must not be used to bypass the specified p-value adjustments. Task resampling
assumes tasks are suitable independent clusters; shared repositories, including
the concentration of Django tasks, limit broader generalization.

## Cohorts in the descriptive summaries

A cohort is a group of attempts selected by an explicit rule. Only the full
100-task cohort is used by the current inferential comparison files.

| `cohort` value | Included attempts | Purpose and limitation |
|---|---|---|
| `all_archived_900` | 900 attempts, 100 tasks, 300 attempts per model | Main analysis set |
| `all_models_solved_all_three_trials` | 495 attempts from 55 tasks where all nine attempts succeed | Descriptive sensitivity check on commonly solved tasks; conditions on success and selects easier tasks |
| `matched_task_rounds_cost3_timeout60` | 294 attempts: 98 task-round blocks across 96 tasks, 98 attempts per model | Descriptive sensitivity check matching cost cap and shell timeout only; not a full three-trial matched cohort or complete configuration match |

Within each cohort, `group` selects `all`, `success` or `failure` attempts.
Quartiles and medians describe variation among attempts; they are not confidence
intervals for the mean. These sensitivity subsets currently have no separate
inferential tests.

## Normalized analysis data

| File | Rows | Contents and role |
|---|---:|---|
| [per_attempt.csv](per_attempt.csv) | 900 | One model/task/trial per row. Contains outcomes, steps, token totals, estimated cost, settings, hashes, submission checks, shell actions, format errors, timeouts, length stops, native tool calls and feedback diagnostics. Input to the main inference script. |
| [per_response.csv](per_response.csv) | 28,479 | One saved assistant response per row. Contains token values/states, response model, timestamps, choice/finish information, bash parsing, timeout and native-tool diagnostics. Supports reconstruction of attempt totals and investigation of reporting differences. |

In `per_response.csv`, token `*.state` distinguishes `numeric`, `null`, `missing`
and `other`. In `per_attempt.csv`, `*.reported_sum` sums only numeric reports,
`*.observed_responses` counts them, and `*.complete` states whether all responses
had numeric values. The unsuffixed aggregate is blank if any response lacks
that field. Partial cache/reasoning sums must not be treated as complete totals.
Extra diagnostic columns have no dedicated inferential tests in this package.

## Settings, prompts and token-accounting evidence

| File | Contents | Interpretation |
|---|---|---|
| [settings.csv](settings.csv) | 110 rows covering client parameters and agent settings, including value, status and attempt count | Main configuration inventory. `explicit` means saved in client arguments; `unset` means omitted; `recorded` identifies saved agent settings. Historical effective provider values are not inferred from omitted arguments. |
| [parameter_inventory.csv](parameter_inventory.csv) | 68 rows containing the client-API subset of `settings.csv` | An alternative filtered view, not additional observations. |
| [configuration_variants.json](configuration_variants.json) | 13 saved configuration variants and their model/task/trial members | Preserves complete model kwargs and non-template orchestration differences, including cost caps, timeouts and wrappers. |
| [prompt_consistency.csv](prompt_consistency.csv) | 100 tasks, each with nine initial-prompt hashes and image-string variant counts | Every task has one initial system/user prompt variant. Initial prompt equality does not imply identical later histories or effective decoding. Image strings are compared, not container-content digests. |
| [prompt_templates.json](prompt_templates.json) | One unique set of agent templates | Full system, task, observation, timeout and format-error instructions used by the saved configurations. |
| [usage_field_coverage.csv](usage_field_coverage.csv) | 30 rows: three models x ten token fields; numeric/null/missing counts, zeros/nonzeros and observed sums | Measures reporting availability. Both top-level token totals are numeric for every response. Optional-field availability is not model accuracy or an estimate of hidden computation. |
| [failure_boundary_checks.json](failure_boundary_checks.json) | Fourteen small baseline/candidate behavior checks, including an optional historical SymPy source check | Diagnostic evidence for the S2/V3 distinction. Sphinx and printer checks use stubs; this file is not a set of new model trials or full benchmark evaluations. Reproduce with `scripts/check_failure_boundary_examples.py` and the documented historical source for the fourteenth check. |
| [response_model_mapping.csv](response_model_mapping.csv) | Six requested/returned model-label combinations and response counts | Route-label metadata; labels alone do not independently identify an upstream backend. |

Gemini's cache field is numeric in 7,930/11,683 responses (67.88%) and null in
3,753. The numeric values are all nonzero; `text_tokens + cached_tokens` equals
`prompt_tokens` when numeric, and `text_tokens` equals `prompt_tokens` when null.
This is availability of an explicit cache subdivision, not missing prompt totals.
Reported reasoning subdivisions are numeric for Claude 24/12,872, Gemini
452/11,683 and GPT 3,661/3,924 responses. Unreported thinking cannot be recovered
from these totals alone. Cache/reasoning subdivisions are already included in
their corresponding normalized totals and are not added again.

All runs request temperature 0.0 with `drop_params=true`. The common framework
configuration serialized those values; the only model-specific decoding
override added during the mini-SWE-agent 1.15.0 upgrade was medium reasoning for
GPT. It appears under `reasoning` in 299 attempts and `reasoning_effort` in one.
Claude/Gemini have no explicit thinking parameter. Top-p/top-k, maximum output
aliases and other omitted decoding parameters remain client-unset. The official
provider references and the boundary between documented defaults, archived
arguments and model capability ceilings are reported in
[tables/settings.md](tables/settings.md). All runs have step limit 250, but cost
caps, Gemini shell timeouts and batch/interactive wrappers vary. No native API
tools are configured or used; commands are parsed from textual bash blocks.

All 900 archived trajectories record mini-SWE-agent 1.15.0. Historical upstream
defaults that were not saved in the trajectories remain unrecorded.

## Integrity, provenance and independent cross-checks

These files help reproduce or check the results; they do not add independent
samples or hypothesis tests.

| File | Contents and current result |
|---|---|
| [audit.json](audit.json) | Main extraction summary: 900 attempts, 28,479 responses, one template variant, no initial-prompt mismatch, cohort sizes, usage checks and length-stop diagnostics |
| [anomalies.csv](anomalies.csv) | Structural extraction anomalies; currently zero rows |
| [input_manifest.json](input_manifest.json) | SHA-256 hashes for 900 trajectories and nine verified-label JSON files |
| [validation.json](validation.json) | Main output validation: coverage, arithmetic, 909 input hashes and 15 comparison rows pass |
| [failure_analysis_inputs.json](failure_analysis_inputs.json) | Hashes for 887 indexed evidence files and three annotation-input files |
| [failure_analysis_validation.json](failure_analysis_validation.json) | Failure catalogue validation: 242 unique failures on 45 tasks, five stages, eleven subcategories, zero missing failure records or successful trials in the catalogue |
| [trajectory_audit/per_trajectory.csv](trajectory_audit/per_trajectory.csv) | Independent trajectory-level extraction for 900 attempts; overlaps the canonical `per_attempt.csv` as a cross-check |
| [trajectory_audit/audit.json](trajectory_audit/audit.json) | Independent usage/configuration/completeness summary; no missing trajectories or reported issues |
| [submission_integrity/submission_inventory.csv](submission_integrity/submission_inventory.csv) | 900 attempts comparing archived submissions, verified patches and evaluation labels |
| [submission_integrity/nonempty_patch_text_differences.csv](submission_integrity/nonempty_patch_text_differences.csv) | 64 attempts with nonempty but differing submission/verified patch text; 63 Claude and one GPT. Text inequality alone does not establish behavioral inequality or its cause. |
| [submission_integrity/submission_audit.json](submission_integrity/submission_audit.json) | All 900 terminate as Submitted, with no priority issues or evaluation-label conflicts; 64 text differences are retained for inspection |
| [token_usage_stats.txt](token_usage_stats.txt) | Independent success/failure token means from `cal.py`; overlaps the canonical descriptive summaries and supplies no additional significance test |

An empty anomaly list means the implemented checks passed. It does not certify
equal provider tokenization, identical upstream settings, or complete billing.

## Markdown display tables

These are presentation views of the canonical results or method definitions.

| File | Source and scope |
|---|---|
| [tables/resource_usage.md](tables/resource_usage.md) | Success/failure rows from `summary_metrics.csv`; descriptive only |
| [tables/resource_inference.md](tables/resource_inference.md) | Nine comparisons from `resource_comparisons.csv` |
| [tables/estimated_cost.md](tables/estimated_cost.md) | Three exploratory comparisons from `estimated_cost_comparisons.csv` |
| [tables/success_stability.md](tables/success_stability.md) | Model counts/rates from `success_stability_summary.csv` |
| [tables/success_inference.md](tables/success_inference.md) | Three comparisons from `success_comparisons.csv` |
| [tables/stability_inference.md](tables/stability_inference.md) | Three comparisons from `stability_comparisons.csv` |
| [tables/settings.md](tables/settings.md) | Selected rows of `settings.csv`, configuration provenance, and linked official provider defaults/capability limits, with claim boundaries |
| [tables/accounting_coverage.md](tables/accounting_coverage.md) | Selected fields from `usage_field_coverage.csv` |
| [tables/token_accounting.md](tables/token_accounting.md) | Saved normalized fields and available subdivisions used by the analysis; not estimated effects |
| [tables/output_limit_diagnostics.md](tables/output_limit_diagnostics.md) | Recorded length stops: Claude 73/12,872 at reported completion=4,096; Gemini 1/11,683 at 65,548; GPT 0/3,924. These are response counts and observations, not recovered maximum-output settings. |

## Rebuild commands

Run from the repository root:

```bash
python3 scripts/run_analysis.py
python3 scripts/build_failure_analysis.py
```

The first command rebuilds the normalized data, main statistical comparisons,
Markdown report/tables and main validation. The second rebuilds the failure
catalogue, frequency summaries, evidence index, validation and case report.
This catalogue is maintained separately from generated tables.

Optional independent cross-checks:

```bash
python3 scripts/audit_inference_usage.py
python3 scripts/audit_submission_integrity.py
python3 scripts/cal.py
```
