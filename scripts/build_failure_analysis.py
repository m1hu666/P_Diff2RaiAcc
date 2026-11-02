"""Build and validate the public failure-analysis catalogue.

Inputs are the final trial annotations, category codebook, task-level notes, and
archived experiment data. The human-readable report is written to
``result/analyse.md`` and generated CSV/JSON summaries to
``result/Statistics results``. The script is offline and performs no model calls,
benchmark execution, or automatic causal classification.
"""

import argparse
import csv
import hashlib
import json
import os
import re
from urllib.parse import unquote
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
FAILURE_DOCS = ROOT / 'docs' / 'failure_analysis'
DEFAULT_OUTPUT = ROOT / 'result' / 'Statistics results'
MODELS = {
    'Claude': 'claude-sonnet-4-5-20250929',
    'Gemini': 'gemini-3-pro-preview',
    'GPT': 'gpt-5-2025-08-07-medium-reasoning',
}
SHORT = {value: key for key, value in MODELS.items()}
VERIFIED_MODEL_NAMES = {
    MODELS['Claude']: 'claude-sonnet-4-5-20250929',
    MODELS['Gemini']: 'gemini/gemini-3-pro-preview',
    MODELS['GPT']: 'gpt-5-2025-08-07',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path):
    with path.open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def write_csv(path, rows, fieldnames=None):
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=fieldnames or list(rows[0]),
            lineterminator='\n',
        )
        writer.writeheader()
        writer.writerows(rows)


def english_portable(content, name):
    personal = re.compile(r'/(?:home|Users)/[^/\\\s"\x27<>]+|[A-Za-z]:\\Users\\[^\\\s]+')
    require(not personal.search(content), f'Personal path in {name}')
    require(not any('\u4e00' <= c <= '\u9fff' for c in content), f'Non-English text in {name}')


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def table(headers, rows):
    return '\n'.join([
        '| ' + ' | '.join(headers) + ' |',
        '| ' + ' | '.join('---' for _ in headers) + ' |',
        *['| ' + ' | '.join(cell(x) for x in row) + ' |' for row in rows],
    ])


def link(path, report):
    return Path(os.path.relpath(path, report.parent)).as_posix().replace(' ', '%20')


