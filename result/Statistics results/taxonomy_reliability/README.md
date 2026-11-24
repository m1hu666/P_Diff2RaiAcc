# Final chronological-link audit

The audit covers 242 failed trials on 45 tasks. The primary categories are the canonical post-discussion categories.

| Final earliest_link | Count | Percent of all failed trials |
| --- | --- | --- |
| SUPPORTED | 130 | 53.72% |
| NOT_SUPPORTED | 32 | 13.22% |
| INDETERMINATE | 80 | 33.06% |

Explicit [discussion decisions](../../../docs/taxonomy_methodology/earliest_link_decisions.csv) take priority. For remaining trials, use NOT_SUPPORTED as a conservative negative flag when the primary category is unchanged and at least one coder recorded NOT_SUPPORTED. Use SUPPORTED only when the category is unchanged and all three coder values are SUPPORTED. All other cases are INDETERMINATE. Blank coder statuses were filled with INDETERMINATE before applying this rule.

An aggregate NOT_SUPPORTED status records at least one negative assessment or an explicit final discussion decision; it does not imply unanimous reviewer agreement or establish that a causal claim has been disproved.

At least one coder recorded NOT_SUPPORTED on 61 pre-discussion trials. Of these, 29 have a changed primary category and are not transferred automatically to the new category.

The INDETERMINATE total includes 29 trials whose category changed without a new chronological-link assessment and 51 trials with incomplete or indeterminate support and no eligible negative assessment. These entries are not counted as NOT_SUPPORTED. SUPPORTED is an observational evidence-link judgment and does not establish a causal root cause.

## Counts by final category

| Category | SUPPORTED | NOT_SUPPORTED | INDETERMINATE | Total |
| --- | --- | --- | --- | --- |
| P1 | 17 | 15 | 13 | 45 |
| P2 | 18 | 1 | 7 | 26 |
| L1 | 9 | 3 | 0 | 12 |
| S1 | 34 | 6 | 9 | 49 |
| S2 | 14 | 1 | 4 | 19 |
| I1 | 2 | 0 | 6 | 8 |
| V1 | 4 | 4 | 2 | 10 |
| V2 | 20 | 0 | 10 | 30 |
| V3 | 10 | 1 | 11 | 22 |
| V4 | 2 | 1 | 0 | 3 |
| V5 | 0 | 0 | 18 | 18 |

[Trial-level decisions](final_earliest_links.csv) retain all three coder statuses and the resolution basis. The [grouped table](earliest_link_summary.csv) adds model/category counts and percentages. Rebuild with:

```bash
python3 scripts/summarize_earliest_links.py
```
