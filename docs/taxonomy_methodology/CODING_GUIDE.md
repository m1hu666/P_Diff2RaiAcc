# Coder instructions: verify existing trial assignments

This is the original review protocol. The linked packet and codebook have
since been regenerated or revised after discussion. The English CSV
transcriptions retain the categories and review judgments seen by each coder;
their conversion policy is documented in ANNOTATION_AGREEMENT.md.

## What to review

Independently check the current category and diagnosis for every failed trial
in your assigned sheet. Start with the readable
[verification packet](VERIFICATION_CASES.md), which presents the authors'
existing analysis and links to the underlying materials. The original review
used eleven categories. The linked final
[failure codebook](../../FINAL-CODEBOOK/FAILURE_CODEBOOK.md) replaces the now-retired
S3 with V5 after all nine S3 assignments were reclassified during
reconciliation. Decide whether
that analysis supports the current category. The packet and original label are
provided intentionally; this is informed verification, not blind recoding.

Begin with the task summary, current diagnosis, and candidate patch. Check the
decisive behavioral claim against the relevant issue, reference, test, or
trajectory material. Open the remaining artifacts when the claim is unclear
or appears wrong; a complete fresh diagnosis of every trial is not required
for this post hoc check. The sheet order groups tasks by repository and places
tasks with fewer failed attempts first. Check all failed trials of one task
before moving to the next.

The model names in the sheet correspond to these source directories:

| Sheet value | Repository directory |
| --- | --- |
| `Claude` | `claude-sonnet-4-5-20250929` |
| `Gemini` | `gemini-3-pro-preview` |
| `GPT` | `gpt-5-2025-08-07-medium-reasoning` |

The packet links directly to the materials, including the dataset's
`FAIL_TO_PASS` and `PASS_TO_PASS` test-ID lists. Those lists describe expected
benchmark tests, not the outcome of the particular model trial. The materials
can also be found under
`analyse/<model-directory>/<task_id>/` and
`data/traj/<model-directory>/round<trial>/<task_id>/`.

## How to check a trial

Use the manuscript's three-phase, seven-step Failure Diagnosis Workflow as
the basis for the check. The existing diagnosis gives you a starting point;
verify its decisive claim against the relevant materials. Where that claim is
unclear or the label appears wrong, follow the applicable steps in greater
depth:

**Phase 1: task preparation and triage**

1. Group tasks from the same repository.
2. Within each repository, review tasks in ascending order of failed attempts.

**Phase 2: diagnostic iteration**

3. Compare failed candidate patches with the developer patch, including
   behavior and modified locations; a different implementation can still be
   correct.
4. Reconstruct the historical repository context at the task's `base_commit`
   when patch comparison alone does not explain the behavior.
5. Trace the saved trajectory step by step and distinguish submitted
   deviations from errors the agent later corrected.
6. Inspect the evaluation tests and harness requirements when the agent's own
   reproduction succeeds but official evaluation fails.

**Phase 3: synthesis**

7. Synthesize the observable failure modes and check the one current primary
   assignment against the codebook. Use chronology only to break a tie among
   directly supported unrecovered deviations; an earlier event alone does not
   establish a cause.

The repository contains summary evaluation reports rather than detailed
per-test traces for every trial and does not include a checkout for every
historical `base_commit`. If a decisive source remains unavailable, retain the
original category (`ACCEPT`) and explain what is missing in `reason`; the
original category remains in place until the post-review discussion.

## Fill your sheet

Keep the prefilled `task_id`, `model`, `trial`, and `current_category` unchanged.
Complete only these fields:

| Field | Entry |
| --- | --- |
| `decision` | `ACCEPT` if the current category is supported; `CHANGE` if another category fits better. |
| `proposed_category` | In the original review, `CHANGE` selected `P1`, `P2`, `L1`, `S1`, `S2`, `S3`, `I1`, `V1`, `V2`, `V3`, `V4`, or `OTHER`. Leave blank for `ACCEPT`. |
| `reason` | Required if `decision` is `CHANGE`, or if `earliest_link` is `NOT_SUPPORTED` or `INDETERMINATE`. Explain the category distinction, earlier deviation, contradiction, or missing evidence. Otherwise optional. |
| `earliest_link` | Judge the displayed current category using `SUPPORTED`, `NOT_SUPPORTED`, or `INDETERMINATE` as defined below. |

Use `OTHER` only when the evidence supports an observed failure mode outside
the current taxonomy; name and explain that mode in `reason`. A different patch
from the reference solution or an unsuccessful benchmark outcome does not by
itself establish a different failure mode.

Write free-text comments in English. A trial with multiple problems still
receives one proposed primary category; mention a relevant secondary problem
in `reason`. For S2 and V3, first determine whether the reported issue was
resolved. S2 applies when an incorrect strategy leaves it unresolved. V3
requires evidence both that the patch resolves the reported issue and that it
breaks previously correct behavior. If the reported issue remains unresolved,
do not assign V3 even when the patch also introduces a regression.

## Chronological-link check

For every row, assess whether the **displayed current category** also marks
the earliest observable unrecovered deviation whose retained effect can be
traced to the unsuccessful submission. Record the assessment in
`earliest_link` even if you propose a different category. This operationally
checks the manuscript's earlier "earliest causally dominant breakdown"
wording; a `SUPPORTED` response does not prove a causal root cause.

| Value | Use when |
| --- | --- |
| `SUPPORTED` | The current category identifies the earliest observable unrecovered deviation with a direct evidence link to the unsuccessful submission. |
| `NOT_SUPPORTED` | An earlier unrecovered deviation has an equally or more direct link, or the proposed link for the current category is contradicted. |
| `INDETERMINATE` | Missing evidence, competing explanations, or an unclear sequence prevents this judgment. |

Do not mark `SUPPORTED` solely because an event came first in the trajectory.
If you mark `NOT_SUPPORTED` or `INDETERMINATE`, explain why in `reason`. The
discussion table will separately reassess `final_earliest_link` if the final
category changes. When both judgments need explanation, address both in the
same `reason` cell.

## Independence and discussion

Review the existing analysis and underlying materials without viewing or
discussing the other coders' sheets. Submit a locked copy of your completed
sheet before any case-by-case discussion. The comparison script records the
hash of each submitted sheet and creates the discussion table only after all
three are complete. Any changes after discussion belong in that comparison
table; do not silently revise the locked pre-discussion sheets.

The original label is visible to all three coders, so agreement in this check
measures verification concordance, not agreement from the original taxonomy
construction or an independent blind application of the codebook.
