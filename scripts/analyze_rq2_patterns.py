"""Analyze observed three-trial failure persistence and resource use for RQ2.

Inputs: the shared per_attempt.csv and canonical failure_annotations.csv.
Outputs: descriptive CSVs, exploratory task-bootstrap intervals and a report in
result/Statistics results/full/rq2/. Does not alter input data or figures.
Run: python3 scripts/analyze_rq2_patterns.py
"""

import argparse
import csv
import hashlib
import itertools
import json
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean

from inferential_analysis import interval

ROOT = Path(__file__).resolve().parents[1]
STATS = ROOT / 'result' / 'Statistics results'
MODELS = {
    'claude-sonnet-4-5-20250929': 'Claude',
    'gemini-3-pro-preview': 'Gemini',
    'gpt-5-2025-08-07-medium-reasoning': 'GPT',
}


def read_csv(path):
    with path.open(newline='', encoding='utf-8') as stream:
        return list(csv.DictReader(stream))


def write_csv(path, rows):
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def percent(a, b):
    return 100 * a / b if b else None


def bootstrap_totals(vectors, repetitions, seed):
    rng = random.Random(seed)
    for _ in range(repetitions):
        yield [sum(column) for column in zip(*rng.choices(vectors, k=len(vectors)))]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=STATS / 'full' / 'rq2')
    parser.add_argument('--bootstrap-repetitions', type=int, default=10000)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()
    if args.bootstrap_repetitions < 1:
        parser.error('Bootstrap repetitions must be positive')
    args.output.mkdir(parents=True, exist_ok=True)
    inputs = [STATS / 'data' / 'per_attempt.csv',
              ROOT / 'FINAL-CODEBOOK' / 'failure_annotations.csv']
    attempts = read_csv(inputs[0])
    annotations = {(r['task_id'], r['model'], int(r['trial'])): r['primary_category']
                   for r in read_csv(inputs[1])}
    grouped = defaultdict(list)
    for row in attempts:
        row['trial'] = int(row['round'].removeprefix('round'))
        row['success'] = {'True': True, 'False': False}[row['label']]
        row['cost'] = float(row['recorded_cost_usd'])
        for field in ['steps', 'prompt_tokens', 'completion_tokens']:
            row[field] = int(row[field])
        grouped[(row['task'], row['model'])].append(row)
    tasks = sorted({row['task'] for row in attempts})
    assert len(attempts) == 900 and len(tasks) == 100
    assert set(grouped) == set(itertools.product(tasks, MODELS))
    for rows in grouped.values():
        assert sorted(r['trial'] for r in rows) == [1, 2, 3]
    failed_keys = {(r['task'], r['model'], r['trial']) for r in attempts if not r['success']}
    assert failed_keys == set(annotations)
    infrastructure_tasks = {t for (t, m, r), category in annotations.items() if category == 'V5'}
    patterns = []
    stats = {}
    for (task, model), rows in sorted(grouped.items()):
        rows.sort(key=lambda r: r['trial'])
        successes = sum(r['success'] for r in rows)
        failures = [r for r in rows if not r['success']]
        categories = [annotations.get((task, model, r['trial']), '-') for r in rows]
        persistent = successes == 0
        same_category = persistent and len(set(categories)) == 1
        record = {
            'task': task, 'repository': rows[0]['repository'], 'model': MODELS[model],
            'successes': successes, 'outcomes': ' '.join('S' if r['success'] else 'F' for r in rows),
            'failure_categories': ' '.join(categories),
            'persistent_failure': persistent, 'same_primary_category_all_three_failures': same_category,
            'mean_steps': mean(r['steps'] for r in rows),
            'mean_estimated_usd': mean(r['cost'] for r in rows),
        }
        patterns.append(record)
        # Seven sufficient statistics per model/task, retaining all three trials.
        stats[(task, model)] = [len(failures), 3 * int(persistent),
                               sum(r['cost'] for r in rows), sum(r['cost'] for r in failures),
                               sum(r['cost'] for r in failures) if persistent else 0,
                               int(persistent), int(same_category)]
    write_csv(args.output / 'task_model_patterns.csv', patterns)

    def measures(v, n_tasks, n_models=1):
        fail, persistent_fail, cost, fail_cost, persistent_cost, persistent_tasks, same = v
        return {
            'persistent_share_of_failed_trials_percent': percent(persistent_fail, fail),
            'same_category_share_of_persistent_groups_percent': percent(same, persistent_tasks),
            'failure_rate_percent': percent(fail, 3 * n_tasks * n_models),
            'failure_share_of_estimated_budget_percent': percent(fail_cost, cost),
            'failure_budget_share_minus_failure_rate_pp':
                percent(fail_cost, cost) - percent(fail, 3 * n_tasks * n_models),
            'persistent_share_of_failure_budget_percent': percent(persistent_cost, fail_cost),
        }

    # All models use the same complete-task draws. The pooled estimates also
    # retain the three-model dependence within each sampled task.
    vectors = []
    groups = list(MODELS) + ['All']
    for task in tasks:
        values = [stats[(task, m)] for m in MODELS]
        vectors.append([x for v in values + [[sum(c) for c in zip(*values)]] for x in v])
    draws = defaultdict(list)
    for totals in bootstrap_totals(vectors, args.bootstrap_repetitions, args.seed):
        for index, model in enumerate(groups):
            for metric, value in measures(totals[index * 7:(index + 1) * 7], len(tasks),
                                          3 if model == 'All' else 1).items():
                if value is not None:
                    draws[(model, metric)].append(value)
    persistence, budgets = [], []
    cohorts = {'full': tasks,
               'without_django': [t for t in tasks if not t.startswith('django__')],
               'without_infrastructure_task': [t for t in tasks if t not in infrastructure_tasks]}
    for cohort, selected in cohorts.items():
        for model in groups:
            members = list(MODELS) if model == 'All' else [model]
            records = [r for r in patterns if r['task'] in selected and r['model'] in
                       [MODELS[m] for m in members]]
            total = [sum(c) for c in zip(*(stats[(t, m)] for t in selected for m in members))]
            metrics = measures(total, len(selected), len(members))
            base = {'cohort': cohort, 'model': MODELS.get(model, model), 'n_tasks': len(selected)}
            rec = base | {'task_model_groups': len(records),
                          'all_success_groups': sum(r['successes'] == 3 for r in records),
                          'mixed_outcome_groups': sum(r['successes'] in (1, 2) for r in records),
                          'all_failure_groups': int(total[5]), 'failed_trials': int(total[0]),
                          'persistent_failed_trials': int(total[1]),
                          'same_primary_category_groups': int(total[6])}
            budget = base | {'attempts': 3 * len(records), 'failed_trials': int(total[0]),
                             'estimated_total_usd': total[2], 'estimated_failure_usd': total[3]}
            for metric, value in metrics.items():
                destination = rec if metric.startswith(('persistent_share_of_failed', 'same_category')) else budget
                destination[metric] = value
                samples = draws[(model, metric)] if cohort == 'full' else []
                lo, hi = interval(samples)
                destination[metric + '_ci95_lower'] = lo
                destination[metric + '_ci95_upper'] = hi
                destination[metric + '_valid_draws'] = len(samples)
            persistence.append(rec)
            budgets.append(budget)
    write_csv(args.output / 'failure_persistence.csv', persistence)
    write_csv(args.output / 'failure_budget_shares.csv', budgets)

    common = [t for t in tasks if all(r['success'] for m in MODELS for r in grouped[(t, m)])]
    common_summary = []
    for cohort, selected in [('full', common),
                             ('without_django', [t for t in common if not t.startswith('django__')])]:
        for model in MODELS:
            rows = [r for t in selected for r in grouped[(t, model)]]
            common_summary.append({'cohort': cohort, 'model': MODELS[model], 'n_tasks': len(selected),
                                   'attempts': len(rows), 'mean_steps': mean(r['steps'] for r in rows),
                                   'mean_estimated_usd': mean(r['cost'] for r in rows)})
    write_csv(args.output / 'common_success_summary.csv', common_summary)
    common_vectors = [[mean(r[f] for r in grouped[(t, m)]) for m in MODELS for f in ['steps', 'cost']]
                      for t in common]
    common_draws = defaultdict(list)
    pairs = [(0, 2), (1, 2)]
    for totals in bootstrap_totals(common_vectors, args.bootstrap_repetitions, args.seed):
        means = [x / len(common) for x in totals]
        for left, right in pairs:
            for offset, metric in enumerate(['steps', 'estimated_usd']):
                a, b = means[2 * left + offset], means[2 * right + offset]
                common_draws[(left, right, metric, 'difference')].append(a - b)
                common_draws[(left, right, metric, 'ratio')].append(a / b)
    comparison_rows = []
    observed = [mean(v[i] for v in common_vectors) for i in range(6)]
    names = list(MODELS.values())
    for left, right in pairs:
        for offset, metric in enumerate(['steps', 'estimated_usd']):
            a, b = observed[2 * left + offset], observed[2 * right + offset]
            rec = {'left_model': names[left], 'right_model': names[right], 'metric': metric,
                   'n_tasks': len(common), 'left_mean': a, 'right_mean': b,
                   'mean_difference': a - b, 'ratio_of_means': a / b}
            for effect in ['difference', 'ratio']:
                lo, hi = interval(common_draws[(left, right, metric, effect)])
                rec[effect + '_ci95_lower'], rec[effect + '_ci95_upper'] = lo, hi
            comparison_rows.append(rec)
    write_csv(args.output / 'common_success_comparisons.csv', comparison_rows)

    mixed_rows = []
    for model in MODELS:
        mixed = [t for t in tasks if 0 < sum(r['success'] for r in grouped[(t, model)]) < 3]
        vectors = [[mean(r[f] for r in grouped[(t, model)] if not r['success']) -
                    mean(r[f] for r in grouped[(t, model)] if r['success']) for f in ['steps', 'cost']]
                   for t in mixed]
        samples = list(bootstrap_totals(vectors, args.bootstrap_repetitions, args.seed))
        for index, metric in enumerate(['steps', 'estimated_usd']):
            lo, hi = interval([v[index] / len(mixed) for v in samples])
            mixed_rows.append({'model': MODELS[model], 'metric': metric, 'n_tasks': len(mixed),
                               'mean_failure_minus_success': mean(v[index] for v in vectors),
                               'ci95_lower': lo, 'ci95_upper': hi,
                               'tasks_with_positive_difference': sum(v[index] > 0 for v in vectors)})
    write_csv(args.output / 'within_task_outcome_differences.csv', mixed_rows)
    design = {
        'rq2': 'What behavioral patterns do LLMs exhibit during failures, and how do execution stability and trajectory efficiency reflect their reasoning capabilities?',
        'input_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
        'seed': args.seed, 'bootstrap_repetitions': args.bootstrap_repetitions,
        'persistence_and_budget_bootstrap': 'Whole tasks, retaining all models and all three trials; ratios recomputed in each draw.',
        'common_success_bootstrap': 'Paired complete-task bootstrap conditional on the 55 observed tasks solved by every model in all three trials.',
        'mixed_outcome_bootstrap': 'Resample the observed mixed-outcome tasks within each model, retaining all three trials; different selected task sets per model.',
        'intervals': 'Pointwise 95% percentile exploratory intervals, not simultaneous or confirmatory tests.',
        'additional_hypothesis_tests': False,
        'infrastructure_sensitivity_excludes': sorted(infrastructure_tasks),
        'interpretation': [
            'Persistence describes three observed failures, not a zero underlying success probability.',
            'Repeated primary categories do not establish identical reasoning paths or within-trajectory redundant loops.',
            'Common-success comparisons condition on an observed selected subset and retain route/setting differences.',
            'Mixed-outcome differences are descriptive selected-subset comparisons, not causal effects of failure.',
            'Costs are framework estimates. A failure-associated budget is not a counterfactually avoidable waste estimate.',
            'Task bootstrap conditions on the observed repository mix; only 11 repositories are represented.',
        ],
    }
    (args.output / 'analysis_design.json').write_text(json.dumps(design, indent=2) + '\n')
    full_persistence = {r['model']: r for r in persistence if r['cohort'] == 'full'}
    full_budgets = {r['model']: r for r in budgets if r['cohort'] == 'full'}
    pooled = full_persistence['All']
    report = [
        '# RQ2: failure persistence, repeatability and interaction economy', '',
        '> ' + design['rq2'], '',
        'All results describe the archived configurations. The two existing resource PDFs are unchanged.', '',
        '## Main finding 1: consistency can conceal persistent failure', '',
        f"Of {pooled['failed_trials']} observed failed attempts, {pooled['persistent_failed_trials']} "
        f"({pooled['persistent_share_of_failed_trials_percent']:.2f}%; task-bootstrap 95% CI "
        f"{pooled['persistent_share_of_failed_trials_percent_ci95_lower']:.2f}--"
        f"{pooled['persistent_share_of_failed_trials_percent_ci95_upper']:.2f}%) belong to model--task groups "
        'that failed in all three observed trials. These are repeatable unresolved outcomes, '
        'not estimates of a zero underlying success probability.', '',
        f"Among {pooled['all_failure_groups']} such model--task groups, "
        f"{pooled['same_primary_category_groups']} ({pooled['same_category_share_of_persistent_groups_percent']:.2f}%) "
        'retain the same primary failure category in all three trials. Category recurrence '
        'does not establish identical reasoning traces or redundant within-trajectory loops.', '',
        '| Model | 3/3 successes | Mixed outcomes | 0/3 successes | Observed consistency (%) | Persistent / all failed trials |',
        '| --- | ---: | ---: | ---: | ---: | ---: |',
    ]
    for model in MODELS.values():
        r = full_persistence[model]
        consistency = percent(r['all_success_groups'] + r['all_failure_groups'], r['task_model_groups'])
        report.append(f"| {model} | {r['all_success_groups']} | {r['mixed_outcome_groups']} | "
                      f"{r['all_failure_groups']} | {consistency:.2f} | "
                      f"{r['persistent_failed_trials']}/{r['failed_trials']} |")
    report += [
        '', 'Gemini and Claude both have 69 tasks with three successful trials. Gemini\'s '
        'eight-point higher observed consistency consists entirely of its eight additional '
        '0/3-success tasks. Existing [paired instability tests](../outcomes/stability_comparisons.csv) '
        'do not support an adjusted significant difference between models.', '',
        '| Sensitivity cohort | Persistent / all failed trials | Share (%) | Same-category / persistent groups |',
        '| --- | ---: | ---: | ---: |',
    ]
    for r in persistence:
        if r['model'] == 'All':
            report.append(f"| {r['cohort']} | {r['persistent_failed_trials']}/{r['failed_trials']} | "
                          f"{r['persistent_share_of_failed_trials_percent']:.2f} | "
                          f"{r['same_primary_category_groups']}/{r['all_failure_groups']} |")
    report += [
        '', 'The V5 sensitivity removes all infrastructure-blocked tasks, including '
        'all their models and trials. This is distinct from attributing an evaluation blocker to model reasoning.', '',
        '## Main finding 2: compact successful execution persists on the same solved tasks', '',
        f'The common-success subset contains {len(common)} tasks for which all nine model/trial '
        'attempts succeed. It compares the same task set and the same observed resolution outcome, '
        'rather than each model\'s different success set.', '',
        '| Cohort | Model | Tasks | Attempts | Mean steps | Mean estimated USD |',
        '| --- | --- | ---: | ---: | ---: | ---: |',
    ]
    for r in common_summary:
        report.append(f"| {r['cohort']} | {r['model']} | {r['n_tasks']} | {r['attempts']} | "
                      f"{r['mean_steps']:.2f} | {r['mean_estimated_usd']:.3f} |")
    report += [
        '', 'GPT\'s lower interaction overhead is therefore also observed in successfully solved common cases. '
        'This selected subset does not establish overall superiority or matched intrinsic reasoning computation. '
        'Provider routes, decoding and orchestration settings remain those of the archive. '
        'In the full cohort, GPT has 62 tasks with three successful trials, versus 69 for each other model.', '',
        '| Comparison | Metric | Mean difference [pointwise 95% CI] | Ratio [pointwise 95% CI] |',
        '| --- | --- | ---: | ---: |',
    ]
    for r in comparison_rows:
        digits = 3 if r['metric'] == 'estimated_usd' else 2
        report.append(f"| {r['left_model']} - {r['right_model']} | {r['metric']} | "
                      f"{r['mean_difference']:.{digits}f} "
                      f"[{r['difference_ci95_lower']:.{digits}f}, {r['difference_ci95_upper']:.{digits}f}] | "
                      f"{r['ratio_of_means']:.2f} [{r['ratio_ci95_lower']:.2f}, {r['ratio_ci95_upper']:.2f}] |")
    report += [
        '', 'These exploratory intervals condition on the observed common-success subset; '
        'no new hypothesis tests are run. The existing [all-task interaction-step tests](../resources/resource_comparisons.csv) '
        'are separate and must not be presented as tests of this subset or of outcome-specific plotted cells.', '',
        '## Supporting cost finding: unresolved attempts absorb disproportionate estimated spending', '',
        '| Model | Failure rate (%) | Failure budget share (%) [95% CI] | Estimated USD spent on failed attempts |',
        '| --- | ---: | ---: | ---: |',
    ]
    for model in MODELS.values():
        r = full_budgets[model]
        report.append(f"| {model} | {r['failure_rate_percent']:.2f} | "
                      f"{r['failure_share_of_estimated_budget_percent']:.2f} "
                      f"[{r['failure_share_of_estimated_budget_percent_ci95_lower']:.2f}, "
                      f"{r['failure_share_of_estimated_budget_percent_ci95_upper']:.2f}] | "
                      f"{r['estimated_failure_usd']:.2f} |")
    report += [
        '', 'Failure budget share is the sum of recorded costs of failed attempts divided by '
        'the recorded cost of all attempts. GPT has the highest share but the lowest absolute '
        'estimated failure spending. These costs are framework estimates, not invoices; '
        'the share is not an estimate of avoidable waste or savings from early stopping.', '',
        '## Boundary: aggregate failure premiums do not establish reasoning inertia', '',
        'Restricting each model to tasks with both successful and failed trials allows a '
        'within-task outcome contrast. Average failure-minus-success differences are:', '',
        '| Model | Mixed-outcome tasks | Step difference [95% CI] | USD difference [95% CI] |',
        '| --- | ---: | ---: | ---: |',
    ]
    for model in MODELS.values():
        s, c = [next(r for r in mixed_rows if r['model'] == model and r['metric'] == metric)
                for metric in ['steps', 'estimated_usd']]
        report.append(f"| {model} | {s['n_tasks']} | {s['mean_failure_minus_success']:+.2f} "
                      f"[{s['ci95_lower']:+.2f}, {s['ci95_upper']:+.2f}] | "
                      f"{c['mean_failure_minus_success']:+.3f} "
                      f"[{c['ci95_lower']:+.3f}, {c['ci95_upper']:+.3f}] |")
    report += [
        '', 'These small, outcome-selected subsets differ between models. The intervals are '
        'exploratory and pointwise, and cannot establish a causal effect of failure or population '
        'equivalence. They do not show a uniform within-task increase across models. '
        'Direct claims about redundant loops would require separately defined sequence-level '
        'coding of repeated actions or hypotheses and their subsequent evidence.', '',
        '## Files and reproducibility', '',
        '- [task_model_patterns.csv](task_model_patterns.csv): 300 model--task outcomes and category sequences.',
        '- [failure_persistence.csv](failure_persistence.csv): repetition, category recurrence and sensitivity counts.',
        '- [failure_budget_shares.csv](failure_budget_shares.csv): spending ratios and task-bootstrap intervals.',
        '- [common_success_summary.csv](common_success_summary.csv): the 55-task and 25-task shared-success sets.',
        '- [common_success_comparisons.csv](common_success_comparisons.csv): paired estimation intervals.',
        '- [within_task_outcome_differences.csv](within_task_outcome_differences.csv): selected mixed-task contrasts.',
        '- [analysis_design.json](analysis_design.json): definitions, source hashes and resampling settings.', '',
        'Reproduce from the repository root with `python3 scripts/analyze_rq2_patterns.py`.', '',
        'Inputs are [per_attempt.csv](../../data/per_attempt.csv) and the '
        '[canonical failure annotations](../../../../FINAL-CODEBOOK/failure_annotations.csv). '
        f'Bootstrap intervals use {args.bootstrap_repetitions:,} draws with seed {args.seed}. '
        'Whole-task draws preserve all models and three trials for pooled persistence and budget '
        'ratios; common-success draws preserve pairing; mixed-task draws retain the selected tasks\' '
        'trials within each model. All new intervals are pointwise exploratory estimates. '
        'Task sampling conditions on the observed repository mix; repository-level sensitivity '
        'with only 11 observed clusters remains exploratory.',
    ]
    (args.output / 'README.md').write_text('\n'.join(report) + '\n', encoding='utf-8')
    print('Wrote RQ2 analysis to', args.output)
    print('Pooled persistence:', next(r for r in persistence if r['cohort'] == 'full' and r['model'] == 'All'))
    for r in budgets:
        if r['cohort'] == 'full' and r['model'] != 'All':
            print('Budget:', r['model'], r['failure_rate_percent'], r['failure_share_of_estimated_budget_percent'])
    print('Common success tasks:', len(common), '; mixed-outcome estimates:', mixed_rows)


if __name__ == '__main__':
    main()
