# Experimental settings

The first table is generated from the 900 archived trajectories. `Unset` means
the field was absent from the saved client arguments; it does not by itself
identify the value ultimately sent by an adapter or gateway. All trajectories
record mini-SWE-agent 1.15.0. During that upgrade, the experimenter added only
one model-specific decoding override: medium reasoning for GPT. The serialized
`temperature=0.0` and `drop_params=true` values otherwise came from the common
framework/client configuration.

## Archived client and agent configuration

| Saved setting | Claude | Gemini | GPT |
| --- | --- | --- | --- |
| temperature | 0.0 | 0.0 | 0.0 |
| drop_params | true | true | true |
| reasoning | Unset | Unset | medium (299); Unset (1) |
| reasoning_effort | Unset | Unset | Unset (299); medium (1) |
| thinking | Unset | Unset | Unset |
| thinking_config | Unset | Unset | Unset |
| top_p | Unset | Unset | Unset |
| top_k | Unset | Unset | Unset |
| max_tokens | Unset | Unset | Unset |
| max_completion_tokens | Unset | Unset | Unset |
| max_output_tokens | Unset | Unset | Unset |
| seed | Unset | Unset | Unset |
| stop | Unset | Unset | Unset |
| frequency_penalty | Unset | Unset | Unset |
| presence_penalty | Unset | Unset | Unset |
| verbosity | Unset | Unset | Unset |
| response_format | Unset | Unset | Unset |
| n | Unset | Unset | Unset |
| stream | Unset | Unset | Unset |
| tools | Unset | Unset | Unset |
| tool_choice | Unset | Unset | Unset |
| parallel_tool_calls | Unset | Unset | Unset |
| cache_control | default_end | None | None |
| step_limit | 250 | 250 | 250 |
| cost_limit_usd | 3.0 (299); 5.0 (1) | 3.0 (231); 5.0 (68); 8.0 (1) | 3.0 (299); 5.0 (1) |
| shell_timeout_seconds | 60 | 60 (101); 300 (199) | 60 |
| agent_wrapper | Batch (299); Interactive/yolo (1) | Batch (297); Interactive/yolo (3) | Batch (297); Interactive/yolo (3) |
| framework_version | 1.15.0 | 1.15.0 | 1.15.0 |

## Official provider reference context

Official documentation supplies reference defaults and model capability
ceilings for omitted fields. It does not reconstruct the unarchived native
payload produced by the intermediary service. Capability ceilings must not be
reported as configured output limits. Provider pages were accessed on
2026-10-31.

| Model | Archived client/adapter configuration | Official direct-API reference | Interpretation boundary |
| --- | --- | --- | --- |
| Claude Sonnet 4.5 | `temperature=0.0`, `drop_params=true`; `top_p`, `top_k`, `max_tokens` aliases, `thinking`, and native `tools` unset. | [Messages API](https://platform.claude.com/docs/en/api/messages/create): `max_tokens` is required. [API reference](https://platform.claude.com/docs/en/api/beta/messages/create): temperature defaults to 1.0 only when omitted. [Release notes](https://platform.claude.com/docs/en/release-notes/overview): `top_p` default 0.99 from 2025-05-22. [Thinking defaults](https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting): thinking off when omitted. [Output limits](https://platform.claude.com/docs/en/build-with-claude/thinking): 64K model output ceiling. | The archived 0.0 request, rather than the temperature default, is the reproducible client setting. Any direct Anthropic Messages request would have required a `max_tokens` value, but the gateway-filled value was not archived; 64K is a capability ceiling, not the experimental request limit. |
| Gemini 3 Pro Preview | `temperature=0.0`, `drop_params=true`; `top_p`, `top_k`, `max_output_tokens`, `thinking_config`, `seed`, and native `tools` unset. | [Gemini 3 guide](https://ai.google.dev/gemini-api/docs/gemini-3): temperature default 1.0 and omitted thinking level defaults to high. [Generation API](https://ai.google.dev/api/generate-content): sampling/output defaults are model-dependent and an omitted seed is randomized. [Prompt guide](https://ai.google.dev/gemini-api/docs/prompting-strategies): general `topP` default 0.95. [Model page](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-preview): 65,536-token output ceiling. | If forwarded, the archived 0.0 request overrides the documented temperature default. High thinking is the documented omitted-field behavior, not a saved gateway setting. The exact historical `topP`, `topK`, and output-limit values were not archived; 65,536 is a ceiling. |
| GPT-5 (2025-08-07) | `temperature=0.0`, `drop_params=true`; medium reasoning requested in all 300 attempts (`reasoning` in 299, `reasoning_effort` in one); `top_p`, output limit, and native `tools` unset. | [GPT-5 guide](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5): reasoning effort defaults to medium. [Model page](https://developers.openai.com/api/docs/models/gpt-5): 128K model output ceiling. [Parameter compatibility](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.4): older GPT-5 models reject `temperature` and `top_p`. | Medium was the only model-specific decoding override added by the experimenter during the mini-SWE-agent 1.15.0 upgrade. Successful calls, `drop_params=true`, and the documented incompatibility are consistent with adapter removal of temperature; the native payload was not archived. The 128K ceiling is not a recovered request limit. |

[Output-limit diagnostics](output_limit_diagnostics.md) reports observed
length-stop responses and their saved completion counts. Those observations do
not recover the configured maximum-output value.

No native provider tools were configured. The common agent instead requested
one textual Bash block, parsed it locally, and executed commands serially.
