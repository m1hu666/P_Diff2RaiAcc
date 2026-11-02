"""Build a readable, linked packet for independent checks of existing labels.

The packet presents the authors' current task summaries and trial diagnoses
alongside links to the archived source materials. It adds no new evidence or
category judgments. Run with ``--check`` to verify the generated page is current.
"""

import argparse
import csv
import hashlib
import json
import os
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CATALOGUE = ROOT / 'result' / 'Statistics results' / 'failure_trial_catalog.csv'
DEFAULT_ANNOTATIONS = ROOT / 'docs' / 'failure_analysis' / 'failure_annotations.csv'
DEFAULT_NOTES = ROOT / 'docs' / 'failure_analysis' / 'failure_case_notes.json'
DEFAULT_CODEBOOK = ROOT / 'docs' / 'failure_analysis' / 'failure_codebook.json'
DEFAULT_OUTPUT = ROOT / 'docs' / 'taxonomy_methodology' / 'VERIFICATION_CASES.md'
MATERIALS = (
    ('Issue', 'problem_statement_path'),
    ('Hints', 'hints_path'),
    ('Reference patch', 'gold_patch_path'),
    ('Evaluation tests', 'test_patch_path'),
)
MODEL_ORDER = {'Claude': 0, 'Gemini': 1, 'GPT': 2}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_csv(path):
    with path.open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def cell(value):
    return ' '.join(str(value).split()).replace('|', '\\|')


def link(path_string, output):
    source = ROOT / path_string
    require(source.is_file(), f'Missing review artifact: {path_string}')
    relative = Path(os.path.relpath(source, output.parent)).as_posix()
    return quote(relative, safe='/._-')


