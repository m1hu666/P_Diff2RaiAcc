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

The analysis uses the normalized fields stored for each routed interface:

| Interface | Analyzed input | Analyzed completion | Available subdivisions |
|---|---|---|
| Anthropic route | Saved `usage.prompt_tokens` | Saved `usage.completion_tokens` | Cache-read and cache-creation counters when reported |
| OpenAI-compatible route | Saved `usage.prompt_tokens` | Saved `usage.completion_tokens` | Cached-input and reasoning counters when reported |
| Gemini route | Saved `usage.prompt_tokens` | Saved `usage.completion_tokens` | Cached, text and reasoning counters when reported |

These totals are normalized gateway/adapter reports. Native provider payloads and
the exact historical adapter source were not archived, so the native-to-normalized
transformation is not independently reconstructed. Cache and reasoning counters
are treated as subdivisions already represented in the corresponding saved
totals and are not added again. A None cache-marker setting means no explicit
client marker, not disabled automatic caching. Optional fields have
provider-dependent coverage. A null or absent subdivision is not treated as
zero, and an incomplete reported reasoning sum is not a complete thinking total.
In particular, the archive cannot independently reconstruct thinking omitted
upstream. Coverage is reported by model and field.

P repeatedly counts the conversation history. It is neither the maximum single-request context size nor unique input. C is not visible-text verbosity. Different tokenizers, cache treatment and reasoning modes prevent interpreting cross-provider token counts as directly comparable physical computation. Steps and reported tokens are therefore presented together as observed interaction overhead.

The archived `info.model_stats.instance_cost` is a framework-estimated API cost. It is summarized with paired estimation intervals as a secondary measure, not treated as an invoice or subjected to a cost-efficiency superiority test. Recomputing billed cost would additionally require historical rates, cache price tiers and chargeable retry records.

## Experimental settings and prompts

`result/Statistics results/settings.csv` contains one row per model, setting and value, with its run count and status. `explicit` means present in saved client model arguments; `unset` means omitted; agent settings use their recorded values. The publication table includes temperature, top-p/top-k, output-limit aliases, reasoning/thinking, seed, stop, penalties, verbosity, n, stream, native API tools, cache markers and execution limits.

All 900 trajectories record mini-SWE-agent 1.15.0. During the upgrade to that version, the only model-specific decoding override added by the experimenter was medium reasoning for GPT; the other model arguments were left at the common framework/client configuration values. This provenance is distinct from serialization status: all archived client configurations contain `temperature=0.0` and `drop_params=true`, while GPT contains `reasoning: medium` in 299 attempts and `reasoning_effort: medium` in one. Thus medium reasoning was requested in every GPT attempt. Unsupported values may be removed by the adapter, so the common serialized temperature is not evidence of equal upstream temperatures.

Official documentation is used as reference context for omitted fields, not as a substitute for the archived request. For direct Anthropic Messages requests, temperature defaults to 1.0 if omitted, `top_p` defaulted to 0.99 during the experiments, `max_tokens` is required, and Claude Sonnet 4.5 defaults to thinking off with a 64K model output ceiling. Google documents a Gemini 3 temperature default of 1.0, high thinking when `thinking_level` is omitted, a general `topP` default of 0.95 while noting model-dependent generation defaults, a randomized seed when omitted, and a 65,536-token output ceiling for `gemini-3-pro-preview`. OpenAI documents medium as the original GPT-5 reasoning default, a 128K output ceiling, and incompatibility of older GPT-5 models with `temperature` and `top_p`. These documented defaults and ceilings are linked in the generated [settings table](../result/Statistics%20results/tables/settings.md) and below.

Top-p, top-k and maximum generation tokens were not explicitly specified in the archived client arguments. Any direct Anthropic Messages request would have required a `max_tokens` value after adapter/gateway processing, but that native payload was not retained. For GPT, successful calls together with `drop_params=true` and OpenAI's documented incompatibility are consistent with the adapter dropping temperature; this cannot be confirmed from a native payload. The exact historical gateway-effective values are consequently marked unrecorded. The 64K, 65,536 and 128K values are model capability ceilings, not reconstructed experimental limits. Observed `length` stops and their completion counts are descriptive diagnostics only. Claude and Gemini have no explicitly configured thinking field; their documented off/high behaviors apply only if the route preserved omitted-field behavior. A prompt requiring a THOUGHT section does not establish equal hidden-reasoning budgets.

