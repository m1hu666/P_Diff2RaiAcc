# Analysis results

Cohort: `full`. Analysis set: 100 tasks x 3 models x 3 trials = 900 attempts. Inference uses 100 paired task clusters. Input and completion totals are numeric for every saved response. Full methods are in [METHODS.md](../../../docs/METHODS.md).

## Resource use

| Model | Outcome | n | Mean steps | Median steps [Q1, Q3] | Mean input (k) | Mean output (k) | Estimated USD |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Claude | all | 300 | 42.91 | 40.00 [30.00, 52.00] | 721.27 | 10.48 | 0.545 |
| Claude | success | 230 | 39.62 | 38.00 [28.00, 48.00] | 606.03 | 9.42 | 0.473 |
| Claude | failure | 70 | 53.71 | 51.00 [40.00, 66.25] | 1099.92 | 13.98 | 0.782 |
| Gemini | all | 300 | 38.94 | 34.00 [27.00, 47.00] | 581.09 | 10.19 | 0.591 |
| Gemini | success | 218 | 36.05 | 31.00 [25.00, 44.00] | 482.89 | 8.66 | 0.519 |
| Gemini | failure | 82 | 46.65 | 41.50 [33.00, 56.75] | 842.17 | 14.24 | 0.782 |
| GPT | all | 300 | 13.08 | 12.00 [8.00, 15.25] | 146.98 | 10.47 | 0.238 |
| GPT | success | 210 | 11.55 | 10.00 [8.00, 14.00] | 107.70 | 8.15 | 0.183 |
| GPT | failure | 90 | 16.66 | 14.50 [11.00, 20.00] | 238.63 | 15.89 | 0.365 |

k = 1,000 reported tokens. Outcome-specific rows are descriptive because the successful/failed task sets differ across models. Model inference below uses the same complete set of 100 tasks in this cohort.

| Comparison | Metric | Difference [95% CI] | Ratio [95% CI] | Family Holm p | Global Holm p |
| --- | --- | --- | --- | --- | --- |
| Claude - Gemini | Steps | 3.96 [1.43, 6.51] | 1.10 [1.04, 1.17] | 0.009 | 0.024 |
| Claude - Gemini | Input (k) | 140.18 [59.00, 221.96] | 1.24 [1.09, 1.40] | 0.003 | 0.007 |
| Claude - Gemini | Output (k) | 0.29 [-0.59, 1.09] | 1.03 [0.95, 1.11] | 1.000 | 1.000 |
| Claude - GPT | Steps | 29.83 [27.04, 32.81] | 3.28 [3.06, 3.52] | <0.001 | <0.001 |
| Claude - GPT | Input (k) | 574.30 [489.27, 670.56] | 4.91 [4.25, 5.69] | <0.001 | <0.001 |
| Claude - GPT | Output (k) | 0.01 [-1.13, 1.10] | 1.00 [0.90, 1.12] | 1.000 | 1.000 |
| Gemini - GPT | Steps | 25.86 [23.31, 28.61] | 2.98 [2.76, 3.21] | <0.001 | <0.001 |
| Gemini - GPT | Input (k) | 434.12 [364.06, 513.22] | 3.95 [3.41, 4.58] | <0.001 | <0.001 |
| Gemini - GPT | Output (k) | -0.28 [-1.38, 0.84] | 0.97 [0.88, 1.09] | 1.000 | 1.000 |

Differences are left minus right; ratios are left divided by right. Intervals are pointwise task-bootstrap estimates. Holm correction covers the nine resource tests. Read the adjusted p-values for this cohort; a non-significant result does not establish equivalence. Cross-provider token counts do not measure matched internal reasoning computation. A joint adjustment over both cohorts is provided in `../sensitivity/model_comparisons_both_cohorts.csv`.

## Resolution and execution consistency

| Model | Resolved attempts | Resolution (%) | 0/3 tasks | 1/3 tasks | 2/3 tasks | 3/3 tasks | Unstable tasks |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Claude | 230/300 | 76.67 | 16 | 7 | 8 | 69 | 15 |
| Gemini | 218/300 | 72.67 | 24 | 3 | 4 | 69 | 7 |
| GPT | 210/300 | 70.00 | 24 | 4 | 10 | 62 | 14 |

| Comparison | Difference in pp [95% CI] | Family Holm p | Global Holm p |
| --- | --- | --- | --- |
| Claude - Gemini | 4.00 [-1.00, 9.00] | 0.329 | 1.000 |
| Claude - GPT | 6.67 [2.00, 11.67] | 0.029 | 0.087 |
| Gemini - GPT | 2.67 [-3.33, 9.00] | 0.457 | 1.000 |

Resolution differences use task success fractions. Family Holm adjustment covers three model pairs; global adjustment covers all 15 resource/outcome tests within this cohort. Intervals are pointwise, not multiplicity-adjusted.

| Comparison | Difference in pp [95% CI] | Family Holm p | Global Holm p |
| --- | --- | --- | --- |
| Claude - Gemini | 8.00 [0.00, 16.00] | 0.289 | 0.770 |
| Claude - GPT | 1.00 [-7.00, 9.00] | 1.000 | 1.000 |
| Gemini - GPT | -7.00 [-15.00, 1.00] | 0.289 | 1.000 |

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
