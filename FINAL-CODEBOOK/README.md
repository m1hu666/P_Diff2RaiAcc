# Final Failure Codebook

This directory is the single authoritative, reconciled source package for the
failure taxonomy and trial-level coding of the current experimental corpus.

“Final” means that these records incorporate the completed three-coder review
and reconciliation for this fixed corpus. It does not mean that the taxonomy is
universally complete, immutable, causally proven, or formally saturated. New
trials may justify new evidence, revised boundaries, or additional categories,
but those changes must be documented and revalidated.

The taxonomy was refined iteratively from observed trial failures and then
reconciled through the documented reviewer process. Its construction history
and retained pre-discussion records are in the
[taxonomy methodology package](../docs/taxonomy_methodology/README.md).

## Contents

| File | Role |
|---|---|
| [FAILURE_CODEBOOK.md](FAILURE_CODEBOOK.md) | Human-readable category definitions, decision rules, boundaries, and annotation policy |
| [failure_codebook.json](failure_codebook.json) | Machine-readable representation of the taxonomy |
| [failure_annotations.csv](failure_annotations.csv) | Canonical primary-category assignment and diagnosis for every failed trial |
| [failure_case_notes.json](failure_case_notes.json) | Task-level issue summaries, cross-trial diagnosis summaries, and interpretation notes |

These four files are the editable source records. Generated reports and tables
must not be edited in their place. If the Markdown and JSON definitions ever
disagree, reconcile both files before rebuilding outputs.

## Current scope

The current snapshot contains:

- 242 uniquely identified failed trials;
- 45 tasks with at least one failed trial;
- 11 final failure categories across 5 broader stages; and
- one retained primary category for every failed trial.

All 45 failed tasks have a corresponding entry in
`failure_case_notes.json`. S3 is not part of the final taxonomy: its nine
pre-reconciliation assignments were reassigned to V5. S3 remains visible only
in the historical coder sheets and discussion record.

## Trial annotation fields

`failure_annotations.csv` contains:

| Field | Meaning |
|---|---|
| `task_id` | Benchmark task identifier |
| `model` | Full archived model-directory identifier |
| `trial` | Trial number within the model/task combination |
| `primary_category` | One category code defined in the codebook |
| `diagnosis` | Concise trial-specific explanation of the retained observed failure mode |
| `verified_patch_sha256` | Hash of the exact candidate patch stored in the verified outcome record |
| `trajectory_sha256` | Hash of the archived trajectory used during review |

The tuple `(task_id, model, trial)` must be unique. Successful trials receive
no failure category and must not be added to this table. A trial can contain
several problems, but only one primary category is counted; relevant secondary
or downstream problems can be recorded in the diagnosis or task-level notes.

## Adding or revisiting a trial

1. Confirm that the archived outcome is an unresolved `label=false` trial.
2. Inspect the issue, candidate patch, reference patch, evaluation tests,
   historical repository context, and trajectory where available.
3. Enumerate observable deviations and exclude errors that the agent
   demonstrably recovered.
4. Select the unrecovered mode with the clearest archived evidence link to the
   submitted failure. Use chronology only as a deterministic tie-breaker
   between similarly supported candidates.
5. Add or revise the row in `failure_annotations.csv`, preserving its unique
   trial key and exact evidence hashes.
6. Add a task-level entry to `failure_case_notes.json` when the task is new.
7. If a category or boundary changes, update both `FAILURE_CODEBOOK.md` and
   `failure_codebook.json`.
8. Preserve pre-discussion coder responses and record any new formal review or
   reconciliation separately before changing a canonical assignment.
9. Rebuild and validate all derived outputs.

Do not assign a category from a failed outcome alone. A difference from the
reference patch is also insufficient evidence. When decisive evidence is
unavailable, state that limitation rather than presenting an attribution as
newly confirmed.

## Validation and regeneration

From the repository root, run:

```bash
python3 scripts/build_failure_analysis.py
python3 scripts/build_taxonomy_review_packet.py
python3 scripts/build_taxonomy_review_packet.py --check
python3 scripts/summarize_earliest_links.py
```

For the complete quantitative rebuild and cross-output validation, run:

```bash
python3 scripts/run_analysis.py
```

The failure-analysis builder checks exact coverage of archived failed trials,
unique trial keys, valid categories, archived outcome labels, patch and
trajectory hashes, task-note coverage, evidence-file availability, and the
completeness of the generated catalogue and report.

## Derived catalogues

The expanded
[failure trial catalogue](../result/Statistics%20results/full/failures/failure_trial_catalog.csv)
is generated from this package. It joins each annotation with the category
name, stage, evidence paths, and reporting fields. The human-readable
[failure report](../result/analyse.md) is generated as well.

These outputs are useful for analysis and browsing but are not additional
editable coding sources. Change the files in this directory and rebuild them.

## Chronological-link judgments

The primary failure category and the `earliest_link` audit answer different
questions. The primary category records the retained observed failure mode.
The chronological-link audit asks whether that category is also the earliest
observable unrecovered deviation with a direct archived link to the
unsuccessful submission; it is not a causal label.

Explicit reconciliation inputs remain in
[earliest_link_decisions.csv](../docs/taxonomy_methodology/earliest_link_decisions.csv).
The complete generated trial table is
[final_earliest_links.csv](../result/Statistics%20results/taxonomy_reliability/final_earliest_links.csv).
Its `SUPPORTED`, `NOT_SUPPORTED`, and `INDETERMINATE` values must not be folded
into or treated as replacements for the primary category.

## Interpretation limits

These annotations are evidence-based diagnostic attributions over observational
trajectories, not experimentally identified causal root causes. Retaining an
assignment with a documented evidence limitation does not mean that later
review independently confirmed it.

V5 records an evaluation-infrastructure blocker and remains an unresolved
benchmark trial without being evidence of a model-repair defect. More
generally, a final code, failed benchmark label, or reviewer agreement does not
establish semantic incorrectness, universal taxonomy completeness, blind
independent coding, or formal saturation.