def load_inputs(root, annotations, codebook_path, notes_path):
    codebook = json.loads(codebook_path.read_text(encoding='utf-8'))
    categories = {r['code']: r for r in codebook['categories']}
    require(len(categories) == len(codebook['categories']), 'Duplicate category codes')
    notes = json.loads(notes_path.read_text(encoding='utf-8'))
    annotation_rows = read_csv(annotations)
    required_columns = {
        'task_id', 'model', 'trial', 'primary_category', 'diagnosis',
        'verified_patch_sha256', 'trajectory_sha256',
    }
    require(bool(annotation_rows), 'No failure annotations found')
    require(set(annotation_rows[0]) == required_columns,
            f'Unexpected annotation columns: {set(annotation_rows[0])}')
    for path in (annotations, codebook_path, notes_path):
        english_portable(path.read_text(encoding='utf-8'), path.name)
    labels = {}
    input_paths = []
    for model in MODELS.values():
        model_tasks = None
        for trial in range(1, 4):
            path = root / f'data/data/verified/{model}/round{trial}.json'
            data = json.loads(path.read_text(encoding='utf-8'))
            input_paths.append(path)
            require(len(data) > 0, f'Empty verified dataset: {model}, trial {trial}')
            require(model_tasks is None or set(data) == model_tasks, f'Task mismatch: {model}, trial {trial}')
            model_tasks = set(data)
            for task, item in data.items():
                require(type(item['label']) is bool, f'Non-boolean outcome: {task}')
                require(item['instance_id'] == task, f'Instance ID mismatch: {task}')
                require(item['model_name_or_path'] == VERIFIED_MODEL_NAMES[model], f'Model ID mismatch: {task}')
                labels[(task, model, trial)] = item
    task_sets = [{task for task, m, _ in labels if m == model} for model in MODELS.values()]
    require(all(tasks == task_sets[0] for tasks in task_sets), 'Models do not share the same tasks')
    expected_failed = {key for key, item in labels.items() if item['label'] is False}
    seen = set()
    catalogue = []
    for annotation in annotation_rows:
        task, model, trial = annotation['task_id'], annotation['model'], int(annotation['trial'])
        key = task, model, trial
        require(key not in seen, f'Duplicate annotation: {key}')
        seen.add(key)
        require(key in expected_failed, f'Annotation is not a recorded failure: {key}')
        category = annotation['primary_category']
        require(category in categories, f'Unknown category: {category}')
        require(bool(annotation['diagnosis'].strip()), f'Empty diagnosis: {key}')
        item = labels[key]
        patch_hash = hashlib.sha256(item['model_patch'].encode('utf-8')).hexdigest()
        require(patch_hash == annotation['verified_patch_sha256'], f'Annotated patch changed: {key}')
        folder = f'analyse/{model}/{task}'
        paths = {
            'model_patch_path': f'{folder}/{trial}{task}_model.patch',
            'gold_patch_path': f'{folder}/{task}_gold.patch',
            'test_patch_path': f'{folder}/{task}_test.patch',
            'problem_statement_path': f'{folder}/{task}_problem_statement.txt',
            'hints_path': f'{folder}/{task}_hints.txt',
            'trajectory_path': f'data/traj/{model}/round{trial}/{task}/{task}.traj.json',
            'verified_path': f'data/data/verified/{model}/round{trial}.json',
        }
        for field, suffix in (('gold_patch_path','gold.patch'), ('test_patch_path','test.patch'),
                              ('problem_statement_path','problem_statement.txt'), ('hints_path','hints.txt')):
            if not (root/paths[field]).is_file():
                alternatives = [f'analyse/{m}/{task}/{task}_{suffix}' for m in MODELS.values()
                                if (root/f'analyse/{m}/{task}/{task}_{suffix}').is_file()]
                require(bool(alternatives),f'Missing shared task evidence: {task}, {suffix}')
                paths[field] = alternatives[0]
        for path in paths.values():
            require((root/path).is_file(), f'Missing evidence: {path}')
        trajectory = root/paths['trajectory_path']
        require(sha256(trajectory) == annotation['trajectory_sha256'], f'Annotated trajectory changed: {key}')
        input_paths.extend(root/p for p in paths.values())
        definition = categories[category]
        catalogue.append({
            'trial_id': f'{task}::{SHORT[model]}::trial{trial}',
            'task_id': task, 'model': model, 'model_short': SHORT[model], 'trial': trial,
            'recorded_resolved': False, 'stage': definition['stage'],
            'primary_category': category, 'subcategory': definition['name'],
            'legacy_category': definition['legacy_code'],
            'diagnosis': annotation['diagnosis'], **paths,
            'verified_patch_sha256': patch_hash, 'trajectory_sha256': annotation['trajectory_sha256'],
        })
    require(seen == expected_failed, f'Missing failed-trial annotations: {sorted(expected_failed - seen)}')
    failed_tasks = {r['task_id'] for r in catalogue}
    require(failed_tasks <= set(notes), f'Missing case notes: {sorted(failed_tasks - set(notes))}')
    require(set(notes) <= failed_tasks, f'Case notes without a recorded failure: {sorted(set(notes) - failed_tasks)}')
    for task, note in notes.items():
        require(set(note) == {'issue_summary', 'diagnosis_summary', 'interpretation_note'}, f'Invalid case fields: {task}')
        require(note['issue_summary'] and note['diagnosis_summary'], f'Empty case summary: {task}')
    catalogue.sort(key=lambda r: (r['task_id'], list(MODELS).index(r['model_short']), r['trial']))
    return catalogue, labels, categories, notes, sorted(set(input_paths))


