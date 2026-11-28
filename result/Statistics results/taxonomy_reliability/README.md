# Final chronological-link audit

The audit covers 242 failed trials on 45 tasks. The primary categories are the canonical post-discussion categories.

| Final earliest_link | Count | Percent of all failed trials |
| --- | --- | --- |
| SUPPORTED | 234 | 96.69% |
| NOT_SUPPORTED | 8 | 3.31% |
| INDETERMINATE | 0 | 0.00% |

Explicit [discussion and adjudication decisions](../../../docs/taxonomy_methodology/earliest_link_decisions.csv) take priority. For remaining trials, when the primary category is unchanged, the status receiving at least two of the three coder votes becomes final. A majority of INDETERMINATE votes, a three-way split, or a changed category produces a provisional INDETERMINATE result that must be adjudicated as SUPPORTED or NOT_SUPPORTED. Votes on a replaced category cannot be transferred to its replacement. Blank coder statuses were filled with INDETERMINATE before applying this rule.

The vote is symmetric across SUPPORTED, NOT_SUPPORTED, and INDETERMINATE. A majority result means at least two coders selected that status; it need not be unanimous. The completed adjudication assigns SUPPORTED to the provisional V-category cases under the validation-stage rule and resolves every other provisional case from its trajectory, patch, repository-state, and evaluation evidence. Explicit decisions may supersede the vote. Neither SUPPORTED nor NOT_SUPPORTED establishes or disproves a causal root cause.

Resolution basis: 53 explicit decisions; majority-vote results of SUPPORTED 188, NOT_SUPPORTED 1, and INDETERMINATE 0; 0 three-way splits; and 0 changed categories without a new chronological-link assessment.

## Counts by final category

| Category | SUPPORTED | NOT_SUPPORTED | INDETERMINATE | Total |
| --- | --- | --- | --- | --- |
| P1 | 45 | 0 | 0 | 45 |
| P2 | 26 | 0 | 0 | 26 |
| L1 | 12 | 0 | 0 | 12 |
| S1 | 45 | 4 | 0 | 49 |
| S2 | 19 | 0 | 0 | 19 |
| I1 | 5 | 3 | 0 | 8 |
| V1 | 10 | 0 | 0 | 10 |
| V2 | 30 | 0 | 0 | 30 |
| V3 | 21 | 1 | 0 | 22 |
| V4 | 3 | 0 | 0 | 3 |
| V5 | 18 | 0 | 0 | 18 |

[Trial-level decisions](final_earliest_links.csv) retain all three coder statuses and the resolution basis. The [grouped table](earliest_link_summary.csv) adds model/category counts and percentages. Rebuild with:

```bash
python3 scripts/summarize_earliest_links.py
```
