"""Validate all canonical quantitative outputs against their archived inputs.

The validator checks coverage, arithmetic, task-paired comparison families,
input hashes, and portable English paths in ``scripts/``, ``docs/``, and
``result/Statistics results``. It only writes ``validation.json`` in the output
directory and never changes trajectories, labels, patches, or manuscript files.
"""

import csv
import hashlib
import json
import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path
from analysis_layout import artifact, COHORTS, DJANGO
from inferential_analysis import holm_adjust

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
DOCS = ROOT / 'docs'
OUT = ROOT / 'result' / 'Statistics results'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path, default=OUT)
    args = parser.parse_args()
    out = args.output
    def read(name, cohort='full'):
        with artifact(out, name, cohort).open() as stream:
            return list(csv.DictReader(stream))
    audit = json.loads(artifact(out, 'audit.json').read_text())
    attempts = read('per_attempt.csv')
    calls = read('per_response.csv')
    manifest = json.loads(artifact(out, 'input_manifest.json').read_text())
    assert len(attempts) == audit['expected_attempts'] == audit['observed_attempts'] == 900
    assert len(calls) == audit['recorded_responses']
    assert set(Counter(r['exit_status'] for r in attempts)) == {'Submitted'}
    assert all(r['submission_nonempty']=='True' for r in attempts)
    assert set(Counter((r['model'], r['round']) for r in attempts).values()) == {100}
    assert len({r['task'] for r in attempts}) == 100
    by_attempt = defaultdict(list)
    for call in calls:
        by_attempt[(call['model'], call['round'], call['task'])].append(call)
        assert all(call[k+'.state']=='numeric' for k in ('prompt_tokens', 'completion_tokens', 'total_tokens'))
        assert int(call['prompt_tokens'])+int(call['completion_tokens']) == int(call['total_tokens'])
    for row in attempts:
        group = by_attempt[(row['model'], row['round'], row['task'])]
        assert len(group) == int(row['steps']) == int(row['api_calls_recorded'])
        for metric in ('prompt_tokens', 'completion_tokens', 'total_tokens', 'visible_output_characters'):
            assert sum(int(c[metric]) for c in group) == int(row[metric])
        for field in ('prompt_tokens_details.cached_tokens', 'completion_tokens_details.reasoning_tokens'):
            observed = [c for c in group if c[field+'.state']=='numeric']
            assert int(row[field+'.observed_responses']) == len(observed)
            assert (row[field+'.complete']=='True') == (len(observed)==len(group))
            if len(observed)!=len(group):
                assert row[field]==''
    stale = [entry['path'] for entry in manifest
             if hashlib.sha256((args.data_root/entry['path']).read_bytes()).hexdigest() != entry['sha256']]
    assert not stale, f"Inputs changed since audit: {stale}"
    assert not audit['anomalies'], audit['anomalies']
    metadata = {r['task']: r for r in read('task_metadata.csv')}
    assert len(metadata) == 100
    assert sum(r['repository'] == DJANGO for r in metadata.values()) == 50
    expected_failed = {(r['task'], r['model'], r['round']) for r in attempts if r['label']=='False'}
    checked_comparisons, checked_taxonomy = 0, 0
    taxonomy_tests = []
    for cohort in COHORTS:
        selected = {t for t, r in metadata.items() if cohort == 'full' or r['repository'] != DJANGO}
        expected_n = 100 if cohort == 'full' else 50
        design = json.loads(artifact(out, 'analysis_design.json', cohort).read_text())
        assert set(design['included_tasks']) == selected
        assert design['n_tasks'] == expected_n and design['n_attempts'] == 9*expected_n
        assert design['input_sha256'] == hashlib.sha256(artifact(out, 'per_attempt.csv').read_bytes()).hexdigest()
        resources, success, stability = [read(name, cohort) for name in
                                         ('resource_comparisons.csv', 'success_comparisons.csv', 'stability_comparisons.csv')]
        assert len(resources)==9 and len(success)==len(stability)==3
        for family, size in ((resources, 9), (success, 3), (stability, 3)):
            for row in family:
                assert int(row['n_tasks'])==expected_n and int(row['holm_family_size'])==size
                assert 0 < float(row['p_value']) <= float(row['p_value_holm']) <= 1
                assert int(row['global_family_size'])==15
                assert float(row['p_value_holm']) <= float(row['p_value_holm_global']) <= 1
        checked_comparisons += 15
        catalogue = read('failure_trial_catalog.csv', cohort)
        observed_failed = {(r['task_id'], r['model'], 'round'+r['trial']) for r in catalogue}
        assert observed_failed == {key for key in expected_failed if key[0] in selected}
        for name in ('failure_taxonomy_summary.csv', 'failure_stage_summary.csv'):
            summary = read(name, cohort)
            assert sum(int(r['assigned_trials']) for r in summary) == len(catalogue)
            assert abs(sum(float(r['share_of_all_failures_percent']) for r in summary)-100) < 1e-8
        tests = read('category_inference.csv', cohort)
        assert len(tests) == 48
        for r, adjusted in zip(tests, holm_adjust([float(r['p_value']) for r in tests])):
            assert int(r['n_tasks']) == expected_n
            assert int(r['holm_family_size']) == 48
            assert abs(float(r['p_value_holm'])-adjusted) < 1e-12
        taxonomy_tests.extend(tests)
        checked_taxonomy += len(tests)
        strata = list(csv.DictReader((out/cohort/'stratified/stratum_sizes.csv').open()))
        for dimension in ('repository', 'difficulty'):
            assert sum(int(r['n_tasks']) for r in strata if r['dimension']==dimension) == expected_n
            assert sum(int(r['n_attempts']) for r in strata if r['dimension']==dimension) == 9*expected_n
        records = list(csv.DictReader((out/cohort/'stratified/failure_summary.csv').open()))
        for stratum in strata:
            for level in ('primary_category', 'stage'):
                composition = [r for r in records if r['dimension']==stratum['dimension'] and r['stratum']==stratum['stratum']
                               and r['model']=='All' and r.get('level')==level and r['measure']=='composition_percent']
                defined = [float(r['estimate']) for r in composition if r['estimate'] != '']
                assert not defined or abs(sum(defined)-100) < 1e-8
            if int(stratum['n_tasks']) == 1:
                assert all(r['ci95_lower']==r['ci95_upper']=='' for r in records
                           if r['dimension']==stratum['dimension'] and r['stratum']==stratum['stratum'])
    for row, p in zip(taxonomy_tests, holm_adjust([float(r['p_value']) for r in taxonomy_tests])):
        assert int(row['both_cohorts_family_size'])==96
        assert abs(float(row['p_value_holm_both_cohorts'])-p) < 1e-12
    joint = list(csv.DictReader((out/'sensitivity/model_comparisons_both_cohorts.csv').open()))
    assert len(joint)==30
    for row, p in zip(joint, holm_adjust([float(r['p_value']) for r in joint])):
        assert int(row['both_cohorts_family_size'])==30
        assert abs(float(row['p_value_holm_both_cohorts'])-p) < 1e-12
    shifts = list(csv.DictReader((out/'sensitivity/django_taxonomy_shift.csv').open()))
    assert len(shifts) == 16
    for r in shifts:
        assert int(r['full_count']) == int(r['without_django_count']) + int(r['django_count'])
        assert abs(float(r['change_without_minus_full_pp']) -
                   (float(r['without_django_share_percent'])-float(r['full_share_percent']))) < 1e-9
    shapes = read('missing_usage_shapes.csv')
    coverage = read('usage_field_coverage.csv')
    for row in coverage:
        assert sum(int(r['responses']) for r in shapes if r['model']==row['model'] and r['field']==row['field']) == int(row['responses'])
    for row in json.loads(artifact(out, 'missing_usage_examples.json').read_text()):
        source = json.loads((args.data_root/row['trajectory_path']).read_text())
        assert source['messages'][row['message_index']]['extra']['response']['usage'] == row['saved_usage']
    assert not any(p.is_file() and p.name not in {'README.md', 'REPORT.md'} for p in out.iterdir()), 'Uncategorized root output'
    package = SCRIPT_DIR
    personal = re.compile(r'/(?:home|Users)/[^/\\\s"\x27<>]+|[A-Za-z]:\\Users\\[^\\\s]+')
    checked = []
    candidates = list(package.rglob('*.py')) + list(DOCS.rglob('*')) + list(out.rglob('*'))
    for path in candidates:
        if path.is_file() and path.suffix in {'.py', '.md', '.tex', '.json', '.csv'}:
            content = path.read_text()
            assert not personal.search(content), f'Personal path in published artifact: {path.name}'
            assert not any('\u4e00' <= c <= '\u9fff' for c in content), f'Non-English artifact: {path.name}'
            checked.append(path.name)
    result = {"passed": True, "attempts": len(attempts), "responses": len(calls),
              "checked_input_hashes": len(manifest), "initial_prompt_mismatch_tasks": audit['initial_prompt_mismatch_tasks'],
              "anomalies": len(audit['anomalies']),
              "validated_comparison_rows": checked_comparisons,
              "validated_taxonomy_comparison_rows": checked_taxonomy,
              "cohorts": list(COHORTS), "django_excluded_tasks": 50,
              "portable_english_artifacts_checked": len(checked)}
    artifact(out, 'validation.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
