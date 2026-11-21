"""Resolve and count final chronological-link judgments for all failed trials.

Read the three English coder CSVs, canonical final categories, and explicit
discussion decisions. Missing coder statuses become INDETERMINATE. Discussion
decisions take priority. For unchanged categories, any NOT_SUPPORTED vote
produces a negative flag; SUPPORTED requires all three votes. Changed categories
without reassessment and all remaining cases become INDETERMINATE.
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
    if 'NOT_SUPPORTED' in statuses:
        return 'NOT_SUPPORTED', 'at_least_one_not_supported'
    if all(status == 'SUPPORTED' for status in statuses):
        return 'SUPPORTED', 'three_supported_statuses'
    return 'INDETERMINATE', 'incomplete_supported_assessment'


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
        raise ValueError('Discussion decisions include unknown trials')
    for trial_key, row in decisions.items():
        if (row['final_category'] != canonical[trial_key]['primary_category']
                or row['final_earliest_link'] not in STATUSES or not row['reason'].strip()):
            raise ValueError(f'Invalid or stale discussion decision: {trial_key}')
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
    any_negative = sum(any(r[f'coder_{name}_earliest_link'] == 'NOT_SUPPORTED'
                           for name in ('a', 'b', 'c')) for r in rows)
    changed_negative = sum(r['reviewed_category'] != r['final_category']
                           and any(r[f'coder_{name}_earliest_link'] == 'NOT_SUPPORTED'
                                   for name in ('a', 'b', 'c')) for r in rows)
    relative = quote(Path(os.path.relpath(decisions_path, report.parent)).as_posix(), safe='/._-')
    lines = [
        '# Final chronological-link audit', '',
        f'The audit covers {len(rows)} failed trials on {len({r["task_id"] for r in rows})} tasks. '
        'The primary categories are the canonical post-discussion categories.', '',
        '| Final earliest_link | Count | Percent of all failed trials |',
        '| --- | --- | --- |',
        *[f'| {status} | {overall[status]} | {overall[status+"_percent"]:.2f}% |'
          for status in STATUSES], '',
        f'Explicit [discussion decisions]({relative}) take priority. For remaining trials, '
        'use NOT_SUPPORTED as a conservative negative flag when the primary category '
        'is unchanged and at least one coder recorded NOT_SUPPORTED. Use SUPPORTED '
        'only when the category is unchanged and all three coder values are SUPPORTED. '
        'All other cases are INDETERMINATE. '
        'Blank coder statuses were filled with INDETERMINATE before applying this rule.', '',
        'An aggregate NOT_SUPPORTED status records at least one negative assessment '
        'or an explicit final discussion decision; it does not imply unanimous '
        'reviewer agreement or establish that a causal claim has been disproved.', '',
        f'At least one coder recorded NOT_SUPPORTED on {any_negative} pre-discussion '
        f'trials. Of these, {changed_negative} have a changed primary category and '
        'are not transferred automatically to the new category.', '',
        f'The INDETERMINATE total includes {basis["changed_category_not_reassessed"]} trials '
        'whose category changed without a new chronological-link assessment and '
        f'{basis["incomplete_supported_assessment"]} trials with incomplete or '
        'indeterminate support and no eligible negative assessment. '
        'These entries are not counted as NOT_SUPPORTED. SUPPORTED is an observational '
        'evidence-link judgment and does not establish a causal root cause.', '',
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
                        default=ROOT/'docs/failure_analysis/failure_annotations.csv')
    parser.add_argument('--codebook', type=Path,
                        default=ROOT/'docs/failure_analysis/failure_codebook.json')
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
