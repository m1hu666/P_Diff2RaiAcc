# Analysis results

Cohort: `without_django`. Analysis set: 50 tasks x 3 models x 3 trials = 450 attempts. Inference uses 50 paired task clusters. Input and completion totals are numeric for every saved response. Full methods are in [METHODS.md](../../../docs/METHODS.md).

## Resource use

| Model | Outcome | n | Mean steps | Median steps [Q1, Q3] | Mean input (k) | Mean output (k) | Estimated USD |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Claude | all | 150 | 44.08 | 41.00 [31.00, 55.75] | 740.80 | 9.71 | 0.541 |
| Claude | success | 110 | 40.76 | 38.50 [28.00, 50.50] | 613.84 | 8.37 | 0.457 |
| Claude | failure | 40 | 53.20 | 50.50 [40.00, 67.50] | 1089.92 | 13.40 | 0.770 |
| Gemini | all | 150 | 42.06 | 37.00 [28.25, 49.75] | 654.77 | 9.89 | 0.628 |
| Gemini | success | 106 | 38.91 | 34.50 [25.00, 46.75] | 540.09 | 8.15 | 0.549 |
| Gemini | failure | 44 | 49.66 | 42.50 [34.50, 59.75] | 931.03 | 14.08 | 0.818 |
| GPT | all | 150 | 14.01 | 12.00 [9.00, 16.75] | 174.35 | 11.34 | 0.269 |
| GPT | success | 98 | 12.06 | 11.00 [8.00, 14.00] | 121.87 | 8.45 | 0.198 |
| GPT | failure | 52 | 17.67 | 15.00 [12.00, 22.25] | 273.25 | 16.78 | 0.402 |

k = 1,000 reported tokens. Outcome-specific rows are descriptive because the successful/failed task sets differ across models. Model inference below uses the same complete set of 50 tasks in this cohort.

| Comparison | Metric | Difference [95% CI] | Ratio [95% CI] | Family Holm p | Global Holm p |
| --- | --- | --- | --- | --- | --- |
| Claude - Gemini | Steps | 2.02 [-1.56, 5.64] | 1.05 [0.96, 1.14] | 0.283 | 1.000 |
| Claude - GPT | Steps | 30.07 [25.93, 34.21] | 3.15 [2.84, 3.47] | <0.001 | <0.001 |
| Gemini - GPT | Steps | 28.05 [23.98, 32.40] | 3.00 [2.70, 3.32] | <0.001 | <0.001 |

Differences are left minus right; ratios are left divided by right. Intervals are pointwise task-bootstrap estimates. Holm correction covers the three pairwise interaction-step tests. Read the adjusted p-values for this cohort; a non-significant result does not establish equivalence. Cross-provider token counts are summarized descriptively and are not subjected to model-comparison tests. A joint adjustment over both cohorts is provided in `../sensitivity/model_comparisons_both_cohorts.csv`.

## Resolution and execution consistency

| Model | Resolved attempts | Resolution (%) | 0/3 tasks | 1/3 tasks | 2/3 tasks | 3/3 tasks | Unstable tasks |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Claude | 110/150 | 73.33 | 10 | 4 | 2 | 34 | 6 |
| Gemini | 106/150 | 70.67 | 13 | 2 | 1 | 34 | 3 |
| GPT | 98/150 | 65.33 | 13 | 3 | 7 | 27 | 10 |

| Comparison | Difference in pp [95% CI] | Family Holm p | Global Holm p |
| --- | --- | --- | --- |
| Claude - Gemini | 2.67 [-2.67, 8.00] | 0.492 | 1.000 |
| Claude - GPT | 8.00 [2.67, 14.00] | 0.029 | 0.068 |
| Gemini - GPT | 5.33 [-1.33, 12.67] | 0.453 | 1.000 |

Resolution differences use task success fractions. Family Holm adjustment covers three model pairs; global adjustment covers all nine interaction-step and outcome tests within this cohort. Intervals are pointwise, not multiplicity-adjusted.

| Comparison | Difference in pp [95% CI] | Family Holm p | Global Holm p |
| --- | --- | --- | --- |
| Claude - Gemini | 6.00 [-6.00, 18.00] | 0.688 | 1.000 |
| Claude - GPT | -8.00 [-20.00, 4.00] | 0.688 | 1.000 |
| Gemini - GPT | -14.00 [-26.00, -2.00] | 0.196 | 0.393 |

Instability means one or two successes out of three trials. Counts and paired comparisons are shown above; consistently failed tasks also count as consistent.

## Settings and accounting

Archived settings, configuration provenance, and linked official provider references are in [settings](../settings/settings.md); token-field definitions are in [token definitions](../accounting/token_accounting.md). Official defaults are used only to interpret omitted fields and are kept separate from saved client arguments and model capability ceilings. An unrecorded gateway-effective value is not reconstructed from current documentation. [output diagnostics](../accounting/output_limit_diagnostics.md) reports observed length stops and their reported completion counts; these are observations, not configured request limits.

| Model | Field | Numeric/total | Coverage (%) | Null | Missing |
| --- | --- | --- | --- | --- | --- |
| Claude | prompt_tokens | 12872/12872 | 100.00 | 0 | 0 |
| Claude | completion_tokens | 12872/12872 | 100.00 | 0 | 0 |
| Claude | prompt_tokens_details.cached_tokens | 12872/12872 | 100.00 | 0 | 0 |
| Claude | cache_creation_input_tokens | 12872/12872 | 100.00 | 0 | 0 |
| Claude | completion_tokens_details.reasoning_tokens | 24/12872 | 0.19 | 0 | 12848 |
| Gemini | prompt_tokens | 11683/11683 | 100.00 | 0 | 0 |
| Gemini | completion_tokens | 11683/11683 | 100.00 | 0 | 0 |
| Gemini | prompt_tokens_details.cached_tokens | 7930/11683 | 67.88 | 3753 | 0 |
| Gemini | cache_creation_input_tokens | 0/11683 | 0.00 | 0 | 11683 |
| Gemini | completion_tokens_details.reasoning_tokens | 452/11683 | 3.87 | 5141 | 6090 |
| GPT | prompt_tokens | 3924/3924 | 100.00 | 0 | 0 |
| GPT | completion_tokens | 3924/3924 | 100.00 | 0 | 0 |
| GPT | prompt_tokens_details.cached_tokens | 3924/3924 | 100.00 | 0 | 0 |
| GPT | cache_creation_input_tokens | 0/3924 | 0.00 | 0 | 3924 |
| GPT | completion_tokens_details.reasoning_tokens | 3661/3924 | 93.30 | 0 | 263 |

Optional cache/thinking details are not uniformly complete. Missing values remain missing, and subdivisions are not added again to their totals. Exact formulas, the common tool protocol, prompt consistency and differing orchestration settings are specified in [METHODS.md](../../../docs/METHODS.md).
