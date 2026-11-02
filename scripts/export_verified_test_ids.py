"""Export SWE-bench Verified test-ID lists into existing ``analyse/`` folders.

Read the same Princeton SWE-bench Verified test split used by ``datavis.py``.
For each task in the archived verified ID list, write one JSON file containing
its FAIL_TO_PASS and PASS_TO_PASS lists in each model's existing task folder.
The script checks task IDs and reference patches before writing. It never
rewrites saved patches, descriptions, trajectories, or existing test-ID files.
Use ``--source-arrow`` to read a previously cached Arrow table offline.
"""

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATASET_ID = 'princeton-nlp/SWE-bench_Verified'
DATASET_REVISION = 'c104f840cc67f8b6eec6f759ebc8b2693d585d4a'
DEFAULT_IDS = ROOT / 'data' / 'data' / 'verified' / 'instance_id_list.json'
DEFAULT_ANALYSE = ROOT / 'analyse'
MODELS = (
    'claude-sonnet-4-5-20250929',
    'gemini-3-pro-preview',
    'gpt-5-2025-08-07-medium-reasoning',
)
TEST_FIELDS = ('FAIL_TO_PASS', 'PASS_TO_PASS')
SAFE_TASK = re.compile(r'[A-Za-z0-9_.-]+__[A-Za-z0-9_.-]+\Z')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_task_ids(path):
    values = json.loads(path.read_text(encoding='utf-8'))
    require(isinstance(values, list) and bool(values), f'Expected nonempty ID list: {path}')
    require(all(isinstance(task, str) and SAFE_TASK.fullmatch(task) for task in values),
            f'Unexpected task ID in {path}')
    require(len(values) == len(set(values)), f'Duplicate task ID in {path}')
    return values


def load_records(source_arrow):
    if source_arrow is not None:
        try:
            import pyarrow as pa
        except ImportError as error:
            raise ValueError('Reading --source-arrow requires pyarrow') from error
        with source_arrow.open('rb') as stream:
            rows = pa.ipc.open_stream(stream).read_all().to_pylist()
    else:
        try:
            from datasets import load_dataset
        except ImportError as error:
            raise ValueError('Install requirements.txt or use --source-arrow with pyarrow') from error
        rows = load_dataset(DATASET_ID, split='test', revision=DATASET_REVISION)
    indexed = {}
    for row in rows:
        task = row['instance_id']
        require(task not in indexed, f'Duplicate dataset task: {task}')
        indexed[task] = row
    return indexed


def test_list(row, task, field):
    raw = row[field]
    try:
        value = json.loads(raw) if isinstance(raw, str) else raw
    except json.JSONDecodeError as error:
        raise ValueError(f'Invalid JSON in {field} for {task}') from error
    require(isinstance(value, list) and all(isinstance(test, str) for test in value),
            f'Expected a list of test IDs in {field} for {task}')
    return value


def export(ids_file, analyse_root, source_arrow, check):
    task_ids = read_task_ids(ids_file)
    source = load_records(source_arrow)
    require(set(task_ids) <= set(source),
            f'Dataset is missing {len(set(task_ids) - set(source))} archived tasks')

    expected = {}
    counts = {field: 0 for field in TEST_FIELDS}
    for task in task_ids:
        row = source[task]
        lists = {field: test_list(row, task, field) for field in TEST_FIELDS}
        for field in TEST_FIELDS:
            counts[field] += len(lists[field])
        contents = json.dumps(lists, ensure_ascii=True, indent=2) + '\n'
        for model in MODELS:
            folder = analyse_root / model / task
            require(folder.is_dir(), f'Missing task folder: {folder}')
            gold = folder / f'{task}_gold.patch'
            require(gold.is_file(), f'Missing reference patch: {gold}')
            require(gold.read_text(encoding='utf-8') == row['patch'],
                    f'Reference patch differs from dataset for {model}/{task}')
            target = folder / f'{task}_test_ids.json'
            expected[target] = contents

    # Check every target before creating any file; an existing difference
    # indicates a source mismatch or a manually edited artifact.
    new_files = []
    for target, contents in expected.items():
        if target.exists():
            require(target.is_file(), f'Test-ID target is not a file: {target}')
            require(target.read_text(encoding='utf-8') == contents,
                    f'Existing test-ID file differs: {target}')
        else:
            require(not check, f'Missing test-ID file: {target}')
            new_files.append((target, contents))
    for target, contents in new_files:
        with target.open('x', encoding='utf-8') as stream:
            stream.write(contents)
    return len(task_ids), len(expected), len(new_files), counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ids-file', type=Path, default=DEFAULT_IDS)
    parser.add_argument('--analyse-root', type=Path, default=DEFAULT_ANALYSE)
    parser.add_argument('--source-arrow', type=Path,
                        help='Previously cached SWE-bench Verified Arrow test split')
    parser.add_argument('--check', action='store_true', help='Verify outputs without writing')
    args = parser.parse_args()
    try:
        n_tasks, n_files, created, counts = export(
            args.ids_file, args.analyse_root, args.source_arrow, args.check,
        )
    except (KeyError, OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps({
        'source_dataset': DATASET_ID,
        'source_revision': DATASET_REVISION,
        'tasks': n_tasks,
        'model_task_files': n_files,
        'created': created,
        'test_ids_across_unique_tasks': counts,
    }, indent=2))


if __name__ == '__main__':
    main()
