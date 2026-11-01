"""Generate Markdown tables and a concise report from canonical statistics.

The script reads CSV/JSON results produced by the audit and inferential scripts,
writes Markdown tables below ``result/Statistics results/tables``, and
writes ``REPORT.md`` beside the statistical data. It does not inspect raw
trajectories or modify experimental inputs.
"""

import argparse
import csv
import json
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
DEFAULT_OUTPUT = ROOT / 'result' / 'Statistics results'
DEFAULT_METHODS = ROOT / 'docs' / 'METHODS.md'
MODELS = ['claude-sonnet-4-5-20250929', 'gemini-3-pro-preview',
          'gpt-5-2025-08-07-medium-reasoning']
SHORT = dict(zip(MODELS, ['Claude', 'Gemini', 'GPT']))


def read_csv(directory, name):
    with (directory/name).open() as stream:
        return list(csv.DictReader(stream))


def number(value, scale=1, places=2):
    return f'{float(value)/scale:.{places}f}'


def ci(low, high, scale=1, places=2):
    return f'[{number(low, scale, places)}, {number(high, scale, places)}]'


def probability(value):
    return '<0.001' if float(value) < .001 else f'{float(value):.3f}'


def markdown_table(headers, rows):
    md = ['| '+' | '.join(headers)+' |', '| '+' | '.join('---' for _ in headers)+' |']
    md.extend('| '+' | '.join(map(str, row))+' |' for row in rows)
    return '\n'.join(md)


def table(directory, name, headers, rows):
    md = markdown_table(headers, rows)
    directory.mkdir(parents=True, exist_ok=True)
    (directory/(name+'.md')).write_text(md+'\n')
    return md


