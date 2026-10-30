"""Generate publication tables and a concise report from canonical statistics.

The script reads CSV/JSON results produced by the audit and inferential scripts,
writes Markdown/LaTeX tables below ``result/Statistics results/tables``, and
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


def tex_escape(text):
    special = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$',
               '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}',
               '<': r'\textless{}', '>': r'\textgreater{}'}
    return ''.join(special.get(char, char) for char in str(text))


def table(directory, name, headers, rows):
    md = ['| '+' | '.join(headers)+' |', '| '+' | '.join('---' for _ in headers)+' |']
    md.extend('| '+' | '.join(map(str, row))+' |' for row in rows)
    directory.mkdir(parents=True, exist_ok=True)
    (directory/(name+'.md')).write_text('\n'.join(md)+'\n')
    latex = [r'\begin{tabular}{'+'l'*len(headers)+'}', r'\hline',
             ' & '.join(tex_escape(h) for h in headers)+r' \\', r'\hline']
    latex.extend(' & '.join(tex_escape(cell) for cell in row)+r' \\' for row in rows)
    latex.extend([r'\hline', r'\end{tabular}'])
    (directory/(name+'.tex')).write_text('\n'.join(latex)+'\n')
    return '\n'.join(md)


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
    settings_md = table(tables, 'settings', ['Saved setting', 'Claude', 'Gemini', 'GPT'], parameter_rows)
    accounting_rows = [
        ['Anthropic', 'Native input + cache read + cache creation', 'Native reported output', 'Cache counters are included in normalized input; output retains reported thinking.'],
        ['OpenAI-compatible', 'Reported prompt/input total', 'Reported completion/output total', 'Cached input and reported reasoning are subdivisions of the totals.'],
        ['Gemini', 'Native promptTokenCount', 'Candidates plus thoughts, unless candidates already include thoughts', 'The adapter avoids adding thinking twice; missing upstream details cannot be independently reconstructed.'],
    ]
    table(tables, 'token_accounting', ['Provider interface', 'Normalized input', 'Normalized completion', 'Inclusion rule'], accounting_rows)
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

Publication-ready settings and provider definitions are in `tables/settings` and `tables/token_accounting` (Markdown and LaTeX). Client-unset output limits and top-p are reported explicitly; an unrecorded effective value is not replaced by a current default. `tables/output_limit_diagnostics` reports observed length stops and their reported completion counts; these are observations, not reconstructed request limits.

{coverage_md}

Optional cache/thinking details are not uniformly complete. Missing values remain missing, and subdivisions are not added again to their totals. Exact formulas, the common tool protocol, prompt consistency and differing orchestration settings are specified in [METHODS.md]({methods_link}).
'''
    (out/'REPORT.md').write_text(report)
    print('Generated publication tables and REPORT.md.')


if __name__ == '__main__':
    main()
