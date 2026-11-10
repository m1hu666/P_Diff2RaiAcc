"""Trace optional usage-field absence to saved response objects, without imputation."""

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from analysis_layout import artifact
from audit_token_methodology import FIELDS, numeric, ABSENT, nested

ROOT = Path(__file__).resolve().parent.parent


def source_shape(usage, field):
    current, traversed = usage, []
    for key in field.split('.'):
        if current is None:
            return 'parent_null:' + '.'.join(traversed)
        if not isinstance(current, dict):
            return 'parent_not_object:' + '.'.join(traversed)
        if key not in current:
            return 'key_absent:' + '.'.join(traversed + [key])
        traversed.append(key)
        current = current[key]
    return 'numeric' if numeric(current) else 'leaf_null' if current is None else 'other'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path, default=ROOT/'result/Statistics results')
    args = parser.parse_args()
    with artifact(args.output, 'per_attempt.csv').open() as stream:
        attempts = list(csv.DictReader(stream))
    counts, examples, states = Counter(), {}, Counter()
    for row in attempts:
        document = json.loads((args.data_root/row['trajectory_path']).read_text())
        for index, message in enumerate(document['messages']):
            if message['role'] != 'assistant':
                continue
            response = message.get('extra', {}).get('response', {})
            usage = response.get('usage')
            for field in FIELDS:
                shape = source_shape(usage, field)
                key = row['model'], field, shape, str(response.get('model'))
                counts[key] += 1
                v = nested(usage, field)
                state = 'missing' if v is ABSENT else 'null' if v is None else 'numeric' if numeric(v) else 'other'
                states[row['model'], field, state] += 1
                if key not in examples:
                    examples[key] = {'model': row['model'], 'field': field, 'source_shape': shape,
                                     'returned_model': response.get('model'), 'normalized_state': state,
                                     'trajectory_path': row['trajectory_path'], 'message_index': index,
                                     'saved_usage': usage}
    with artifact(args.output, 'usage_field_coverage.csv').open() as stream:
        coverage = list(csv.DictReader(stream))
    for row in coverage:
        for state in ('numeric', 'null', 'missing', 'other'):
            if states[row['model'], row['field'], state] != int(row[state]):
                raise ValueError(f'Raw/extracted coverage mismatch: {row["model"]}, {row["field"]}, {state}')
    records = [{'model': model, 'field': field, 'source_shape': shape, 'returned_model': returned,
                'responses': count} for (model, field, shape, returned), count in sorted(counts.items())]
    path = artifact(args.output, 'missing_usage_shapes.csv')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(records)
    artifact(args.output, 'missing_usage_examples.json').write_text(json.dumps(list(examples.values()), indent=2)+'\n')
    lines = ['# Why optional usage details are unavailable', '',
             'Every saved response has numeric prompt and completion totals. Optional subdivisions have a different reporting contract. This audit re-reads the saved response objects and verifies their numeric/null/missing counts against the extracted coverage table.', '',
             'The archive shows three distinct situations: a detail object is null (so its nested field is unavailable), a detail object exists but its field is null, or a key is absent. A reported numeric zero is retained as zero and is distinct from all three cases.', '',
             'These patterns already occur in `messages[*].extra.response.usage`; they are not caused by the statistics extractor dropping numeric values. The normalized state `missing` can include a null parent object; the shape table distinguishes these cases.', '',
             'The archive does not identify where upstream information was lost or not generated. Provider non-reporting, gateway/adapter conversion, and SDK serialization are possible explanations, not established causes. Native upstream payloads and the exact historical conversion implementation are unavailable. Different saved object shapes do not by themselves prove a version change or a particular backend.', '',
             'Do not impute optional values as zero, infer thinking off from an absent field, or subtract a partial reasoning sum to obtain complete visible-output usage. Cache/reasoning subdivisions are not added to their corresponding totals again.', '',
             '| Model | Reasoning numeric | Reasoning leaf null | Reasoning unavailable | Total responses |',
             '| --- | ---: | ---: | ---: | ---: |']
    for row in coverage:
        if row['field'] == 'completion_tokens_details.reasoning_tokens':
            lines.append(f"| {row['model']} | {row['numeric']} | {row['null']} | {row['missing']} | {row['responses']} |")
    lines += ['', 'See [source shapes](missing_usage_shapes.csv), [examples with exact saved usage objects](missing_usage_examples.json), and [field coverage](usage_field_coverage.csv). Examples contain usage objects and source locations only, not message text.', '']
    artifact(args.output, 'MISSINGNESS.md').write_text('\n'.join(lines))
    print(f'Validated raw optional-field shapes for {len(attempts)} trajectories; no imputation.', flush=True)


if __name__ == '__main__':
    main()
