# RQ2: failure persistence, repeatability and interaction economy

> What behavioral patterns do LLMs exhibit during failures, and how do execution stability and trajectory efficiency reflect their reasoning capabilities?

All results describe the archived configurations. The two existing resource PDFs are unchanged.

## Main finding 1: consistency can conceal persistent failure

Of 242 observed failed attempts, 192 (79.34%; task-bootstrap 95% CI 69.83--86.89%) belong to model--task groups that failed in all three observed trials. These are repeatable unresolved outcomes, not estimates of a zero underlying success probability.

Among 64 such model--task groups, 56 (87.50%) retain the same primary failure category in all three trials. Category recurrence does not establish identical reasoning traces or redundant within-trajectory loops.

| Model | 3/3 successes | Mixed outcomes | 0/3 successes | Observed consistency (%) | Persistent / all failed trials |
| --- | ---: | ---: | ---: | ---: | ---: |
| Claude | 69 | 15 | 16 | 85.00 | 48/70 |
| Gemini | 69 | 7 | 24 | 93.00 | 72/82 |
| GPT | 62 | 14 | 24 | 86.00 | 72/90 |

Gemini and Claude both have 69 tasks with three successful trials. Gemini's eight-point higher observed consistency consists entirely of its eight additional 0/3-success tasks. Existing [paired instability tests](../outcomes/stability_comparisons.csv) do not support an adjusted significant difference between models.

| Sensitivity cohort | Persistent / all failed trials | Share (%) | Same-category / persistent groups |
| --- | ---: | ---: | ---: |
| full | 192/242 | 79.34 | 56/64 |
| without_django | 108/136 | 79.41 | 31/36 |
| without_infrastructure_task | 174/224 | 77.68 | 50/58 |

The V5 sensitivity removes all infrastructure-blocked tasks, including all their models and trials. This is distinct from attributing an evaluation blocker to model reasoning.

## Main finding 2: compact successful execution persists on the same solved tasks

The common-success subset contains 55 tasks for which all nine model/trial attempts succeed. It compares the same task set and the same observed resolution outcome, rather than each model's different success set.

| Cohort | Model | Tasks | Attempts | Mean steps | Mean estimated USD |
| --- | --- | ---: | ---: | ---: | ---: |
| full | Claude | 55 | 165 | 37.38 | 0.432 |
| full | Gemini | 55 | 165 | 33.73 | 0.462 |
| full | GPT | 55 | 165 | 11.38 | 0.178 |
| without_django | Claude | 25 | 75 | 39.12 | 0.433 |
| without_django | Gemini | 25 | 75 | 34.68 | 0.472 |
| without_django | GPT | 25 | 75 | 11.80 | 0.192 |

GPT's lower interaction overhead is therefore also observed in successfully solved common cases. This selected subset does not establish overall superiority or matched intrinsic reasoning computation. Provider routes, decoding and orchestration settings remain those of the archive. In the full cohort, GPT has 62 tasks with three successful trials, versus 69 for each other model.

| Comparison | Metric | Mean difference [pointwise 95% CI] | Ratio [pointwise 95% CI] |
| --- | --- | ---: | ---: |
| Claude - GPT | steps | 26.01 [22.67, 29.70] | 3.29 [3.01, 3.59] |
| Claude - GPT | estimated_usd | 0.254 [0.210, 0.301] | 2.43 [2.13, 2.75] |
| Gemini - GPT | steps | 22.36 [19.78, 25.22] | 2.97 [2.70, 3.25] |
| Gemini - GPT | estimated_usd | 0.285 [0.236, 0.337] | 2.60 [2.24, 3.01] |

These exploratory intervals condition on the observed common-success subset; no new hypothesis tests are run. The existing [all-task resource tests](../resources/resource_comparisons.csv) are separate and must not be presented as tests of this subset or of outcome-specific plotted cells.

## Supporting cost finding: unresolved attempts absorb disproportionate estimated spending

| Model | Failure rate (%) | Failure budget share (%) [95% CI] | Estimated USD spent on failed attempts |
| --- | ---: | ---: | ---: |
| Claude | 23.33 | 33.49 [23.74, 43.06] | 54.75 |
| Gemini | 27.33 | 36.16 [25.20, 47.18] | 64.15 |
| GPT | 30.00 | 46.07 [34.08, 57.07] | 32.83 |

Failure budget share is the sum of recorded costs of failed attempts divided by the recorded cost of all attempts. GPT has the highest share but the lowest absolute estimated failure spending. These costs are framework estimates, not invoices; the share is not an estimate of avoidable waste or savings from early stopping.

## Boundary: aggregate failure premiums do not establish reasoning inertia

Restricting each model to tasks with both successful and failed trials allows a within-task outcome contrast. Average failure-minus-success differences are:

| Model | Mixed-outcome tasks | Step difference [95% CI] | USD difference [95% CI] |
| --- | ---: | ---: | ---: |
| Claude | 15 | +4.37 [-6.83, +15.93] | +0.030 [-0.150, +0.213] |
| Gemini | 7 | -16.64 [-36.64, -1.93] | -0.504 [-0.990, -0.096] |
| GPT | 14 | +2.64 [-0.39, +5.71] | +0.069 [-0.019, +0.168] |

These small, outcome-selected subsets differ between models. The intervals are exploratory and pointwise, and cannot establish a causal effect of failure or population equivalence. They do not show a uniform within-task increase across models. Direct claims about redundant loops would require separately defined sequence-level coding of repeated actions or hypotheses and their subsequent evidence.

## Files and reproducibility

- [task_model_patterns.csv](task_model_patterns.csv): 300 model--task outcomes and category sequences.
- [failure_persistence.csv](failure_persistence.csv): repetition, category recurrence and sensitivity counts.
- [failure_budget_shares.csv](failure_budget_shares.csv): spending ratios and task-bootstrap intervals.
- [common_success_summary.csv](common_success_summary.csv): the 55-task and 25-task shared-success sets.
- [common_success_comparisons.csv](common_success_comparisons.csv): paired estimation intervals.
- [within_task_outcome_differences.csv](within_task_outcome_differences.csv): selected mixed-task contrasts.
- [analysis_design.json](analysis_design.json): definitions, source hashes and resampling settings.

Reproduce from the repository root with `python3 scripts/analyze_rq2_patterns.py`.

Inputs are [per_attempt.csv](../../data/per_attempt.csv) and the [canonical failure annotations](../../../../docs/failure_analysis/failure_annotations.csv). Bootstrap intervals use 10,000 draws with seed 42. Whole-task draws preserve all models and three trials for pooled persistence and budget ratios; common-success draws preserve pairing; mixed-task draws retain the selected tasks' trials within each model. All new intervals are pointwise exploratory estimates. Task sampling conditions on the observed repository mix; repository-level sensitivity with only 11 observed clusters remains exploratory.
