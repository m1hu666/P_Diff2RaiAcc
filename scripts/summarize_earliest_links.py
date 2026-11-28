"""Resolve and count final chronological-link judgments for all failed trials.

Read the three English coder CSVs, canonical final categories, and explicit
discussion or adjudication decisions. Missing coder statuses become
INDETERMINATE. Explicit decisions take priority. For unchanged categories, a
status wins when it receives at least two of the three votes. A provisional
INDETERMINATE result or a changed category requires an explicit evidence-based
adjudication before final output.
Write a trial-level result, grouped count/percentage table, and readable report under
result/Statistics results/taxonomy_reliability. No source labels are modified.
"""

import argparse
import csv
import os
from collections import Counter
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT/'docs/taxonomy_methodology'
MODEL_IDS = {
    'Claude': 'claude-sonnet-4-5-20250929',
    'Gemini': 'gemini-3-pro-preview',
    'GPT': 'gpt-5-2025-08-07-medium-reasoning',
}
MODEL_SHORT = {value: key for key, value in MODEL_IDS.items()}
STATUSES = ('SUPPORTED', 'NOT_SUPPORTED', 'INDETERMINATE')


def read_csv(path):
    with path.open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def key(row):
    return row['task_id'], row['model'], row['trial']


def index(rows, name):
    result = {key(row): row for row in rows}
    if not rows or len(result) != len(rows):
        raise ValueError(f'Empty or duplicated trial identities: {name}')
    return result


def resolve_status(reviewed, final, statuses, explicit=None):
    if explicit is not None:
        return explicit, 'discussion_decision'
    if reviewed != final:
        return 'INDETERMINATE', 'changed_category_not_reassessed'
    status, votes = Counter(statuses).most_common(1)[0]
    if votes >= 2:
        return status, f'majority_{status.lower()}'
    return 'INDETERMINATE', 'no_majority'


def resolve_reviews(coder_paths, annotations_path, decisions_path, codebook_path):
    import json
    categories = [r['code'] for r in json.loads(codebook_path.read_text())['categories']]
    source = read_csv(annotations_path)
    canonical = {}
    for row in source:
        short = MODEL_SHORT[row['model']]
        trial_key = row['task_id'], short, row['trial']
        if trial_key in canonical or row['primary_category'] not in categories:
            raise ValueError(f'Invalid canonical annotation: {trial_key}')
        canonical[trial_key] = row
    coders = []
    for path in coder_paths:
        rows = read_csv(path)
        records = index(rows, path.name)
        if set(records) != set(canonical):
            raise ValueError(f'Coder coverage differs from final annotations: {path.name}')
        for trial_key, row in records.items():
            status = row['earliest_link'].strip().upper() or 'INDETERMINATE'
            if status not in STATUSES:
                raise ValueError(f'Invalid earliest_link in {path.name}: {trial_key}')
            row['earliest_link'] = status
        coders.append(records)
    decisions = index(read_csv(decisions_path), decisions_path.name)
    if not set(decisions) <= set(canonical):
        raise ValueError('Explicit decisions include unknown trials')
    for trial_key, row in decisions.items():
        if (row['final_category'] != canonical[trial_key]['primary_category']
                or row['final_earliest_link'] not in {'SUPPORTED', 'NOT_SUPPORTED'}
                or not row['reason'].strip()):
            raise ValueError(f'Invalid or stale explicit decision: {trial_key}')
    resolved = []
    for trial_key in coders[0]:
        reviewed = [coder[trial_key]['current_category'] for coder in coders]
        if len(set(reviewed)) != 1:
            raise ValueError(f'Coders received different categories: {trial_key}')
        statuses = [coder[trial_key]['earliest_link'] for coder in coders]
        final_category = canonical[trial_key]['primary_category']
        override = decisions.get(trial_key)
        status, basis = resolve_status(
            reviewed[0], final_category, statuses,
            override['final_earliest_link'] if override else None,
        )
        if status == 'INDETERMINATE':
            raise ValueError(
                f'Unadjudicated final earliest_link for {trial_key}; add an explicit '
                'SUPPORTED or NOT_SUPPORTED adjudication decision'
            )
        resolved.append({
            'task_id': trial_key[0], 'model': trial_key[1], 'trial': trial_key[2],
            'reviewed_category': reviewed[0], 'final_category': final_category,
            **{f'coder_{name}_earliest_link': value
               for name, value in zip(('a', 'b', 'c'), statuses)},
            'final_earliest_link': status, 'decision_basis': basis,
        })
    return resolved, categories