def summarize(catalogue, labels, categories):
    failed_tasks = {row['task_id'] for row in catalogue}
    total = len(catalogue)
    failures = Counter(r['model_short'] for r in catalogue)
    model_summary = []
    for short, model in MODELS.items():
        count = sum(m == model for _, m, _ in labels)
        model_summary.append({
            'model': model, 'model_short': short, 'attempts': count,
            'recorded_failures': failures[short], 'failure_rate_percent': 100*failures[short]/count,
            'tasks_with_failure': len({r['task_id'] for r in catalogue if r['model'] == model}),
        })
    summaries = {}
    for group in ('primary_category', 'stage'):
        values = list(categories) if group == 'primary_category' else list(dict.fromkeys(c['stage'] for c in categories.values()))
        rows = []
        for value in values:
            selected = [r for r in catalogue if r[group] == value]
            row = {group: value}
            if group == 'primary_category':
                row.update(subcategory=categories[value]['name'],
                           stage=categories[value]['stage'])
            row.update(assigned_trials=len(selected), share_of_all_failures_percent=100*len(selected)/total,
                       distinct_tasks=len({r['task_id'] for r in selected}))
            for short, model in MODELS.items():
                n = sum(r['model'] == model for r in selected)
                attempted = sum(m == model for _, m, _ in labels)
                row[f'{short}_count'] = n
                row[f'{short}_share_of_model_failures_percent'] = 100*n/failures[short] if failures[short] else 0
                row[f'{short}_incidence_per_all_attempts_percent'] = 100*n/attempted
                row[f'{short}_distinct_tasks'] = len({r['task_id'] for r in selected if r['model'] == model})
            rows.append(row)
        require(sum(r['assigned_trials'] for r in rows) == total, f'Invalid {group} total')
        summaries[group] = rows
    task_rows = []
    for task in sorted(failed_tasks):
        selected = [r for r in catalogue if r['task_id'] == task]
        row = {'task_id': task, 'failed_trials': len(selected)}
        for short, model in MODELS.items():
            row[f'{short}_outcomes'] = ' '.join('S' if labels[(task,model,t)]['label'] else 'F' for t in range(1,4))
            row[f'{short}_failure_categories'] = ' '.join(
                next((r['primary_category'] for r in selected if r['model'] == model and r['trial'] == t), '-')
                for t in range(1,4))
        task_rows.append(row)
    return model_summary, summaries['primary_category'], summaries['stage'], task_rows