The initial system/user text is compared as exact strings for all nine attempts of each task. All initial prompts and agent templates match. Subsequent prompts naturally diverge with the trajectories. Orchestration is not completely identical: the saved cost limits, shell timeouts and batch/interactive wrappers vary, as reported in the settings table. The step limit is 250 in every run. Raising the cost limit from 3 to 5 USD followed early resource-limited runs; the actual retained settings, including the 8 USD exception, are reported rather than overwritten with that intended limit.

The common agent protocol uses exactly one bash code block per response, serial execution and format-error feedback. Long shell output is reduced to its first and last 5,000 characters. No native API tool definitions are configured, and no native tool calls appear in the responses. These settings distinguish the agent's shell interface from provider-native tool APIs.

## Statistical analysis

The task is the resampling and pairing unit. For each resource measure, the three trials are first averaged within model/task. Every bootstrap resample draws 100 tasks with replacement and retains all models and their three trials together. We use 10,000 resamples with seed 42 to estimate pointwise 95% percentile intervals for paired mean differences and ratios of arithmetic means. These are estimation intervals, not simultaneous multiple-comparison intervals. The task-level assumption is conditional on the sampled benchmark and repository mix, not a guarantee of transfer to new repositories.

For steps, input tokens and completion tokens, two-sided paired permutation tests swap the complete three-trial model blocks within each task. The statistic is the absolute mean paired difference. We use 19,999 Monte Carlo sign flips and `(extreme + 1)/(permutations + 1)`. The null is exchangeability of the two configured systems' outcomes within each task; it is not a randomized causal comparison of model architecture under matched decoding settings. Holm adjustment covers the nine model-pair by resource tests.

For resolution, the task-level value is its success fraction among three trials. Paired differences are reported in percentage points. An exact task-swap test computes the signed-sum distribution of integer success-count differences by dynamic programming. Holm adjustment covers the three model pairs.

For stability, a task is unstable when exactly one or two of its three attempts succeed. A two-sided exact McNemar test compares the paired task-level indicators, using the binomial distribution of discordant orientations. Holm adjustment covers the three model pairs. Counts of 0/3, 1/3, 2/3 and 3/3 are also reported because consistency includes persistent failure and is not equivalent to reliable resolution.

As a multiplicity sensitivity analysis, all 15 hypothesis tests are additionally adjusted together using Holm. Both adjustments are exported. The outcome-family analysis and the conservative global analysis are distinguished in the results, particularly for marginal resolution findings. Confidence intervals are not used to bypass the specified p-value corrections.

Success/failure resource splits, the all-models/all-trials-successful subset, and common-budget task-round subsets remain descriptive sensitivity summaries. Conditioning on success selects different task sets across models, so those splits are not causal evidence that failure causes extra reasoning or that one model is intrinsically more efficient. Task/attempt-level failure labels are available in `failure_trial_catalog.csv`, but category-level inferential tests are not implemented in the current pipeline. Such tests must retain task dependence; aggregate category counts alone do not preserve that structure.

## References

- [LiteLLM normalized cache accounting](https://docs.litellm.ai/docs/completion/prompt_caching) and [unsupported-parameter handling](https://docs.litellm.ai/docs/completion/drop_params).
- [Anthropic native cache counters](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), [OpenAI output-token accounting](https://developers.openai.com/api/docs/guides/token-counting), and [Gemini token counters](https://ai.google.dev/gemini-api/docs/generate-content/tokens).
- Claude: [Messages request parameters](https://platform.claude.com/docs/en/api/messages/create), [temperature default](https://platform.claude.com/docs/en/api/beta/messages/create), [May 2025 `top_p` default change](https://platform.claude.com/docs/en/release-notes/overview), [Claude 4.5 thinking default](https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting), and [output limits](https://platform.claude.com/docs/en/build-with-claude/thinking).
- Gemini: [Gemini 3 defaults](https://ai.google.dev/gemini-api/docs/gemini-3), [generation-parameter definitions](https://ai.google.dev/api/generate-content), [sampling guidance](https://ai.google.dev/gemini-api/docs/prompting-strategies), and [`gemini-3-pro-preview` limits](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-preview).
- OpenAI: [original GPT-5 reasoning defaults](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5), [`gpt-5-2025-08-07` limits](https://developers.openai.com/api/docs/models/gpt-5), and [GPT-5 parameter compatibility](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.4).
- [Paired permutation definitions and finite-resampling correction](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.permutation_test.html), [exact McNemar definition](https://www.statsmodels.org/stable/generated/statsmodels.stats.contingency_tables.mcnemar.html), and [Holm adjustment](https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html). Implementations in this package use the Python standard library.