def displayed_setting(settings, model, parameter):
    selected = [r for r in settings if r['model']==model and r['parameter']==parameter]
    parts = []
    for row in selected:
        if row['status']=='unset':
            value = 'Unset'
        else:
            decoded = json.loads(row['value'])
            if isinstance(decoded, bool):
                value = str(decoded).lower()
            elif decoded is None:
                value = 'None'
            elif isinstance(decoded, str):
                value = decoded.replace('minisweagent.run.extra.swebench.ProgressTrackingAgent', 'Batch')
                value = value.replace('minisweagent.agents.interactive.InteractiveAgent', 'Interactive/yolo')
            else:
                value = row['value']
        parts.append(value+(f" ({row['n_attempts']})" if len(selected)>1 else ''))
    return '; '.join(parts) if parts else 'Not recorded'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--methods', type=Path, default=DEFAULT_METHODS)
    args = parser.parse_args()
    out, tables = args.output, args.output/'tables'
    methods_link = Path(os.path.relpath(args.methods.resolve(), out.resolve())).as_posix().replace(' ', '%20')
    audit = json.loads((out/'audit.json').read_text())
    design = json.loads((out/'analysis_design.json').read_text())
    summaries = read_csv(out, 'summary_metrics.csv')
    resources = read_csv(out, 'resource_comparisons.csv')
    success = read_csv(out, 'success_comparisons.csv')
    stability = read_csv(out, 'stability_comparisons.csv')
    costs = read_csv(out, 'estimated_cost_comparisons.csv')
    outcomes = read_csv(out, 'success_stability_summary.csv')
    settings = read_csv(out, 'settings.csv')
    coverage = read_csv(out, 'usage_field_coverage.csv')

    resource_rows = []
    for model in MODELS:
        for group in ['success', 'failure']:
            values = {r['metric']:r for r in summaries if r['model']==model and r['group']==group and r['cohort']=='all_archived_900'}
            steps = values['steps']
            resource_rows.append([SHORT[model], group, steps['attempts'], number(steps['mean']),
                                  number(steps['median'])+' '+ci(steps['q25'], steps['q75']),
                                  number(values['prompt_tokens']['mean'], 1000),
                                  number(values['completion_tokens']['mean'], 1000),
                                  number(values['recorded_cost_usd']['mean'], places=3)])
    resource_md = table(tables, 'resource_usage',
                        ['Model', 'Outcome', 'n', 'Mean steps', 'Median steps [Q1, Q3]',
                         'Mean input (k)', 'Mean output (k)', 'Estimated USD'], resource_rows)
    inference_rows = []
    for row in resources:
        metric = row['metric']
        scale = 1000 if metric.endswith('_tokens') else 1
        label = {'steps':'Steps', 'prompt_tokens':'Input (k)', 'completion_tokens':'Output (k)'}[metric]
        inference_rows.append([SHORT[row['left_model']]+' - '+SHORT[row['right_model']], label,
                               number(row['mean_difference'], scale)+' '+ci(row['difference_ci95_lower'], row['difference_ci95_upper'], scale),
                               number(row['ratio_of_means'])+' '+ci(row['ratio_ci95_lower'], row['ratio_ci95_upper']),
                               probability(row['p_value_holm']), probability(row['p_value_holm_global'])])
    resource_inference = table(tables, 'resource_inference',
                               ['Comparison', 'Metric', 'Difference [95% CI]', 'Ratio [95% CI]', 'Family Holm p', 'Global Holm p'], inference_rows)
    outcome_rows = [[SHORT[r['model']], r['resolved_attempts']+'/'+r['attempts'], number(float(r['resolution_rate'])*100),
                     r['tasks_with_0_successes'], r['tasks_with_1_successes'], r['tasks_with_2_successes'],
                     r['tasks_with_3_successes'], r['unstable_tasks']] for r in outcomes]
    outcome_md = table(tables, 'success_stability',
                       ['Model', 'Resolved attempts', 'Resolution (%)', '0/3 tasks', '1/3 tasks', '2/3 tasks', '3/3 tasks', 'Unstable tasks'], outcome_rows)
    for name, data in [('success_inference', success), ('stability_inference', stability)]:
        rows = [[SHORT[r['left_model']]+' - '+SHORT[r['right_model']],
                 number(r['difference_percentage_points'])+' '+ci(r['difference_ci95_lower_pp'], r['difference_ci95_upper_pp']),
                 probability(r['p_value_holm']), probability(r['p_value_holm_global'])] for r in data]
        result = table(tables, name, ['Comparison', 'Difference in pp [95% CI]', 'Family Holm p', 'Global Holm p'], rows)
        if name=='success_inference':
            success_md = result
        else:
            stability_md = result
    table(tables, 'estimated_cost', ['Comparison', 'USD difference [95% CI]', 'Ratio [95% CI]'],
          [[SHORT[r['left_model']]+' - '+SHORT[r['right_model']],
            number(r['mean_difference'], places=3)+' '+ci(r['difference_ci95_lower'], r['difference_ci95_upper'], places=3),
            number(r['ratio_of_means'])+' '+ci(r['ratio_ci95_lower'], r['ratio_ci95_upper'])] for r in costs])

    parameter_rows = []
    for parameter in ['temperature', 'drop_params', 'reasoning', 'reasoning_effort', 'thinking', 'thinking_config',
                      'top_p', 'top_k', 'max_tokens', 'max_completion_tokens', 'max_output_tokens',
                      'seed', 'stop', 'frequency_penalty', 'presence_penalty', 'verbosity', 'response_format', 'n',
                      'stream', 'tools', 'tool_choice', 'parallel_tool_calls', 'cache_control',
                      'step_limit', 'cost_limit_usd', 'shell_timeout_seconds', 'agent_wrapper', 'framework_version']:
        parameter_rows.append([parameter]+[displayed_setting(settings, model, parameter) for model in MODELS])
    archived_settings_md = markdown_table(['Saved setting', 'Claude', 'Gemini', 'GPT'], parameter_rows)
    provider_rows = [
        [
            'Claude Sonnet 4.5',
            '`temperature=0.0`, `drop_params=true`; `top_p`, `top_k`, '
            '`max_tokens` aliases, `thinking`, and native `tools` unset.',
            '[Messages API](https://platform.claude.com/docs/en/api/messages/create): '
            '`max_tokens` is required. [API reference](https://platform.claude.com/docs/en/api/beta/messages/create): '
            'temperature defaults to 1.0 only when omitted. '
            '[Release notes](https://platform.claude.com/docs/en/release-notes/overview): '
            '`top_p` default 0.99 from 2025-05-22. '
            '[Thinking defaults](https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting): '
            'thinking off when omitted. '
            '[Output limits](https://platform.claude.com/docs/en/build-with-claude/thinking): '
            '64K model output ceiling.',
            'The archived 0.0 request, rather than the temperature default, is the reproducible client setting. '
            'Any direct Anthropic Messages request would have required a `max_tokens` value, but the '
            'gateway-filled value was not archived; '
            '64K is a capability ceiling, not the experimental request limit.',
        ],
        [
            'Gemini 3 Pro Preview',
            '`temperature=0.0`, `drop_params=true`; `top_p`, `top_k`, '
            '`max_output_tokens`, `thinking_config`, `seed`, and native `tools` unset.',
            '[Gemini 3 guide](https://ai.google.dev/gemini-api/docs/gemini-3): '
            'temperature default 1.0 and omitted thinking level defaults to high. '
            '[Generation API](https://ai.google.dev/api/generate-content): '
            'sampling/output defaults are model-dependent and an omitted seed is randomized. '
            '[Prompt guide](https://ai.google.dev/gemini-api/docs/prompting-strategies): '
            'general `topP` default 0.95. '
            '[Model page](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-preview): '
            '65,536-token output ceiling.',
            'If forwarded, the archived 0.0 request overrides the documented temperature default. '
            'High thinking is the documented omitted-field behavior, not a saved gateway setting. '
            'The exact historical `topP`, `topK`, and output-limit values were not archived; 65,536 is a ceiling.',
        ],
        [
            'GPT-5 (2025-08-07)',
            '`temperature=0.0`, `drop_params=true`; medium reasoning requested in all 300 attempts '
            '(`reasoning` in 299, `reasoning_effort` in one); `top_p`, output limit, and native `tools` unset.',
            '[GPT-5 guide](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5): '
            'reasoning effort defaults to medium. '
            '[Model page](https://developers.openai.com/api/docs/models/gpt-5): '
            '128K model output ceiling. '
            '[Parameter compatibility](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.4): '
            'older GPT-5 models reject `temperature` and `top_p`.',
            'Medium was the only model-specific decoding override added by the experimenter during the '
            'mini-SWE-agent 1.15.0 upgrade. Successful calls, `drop_params=true`, and the documented '
            'incompatibility are consistent with adapter removal of temperature; the native payload was not archived. '
            'The 128K ceiling is not a recovered request limit.',
        ],
    ]
    provider_md = markdown_table(
        ['Model', 'Archived client/adapter configuration', 'Official direct-API reference', 'Interpretation boundary'],
        provider_rows,
    )
    settings_document = f'''# Experimental settings

The first table is generated from the 900 archived trajectories. `Unset` means
the field was absent from the saved client arguments; it does not by itself
identify the value ultimately sent by an adapter or gateway. All trajectories
record mini-SWE-agent 1.15.0. During that upgrade, the experimenter added only
one model-specific decoding override: medium reasoning for GPT. The serialized
`temperature=0.0` and `drop_params=true` values otherwise came from the common
framework/client configuration.

## Archived client and agent configuration

{archived_settings_md}

## Official provider reference context

Official documentation supplies reference defaults and model capability
ceilings for omitted fields. It does not reconstruct the unarchived native
payload produced by the intermediary service. Capability ceilings must not be
reported as configured output limits. Provider pages were accessed on
2026-10-31.

{provider_md}

[Output-limit diagnostics](output_limit_diagnostics.md) reports observed
length-stop responses and their saved completion counts. Those observations do
not recover the configured maximum-output value.

No native provider tools were configured. The common agent instead requested
one textual Bash block, parsed it locally, and executed commands serially.
'''
    tables.mkdir(parents=True, exist_ok=True)
    (tables/'settings.md').write_text(settings_document)
    accounting_rows = [
        ['Anthropic route', 'Saved usage.prompt_tokens', 'Saved usage.completion_tokens', 'Cache-read and cache-creation counters when reported.'],
        ['OpenAI-compatible route', 'Saved usage.prompt_tokens', 'Saved usage.completion_tokens', 'Cached-input and reasoning counters when reported.'],
        ['Gemini route', 'Saved usage.prompt_tokens', 'Saved usage.completion_tokens', 'Cached, text and reasoning counters when reported.'],
    ]
    table(tables, 'token_accounting', ['Routed interface', 'Analyzed input', 'Analyzed completion', 'Available subdivisions'], accounting_rows)
    coverage_rows = []
    for model in MODELS:
        for field in ['prompt_tokens', 'completion_tokens', 'prompt_tokens_details.cached_tokens',
                      'cache_creation_input_tokens', 'completion_tokens_details.reasoning_tokens']:
            row = next(r for r in coverage if r['model']==model and r['field']==field)
            coverage_rows.append([SHORT[model], field, row['numeric']+'/'+row['responses'],
                                  number(100*int(row['numeric'])/int(row['responses'])), row['null'], row['missing']])
    coverage_md = table(tables, 'accounting_coverage',
                        ['Model', 'Field', 'Numeric/total', 'Coverage (%)', 'Null', 'Missing'], coverage_rows)
    limit_rows = []
    for model in MODELS:
        responses = next(int(r['responses']) for r in coverage if r['model']==model)
        observed_counts = audit['length_completion_counts'][model]
        stopped = sum(observed_counts.values())
        observations = '; '.join(f'{tokens} ({count})' for tokens, count in observed_counts.items()) or 'None'
        limit_rows.append([SHORT[model], str(stopped)+'/'+str(responses), number(100*stopped/responses), observations])
    table(tables, 'output_limit_diagnostics',
          ['Model', 'Length-stop responses/total', 'Percent', 'Reported completion count (frequency)'], limit_rows)

    report = f'''# Analysis results

Analysis set: {audit['tasks']} tasks x 3 models x 3 trials = {audit['observed_attempts']} attempts. Inference uses {design['n_tasks']} paired task clusters; all {audit['recorded_responses']:,} saved responses have input and completion counts. Full methods are in [METHODS.md]({methods_link}).

## Resource use

{resource_md}

k = 1,000 reported tokens. Outcome-specific rows are descriptive because the successful/failed task sets differ across models. Model inference below uses the same complete set of 100 tasks.

{resource_inference}

Differences are left minus right; ratios are left divided by right. Intervals are pointwise task-bootstrap estimates. Holm correction covers the nine resource tests. Step and reported-input differences are supported; completion-count differences are not statistically established. This is not evidence of equivalent completion usage or matched internal reasoning computation.

## Resolution and execution consistency

{outcome_md}

{success_md}

Resolution: the Claude-GPT difference passes correction within the three resolution comparisons, but does not pass the conservative global correction across all 15 tests. Treat this finding as exploratory rather than robust across endpoints.

{stability_md}

Instability means one or two successes out of three trials. The counts are 15/7/14 for Claude/Gemini/GPT. Gemini is numerically more consistent, but no paired stability comparison is significant after correction; consistently failed tasks also count as consistent.

## Settings and accounting

Archived settings, configuration provenance, and linked official provider references are in `tables/settings.md`; token-field definitions are in `tables/token_accounting.md`. Official defaults are used only to interpret omitted fields and are kept separate from saved client arguments and model capability ceilings. An unrecorded gateway-effective value is not reconstructed from current documentation. `tables/output_limit_diagnostics.md` reports observed length stops and their reported completion counts; these are observations, not configured request limits.

{coverage_md}

Optional cache/thinking details are not uniformly complete. Missing values remain missing, and subdivisions are not added again to their totals. Exact formulas, the common tool protocol, prompt consistency and differing orchestration settings are specified in [METHODS.md]({methods_link}).
'''
    (out/'REPORT.md').write_text(report)
    print('Generated Markdown tables and REPORT.md.')


if __name__ == '__main__':
    main()