def report_text(report, root, out, catalogue, labels, categories, notes, model_rows, category_rows, stage_rows, task_rows):
    total = len(catalogue)
    tasks = {key[0] for key in labels}
    failed_tasks = {r['task_id'] for r in catalogue}
    reference = lambda filename: link(out/filename, report)
    package_link = lambda filename: link(FAILURE_DOCS/filename, report)
    lines = ['# Failure Analysis and Trial-Level Catalogue', '',
             f'The evaluated dataset contains {len(labels):,} trials: {len(tasks)} tasks, three model groups, and three trials per task. '
             f'The archived labels record {len(labels)-total} resolved trials and {total} unresolved trials ({100*total/len(labels):.1f}%). '
             f'The unresolved trials span {len(failed_tasks)} tasks. Every unresolved trial is listed individually in Appendix A with its model, trial number, and primary category.', '',
             'The five stages and eleven subcategories follow the study taxonomy. '
             f'The accompanying [catalogue CSV]({reference("failure_trial_catalog.csv")}) includes a trial-specific diagnosis and a repository-relative index of available patches, issue descriptions, hints, trajectories, and verified outcome records. '
             f'The [codebook]({package_link("FAILURE_CODEBOOK.md")}) defines the category boundaries.', '',
             'Artifact paths are provided for navigation and reproducibility. They identify the archived inputs used by the public catalogue without asserting that every linked artifact independently establishes the assigned cause.', '',
             '## Scope and interpretation', '',
             'Each unresolved trial retains one primary category. Secondary defects may coexist, but are not counted again. '
             'Assignments awaiting further verification remain in their existing categories, with evidence limitations stated in their diagnoses and case notes; retention does not mean that a recheck confirmed the attribution. '
             'An evaluation outcome and its qualitative explanation are separate: a failed label does not establish a cause, and a difference from the reference patch does not establish incorrectness. '
             'In particular, V1/V2 annotations identify a specification or representation distinction; they do not automatically establish that the patch is semantically correct or that the benchmark is invalid.', '',
             'The counts below are descriptive. The three trials on one task and the model results for that task are dependent. '
             'Category percentages do not constitute model-comparison significance tests, and the unresolved trials are not treated as independent statistical samples. '
             'Within-model percentages use that model\'s number of failures as the denominator. The CSV summaries additionally report category incidence among all evaluated attempts per model and the number of distinct tasks. '
             'Task coverage can overlap across categories, so distinct-task counts must not be added across rows. The annotations are study data; they do not constitute a new independent-coder agreement study.', '',
             '## Recorded outcomes', '',
             table(['Model', 'Attempts', 'Unresolved trials', 'Failure rate', 'Tasks with a failure'],
                   [(r['model_short'],r['attempts'],r['recorded_failures'],f"{r['failure_rate_percent']:.1f}%",r['tasks_with_failure']) for r in model_rows]), '',
             'Model groups are Claude (`claude-sonnet-4-5-20250929`), Gemini (`gemini-3-pro-preview`), and GPT (`gpt-5-2025-08-07-medium-reasoning`). '
             'Trial numbers identify the archived rounds and do not imply paired random seeds across model providers.', '',
             '## Distribution by broader stage', '',
             table(['Stage','Claude, n (%)','Gemini, n (%)','GPT, n (%)','Total, n (%)','Distinct tasks'],
                   [(r['stage'],*[f"{r[m+'_count']} ({r[m+'_share_of_model_failures_percent']:.1f}%)" for m in MODELS],
                     f"{r['assigned_trials']} ({r['share_of_all_failures_percent']:.1f}%)",r['distinct_tasks']) for r in stage_rows]), '',
             '## Distribution by subcategory', '',
             table(['Code','Broader stage','Subcategory','Claude','Gemini','GPT','Total','Share of failures','Distinct tasks'],
                   [(r['primary_category'],r['stage'],r['subcategory'],*[r[m+'_count'] for m in MODELS],r['assigned_trials'],
                     f"{r['share_of_all_failures_percent']:.1f}%",r['distinct_tasks']) for r in category_rows]), '',
             'The largest category is S1 (partial or incomplete logic). Its count describes the assigned repair failures in this dataset; '
             'it does not demonstrate a general reasoning limit or establish that localization is solved. The I1 category counts primary execution failures, '
             'so it also does not measure every transient tool error recovered during otherwise successful or differently classified trajectories.', '',
             '## Task-level outcome index', '',
             'S denotes a recorded success and F a recorded failure. Within each model cell, the order is trial 1, trial 2, trial 3. '
             'A dash in the CSV category columns denotes a successful trial, which receives no failure category.', '',
             table(['Task','Claude','Gemini','GPT','Unresolved / 9','Primary categories'],
                   [(f"[{r['task_id']}](#case-{r['task_id']})",*[r[m+'_outcomes'] for m in MODELS],r['failed_trials'],
                     ', '.join(code for code in categories if any(x['task_id']==r['task_id'] and x['primary_category']==code for x in catalogue))) for r in task_rows]), '',
             '## Case analyses', '',
             'The following cases cover every task with an unresolved trial and summarize the task requirements, recorded outcomes, and assigned failure-mode attributions.', '']
    for task in sorted(failed_tasks):
        lines.extend(case_text(task, notes[task], catalogue, categories, labels, root, report))
    lines += ['## Appendix A. Complete unresolved-trial catalogue', '',
              f'All {total} rows below correspond one-to-one to the archived `label=false` records. The full stage and subcategory names are repeated to make each assignment self-contained. '
              'Trial links open the archived trajectories indexed for each attempt.', '',
              table(['No.','Task','Model','Trial','Subcategory','Broader stage'],
                    [(i,r['task_id'],r['model_short'],f"[{r['trial']}]({link(root/r['trajectory_path'],report)})",
                      f"{r['primary_category']} {r['subcategory']}",r['stage']) for i,r in enumerate(catalogue,1)]), '',
              '## Reproduction and data fields', '',
              'From the repository root, rebuild this document and its tables with:', '',
              '```bash', 'python3 scripts/build_failure_analysis.py', '```', '',
              f'The editable inputs are [trial annotations]({package_link("failure_annotations.csv")}), '
              f'[category definitions]({package_link("failure_codebook.json")}), and [English case notes]({package_link("failure_case_notes.json")}). '
              'The script checks exact coverage of all recorded failures, uniqueness, outcome consistency, category validity, evidence-file availability, '
              'and the patch/trajectory hashes attached to the annotations. Changed evidence requires annotation review rather than automatic reuse of an old explanation.', '',
              f'The [validation result]({reference("failure_analysis_validation.json")}) records the coverage checks. '
              f'[Category]({reference("failure_taxonomy_summary.csv")}), [stage]({reference("failure_stage_summary.csv")}), '
              f'[model]({reference("failure_model_summary.csv")}), and [task]({reference("failure_task_summary.csv")}) CSVs reproduce the descriptive counts. '
              'Hashes identify the indexed input snapshot. The catalogue builder performs no API calls, benchmark execution, or automatic causal classification.', '']
    return '\n'.join(lines)


