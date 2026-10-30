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
    audit = json.loads((out/'audit.json').read_text())
    attempts = list(csv.DictReader((out/'per_attempt.csv').open()))
    calls = list(csv.DictReader((out/'per_response.csv').open()))
    manifest = json.loads((out/'input_manifest.json').read_text())
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
    design = json.loads((out/'analysis_design.json').read_text())
    assert design['input_sha256'] == hashlib.sha256((out/'per_attempt.csv').read_bytes()).hexdigest()
    resources = list(csv.DictReader((out/'resource_comparisons.csv').open()))
    success = list(csv.DictReader((out/'success_comparisons.csv').open()))
    stability = list(csv.DictReader((out/'stability_comparisons.csv').open()))
    assert len(resources)==9 and len(success)==len(stability)==3
    for family, size in ((resources, 9), (success, 3), (stability, 3)):
        for row in family:
            assert int(row['n_tasks'])==100 and int(row['holm_family_size'])==size
            assert 0 < float(row['p_value']) <= float(row['p_value_holm']) <= 1
            assert int(row['global_family_size'])==15
            assert float(row['p_value_holm']) <= float(row['p_value_holm_global']) <= 1
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
              "validated_comparison_rows": len(resources)+len(success)+len(stability),
              "portable_english_artifacts_checked": len(checked)}
    (out/'validation.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
