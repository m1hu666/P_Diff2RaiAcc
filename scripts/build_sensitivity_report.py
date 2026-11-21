"""Render the two-cohort overview from generated CSVs; no fixed conclusions."""

import csv
import json

from analysis_layout import artifact, COHORTS


def read(path):
    with path.open() as stream:
        return list(csv.DictReader(stream))


def table(headers, rows):
    return '\n'.join(['| '+' | '.join(headers)+' |', '| '+' | '.join('---' for _ in headers)+' |',
                       *['| '+' | '.join(str(v).replace('|', '\\|') for v in row)+' |' for row in rows]])


def overview(out):
    design = json.loads((out/'sensitivity/analysis_design.json').read_text())
    shift = read(out/'sensitivity/django_taxonomy_shift.csv')
    short = {'claude-sonnet-4-5-20250929': 'Claude', 'gemini-3-pro-preview': 'Gemini',
             'gpt-5-2025-08-07-medium-reasoning': 'GPT'}
    lines = ['# Full-data and Django-exclusion analysis', '',
             'Start here for the reviewer-facing sensitivity comparison. See [methods](../../docs/METHODS.md) and the [file catalogue](README.md). All results describe the archived configurations; token counts are normalized reports and costs are framework estimates.', '',
             '## Cohort sizes', '',
             table(['Cohort', 'Tasks', 'Attempts', 'Failures', 'Repositories'],
                   [(c, *[design['cohorts'][c][k] for k in ('tasks', 'attempts', 'failures', 'repositories')]) for c in COHORTS]), '',
             'The exclusion cohort is nested in the full cohort. It is a sensitivity analysis, not an independent replication. The taxonomy and annotations are retained without relabeling.', '',
             '## Resources and outcomes', '']
    resource_rows = []
    for cohort in COHORTS:
        resources = read(artifact(out, 'summary_metrics.csv', cohort))
        outcomes = read(artifact(out, 'success_stability_summary.csv', cohort))
        for r in outcomes:
            metrics = {s['metric']: float(s['mean']) for s in resources
                       if s['model'] == r['model'] and s['group'] == 'all' and s['cohort'] == cohort}
            resource_rows.append([cohort, short[r['model']], f"{100*float(r['resolution_rate']):.2f}",
                                  f"{metrics['steps']:.2f}", f"{metrics['prompt_tokens']/1000:.2f}",
                                  f"{metrics['completion_tokens']/1000:.2f}", f"{metrics['recorded_cost_usd']:.3f}"])
    lines += [table(['Cohort', 'Model', 'Resolution (%)', 'Mean steps', 'Input (k)', 'Output (k)', 'Estimated USD'], resource_rows), '',
              'Per-cohort paired tests and confidence intervals are in [full](full/REPORT.md) and [without Django](without_django/REPORT.md). The [joint comparison table](sensitivity/model_comparisons_both_cohorts.csv) additionally applies Holm to all 30 resource/outcome tests across both cohorts. Within-cohort global adjustment covers 15 tests. These scopes must not be interchanged.', '',
              '## Influence on taxonomy', '']
    stage = [r for r in shift if r['level'] == 'stage']
    categories = [r for r in shift if r['level'] == 'primary_category']
    first = shift[0]
    n_django = int(float(first['django_failures']))
    n_all = int(float(first['full_failures']))
    lines += [f"Django contains half of the tasks and contributes {n_django}/{n_all} failures ({100*n_django/n_all:.2f}%). The table distinguishes its contribution to the failure pool from changes in category composition after exclusion.", '']
    for label, records in [('Broader stages', stage), ('Subcategories', categories)]:
        lines += [f'### {label}', '', table(['Category', 'Full n (%)', 'Without Django n (%)',
                                           'Change (pp), 95% CI', 'Django share of category (%)', 'Rank full -> excluded'],
                  [(r['category'], f"{int(float(r['full_count']))} ({float(r['full_share_percent']):.2f})",
                    f"{int(float(r['without_django_count']))} ({float(r['without_django_share_percent']):.2f})",
                    f"{float(r['change_without_minus_full_pp']):+.2f} [{float(r['change_ci95_lower_pp']):+.2f}, {float(r['change_ci95_upper_pp']):+.2f}]",
                    f"{float(r['django_share_of_category_percent']):.2f}" if r['django_share_of_category_percent'] else 'undefined',
                    r['full_rank']+' -> '+r['without_django_rank']) for r in records]), '']
    largest = max(categories, key=lambda r: abs(float(r['change_without_minus_full_pp'])))
    top_full = next(r['category'] for r in stage if r['full_rank'] == '1')
    top_excluded = next(r['category'] for r in stage if r['without_django_rank'] == '1')
    lines += [f"The largest observed subcategory shift is {largest['category']}: {float(largest['change_without_minus_full_pp']):+.2f} percentage points after removing Django. The leading broader stage is {top_full} in the full cohort and {top_excluded} after exclusion. These observed compositions and rankings are sample-dependent and should not be presented as repository-invariant failure distributions.", '',
              'The [composition-change intervals](sensitivity/django_taxonomy_shift.csv) use a joint task bootstrap stratified by Django status. The same non-Django draws enter both estimates, preserving overlap. They are pointwise descriptive intervals, not a battery of independent full-versus-excluded tests.', '',
              f'Failure [incidence tests](full/failures/category_inference.csv) compare model category counts per all attempts using exact task-block swaps. There are {len(read(artifact(out, "category_inference.csv", "full")))} tests per cohort, corrected within cohort and jointly across all {sum(len(read(artifact(out, "category_inference.csv", c))) for c in COHORTS)} taxonomy tests. Taxonomy findings remain exploratory and separate from the resource/outcome family. V5 counts evaluation-infrastructure blockers, not model repair defects. [Category intervals](full/failures/category_uncertainty.csv) distinguish incidence from composition; zero-event intervals do not bound unseen categories.', '',
              '## Repository and difficulty sensitivity', '',
              'Both cohorts contain `stratified/` results by repository and archived difficulty, including task counts, mean resources, outcome rates, failure incidence/composition, and paired estimation intervals. Strata with one task have no confidence interval. Difficulty is the dataset human-fix-time category, not inferred from model outcomes.', '',
              'Each `repository_sensitivity/` directory contains whole-repository bootstrap intervals, repository-equal summaries, and leave-one-repository-out estimates. Repository resampling retains all tasks, models, and trials and preserves the task-weighted estimand through ratios of sums. Only 11/10 unequal repositories are available, so these intervals are exploratory and have no repository-level significance tests. Repository-equal results deliberately change the weighting and report how many repository-specific failure compositions are defined.', '',
              '## Optional usage details', '',
              'Prompt/completion totals are complete. Some optional detail objects are null or contain null/absent fields in the saved responses themselves. [Raw-shape audit](accounting/MISSINGNESS.md) supplies counts and exact examples. The archive cannot establish whether provider reporting, intermediary conversion, or serialization caused each unavailable value; unavailable values are not zero.', '']
    (out/'REPORT.md').write_text('\n'.join(lines))
