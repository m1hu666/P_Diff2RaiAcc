"""Prepare independent coder sheets and compare the completed classifications.

``prepare`` reads the canonical failure catalogue only to create two minimal,
label-blind CSV sheets. ``compare`` validates the locked sheets, creates a
discussion table, and reports exact agreement and unweighted Cohen's kappa with
task-cluster bootstrap intervals. ``summarize`` validates reconciled decisions
and reports the final earliest-link audit. The script never modifies
trajectories, codebook definitions, canonical annotations, or a previously
created discussion table.
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
FROZEN_CODEBOOK_SHA256 = '355b45fc43e8d587603b752c5321b5d3575fd6669db49668abd522623d9adf54'
MODEL_IDS = {
    'Claude': 'claude-sonnet-4-5-20250929',
    'Gemini': 'gemini-3-pro-preview',
    'GPT': 'gpt-5-2025-08-07-medium-reasoning',
}
MODEL_SHORT = {model_id: short for short, model_id in MODEL_IDS.items()}
IDENTITY_FIELDS = ['task_id', 'model', 'trial']
CODER_FIELDS = ['category', 'failure_reason', 'earliest_link', 'notes']
CODER_COLUMNS = IDENTITY_FIELDS + CODER_FIELDS


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
    require(audit.get('field') == 'earliest_link', 'Codebook lacks the earliest-link audit definition')
    earliest_values = list(audit.get('values', {}))
    require(earliest_values == ['SUPPORTED', 'NOT_SUPPORTED', 'INDETERMINATE'],
            'Unexpected earliest-link values in the codebook')
    codebook_hash = sha256(path)
    require(codebook_hash == FROZEN_CODEBOOK_SHA256,
            'The frozen codebook changed; review it and regenerate the coder sheets')
    return categories, stages, earliest_values, codebook_hash


def prepare(args):
    headers, catalogue = read_csv(args.catalogue)
    require(bool(catalogue), f'No cases in {args.catalogue}')
    required = {'task_id', 'model', 'model_short', 'trial', 'recorded_resolved'}
    require(required <= set(headers or []), f'Catalogue lacks fields: {sorted(required-set(headers or []))}')
    load_codebook(args.codebook)

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
        row = {
            'task_id': source['task_id'],
            'model': source['model_short'],
            'trial': source['trial'],
            **{field: '' for field in CODER_FIELDS},
        }
        rows.append(row)

    targets = [args.output_dir / 'coder_a.csv', args.output_dir / 'coder_b.csv']
    existing = [str(path) for path in targets if path.exists()]
    require(not existing, 'Refusing to overwrite coder sheets: '+', '.join(existing))
    for path in targets:
        write_csv_exclusive(path, CODER_COLUMNS, rows)
    print(f'Created {len(rows)}-row coder sheets: {targets[0]} and {targets[1]}')


def normalized_coder_rows(path, allowed_categories, allowed_earliest):
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
        category = row['category'].strip()
        reason = row['failure_reason'].strip()
        earliest_link = row['earliest_link'].strip()
        require(category in allowed_categories,
                f'Invalid/empty category {category!r} in {path}:{line}')
        require(bool(reason), f'Empty failure reason in {path}:{line}')
        require(earliest_link in allowed_earliest,
                f'Invalid/empty earliest_link {earliest_link!r} in {path}:{line}')
        clean = dict(row)
        clean.update(task_id=task_id, model=model, trial=trial, category=category,
                     failure_reason=reason, earliest_link=earliest_link,
                     notes=row['notes'].strip())
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


def compare(args):
    categories, stages, earliest_values, codebook_hash = load_codebook(args.codebook)
    allowed = categories + ['OTHER']
    coder_a = normalized_coder_rows(args.coder_a, allowed, earliest_values)
    coder_b = normalized_coder_rows(args.coder_b, allowed, earliest_values)
    require(set(coder_a) == set(coder_b), 'Coder sheets do not contain the same trials')
    require(list(coder_a) == list(coder_b), 'Coder sheets do not use the same trial order')

    annotation_headers, annotations = read_csv(args.annotations)
    require({'task_id', 'model', 'trial', 'primary_category', 'diagnosis'} <= set(annotation_headers or []),
            'Canonical annotation file lacks required fields')
    require(all(row['model'] in MODEL_SHORT for row in annotations),
            'Canonical annotations contain an unknown model ID')
    canonical = {
        (row['task_id'], MODEL_SHORT[row['model']], row['trial']): row
        for row in annotations
    }
    require(set(coder_a) == set(canonical), 'Coder trials do not match canonical failure annotations')

    require(not args.comparison.exists(), f'Refusing to overwrite {args.comparison}')
    require(not args.statistics.exists(), f'Refusing to overwrite {args.statistics}')

    rows = []
    for key in coder_a:
        a, b = coder_a[key], coder_b[key]
        original = canonical[key]
        a_label, b_label, original_label = (
            a['category'], b['category'], original['primary_category'])
        a_earliest, b_earliest = a['earliest_link'], b['earliest_link']
        rows.append({
            'task_id': a['task_id'],
            'model': a['model'],
            'trial': a['trial'],
            'canonical_category': original_label,
            'canonical_failure_reason': original['diagnosis'],
            'coder_a_category': a_label,
            'coder_a_failure_reason': a['failure_reason'],
            'coder_a_earliest_link': a_earliest,
            'coder_a_notes': a['notes'],
            'coder_b_category': b_label,
            'coder_b_failure_reason': b['failure_reason'],
            'coder_b_earliest_link': b_earliest,
            'coder_b_notes': b['notes'],
            'a_b_agree': str(a_label == b_label).lower(),
            'earliest_link_agree': str(a_earliest == b_earliest).lower(),
            'a_canonical_agree': str(a_label == original_label).lower(),
            'b_canonical_agree': str(b_label == original_label).lower(),
            'discussion_required': str(
                len({a_label, b_label, original_label}) > 1 or a_earliest != b_earliest
            ).lower(),
            'discussion_summary': '',
            'final_category': '',
            'final_failure_reason': '',
            'final_earliest_link': '',
        })

    a_labels = [row['coder_a_category'] for row in rows]
    b_labels = [row['coder_b_category'] for row in rows]
    original_labels = [row['canonical_category'] for row in rows]
    a_earliest = [row['coder_a_earliest_link'] for row in rows]
    b_earliest = [row['coder_b_earliest_link'] for row in rows]
    all_labels = allowed
    a_b = agreement(a_labels, b_labels, all_labels)
    earliest_a_b = agreement(a_earliest, b_earliest, earliest_values)
    statistics = {
        'scope': 'Locked pre-discussion labels from two additional coders',
        'n_cases': len(rows),
        'n_tasks': len({row['task_id'] for row in rows}),
        'codebook_sha256': codebook_hash,
        'coder_sheet_sha256': {
            'coder_a': sha256(args.coder_a),
            'coder_b': sha256(args.coder_b),
        },
        'subcategory_agreement': a_b,
        'subcategory_task_cluster_bootstrap': cluster_bootstrap(
            rows, all_labels, 'coder_a_category', 'coder_b_category',
            args.bootstrap_repetitions, args.seed,
        ),
        'earliest_link_agreement': earliest_a_b,
        'earliest_link_task_cluster_bootstrap': cluster_bootstrap(
            rows, earliest_values, 'coder_a_earliest_link', 'coder_b_earliest_link',
            args.bootstrap_repetitions, args.seed,
        ),
        'stage_agreement': agreement(
            [stages.get(label, 'OTHER') for label in a_labels],
            [stages.get(label, 'OTHER') for label in b_labels],
            list(dict.fromkeys(stages.values())) + ['OTHER'],
        ),
        'canonical_concordance': {
            'coder_a': agreement(a_labels, original_labels, all_labels),
            'coder_b': agreement(b_labels, original_labels, all_labels),
            'interpretation': ('Secondary concordance with the existing canonical annotation; '
                               'not a third independent-coder agreement estimate.'),
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
        'a_b_raw_agreement': a_b['raw_agreement'],
        'a_b_cohen_kappa': a_b['cohen_kappa'],
        'earliest_link_raw_agreement': earliest_a_b['raw_agreement'],
        'earliest_link_cohen_kappa': earliest_a_b['cohen_kappa'],
    }, indent=2))


def distribution(values, labels):
    counts = Counter(values)
    total = len(values)
    return {
        label: {
            'count': counts[label],
            'percent': 100 * counts[label] / total if total else 0,
        }
        for label in labels
    }


def grouped_distribution(rows, group_field, status_values):
    groups = defaultdict(list)
    for row in rows:
        groups[row[group_field]].append(row['final_earliest_link'])
    return {
        group: {
            'n': len(values),
            'earliest_link': distribution(values, status_values),
        }
        for group, values in sorted(groups.items())
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
            sum(row['final_earliest_link'] == 'SUPPORTED' for row in replicate) / len(replicate)
        )
    return {
        'method': 'task-cluster percentile bootstrap',
        'repetitions': repetitions,
        'seed': seed,
        'tasks_per_replicate': len(tasks),
        'supported_proportion_ci95': [percentile(proportions, .025), percentile(proportions, .975)],
    }


def summarize(args):
    categories, stages, earliest_values, codebook_hash = load_codebook(args.codebook)
    allowed_categories = categories + ['OTHER']
    headers, source_rows = read_csv(args.comparison)
    required = {
        'task_id', 'model', 'trial', 'discussion_required', 'discussion_summary',
        'final_category', 'final_failure_reason', 'final_earliest_link',
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
        reason = source['final_failure_reason'].strip()
        earliest_link = source['final_earliest_link'].strip()
        require(category in allowed_categories,
                f'Invalid/empty final_category {category!r} in {args.comparison}:{line}')
        require(bool(reason), f'Empty final_failure_reason in {args.comparison}:{line}')
        require(earliest_link in earliest_values,
                f'Invalid/empty final_earliest_link {earliest_link!r} in {args.comparison}:{line}')
        discussion_required = source['discussion_required'].strip().lower()
        require(discussion_required in {'true', 'false'},
                f'Invalid discussion_required in {args.comparison}:{line}')
        require(discussion_required == 'false' or bool(source['discussion_summary'].strip()),
                f'Discussion summary required in {args.comparison}:{line}')
        rows.append({
            'task_id': task_id,
            'model': model,
            'trial': trial,
            'final_category': category,
            'final_failure_reason': reason,
            'final_earliest_link': earliest_link,
            'stage': stages.get(category, 'OTHER'),
        })

    annotation_headers, annotations = read_csv(args.annotations)
    require({'task_id', 'model', 'trial'} <= set(annotation_headers or []),
            'Canonical annotation file lacks trial identity fields')
    require(all(row['model'] in MODEL_SHORT for row in annotations),
            'Canonical annotations contain an unknown model ID')
    canonical_keys = {
        (row['task_id'], MODEL_SHORT[row['model']], row['trial'])
        for row in annotations
    }
    require(seen == canonical_keys, 'Final comparison rows do not match canonical failure annotations')
    require(not args.statistics.exists(), f'Refusing to overwrite {args.statistics}')

    final_status = [row['final_earliest_link'] for row in rows]
    summary = {
        'scope': 'Reconciled final attribution decisions',
        'interpretation': (
            'SUPPORTED indicates evidence for the chronological attribution convention; '
            'it does not identify or prove a causal root cause.'
        ),
        'n_cases': len(rows),
        'n_tasks': len({row['task_id'] for row in rows}),
        'codebook_sha256': codebook_hash,
        'comparison_sha256': sha256(args.comparison),
        'final_category_counts': dict(sorted(Counter(row['final_category'] for row in rows).items())),
        'earliest_link': {
            'overall': distribution(final_status, earliest_values),
            'supported_task_cluster_bootstrap': supported_cluster_bootstrap(
                rows, args.bootstrap_repetitions, args.seed,
            ),
            'by_model': grouped_distribution(rows, 'model', earliest_values),
            'by_category': grouped_distribution(rows, 'final_category', earliest_values),
            'by_stage': grouped_distribution(rows, 'stage', earliest_values),
        },
    }
    args.statistics.parent.mkdir(parents=True, exist_ok=True)
    with args.statistics.open('x', encoding='utf-8') as stream:
        json.dump(summary, stream, indent=2)
        stream.write('\n')
    print(json.dumps({
        'statistics': str(args.statistics),
        'n_cases': len(rows),
        'earliest_link': summary['earliest_link']['overall'],
    }, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest='command', required=True)

    prepare_parser = subparsers.add_parser('prepare', help='Create blank label-blind coder sheets')
    prepare_parser.add_argument('--catalogue', type=Path, default=DEFAULT_CATALOGUE)
    prepare_parser.add_argument('--codebook', type=Path, default=DEFAULT_CODEBOOK)
    prepare_parser.add_argument('--output-dir', type=Path, default=DEFAULT_DOCS)
    prepare_parser.set_defaults(function=prepare)

    compare_parser = subparsers.add_parser('compare', help='Validate and compare completed coder sheets')
    compare_parser.add_argument('--coder-a', type=Path, default=DEFAULT_DOCS/'coder_a.csv')
    compare_parser.add_argument('--coder-b', type=Path, default=DEFAULT_DOCS/'coder_b.csv')
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
        default=DEFAULT_STATISTICS/'final_attribution_summary.json')
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
