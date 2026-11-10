"""Offline task/repository sensitivity analyses, including Django exclusion.

All resampling preserves every model and all three trials of a task. Repository
resampling carries entire repositories. Taxonomy tests use incidence among all
attempts, not independent rows selected by failure. No model calls are made.
"""

import argparse
import csv
import hashlib
import itertools
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

from analysis_layout import artifact, COHORTS, DJANGO
from audit_token_methodology import summarize as resource_summary
from build_failure_analysis import summarize as failure_summary
from inferential_analysis import load_attempts, interval, holm_adjust, exact_signed_sum_p_value

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = ROOT / 'result' / 'Statistics results'


def read(path):
    with path.open() as stream:
        return list(csv.DictReader(stream))


def write(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(dict.fromkeys(k for r in rows for k in r))
    if not fields:
        raise ValueError(f'No rows for {path}')
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def total(vectors):
    return [sum(column) for column in zip(*vectors)]


def value(totals, spec):
    denominator = totals[spec['denominator']]
    return spec['scale'] * totals[spec['numerator']] / denominator if denominator else None


def design(rows, catalogue, models, categories):
    """Sufficient statistics per task; column zero is its task weight."""
    tasks = sorted({r['task'] for r in rows})
    attempts = defaultdict(list)
    for row in rows:
        attempts[row['task'], row['model']].append(row)
    failed = {(r['task_id'], r['model'], int(r['trial'])): r for r in catalogue}
    groups = [('primary_category', code) for code in categories]
    groups += [('stage', stage) for stage in dict.fromkeys(c['stage'] for c in categories.values())]
    columns, specs = {}, []

    def column(key):
        if key not in columns:
            columns[key] = len(columns) + 1
        return columns[key]

    for model in models:
        for metric in ('steps', 'prompt_tokens', 'completion_tokens', 'cost', 'resolution', 'instability'):
            specs.append({'model': model, 'kind': 'resource' if metric in
                          ('steps', 'prompt_tokens', 'completion_tokens', 'cost') else 'outcome',
                          'metric': 'recorded_cost_usd' if metric == 'cost' else metric,
                          'measure': 'mean' if metric not in ('resolution', 'instability') else 'percent',
                          'numerator': column((model, metric)), 'denominator': 0,
                          'scale': 100 if metric in ('resolution', 'instability') else 1})
    for model in models + ['All']:
        failure_col = column((model, 'failures'))
        for level, category in groups:
            numerator = column((model, level, category))
            for measure in ('incidence_percent', 'composition_percent'):
                specs.append({'model': model, 'kind': 'taxonomy', 'metric': category, 'level': level,
                              'measure': measure, 'numerator': numerator,
                              'denominator': 0 if measure == 'incidence_percent' else failure_col,
                              'scale': 100/(9 if model == 'All' else 3) if measure == 'incidence_percent' else 100})
    vectors = {}
    for task in tasks:
        vector = [1] + [0] * len(columns)
        for model in models:
            group = attempts[task, model]
            successes = sum(r['success'] for r in group)
            for metric in ('steps', 'prompt_tokens', 'completion_tokens', 'cost'):
                vector[columns[model, metric]] = mean(r[metric] for r in group)
            vector[columns[model, 'resolution']] = successes / 3
            vector[columns[model, 'instability']] = int(successes in (1, 2))
            vector[columns[model, 'failures']] = 3 - successes
            vector[columns['All', 'failures']] += 3 - successes
            for row in group:
                annotation = failed.get((task, model, int(row['round'].removeprefix('round'))))
                if (annotation is not None) != (row['success'] == 0):
                    raise ValueError(f'Failure annotation/outcome mismatch: {task}, {model}, {row["round"]}')
                if annotation:
                    for level in ('primary_category', 'stage'):
                        category = annotation[level]
                        vector[columns[model, level, category]] += 1
                        vector[columns['All', level, category]] += 1
        vectors[task] = vector
    return vectors, specs


def bootstrap(vectors, specs, models, repetitions, seed, blocks=None):
    """Paired percentile estimates and paired differences from common draws."""
    point = total(vectors)
    units = blocks if blocks is not None else vectors
    cols = list(zip(*units))
    unit_count = len(units)
    draws = [[] for _ in specs]
    pairs = []
    for i, spec in enumerate(specs):
        if spec['model'] != models[0] or spec['measure'] == 'composition_percent':
            continue
        matching = [j for j, other in enumerate(specs)
                    if other['model'] in models and all(other.get(k) == spec.get(k)
                    for k in ('kind', 'metric', 'level', 'measure'))]
        pairs.extend((a, b) for a, b in itertools.combinations(matching, 2))
    pair_draws = [[] for _ in pairs]
    rng = random.Random(seed)
    if unit_count >= 2:
        for _ in range(repetitions):
            weights = Counter(rng.randrange(unit_count) for _ in range(unit_count))
            sampled = [sum(col[i]*w for i, w in weights.items()) for col in cols]
            estimates = [value(sampled, spec) for spec in specs]
            for i, estimate in enumerate(estimates):
                if estimate is not None:
                    draws[i].append(estimate)
            for i, (a, b) in enumerate(pairs):
                if estimates[a] is not None and estimates[b] is not None:
                    pair_draws[i].append(estimates[a] - estimates[b])
    summaries = []
    for i, spec in enumerate(specs):
        estimate = value(point, spec)
        low, high = interval(draws[i])
        summaries.append({k: v for k, v in spec.items() if k not in ('numerator', 'denominator', 'scale')} |
                         {'estimate': estimate, 'ci95_lower': low, 'ci95_upper': high,
                          'valid_bootstrap_repetitions': len(draws[i]), 'n_tasks': int(point[0]),
                          'resampling_units': unit_count,
                          'interval_status': 'insufficient_clusters' if unit_count < 2 else
                          'zero_observed_no_unseen_event_bound' if estimate == 0 and spec['kind'] == 'taxonomy'
                          else 'percentile_pointwise'})
    comparisons = []
    for i, (a, b) in enumerate(pairs):
        low, high = interval(pair_draws[i])
        spec = specs[a]
        row = {k: v for k, v in spec.items() if k not in ('model', 'numerator', 'denominator', 'scale')}
        row.update(left_model=specs[a]['model'], right_model=specs[b]['model'], n_tasks=int(point[0]),
                   resampling_units=unit_count, mean_difference=value(point, specs[a])-value(point, specs[b]),
                   difference_ci95_lower=low, difference_ci95_upper=high,
                   valid_bootstrap_repetitions=len(pair_draws[i]))
        if spec['kind'] == 'taxonomy' and blocks is None:
            differences = [int(v[specs[a]['numerator']] - v[specs[b]['numerator']]) for v in vectors]
            row['p_value'] = exact_signed_sum_p_value(differences)
        comparisons.append(row)
    return summaries, comparisons


def descriptive(rows, catalogue, categories, cohort, folder, stratum=None):
    """Re-use the canonical denominator definitions for both cohorts."""
    numeric = [dict(r, label=bool(r['success']), recorded_cost_usd=r['cost']) for r in rows]
    by_task, aligned = defaultdict(list), defaultdict(list)
    for row in numeric:
        by_task[row['task']].append(row)
        if float(row['cost_limit_usd']) == 3 and float(row['shell_timeout_seconds']) == 60:
            aligned[row['task'], row['round']].append(row)
    solved = {task for task, group in by_task.items() if len(group) == 9 and all(r['success'] for r in group)}
    subsets = {cohort: numeric,
               'all_models_solved_all_three_trials': [r for r in numeric if r['task'] in solved],
               'matched_task_rounds_cost3_timeout60': [r for group in aligned.values()
                                                      if len(group) == 3 for r in group]}
    summaries = []
    for subset, selected in subsets.items():
        for name, group in [('all', selected), ('success', [r for r in selected if r['success']]),
                            ('failure', [r for r in selected if not r['success']])]:
            summaries.extend(resource_summary(group, subset, name))
    labels = {(r['task'], r['model'], int(r['round'].removeprefix('round'))):
              {'label': bool(r['success'])} for r in rows}
    model, taxonomy, stages, tasks = failure_summary(catalogue, labels, categories)
    if stratum is None:
        write(artifact(folder, 'summary_metrics.csv', cohort), summaries)
        for name, records in [('failure_trial_catalog.csv', catalogue), ('failure_model_summary.csv', model),
                              ('failure_taxonomy_summary.csv', taxonomy), ('failure_stage_summary.csv', stages),
                              ('failure_task_summary.csv', tasks)]:
            if records:
                write(artifact(folder, name, cohort), records)
        return
    return summaries, model, taxonomy, stages


def django_shift(vectors, specs, metadata, repetitions, seed):
    """Joint full/excluded contrasts; preserve their overlapping observations.

    Task bootstrap is stratified by Django status, fixing its observed 50/50
    task mix. The non-Django draw is reused in the full and excluded estimates.
    """
    django = [v for task, v in vectors.items() if metadata[task]['repository'] == DJANGO]
    other = [v for task, v in vectors.items() if metadata[task]['repository'] != DJANGO]
    pooled = [s for s in specs if s['model'] == 'All' and s['measure'] == 'composition_percent']
    samples = [[] for _ in pooled]
    rng = random.Random(seed)
    cols_d, cols_o = list(zip(*django)), list(zip(*other))
    for _ in range(repetitions):
        wd = Counter(rng.randrange(len(django)) for _ in django)
        wo = Counter(rng.randrange(len(other)) for _ in other)
        sd = [sum(c[i]*w for i, w in wd.items()) for c in cols_d]
        so = [sum(c[i]*w for i, w in wo.items()) for c in cols_o]
        sf = [a+b for a, b in zip(sd, so)]
        for i, spec in enumerate(pooled):
            a, b = value(so, spec), value(sf, spec)
            if a is not None and b is not None:
                samples[i].append(a-b)
    td, to = total(django), total(other)
    tf = [a+b for a, b in zip(td, to)]
    records = []
    for i, spec in enumerate(pooled):
        full, excluded = value(tf, spec), value(to, spec)
        low, high = interval(samples[i])
        peers = [s for s in pooled if s['level'] == spec['level']]
        records.append({'level': spec['level'], 'category': spec['metric'],
                        'full_count': tf[spec['numerator']], 'without_django_count': to[spec['numerator']],
                        'django_count': td[spec['numerator']], 'full_failures': tf[spec['denominator']],
                        'without_django_failures': to[spec['denominator']], 'django_failures': td[spec['denominator']],
                        'full_share_percent': full, 'without_django_share_percent': excluded,
                        'django_share_percent': value(td, spec),
                        'change_without_minus_full_pp': excluded-full if full is not None and excluded is not None else None,
                        'change_ci95_lower_pp': low, 'change_ci95_upper_pp': high,
                        'valid_bootstrap_repetitions': len(samples[i]),
                        'django_share_of_category_percent': 100*td[spec['numerator']]/tf[spec['numerator']]
                        if tf[spec['numerator']] else None,
                        'full_rank': 1+sum(tf[s['numerator']] > tf[spec['numerator']] for s in peers),
                        'without_django_rank': 1+sum(to[s['numerator']] > to[spec['numerator']] for s in peers)})
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--data-root', type=Path, default=ROOT)
    parser.add_argument('--bootstrap-repetitions', type=int, default=10000)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()
    if args.bootstrap_repetitions < 1:
        parser.error('Bootstrap repetitions must be positive')
    out = args.output
    rows, grouped, models, tasks = load_attempts(artifact(out, 'per_attempt.csv'))
    metadata = {r['task']: r for r in read(artifact(out, 'task_metadata.csv'))}
    catalogue = read(artifact(out, 'failure_trial_catalog.csv'))
    for row in catalogue:
        row['trial'] = int(row['trial'])
    codebook = args.data_root/'docs/failure_analysis/failure_codebook.json'
    categories = {r['code']: r for r in json.loads(codebook.read_text())['categories']}
    vectors, specs = design(rows, catalogue, models, categories)
    cohort_tests, cohort_design = {}, {}
    for cohort in COHORTS:
        selected = tasks if cohort == 'full' else [t for t in tasks if metadata[t]['repository'] != DJANGO]
        taskset = set(selected)
        cohort_rows = [r for r in rows if r['task'] in taskset]
        cohort_catalogue = [r for r in catalogue if r['task_id'] in taskset]
        descriptive(cohort_rows, cohort_catalogue, categories, cohort, out)
        vs = [vectors[t] for t in selected]
        summaries, comparisons = bootstrap(vs, specs, models, args.bootstrap_repetitions, args.seed)
        write(artifact(out, 'category_uncertainty.csv', cohort), [r for r in summaries if r['kind'] == 'taxonomy'])
        tests = [r for r in comparisons if r['kind'] == 'taxonomy']
        for r, p in zip(tests, holm_adjust([r['p_value'] for r in tests])):
            r.update(p_value_holm=p, holm_family_size=len(tests), cohort=cohort)
        cohort_tests[cohort] = tests

        strata_resources, strata_outcomes, strata_failures, strata_comparisons = [], [], [], []
        strata_sizes = []
        for dimension in ('repository', 'difficulty'):
            for name in sorted({metadata[t][dimension] for t in selected}):
                st = [t for t in selected if metadata[t][dimension] == name]
                group, pairs = bootstrap([vectors[t] for t in st], specs, models,
                                         args.bootstrap_repetitions, args.seed)
                prefix = {'dimension': dimension, 'stratum': name}
                strata_sizes.append(prefix | {'n_tasks': len(st), 'n_attempts': 9*len(st)})
                for record in group:
                    destination = {'resource': strata_resources, 'outcome': strata_outcomes,
                                   'taxonomy': strata_failures}[record['kind']]
                    destination.append(prefix | record)
                # Stratum comparisons are estimation only; no post-hoc test battery.
                strata_comparisons.extend(prefix | {k: v for k, v in r.items() if k != 'p_value'} for r in pairs)
        folder = out/cohort/'stratified'
        for name, records in [('stratum_sizes.csv', strata_sizes), ('resource_summary.csv', strata_resources),
                              ('outcome_summary.csv', strata_outcomes), ('failure_summary.csv', strata_failures),
                              ('paired_comparisons.csv', strata_comparisons)]:
            write(folder/name, records)

        repositories = sorted({metadata[t]['repository'] for t in selected})
        blocks = [total([vectors[t] for t in selected if metadata[t]['repository'] == repo]) for repo in repositories]
        repo_summary, repo_pairs = bootstrap(vs, specs, models, args.bootstrap_repetitions, args.seed, blocks)
        write(out/cohort/'repository_sensitivity'/'cluster_summary.csv', repo_summary)
        write(out/cohort/'repository_sensitivity'/'paired_comparisons.csv', repo_pairs)
        macro, leave_out = [], []
        for spec in specs:
            observed = [value(block, spec) for block in blocks]
            valid = [x for x in observed if x is not None]
            metadata_fields = {k: v for k, v in spec.items() if k not in ('numerator', 'denominator', 'scale')}
            macro.append(metadata_fields | {'repository_equal_mean': mean(valid) if valid else None,
                                            'repositories': len(repositories), 'defined_repositories': len(valid)})
            for repo, block in zip(repositories, blocks):
                reduced = [a-b for a, b in zip(total(vs), block)]
                leave_out.append(metadata_fields | {'excluded_repository': repo, 'remaining_tasks': reduced[0],
                                                     'estimate': value(reduced, spec)})
        write(out/cohort/'repository_sensitivity'/'repository_equal_summary.csv', macro)
        write(out/cohort/'repository_sensitivity'/'leave_one_repository_out.csv', leave_out)
        cohort_design[cohort] = {'tasks': len(selected), 'attempts': len(cohort_rows),
                                 'failures': len(cohort_catalogue), 'repositories': len(repositories)}
        print(f'{cohort}: {len(selected)} tasks, {len(cohort_catalogue)} failures; strata and repository sensitivity complete.', flush=True)

    all_tests = [r for records in cohort_tests.values() for r in records]
    for r, p in zip(all_tests, holm_adjust([r['p_value'] for r in all_tests])):
        r.update(p_value_holm_both_cohorts=p, both_cohorts_family_size=len(all_tests))
    for cohort, tests in cohort_tests.items():
        write(artifact(out, 'category_inference.csv', cohort), tests)
    shift = django_shift(vectors, specs, metadata, args.bootstrap_repetitions, args.seed)
    write(out/'sensitivity'/'django_taxonomy_shift.csv', shift)
    resource_effects = []
    for filename in ('resource_comparisons.csv', 'success_comparisons.csv', 'stability_comparisons.csv'):
        for cohort in COHORTS:
            resource_effects.extend({'cohort': cohort, 'comparison_family': filename.removesuffix('.csv')} | r
                                    for r in read(artifact(out, filename, cohort)))
    # These are dependent, nested cohorts: adjust the 30 tests jointly without
    # treating the full/excluded estimates as independent samples.
    for r, p in zip(resource_effects, holm_adjust([float(r['p_value']) for r in resource_effects])):
        r.update(p_value_holm_both_cohorts=p, both_cohorts_family_size=len(resource_effects))
    write(out/'sensitivity'/'model_comparisons_both_cohorts.csv', resource_effects)
    record = {'cohorts': cohort_design, 'seed': args.seed, 'bootstrap_repetitions': args.bootstrap_repetitions,
              'codebook_sha256': hashlib.sha256(codebook.read_bytes()).hexdigest(),
              'task_bootstrap': 'Resample complete tasks, preserving all models and three trials.',
              'repository_bootstrap': 'Resample whole repositories; ratio of summed task statistics retains task weighting. Exploratory with only 11/10 unequal repository clusters; no repository-level p-values.',
              'repository_equal_summary': 'Mean of repository-specific estimates; changes the estimand. Undefined within-repository failure compositions are omitted and their count is reported.',
              'strata': 'Archived repository and human-fix-time difficulty labels. Estimation only; singleton strata have blank confidence intervals.',
              'django_shift': 'Joint bootstrap stratified by Django status; both estimates reuse the same non-Django draws. Contrast is without-Django minus full. No independent-cohort test.',
              'taxonomy_tests': '48 exact paired task-swap incidence tests per cohort (11 categories + 5 stages, 3 model pairs). Holm within cohort and additionally across all 96 tests; exploratory, separate from resource/outcome family.',
              'composition': 'Category count / observed failures; incidence uses all attempts. Ratios are recomputed in each bootstrap draw. Undefined zero-denominator draws are omitted and valid counts reported.',
              'intervals': 'Pointwise percentile 95% intervals; not simultaneous intervals. A zero-observed bootstrap interval is not a bound on unseen categories.',
              'inputs': [{'path': str(p.relative_to(out)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                         for p in (artifact(out, 'per_attempt.csv'), artifact(out, 'task_metadata.csv'),
                                   artifact(out, 'failure_trial_catalog.csv'))]}
    (out/'sensitivity'/'analysis_design.json').write_text(json.dumps(record, indent=2)+'\n')


if __name__ == '__main__':
    main()