def render(catalogue_path, annotations_path, notes_path, codebook_path, output):
    rows = read_csv(catalogue_path)
    annotations = read_csv(annotations_path)
    notes = json.loads(notes_path.read_text(encoding='utf-8'))
    codebook = json.loads(codebook_path.read_text(encoding='utf-8'))
    names = {category['code']: category['name'] for category in codebook['categories']}
    require(bool(rows), 'The failure catalogue is empty')
    require(len(rows) == len(annotations), 'Catalogue and annotation row counts differ')
    annotated = {
        (row['task_id'], row['model'], row['trial']): row
        for row in annotations
    }
    require(len(annotated) == len(annotations), 'Duplicate canonical trial annotations')
    seen = set()
    by_task = defaultdict(list)
    for row in rows:
        key = row['task_id'], row['model'], row['trial']
        require(key in annotated and key not in seen, f'Unexpected or duplicate trial: {key}')
        seen.add(key)
        original = annotated[key]
        require(row['recorded_resolved'] == 'False', f'Resolved trial in failure catalogue: {key}')
        require(row['primary_category'] == original['primary_category'], f'Category mismatch: {key}')
        require(row['diagnosis'] == original['diagnosis'], f'Diagnosis mismatch: {key}')
        require(row['primary_category'] in names, f'Unknown category: {key}')
        require(row['model_short'] in MODEL_ORDER, f'Unknown model: {key}')
        by_task[row['task_id']].append(row)
    require(seen == set(annotated), 'Canonical trial missing from catalogue')
    require(set(by_task) == set(notes), 'Task notes do not match failed tasks')

    tasks = sorted(by_task, key=lambda task: (
        task.split('__', 1)[0], len(by_task[task]), task,
    ))
    lines = [
        '# Existing failure assignments: coder review packet',
        '',
        'This page presents the authors\' current labels and analyses for independent '
        'verification by Coders A, B, and C. It is generated from the canonical '
        'annotations and task notes; the descriptions are existing interpretations, '
        'not additional evidence. Check each trial against the '
        '[failure codebook](../failure_analysis/FAILURE_CODEBOOK.md) and the linked '
        'materials, then record both the category decision and chronological-link '
        'judgment in the assigned coder sheet using the '
        '[coder instructions](CODING_GUIDE.md).',
        '',
        'Each task lists shared source materials once and provides a candidate patch '
        'and trajectory for each failed trial. The linked benchmark test-ID file '
        'lists expected tests from the dataset, not this trial\'s execution outcome. '
        'Some retained assignments explicitly note that further verification is needed.',
        '',
        '## Task index',
        '',
    ]
    for task in tasks:
        count = len(by_task[task])
        lines.append(f'- [{task}](#task-{task}) ({count} {"trial" if count == 1 else "trials"})')
    for task in tasks:
        trials = sorted(by_task[task], key=lambda row: (
            MODEL_ORDER[row['model_short']], int(row['trial']),
        ))
        first = trials[0]
        for _, field in MATERIALS:
            fingerprints = {
                hashlib.sha256((ROOT / row[field]).read_bytes()).digest()
                for row in trials
            }
            require(len(fingerprints) == 1, f'Nonshared {field} for {task}')
        test_ids_paths = {
            Path(row['model_patch_path']).parent / f'{task}_test_ids.json'
            for row in trials
        }
        require(all((ROOT / path).is_file() for path in test_ids_paths),
                f'Missing benchmark test-ID file for {task}')
        require(len({hashlib.sha256((ROOT / path).read_bytes()).digest()
                     for path in test_ids_paths}) == 1,
                f'Inconsistent benchmark test-ID files for {task}')
        task_note = notes[task]
        materials = ' · '.join(
            f'[{label}]({link(first[field], output)})'
            for label, field in MATERIALS
        )
        test_ids_path = Path(first['model_patch_path']).parent / f'{task}_test_ids.json'
        materials += f' · [Benchmark test IDs]({link(str(test_ids_path), output)})'
        lines.extend([
            '',
            f'<a id="task-{task}"></a>',
            '',
            f'### {task} ({len(trials)} failed trials)',
            '',
            f'**Task summary:** {cell(task_note["issue_summary"])}',
            '',
            f'**Current task analysis:** {cell(task_note["diagnosis_summary"])}',
            '',
            f'**Shared materials:** {materials}',
            '',
            '| Trial | Current label | Current diagnosis | Candidate patch | Trajectory |',
            '| --- | --- | --- | --- | --- |',
        ])
        for row in trials:
            label = row['primary_category']
            lines.append(
                f'| {row["model_short"]}-{row["trial"]} '
                f'| {label} {cell(names[label])} '
                f'| {cell(row["diagnosis"])} '
                f'| [Patch]({link(row["model_patch_path"], output)}) '
                f'| [Log]({link(row["trajectory_path"], output)}) |'
            )
        if task_note['interpretation_note']:
            lines.extend(['', f'**Interpretation note:** {cell(task_note["interpretation_note"])}'])
    lines.append('')
    return '\n'.join(lines), len(rows), len(tasks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalogue', type=Path, default=DEFAULT_CATALOGUE)
    parser.add_argument('--annotations', type=Path, default=DEFAULT_ANNOTATIONS)
    parser.add_argument('--notes', type=Path, default=DEFAULT_NOTES)
    parser.add_argument('--codebook', type=Path, default=DEFAULT_CODEBOOK)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--check', action='store_true', help='Check output without changing it')
    args = parser.parse_args()
    try:
        content, n_trials, n_tasks = render(
            args.catalogue, args.annotations, args.notes, args.codebook, args.output,
        )
        if args.check:
            require(args.output.exists(), f'Missing review packet: {args.output}')
            require(args.output.read_text(encoding='utf-8') == content,
                    f'Outdated review packet: {args.output}')
        else:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(content, encoding='utf-8')
    except (KeyError, OSError, ValueError) as error:
        parser.error(str(error))
    print(f'{"Checked" if args.check else "Wrote"} {n_trials} trials across {n_tasks} tasks: {args.output}')


if __name__ == '__main__':
    main()
