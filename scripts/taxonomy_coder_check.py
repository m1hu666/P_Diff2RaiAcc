"""Prepare three label-review sheets and compare the completed checks.

``prepare`` pairs archived failed trials with their current primary categories
and creates three eight-column coder sheets. Each coder also audits whether the
current label meets the codebook's earliest supported-link convention.
``compare`` validates the locked sheets, creates a discussion table, and
reports pre-discussion agreement. ``summarize`` validates reconciled decisions
and reports category and earliest-link counts. The script never modifies source
artifacts, canonical annotations, or a previously created discussion table.
"""

import argparse
import csv
import hashlib
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
DEFAULT_CATALOGUE = ROOT / 'result' / 'Statistics results' / 'failure_trial_catalog.csv'
DEFAULT_CODEBOOK = ROOT / 'docs' / 'failure_analysis' / 'failure_codebook.json'
DEFAULT_ANNOTATIONS = ROOT / 'docs' / 'failure_analysis' / 'failure_annotations.csv'
DEFAULT_DOCS = ROOT / 'docs' / 'taxonomy_methodology'
DEFAULT_STATISTICS = ROOT / 'result' / 'Statistics results' / 'taxonomy_reliability'
FROZEN_CODEBOOK_SHA256 = '02cc27631636fb042ec93a65b64213334c13c4ae7f76118d0541a39fb98b418f'
MODEL_IDS = {
    'Claude': 'claude-sonnet-4-5-20250929',
    'Gemini': 'gemini-3-pro-preview',
    'GPT': 'gpt-5-2025-08-07-medium-reasoning',
}
MODEL_SHORT = {model_id: short for short, model_id in MODEL_IDS.items()}
IDENTITY_FIELDS = ['task_id', 'model', 'trial']
CODER_COLUMNS = IDENTITY_FIELDS + [
    'current_category', 'decision', 'proposed_category', 'reason', 'earliest_link',
]
CODER_NAMES = ('a', 'b', 'c')
DECISIONS = ('ACCEPT', 'CHANGE', 'UNSURE')
EARLIEST_VALUES = ('SUPPORTED', 'NOT_SUPPORTED', 'INDETERMINATE')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_csv(path):
    with path.open(encoding='utf-8', newline='') as stream:
        reader = csv.DictReader(stream)
        return reader.fieldnames, list(reader)


