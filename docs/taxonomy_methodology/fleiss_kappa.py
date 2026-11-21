#!/usr/bin/env python3
"""Compute three-coder Fleiss' kappa for the failure annotations.

Usage:
  python fleiss_kappa.py coder_a.csv coder_b.csv coder_c.csv

The coder sheets are pre-discussion verification responses. Each response is
converted to a category as follows:

  ACCEPT            -> the row's current_category
  CHANGE + one code -> the proposed_category
  CHANGE + OTHER-V5 -> V5
  CHANGE + multiple, blank, or unrecognized -> unresolved

Fleiss' kappa is computed over the three fixed reviewers:

  Po    = (agreeing unordered reviewer pairs) / (N * 3)
  Pe    = sum_c (n_c / (3 * N))^2
  kappa = (Po - Pe) / (1 - Pe)

An unresolved rating is placed in one common "UNRESOLVED" nominal state so
that every subject stays in the denominator. In the observed-agreement term,
a pair agrees only when both ratings carry the same value, so an unresolved
rating paired with a substantive category is a disagreement. In the
chance-agreement term, the "UNRESOLVED" state contributes like any other
category through its marginal proportion n_g / (3 * N). The V1/V2 subset
consists of the trials whose prefilled current_category is V1 or V2.
"""

import csv
import json
import re
import sys
from collections import Counter

CATEGORIES = {'P1', 'P2', 'L1', 'S1', 'S2', 'S3', 'I1',
              'V1', 'V2', 'V3', 'V4', 'V5', 'OTHER'}


def read_sheet(path):
    with open(path, encoding='utf-8-sig', newline='') as file:
        return list(csv.DictReader(file))


def response_category(row):
    decision = (row.get('decision') or '').strip().upper()
    current = (row.get('current_category') or '').strip().upper()
    if decision == 'CHANGE':
        text = (row.get('proposed_category') or '').strip().upper()
        codes = set(re.findall(r'\b(?:P[12]|L1|S[123]|I1|V[12345]|OTHER)\b', text))
        if 'V5' in codes:
            codes.discard('OTHER')
        if len(codes) == 1:
            return next(iter(codes))
        return None
    return current if current in CATEGORIES else None


def fleiss(matrix):
    n = len(matrix)
    rows = [[v if v is not None else 'UNRESOLVED' for v in row] for row in matrix]
    agreement = sum(
        row[i] == row[j]
        for row in rows
        for i in range(3)
        for j in range(i + 1, 3)
    )
    po = agreement / (n * 3)
    counts = Counter(v for row in rows for v in row)
    pe = sum((count / (3 * n)) ** 2 for count in counts.values())
    kappa = (po - pe) / (1 - pe)
    return {
        'n': n,
        'agreeing_pairs': agreement,
        'total_pairs': n * 3,
        'po': po,
        'pe': pe,
        'kappa': kappa,
    }


def main(paths):
    sheets = [read_sheet(path) for path in paths]
    keys = [[(row['task_id'], row['model'], row['trial']) for row in sheet]
            for sheet in sheets]
    if not (len(keys[0]) == 242 and keys[0] == keys[1] == keys[2]):
        raise SystemExit('sheets must contain the same 242 aligned attempts')

    converted = [[response_category(row) for row in sheet] for sheet in sheets]
    items = [[converted[reviewer][index] for reviewer in range(3)]
             for index in range(242)]

    overall = fleiss(items)
    v12_index = [
        index for index, row in enumerate(sheets[0])
        if (row.get('current_category') or '').strip().upper() in {'V1', 'V2'}
    ]
    v12 = fleiss([items[index] for index in v12_index])

    unresolved = {
        f'coder_{"ABC"[reviewer]}': sum(v is None for v in converted[reviewer])
        for reviewer in range(3)
    }

    print(json.dumps({
        'overall_fleiss': overall,
        'v1v2_subset_n': len(v12_index),
        'v1v2_fleiss': v12,
        'unresolved_ratings_by_reviewer': unresolved,
    }, indent=2))


if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise SystemExit(
            'usage: python fleiss_kappa.py coder_a.csv coder_b.csv coder_c.csv'
        )
    main(sys.argv[1:])
