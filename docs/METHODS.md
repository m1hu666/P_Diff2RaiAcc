# Methods for accounting, settings and inference

## Analysis design

The analysis includes the same 100 SWE-bench Verified tasks for Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`), Gemini 3 Pro (`gemini-3-pro-preview`) and GPT-5 (`gpt-5-2025-08-07`), with three attempts per model/task. The resulting 900 attempts are repeated measurements on 100 tasks, not 900 independent samples. Repeated harness executions of the same fixed patch are not additional model trials. Requested identifiers and labels come from the archived runs. All analyses operate on the saved data; reproducing them does not require model API access.

## Token and interaction accounting

For attempt i and its saved assistant responses j, define:

```text
P_i = sum_j response.usage.prompt_tokens
C_i = sum_j response.usage.completion_tokens
S_i = number of saved assistant responses
```

The fields are stored under `messages[*].extra.response.usage`. They are normalized API/adapter reports, not tokens obtained by retokenizing the text. Each saved response is counted once, even if its response contains multiple choices; the agent uses the first choice. S includes format retries and the submission response and agrees with the archived model-call counter. A bash block can contain multiple shell subcommands, so S is not a count of subcommands. Unlogged transport or upstream retries are outside this measurement.

Provider-specific inclusion rules are:

| Interface | Normalized input | Normalized completion |
|---|---|---|
| Anthropic | Native non-cached input + cache-read input + cache-creation input | Native reported output, retaining reported thinking when enabled |
| OpenAI or compatible API | Reported prompt/input total, including cached input | Reported completion/output total, including reported reasoning and non-visible formatting |
| Gemini | `promptTokenCount`, including cached content | Candidate tokens plus thought tokens when the candidate count does not already include thoughts |

Cache and reasoning counters are subdivisions of these totals and are not added again. A None cache-marker setting means no explicit client marker, not disabled automatic caching. The standard inclusion rules explain the normalized interface; only the saved reported totals and available subdivisions are measured here. Optional fields have provider-dependent coverage. A null or absent subdivision is not treated as zero, and an incomplete reported reasoning sum is not a complete thinking total. In particular, the archive cannot independently reconstruct thinking omitted upstream. Coverage is reported by model and field.

P repeatedly counts the conversation history. It is neither the maximum single-request context size nor unique input. C is not visible-text verbosity. Different tokenizers, cache treatment and reasoning modes prevent interpreting cross-provider token counts as directly comparable physical computation. Steps and reported tokens are therefore presented together as observed interaction overhead.

The archived `info.model_stats.instance_cost` is a framework-estimated API cost. It is summarized with paired estimation intervals as a secondary measure, not treated as an invoice or subjected to a cost-efficiency superiority test. Recomputing billed cost would additionally require historical rates, cache price tiers and chargeable retry records.

## Experimental settings and prompts

`result/Statistics results/settings.csv` contains one row per model, setting and value, with its run count and status. `explicit` means present in saved client model arguments; `unset` means omitted; agent settings use their recorded values. The publication table includes temperature, top-p/top-k, output-limit aliases, reasoning/thinking, seed, stop, penalties, verbosity, n, stream, native API tools, cache markers and execution limits.

All client configurations request temperature 0.0 with `drop_params=true`. Unsupported values may be omitted by the adapter, so this is not evidence of equal effective temperatures. The original GPT configuration uses the literal `reasoning: medium` in 299 records and `reasoning_effort: medium` in one; these keys are reported separately. Claude and Gemini have no explicitly configured thinking parameter. Standard interface documentation describes different defaults: extended thinking off for Claude Sonnet 4.5, dynamic high thinking for Gemini 3, and medium reasoning effort for original GPT-5. These are reference defaults, not verified gateway settings. A prompt requiring a THOUGHT section does not establish equal hidden-reasoning budgets.

Top-p, top-k and maximum generation tokens were not explicitly specified. The exact historical effective upstream values were not archived and are marked unrecorded, rather than replaced with current defaults or model capability limits. Anthropic's adapter supplies a required output limit when the client omits it; this does not establish the historical injected value. Observed `length` stops and their completion counts are provided as descriptive diagnostics, not reconstructed configured limits. Source references support the transformation rules, while saved run configurations define the experiment settings. Standard documented thinking defaults may provide context but do not verify the gateway's effective values.

The initial system/user text is compared as exact strings for all nine attempts of each task. All initial prompts and agent templates match. Subsequent prompts naturally diverge with the trajectories. Orchestration is not completely identical: the saved cost limits, shell timeouts and batch/interactive wrappers vary, as reported in the settings table. The step limit is 250 in every run. Raising the cost limit from 3 to 5 USD followed early resource-limited runs; the actual retained settings, including the 8 USD exception, are reported rather than overwritten with that intended limit.

The common agent protocol uses exactly one bash code block per response, serial execution and format-error feedback. Long shell output is reduced to its first and last 5,000 characters. No native API tool definitions are configured, and no native tool calls appear in the responses. These settings distinguish the agent's shell interface from provider-native tool APIs.

## Statistical analysis

The task is the resampling and pairing unit. For each resource measure, the three trials are first averaged within model/task. Every bootstrap resample draws 100 tasks with replacement and retains all models and their three trials together. We use 10,000 resamples with seed 42 to estimate pointwise 95% percentile intervals for paired mean differences and ratios of arithmetic means. These are estimation intervals, not simultaneous multiple-comparison intervals. The task-level assumption is conditional on the sampled benchmark and repository mix, not a guarantee of transfer to new repositories.

For steps, input tokens and completion tokens, two-sided paired permutation tests swap the complete three-trial model blocks within each task. The statistic is the absolute mean paired difference. We use 19,999 Monte Carlo sign flips and `(extreme + 1)/(permutations + 1)`. The null is exchangeability of the two configured systems' outcomes within each task; it is not a randomized causal comparison of model architecture under matched decoding settings. Holm adjustment covers the nine model-pair by resource tests.

For resolution, the task-level value is its success fraction among three trials. Paired differences are reported in percentage points. An exact task-swap test computes the signed-sum distribution of integer success-count differences by dynamic programming. Holm adjustment covers the three model pairs.

For stability, a task is unstable when exactly one or two of its three attempts succeed. A two-sided exact McNemar test compares the paired task-level indicators, using the binomial distribution of discordant orientations. Holm adjustment covers the three model pairs. Counts of 0/3, 1/3, 2/3 and 3/3 are also reported because consistency includes persistent failure and is not equivalent to reliable resolution.

As a multiplicity sensitivity analysis, all 15 hypothesis tests are additionally adjusted together using Holm. Both adjustments are exported. The outcome-family analysis and the conservative global analysis are distinguished in the results, particularly for marginal resolution findings. Confidence intervals are not used to bypass the specified p-value corrections.

Success/failure resource splits, the all-models/all-trials-successful subset, and common-budget task-round subsets remain descriptive sensitivity summaries. Conditioning on success selects different task sets across models, so those splits are not causal evidence that failure causes extra reasoning or that one model is intrinsically more efficient. Fine-grained failure-category inference would additionally require the task/attempt-level coding table; aggregate category counts alone do not preserve the dependence structure.

## References

- [LiteLLM normalized cache accounting](https://docs.litellm.ai/docs/completion/prompt_caching) and [unsupported-parameter handling](https://docs.litellm.ai/docs/completion/drop_params).
- [Anthropic native cache counters](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), [OpenAI output-token accounting](https://developers.openai.com/api/docs/guides/token-counting), and [Gemini token counters](https://ai.google.dev/gemini-api/docs/generate-content/tokens).
- [Claude 4.5 thinking defaults](https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting), [Gemini 3 thinking defaults](https://ai.google.dev/gemini-api/docs/gemini-3), and [original GPT-5 reasoning defaults](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide).
- [Paired permutation definitions and finite-resampling correction](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.permutation_test.html), [exact McNemar definition](https://www.statsmodels.org/stable/generated/statsmodels.stats.contingency_tables.mcnemar.html), and [Holm adjustment](https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html). Implementations in this package use the Python standard library.