def write_csv_exclusive(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_codebook(path):
    data = json.loads(path.read_text(encoding='utf-8'))
    categories = [row['code'] for row in data['categories']]
    require(len(categories) == len(set(categories)), 'Duplicate codebook categories')
    stages = {row['code']: row['stage'] for row in data['categories']}
    audit = data.get('attribution_audit', {})
    require(audit.get('field') == 'earliest_link',
            'Codebook lacks the earliest-link audit definition')
    earliest_values = tuple(audit.get('values', {}))
    require(earliest_values == EARLIEST_VALUES,
            'Unexpected earliest-link values in the codebook')
    codebook_hash = sha256(path)
    require(codebook_hash == FROZEN_CODEBOOK_SHA256,
            'The frozen codebook changed; review it and regenerate the coder sheets')
    return categories, stages, earliest_values, codebook_hash


def canonical_annotations(path):
    headers, annotations = read_csv(path)
    required = {'task_id', 'model', 'trial', 'primary_category', 'diagnosis'}
    require(required <= set(headers or []),
            f'Canonical annotation file lacks fields: {sorted(required-set(headers or []))}')
    canonical = {}
    for line, row in enumerate(annotations, 2):
        require(row['model'] in MODEL_SHORT,
                f'Unknown model ID in {path}:{line}: {row["model"]!r}')
        key = row['task_id'], MODEL_SHORT[row['model']], row['trial']
        require(key not in canonical, f'Duplicate canonical trial in {path}:{line}: {key}')
        require(row['primary_category'] and row['diagnosis'],
                f'Empty category/diagnosis in {path}:{line}')
        canonical[key] = row
    require(bool(canonical), f'No canonical annotations in {path}')
    return canonical


def prepare(args):
    headers, catalogue = read_csv(args.catalogue)
    require(bool(catalogue), f'No cases in {args.catalogue}')
    required = {'task_id', 'model', 'model_short', 'trial', 'recorded_resolved'}
    require(required <= set(headers or []), f'Catalogue lacks fields: {sorted(required-set(headers or []))}')
    categories, _, _, _ = load_codebook(args.codebook)
    canonical = canonical_annotations(args.annotations)

    task_failure_counts = Counter(row['task_id'] for row in catalogue)
    model_order = {model: index for index, model in enumerate(MODEL_IDS)}
    ordered_catalogue = sorted(
        catalogue,
        key=lambda row: (
            row['task_id'].split('__', 1)[0],
            task_failure_counts[row['task_id']],
            row['task_id'],
            model_order[row['model_short']],
            int(row['trial']),
        ),
    )

    rows = []
    seen = set()
    for source in ordered_catalogue:
        key = source['task_id'], source['model_short'], source['trial']
        require(key not in seen, f'Duplicate catalogue case: {key}')
        seen.add(key)
        require(source.get('recorded_resolved') == 'False', f'Catalogue includes a resolved case: {key}')
        require(source['model_short'] in MODEL_IDS, f'Unknown model label: {source["model_short"]}')
        require(source['model'] == MODEL_IDS[source['model_short']], f'Model ID mismatch: {key}')
        require(key in canonical, f'Catalogue trial missing from canonical annotations: {key}')
        current_category = canonical[key]['primary_category']
        require(current_category in categories,
                f'Unknown current category {current_category!r} for {key}')
        row = {
            'task_id': source['task_id'],
            'model': source['model_short'],
            'trial': source['trial'],
            'current_category': current_category,
            'decision': '',
            'proposed_category': '',
            'reason': '',
            'earliest_link': '',
        }
        rows.append(row)
    require(seen == set(canonical), 'Catalogue trials do not match canonical annotations')

    targets = [args.output_dir / f'coder_{name}.csv' for name in CODER_NAMES]
    existing = [str(path) for path in targets if path.exists()]
    require(not existing, 'Refusing to overwrite coder sheets: '+', '.join(existing))
    for path in targets:
        write_csv_exclusive(path, CODER_COLUMNS, rows)
    print(f'Created {len(rows)}-row coder sheets: '+', '.join(map(str, targets)))


def normalized_coder_rows(path, allowed_categories, earliest_values):
    headers, rows = read_csv(path)
    require(headers == CODER_COLUMNS, f'Unexpected columns in {path}')
    require(bool(rows), f'No coder rows in {path}')
    normalized = {}
    for line, row in enumerate(rows, 2):
        task_id = row['task_id'].strip()
        model = row['model'].strip()
        trial = row['trial'].strip()
        key = task_id, model, trial
        require(task_id and key not in normalized, f'Duplicate/empty trial identity in {path}:{line}')
        require(model in MODEL_IDS, f'Invalid model {model!r} in {path}:{line}')
        require(trial in {'1', '2', '3'}, f'Invalid trial {trial!r} in {path}:{line}')
        current = row['current_category'].strip()
        decision = row['decision'].strip().upper()
        proposed = row['proposed_category'].strip()
        reason = row['reason'].strip()
        earliest_link = row['earliest_link'].strip().upper()
        require(current in allowed_categories and current != 'OTHER',
                f'Invalid current_category {current!r} in {path}:{line}')
        require(decision in DECISIONS,
                f'Invalid/empty decision {decision!r} in {path}:{line}')
        require(decision != 'CHANGE' or (proposed in allowed_categories and proposed != current),
                f'CHANGE requires a different category or OTHER in {path}:{line}')
        require(decision == 'CHANGE' or not proposed,
                f'Only CHANGE may use proposed_category in {path}:{line}')
        require(decision == 'ACCEPT' or bool(reason),
                f'Reason required for CHANGE or UNSURE in {path}:{line}')
        require(earliest_link in earliest_values,
                f'Invalid/empty earliest_link {earliest_link!r} in {path}:{line}')
        require(earliest_link == 'SUPPORTED' or bool(reason),
                f'Reason required for NOT_SUPPORTED or INDETERMINATE in {path}:{line}')
        clean = dict(row)
        clean.update(task_id=task_id, model=model, trial=trial,
                     current_category=current, decision=decision,
                     proposed_category=proposed, reason=reason,
                     earliest_link=earliest_link,
                     reviewed_category=(current if decision == 'ACCEPT' else
                                        proposed if decision == 'CHANGE' else None))
        normalized[key] = clean
    return normalized


def agreement(left, right, labels):
    require(len(left) == len(right) and left, 'Agreement requires paired non-empty labels')
    n = len(left)
    matches = sum(a == b for a, b in zip(left, right))
    left_counts, right_counts = Counter(left), Counter(right)
    expected = sum(left_counts[label] * right_counts[label] for label in labels) / (n*n)
    kappa = None if math.isclose(expected, 1.0) else (matches/n - expected) / (1-expected)
    confusion = {a: {b: 0 for b in labels} for a in labels}
    for a, b in zip(left, right):
        confusion[a][b] += 1
    return {
        'n': n,
        'matches': matches,
        'raw_agreement': matches/n,
        'cohen_kappa': kappa,
        'left_counts': dict(sorted(left_counts.items())),
        'right_counts': dict(sorted(right_counts.items())),
        'confusion_matrix': confusion,
    }


def percentile(values, probability):
    require(bool(values), 'Cannot calculate a percentile from no values')
    ordered = sorted(values)
    position = (len(ordered)-1)*probability
    lower, upper = math.floor(position), math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position-lower
    return ordered[lower]*(1-fraction) + ordered[upper]*fraction


def cluster_bootstrap(rows, labels, left_field, right_field, repetitions, seed):
    by_task = defaultdict(list)
    for row in rows:
        by_task[row['task_id']].append(row)
    tasks = sorted(by_task)
    rng = random.Random(seed)
    raw_values, kappa_values = [], []
    for _ in range(repetitions):
        sampled = [rng.choice(tasks) for _ in tasks]
        replicate = [row for task in sampled for row in by_task[task]]
        metrics = agreement(
            [row[left_field] for row in replicate],
            [row[right_field] for row in replicate],
            labels,
        )
        raw_values.append(metrics['raw_agreement'])
        if metrics['cohen_kappa'] is not None:
            kappa_values.append(metrics['cohen_kappa'])
    return {
        'method': 'task-cluster percentile bootstrap',
        'repetitions': repetitions,
        'seed': seed,
        'left_field': left_field,
        'right_field': right_field,
        'tasks_per_replicate': len(tasks),
        'raw_agreement_ci95': [percentile(raw_values, .025), percentile(raw_values, .975)],
        'cohen_kappa_ci95': ([percentile(kappa_values, .025), percentile(kappa_values, .975)]
                             if kappa_values else None),
        'valid_kappa_replicates': len(kappa_values),
    }


def fleiss_kappa(ratings, labels):
    """Unweighted Fleiss kappa for three reviewers of the same trial set."""
    require(bool(ratings), 'Fleiss kappa requires at least one jointly reviewed trial')
    require(all(len(row) == 3 for row in ratings), 'Expected three ratings per trial')
    n = len(ratings)
    total = Counter(label for row in ratings for label in row)
    require(set(total) <= set(labels), 'Fleiss kappa received an unknown label')
    observed = sum(
        sum(count * (count - 1) for count in Counter(row).values()) / 6
        for row in ratings
    ) / n
    expected = sum((total[label] / (3 * n)) ** 2 for label in labels)
    return {
        'n': n,
        'mean_pairwise_agreement': observed,
        'fleiss_kappa': (None if math.isclose(expected, 1.0)
                         else (observed - expected) / (1 - expected)),
        'rating_counts': dict(sorted(total.items())),
    }


def fleiss_cluster_bootstrap(rows, labels, repetitions, seed, field_suffix='category'):
    by_task = defaultdict(list)
    for row in rows:
        by_task[row['task_id']].append(row)
    tasks = sorted(by_task)
    rng = random.Random(seed)
    raw_values, kappa_values = [], []
    for _ in range(repetitions):
        sampled = [rng.choice(tasks) for _ in tasks]
        replicate = [row for task in sampled for row in by_task[task]]
        metrics = fleiss_kappa(
            [[row[f'coder_{name}_{field_suffix}'] for name in CODER_NAMES]
             for row in replicate], labels,
        )
        raw_values.append(metrics['mean_pairwise_agreement'])
        if metrics['fleiss_kappa'] is not None:
            kappa_values.append(metrics['fleiss_kappa'])
    return {
        'method': 'task-cluster percentile bootstrap',
        'repetitions': repetitions,
        'seed': seed,
        'tasks_per_replicate': len(tasks),
        'mean_pairwise_agreement_ci95': [percentile(raw_values, .025),
                                         percentile(raw_values, .975)],
        'fleiss_kappa_ci95': ([percentile(kappa_values, .025),
                              percentile(kappa_values, .975)]
                             if kappa_values else None),
        'valid_kappa_replicates': len(kappa_values),
    }


def compare(args):
    categories, _, earliest_values, codebook_hash = load_codebook(args.codebook)
    allowed = categories + ['OTHER']
    coder_paths = {name: getattr(args, f'coder_{name}') for name in CODER_NAMES}
    coders = {name: normalized_coder_rows(path, allowed, earliest_values)
              for name, path in coder_paths.items()}
    first = coders[CODER_NAMES[0]]
    for name in CODER_NAMES[1:]:
        require(set(coders[name]) == set(first),
                f'Coder {name} sheet does not contain the same trials')
        require(list(coders[name]) == list(first),
                f'Coder {name} sheet does not use the same trial order')

    canonical = canonical_annotations(args.annotations)
    require(set(first) == set(canonical),
            'Coder trials do not match canonical failure annotations')
    for name, coder in coders.items():
        for key, row in coder.items():
            require(row['current_category'] == canonical[key]['primary_category'],
                    f'Coder {name} current_category differs from canonical annotation for {key}')

    require(not args.comparison.exists(), f'Refusing to overwrite {args.comparison}')
    require(not args.statistics.exists(), f'Refusing to overwrite {args.statistics}')

    rows = []
    for key in first:
        original = canonical[key]
        decisions = [coders[name][key]['decision'] for name in CODER_NAMES]
        reasons = [coders[name][key]['reason'] for name in CODER_NAMES]
        earliest_links = [coders[name][key]['earliest_link'] for name in CODER_NAMES]
        discussion = (any(decision != 'ACCEPT' for decision in decisions)
                      or any(reasons)
                      or any(status != 'SUPPORTED' for status in earliest_links))
        row = {
            'task_id': key[0],
            'model': key[1],
            'trial': key[2],
            'current_category': original['primary_category'],
            'current_reason': original['diagnosis'],
        }
        for name in CODER_NAMES:
            coder = coders[name][key]
            row[f'coder_{name}_decision'] = coder['decision']
            row[f'coder_{name}_category'] = coder['reviewed_category'] or ''
            row[f'coder_{name}_reason'] = coder['reason']
            row[f'coder_{name}_earliest_link'] = coder['earliest_link']
        row.update(
            discussion_required=str(discussion).lower(),
            discussion_summary='',
            final_category='' if discussion else original['primary_category'],
            final_reason='' if discussion else original['diagnosis'],
            final_earliest_link='' if discussion else 'SUPPORTED',
        )
        rows.append(row)

    pairwise_category = {}
    pairwise_decision = {}
    pairwise_earliest = {}
    for left, right in (('a', 'b'), ('a', 'c'), ('b', 'c')):
        label = f'{left}_{right}'
        left_category = f'coder_{left}_category'
        right_category = f'coder_{right}_category'
        determinate = [row for row in rows
                       if row[left_category] and row[right_category]]
        pairwise_category[label] = {
            'n_jointly_determinate': len(determinate),
            'agreement': (agreement([row[left_category] for row in determinate],
                                    [row[right_category] for row in determinate], allowed)
                          if determinate else None),
            'task_cluster_bootstrap': (
                cluster_bootstrap(determinate, allowed, left_category, right_category,
                                  args.bootstrap_repetitions, args.seed)
                if determinate else None),
        }
        pairwise_decision[label] = agreement(
            [row[f'coder_{left}_decision'] for row in rows],
            [row[f'coder_{right}_decision'] for row in rows], list(DECISIONS),
        )
        left_earliest = f'coder_{left}_earliest_link'
        right_earliest = f'coder_{right}_earliest_link'
        pairwise_earliest[label] = {
            'agreement': agreement(
                [row[left_earliest] for row in rows],
                [row[right_earliest] for row in rows], earliest_values,
            ),
            'task_cluster_bootstrap': cluster_bootstrap(
                rows, earliest_values, left_earliest, right_earliest,
                args.bootstrap_repetitions, args.seed,
            ),
        }
    jointly_determinate = [row for row in rows
                           if all(row[f'coder_{name}_category'] for name in CODER_NAMES)]
    acceptance_counts = Counter(
        sum(row[f'coder_{name}_decision'] == 'ACCEPT' for name in CODER_NAMES)
        for row in rows
    )
    statistics = {
        'scope': 'Locked pre-discussion review of visible current labels by three coders',
        'interpretation': (
            'Coders saw the current category and analysis. These are agreement '
            'and concordance statistics for anchored review, not blind '
            'independent application of an inductive taxonomy. UNSURE is a '
            'review decision, not a failure category; categorical agreement '
            'excludes it and reports the resulting denominator. Earliest-link '
            'statuses audit an observational sequence; SUPPORTED does not '
            'identify or prove a causal root cause.'
        ),
        'n_cases': len(rows),
        'n_tasks': len({row['task_id'] for row in rows}),
        'codebook_sha256': codebook_hash,
        'coder_sheet_sha256': {f'coder_{name}': sha256(coder_paths[name])
                               for name in CODER_NAMES},
        'review_decision_counts': {
            f'coder_{name}': dict(sorted(Counter(row[f'coder_{name}_decision']
                                                for row in rows).items()))
            for name in CODER_NAMES
        },
        'acceptance_by_number_of_coders': {
            str(count): acceptance_counts[count] for count in range(4)
        },
        'unanimous_acceptance': acceptance_counts[3],
        'at_least_one_change': sum(
            any(row[f'coder_{name}_decision'] == 'CHANGE' for name in CODER_NAMES)
            for row in rows
        ),
        'at_least_one_unsure': sum(
            any(row[f'coder_{name}_decision'] == 'UNSURE' for name in CODER_NAMES)
            for row in rows
        ),
        'at_least_one_earliest_not_supported': sum(
            any(row[f'coder_{name}_earliest_link'] == 'NOT_SUPPORTED'
                for name in CODER_NAMES) for row in rows
        ),
        'at_least_one_earliest_indeterminate': sum(
            any(row[f'coder_{name}_earliest_link'] == 'INDETERMINATE'
                for name in CODER_NAMES) for row in rows
        ),
        'discussion_required': sum(row['discussion_required'] == 'true' for row in rows),
        'review_decision_pairwise': pairwise_decision,
        'category_pairwise': pairwise_category,
        'earliest_link_status_counts': {
            f'coder_{name}': dict(sorted(Counter(row[f'coder_{name}_earliest_link']
                                                for row in rows).items()))
            for name in CODER_NAMES
        },
        'earliest_link_pairwise': pairwise_earliest,
        'earliest_link_all_three': {
            'unanimous_status_count': sum(
                len({row[f'coder_{name}_earliest_link'] for name in CODER_NAMES}) == 1
                for row in rows
            ),
            'unanimous_supported_count': sum(
                all(row[f'coder_{name}_earliest_link'] == 'SUPPORTED'
                    for name in CODER_NAMES) for row in rows
            ),
            'agreement': fleiss_kappa(
                [[row[f'coder_{name}_earliest_link'] for name in CODER_NAMES]
                 for row in rows], earliest_values,
            ),
            'task_cluster_bootstrap': fleiss_cluster_bootstrap(
                rows, earliest_values, args.bootstrap_repetitions, args.seed,
                field_suffix='earliest_link',
            ),
        },
        'category_all_three': {
            'n_jointly_determinate': len(jointly_determinate),
            'unanimous_category_count': sum(
                len({row[f'coder_{name}_category'] for name in CODER_NAMES}) == 1
                for row in jointly_determinate
            ),
            'agreement': (fleiss_kappa(
                [[row[f'coder_{name}_category'] for name in CODER_NAMES]
                 for row in jointly_determinate], allowed)
                if jointly_determinate else None),
            'task_cluster_bootstrap': (
                fleiss_cluster_bootstrap(jointly_determinate, allowed,
                                         args.bootstrap_repetitions, args.seed)
                if jointly_determinate else None),
        },
    }

    write_csv_exclusive(args.comparison, list(rows[0]), rows)
    args.statistics.parent.mkdir(parents=True, exist_ok=True)
    with args.statistics.open('x', encoding='utf-8') as stream:
        json.dump(statistics, stream, indent=2)
        stream.write('\n')
    print(json.dumps({
        'comparison': str(args.comparison),
        'statistics': str(args.statistics),
        'n_cases': len(rows),
        'unanimous_acceptance': statistics['unanimous_acceptance'],
        'at_least_one_change': statistics['at_least_one_change'],
        'at_least_one_unsure': statistics['at_least_one_unsure'],
        'n_jointly_determinate': len(jointly_determinate),
        'earliest_unanimous_supported': statistics['earliest_link_all_three'][
            'unanimous_supported_count'],
    }, indent=2))


def status_distribution(statuses, values):
    counts = Counter(statuses)
    total = len(statuses)
    assessable = counts['SUPPORTED'] + counts['NOT_SUPPORTED']
    return {
        'n': total,
        'statuses': {
            status: {'count': counts[status],
                     'percent_of_all': 100 * counts[status] / total if total else 0}
            for status in values
        },
        'assessable_n': assessable,
        'supported_percent_among_assessable': (
            100 * counts['SUPPORTED'] / assessable if assessable else None
        ),
    }


def grouped_status(rows, field, values):
    groups = defaultdict(list)
    for row in rows:
        groups[row[field]].append(row['final_earliest_link'])
    return {
        group: status_distribution(statuses, values)
        for group, statuses in sorted(groups.items())
    }


def supported_cluster_bootstrap(rows, repetitions, seed):
    by_task = defaultdict(list)
    for row in rows:
        by_task[row['task_id']].append(row)
    tasks = sorted(by_task)
    rng = random.Random(seed)
    proportions = []
    for _ in range(repetitions):
        sampled = [rng.choice(tasks) for _ in tasks]
        replicate = [row for task in sampled for row in by_task[task]]
        proportions.append(
            sum(row['final_earliest_link'] == 'SUPPORTED' for row in replicate)
            / len(replicate)
        )
    return {
        'method': 'task-cluster percentile bootstrap',
        'repetitions': repetitions,
        'seed': seed,
        'tasks_per_replicate': len(tasks),
        'supported_proportion_of_all_ci95': [percentile(proportions, .025),
                                             percentile(proportions, .975)],
    }


def summarize(args):
    categories, stages, earliest_values, codebook_hash = load_codebook(args.codebook)
    allowed_categories = categories + ['OTHER']
    headers, source_rows = read_csv(args.comparison)
    required = {
        'task_id', 'model', 'trial', 'current_category', 'discussion_required',
        'discussion_summary', 'final_category', 'final_reason',
        'final_earliest_link',
    }
    require(required <= set(headers or []),
            f'Comparison table lacks fields: {sorted(required-set(headers or []))}')
    require(bool(source_rows), f'No rows in {args.comparison}')

    rows = []
    seen = set()
    for line, source in enumerate(source_rows, 2):
        task_id = source['task_id'].strip()
        model = source['model'].strip()
        trial = source['trial'].strip()
        key = task_id, model, trial
        require(task_id and key not in seen,
                f'Duplicate/empty trial identity in {args.comparison}:{line}')
        seen.add(key)
        require(model in MODEL_IDS, f'Invalid model {model!r} in {args.comparison}:{line}')
        require(trial in {'1', '2', '3'}, f'Invalid trial {trial!r} in {args.comparison}:{line}')
        category = source['final_category'].strip()
        current = source['current_category'].strip()
        reason = source['final_reason'].strip()
        earliest_link = source['final_earliest_link'].strip()
        require(current in categories,
                f'Invalid current_category {current!r} in {args.comparison}:{line}')
        require(category in allowed_categories,
                f'Invalid/empty final_category {category!r} in {args.comparison}:{line}')
        require(bool(reason), f'Empty final_reason in {args.comparison}:{line}')
        require(earliest_link in earliest_values,
                f'Invalid/empty final_earliest_link {earliest_link!r} '
                f'in {args.comparison}:{line}')
        discussion_required = source['discussion_required'].strip().lower()
        require(discussion_required in {'true', 'false'},
                f'Invalid discussion_required in {args.comparison}:{line}')
        require(discussion_required == 'false' or bool(source['discussion_summary'].strip()),
                f'Discussion summary required in {args.comparison}:{line}')
        require(discussion_required == 'true' or category == current,
                f'Undiscussed category change in {args.comparison}:{line}')
        require(discussion_required == 'true' or earliest_link == 'SUPPORTED',
                f'Undiscussed earliest-link change in {args.comparison}:{line}')
        rows.append({
            'task_id': task_id,
            'model': model,
            'trial': trial,
            'current_category': current,
            'final_category': category,
            'final_reason': reason,
            'final_earliest_link': earliest_link,
            'stage': stages.get(category, 'OTHER'),
            'discussion_required': discussion_required,
        })

    canonical = canonical_annotations(args.annotations)
    require(seen == set(canonical),
            'Final comparison rows do not match canonical failure annotations')
    for row in rows:
        key = row['task_id'], row['model'], row['trial']
        require(row['current_category'] == canonical[key]['primary_category'],
                f'Comparison current_category differs from canonical annotation for {key}')
    require(not args.statistics.exists(), f'Refusing to overwrite {args.statistics}')

    transitions = Counter((row['current_category'], row['final_category']) for row in rows
                          if row['current_category'] != row['final_category'])
    summary = {
        'scope': 'Reconciled final categories after three-coder anchored review',
        'n_cases': len(rows),
        'n_tasks': len({row['task_id'] for row in rows}),
        'codebook_sha256': codebook_hash,
        'comparison_sha256': sha256(args.comparison),
        'discussion_cases': sum(row['discussion_required'] == 'true' for row in rows),
        'changed_from_current': sum(row['current_category'] != row['final_category']
                                    for row in rows),
        'category_transitions': [
            {'from': source, 'to': target, 'n': count}
            for (source, target), count in sorted(transitions.items())
        ],
        'final_category_counts': dict(sorted(Counter(row['final_category'] for row in rows).items())),
        'final_stage_counts': dict(sorted(Counter(row['stage'] for row in rows).items())),
        'earliest_link': {
            'interpretation': (
                'SUPPORTED means the retained evidence directly links the selected '
                'failure mode to the earliest observable unrecovered deviation. '
                'This is an observational attribution audit, not proof of a '
                'causal root cause. INDETERMINATE is retained in the all-trial '
                'denominator and excluded only from the secondary assessable '
                'proportion.'
            ),
            'overall': status_distribution(
                [row['final_earliest_link'] for row in rows], earliest_values,
            ),
            'supported_task_cluster_bootstrap': supported_cluster_bootstrap(
                rows, args.bootstrap_repetitions, args.seed,
            ),
            'by_model': grouped_status(rows, 'model', earliest_values),
            'by_category': grouped_status(rows, 'final_category', earliest_values),
            'by_stage': grouped_status(rows, 'stage', earliest_values),
        },
    }
    args.statistics.parent.mkdir(parents=True, exist_ok=True)
    with args.statistics.open('x', encoding='utf-8') as stream:
        json.dump(summary, stream, indent=2)
        stream.write('\n')
    print(json.dumps({
        'statistics': str(args.statistics),
        'n_cases': len(rows),
        'discussion_cases': summary['discussion_cases'],
        'changed_from_current': summary['changed_from_current'],
        'earliest_link': summary['earliest_link']['overall'],
    }, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest='command', required=True)

    prepare_parser = subparsers.add_parser(
        'prepare', help='Create three blank decision sheets with visible current categories')
    prepare_parser.add_argument('--catalogue', type=Path, default=DEFAULT_CATALOGUE)
    prepare_parser.add_argument('--annotations', type=Path, default=DEFAULT_ANNOTATIONS)
    prepare_parser.add_argument('--codebook', type=Path, default=DEFAULT_CODEBOOK)
    prepare_parser.add_argument('--output-dir', type=Path, default=DEFAULT_DOCS)
    prepare_parser.set_defaults(function=prepare)

    compare_parser = subparsers.add_parser('compare', help='Validate and compare completed coder sheets')
    compare_parser.add_argument('--coder-a', type=Path, default=DEFAULT_DOCS/'coder_a.csv')
    compare_parser.add_argument('--coder-b', type=Path, default=DEFAULT_DOCS/'coder_b.csv')
    compare_parser.add_argument('--coder-c', type=Path, default=DEFAULT_DOCS/'coder_c.csv')
    compare_parser.add_argument('--annotations', type=Path, default=DEFAULT_ANNOTATIONS)
    compare_parser.add_argument('--codebook', type=Path, default=DEFAULT_CODEBOOK)
    compare_parser.add_argument('--comparison', type=Path, default=DEFAULT_DOCS/'coder_comparison.csv')
    compare_parser.add_argument('--statistics', type=Path, default=DEFAULT_STATISTICS/'agreement.json')
    compare_parser.add_argument('--bootstrap-repetitions', type=int, default=10000)
    compare_parser.add_argument('--seed', type=int, default=42)
    compare_parser.set_defaults(function=compare)

    summarize_parser = subparsers.add_parser(
        'summarize', help='Summarize reconciled final attribution decisions')
    summarize_parser.add_argument(
        '--comparison', type=Path, default=DEFAULT_DOCS/'coder_comparison.csv')
    summarize_parser.add_argument('--annotations', type=Path, default=DEFAULT_ANNOTATIONS)
    summarize_parser.add_argument('--codebook', type=Path, default=DEFAULT_CODEBOOK)
    summarize_parser.add_argument(
        '--statistics', type=Path,
        default=DEFAULT_STATISTICS/'final_review_summary.json')
    summarize_parser.add_argument('--bootstrap-repetitions', type=int, default=10000)
    summarize_parser.add_argument('--seed', type=int, default=42)
    summarize_parser.set_defaults(function=summarize)

    args = parser.parse_args()
    require(getattr(args, 'bootstrap_repetitions', 1) > 0, 'Bootstrap repetitions must be positive')
    try:
        args.function(args)
    except ValueError as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