def case_text(task, note, catalogue, categories, labels, root, report):
    selected = [r for r in catalogue if r['task_id'] == task]
    outcomes = '; '.join(short + ': ' + ' '.join('S' if labels[(task,model,t)]['label'] else 'F' for t in range(1,4))
                         for short, model in MODELS.items())
    lines = [f'<a id="case-{task}"></a>', '', f'### {task}', '', f'**Issue.** {note["issue_summary"]}', '',
             f'**Recorded outcomes.** {outcomes}.', '', f'**Analysis.** {note["diagnosis_summary"]}', '']
    if selected:
        assigned = []
        for code in categories:
            rows = [r for r in selected if r['primary_category'] == code]
            if rows:
                names = ', '.join(f"{r['model_short']}-{r['trial']}" for r in rows)
                assigned.append(f'{code}: {names}')
        lines += ['**Primary assignments.** ' + '; '.join(assigned) + '.', '']
    if note['interpretation_note']:
        lines += [f'**Interpretation.** {note["interpretation_note"]}', '']
    return lines


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-root', type=Path, default=ROOT, help='Repository containing data/ and analyse/')
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--report', type=Path, default=ROOT/'result/analyse.md')
    parser.add_argument('--annotations', type=Path, default=FAILURE_DOCS/'failure_annotations.csv')
    parser.add_argument('--codebook', type=Path, default=FAILURE_DOCS/'failure_codebook.json')
    parser.add_argument('--case-notes', type=Path, default=FAILURE_DOCS/'failure_case_notes.json')
    args = parser.parse_args()
    root, out, report = args.data_root.resolve(), args.output.resolve(), args.report.resolve()
    catalogue, labels, categories, notes, input_paths = load_inputs(root, args.annotations, args.codebook, args.case_notes)
    model_rows, category_rows, stage_rows, task_rows = summarize(catalogue, labels, categories)
    content = report_text(report,root,out,catalogue,labels,categories,notes,model_rows,category_rows,stage_rows,task_rows)
    english_portable(content, report.name)
    out.mkdir(parents=True,exist_ok=True)
    report.parent.mkdir(parents=True,exist_ok=True)
    datasets = {
        'failure_trial_catalog.csv': catalogue,
        'failure_taxonomy_summary.csv': category_rows,
        'failure_stage_summary.csv': stage_rows,
        'failure_model_summary.csv': model_rows,
        'failure_task_summary.csv': task_rows,
    }
    for filename, rows in datasets.items():
        write_csv(out/filename, rows)
        english_portable((out/filename).read_text(encoding='utf-8'),filename)
        require(len(read_csv(out/filename)) == len(rows), f'CSV serialization changed row count: {filename}')
    report.write_text(content,encoding='utf-8')
    appendix = content.split('## Appendix A. Complete unresolved-trial catalogue',1)[1].split('## Reproduction and data fields',1)[0]
    require(sum(bool(re.match(r'^\| \d+ \|',line)) for line in appendix.splitlines()) == len(catalogue), 'Incomplete appendix')
    manifest = {
        'indexed_inputs': [{'path':p.relative_to(root).as_posix(),'sha256':sha256(p)} for p in sorted(set(input_paths))],
        'annotation_inputs': [{'name':p.resolve().relative_to(root).as_posix(),'sha256':sha256(p)} for p in (args.annotations,args.codebook,args.case_notes)],
    }
    (out/'failure_analysis_inputs.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    validation = {
        'passed': True, 'evaluated_tasks': len({key[0] for key in labels}), 'evaluated_trials':len(labels),
        'recorded_failures':len(catalogue), 'unique_catalogue_rows':len({r['trial_id'] for r in catalogue}),
        'missing_failure_records':0,'successful_trials_in_catalogue':0,'duplicate_annotations':0,
        'failure_tasks':len({r['task_id'] for r in catalogue}),
        'stages':len({r['stage'] for r in categories.values()}),'subcategories':len(categories),
        'category_counts':{r['primary_category']:r['assigned_trials'] for r in category_rows},
        'counts_scope':'One retained primary category per archived unresolved trial; evidence limitations remain in the diagnoses and case notes',
        'checks':'Coverage, uniqueness, labels, categories, source hashes, artifact availability, CSV rows, appendix rows, report links, English and portable paths',
    }
    validation_path = out/'failure_analysis_validation.json'
    for match in re.finditer(r'\]\(([^)]+)\)',content):
        target=unquote(match.group(1).strip('<>'))
        if not target.startswith('#'):
            destination = (report.parent/target).resolve()
            require(destination == validation_path or destination.is_file(),f'Broken report link: {target}')
    validation_path.write_text(json.dumps(validation,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(validation,indent=2))


if __name__ == '__main__':
    main()