def summarize(rows, categories):
    groups = [('overall', 'All', rows)]
    groups += [('model', model, [r for r in rows if r['model'] == model])
               for model in MODEL_IDS]
    groups += [('category', category, [r for r in rows if r['final_category'] == category])
               for category in categories]
    output = []
    for grouping, name, selected in groups:
        counts = Counter(r['final_earliest_link'] for r in selected)
        total = len(selected)
        output.append({
            'grouping': grouping, 'group': name, 'total': total,
            **{status: counts[status] for status in STATUSES},
            **{status+'_percent': 100*counts[status]/total if total else ''
               for status in STATUSES},
        })
    return output


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def report_text(rows, summary, decisions_path, report):
    overall = summary[0]
    basis = Counter(r['decision_basis'] for r in rows)
    relative = quote(Path(os.path.relpath(decisions_path, report.parent)).as_posix(), safe='/._-')
    lines = [
        '# Final chronological-link audit', '',
        f'The audit covers {len(rows)} failed trials on {len({r["task_id"] for r in rows})} tasks. '
        'The primary categories are the canonical post-discussion categories.', '',
        '| Final earliest_link | Count | Percent of all failed trials |',
        '| --- | --- | --- |',
        *[f'| {status} | {overall[status]} | {overall[status+"_percent"]:.2f}% |'
          for status in STATUSES], '',
        f'Explicit [discussion and adjudication decisions]({relative}) take priority. '
        'For remaining trials, '
        'when the primary category is unchanged, the status receiving at least two of '
        'the three coder votes becomes final. A majority of INDETERMINATE votes, a '
        'three-way split, or a changed category produces a provisional INDETERMINATE '
        'result that must be adjudicated as SUPPORTED or NOT_SUPPORTED. Votes on a '
        'replaced category cannot be transferred to its replacement. '
        'Blank coder statuses were filled with INDETERMINATE before applying this rule.', '',
        'The vote is symmetric across SUPPORTED, NOT_SUPPORTED, and INDETERMINATE. '
        'A majority result means at least two coders selected that status; it need not '
        'be unanimous. The completed adjudication assigns SUPPORTED to the provisional '
        'V-category cases under the validation-stage rule and resolves every other '
        'provisional case from its trajectory, patch, repository-state, and evaluation '
        'evidence. Explicit decisions may supersede the vote. Neither '
        'SUPPORTED nor NOT_SUPPORTED establishes or disproves a causal root cause.', '',
        f'Resolution basis: {basis["discussion_decision"]} explicit decisions; '
        'majority-vote results of '
        f'SUPPORTED {basis["majority_supported"]}, '
        f'NOT_SUPPORTED {basis["majority_not_supported"]}, and '
        f'INDETERMINATE {basis["majority_indeterminate"]}; '
        f'{basis["no_majority"]} three-way splits; and '
        f'{basis["changed_category_not_reassessed"]} changed categories without a new '
        'chronological-link assessment.', '',
        '## Counts by final category', '',
        '| Category | SUPPORTED | NOT_SUPPORTED | INDETERMINATE | Total |',
        '| --- | --- | --- | --- | --- |',
        *[f'| {r["group"]} | {r["SUPPORTED"]} | {r["NOT_SUPPORTED"]} | '
          f'{r["INDETERMINATE"]} | {r["total"]} |'
          for r in summary if r['grouping'] == 'category'], '',
        '[Trial-level decisions](final_earliest_links.csv) retain all three coder statuses '
        'and the resolution basis. The [grouped table](earliest_link_summary.csv) adds '
        'model/category counts and percentages. Rebuild with:', '',
        '```bash', 'python3 scripts/summarize_earliest_links.py', '```', '',
    ]
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('a', 'b', 'c'):
        parser.add_argument('--coder-'+name, type=Path, default=DOCS/f'coder_{name}.csv')
    parser.add_argument('--annotations', type=Path,
                        default=ROOT/'FINAL-CODEBOOK/failure_annotations.csv')
    parser.add_argument('--codebook', type=Path,
                        default=ROOT/'FINAL-CODEBOOK/failure_codebook.json')
    parser.add_argument('--decisions', type=Path, default=DOCS/'earliest_link_decisions.csv')
    parser.add_argument('--output', type=Path,
                        default=ROOT/'result/Statistics results/taxonomy_reliability')
    args = parser.parse_args()
    try:
        rows, categories = resolve_reviews(
            [getattr(args, 'coder_'+name) for name in ('a', 'b', 'c')],
            args.annotations, args.decisions, args.codebook,
        )
        summary = summarize(rows, categories)
        write_csv(args.output/'final_earliest_links.csv', rows)
        write_csv(args.output/'earliest_link_summary.csv', summary)
        report = args.output/'README.md'
        report.write_text(report_text(rows, summary, args.decisions, report), encoding='utf-8')
    except (KeyError, OSError, ValueError) as error:
        parser.error(str(error))
    overall = summary[0]
    print(f'Final earliest_link for {len(rows)} failed trials:')
    for status in STATUSES:
        print(f'{status}: {overall[status]} ({overall[status+"_percent"]:.2f}%)')


if __name__ == '__main__':
    main()
