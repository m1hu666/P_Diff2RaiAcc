# Coder instructions

## Task

Independently classify every row in the assigned coder sheet using the frozen
[failure codebook](../failure_analysis/FAILURE_CODEBOOK.md). Do not inspect the
canonical annotations, aggregate category counts, generated failure report, or
the other coder's sheet before submitting your completed file.

For each row, inspect the issue description, hints, generated patch, developer
reference patch, test patch, and trajectory. A difference from the reference
patch or a failed benchmark outcome does not by itself identify the failure
mode.

The CSV uses short model names. Their repository directory names are:

| CSV value | Repository directory |
|---|---|
| `Claude` | `claude-sonnet-4-5-20250929` |
| `Gemini` | `gemini-3-pro-preview` |
| `GPT` | `gpt-5-2025-08-07-medium-reasoning` |

Task materials are under `analyse/<model-directory>/<task_id>/`. The candidate
patch is `<trial><task_id>_model.patch`; the other evidence files use the task
ID in their file names. The trajectory is under
`data/traj/<model-directory>/round<trial>/<task_id>/`.

The repository preserves summary evaluation reports rather than detailed
per-test evaluation traces, and it does not include reconstructed checkouts for
every `base_commit`. When Steps 4 or 6 require material not retained here,
obtain it from the official SWE-bench task metadata or evaluation artifacts.
If it remains unavailable, record that limitation in `notes` and do not infer a
cause that the available evidence cannot support.

## Required diagnostic workflow

Apply the same three-phase, seven-step Failure Diagnosis Workflow reported in
the manuscript.

### Phase 1: task preparation and triage

1. **Repository grouping.** Analyze tasks from the same repository together.
2. **Difficulty ordering.** Within each repository, analyze tasks in ascending
   order of their total failure count across all nine attempts. The supplied
   sheets are already ordered this way. Analyze all failed rows for one task as
   a group before moving to the next task.

### Phase 2: diagnostic iteration

3. **Patch comparison.** Compare every failed generated patch for the task with
   the developer reference patch. Examine modified files, insertion locations,
   logic differences, and behavioral equivalence. A different implementation
   is not automatically incorrect.
4. **Context reconstruction.** If patch comparison does not explain the
   failure, reconstruct the historical repository state at the task's
   `base_commit` and inspect the surrounding control flow, dependencies, and
   framework constraints.
5. **Trajectory attribution.** Trace the saved interaction log step by step and
   align it with the patch and repository context. Enumerate observable
   deviations, determine whether the agent later recovered them, and identify
   any retained effects in the submitted patch or repository state.
6. **Harness diagnosis.** If the agent's self-generated reproduction succeeds
   but official SWE-bench evaluation fails, inspect the official test patch and
   the relevant `FAIL_TO_PASS` and `PASS_TO_PASS` requirements. Attribute the
   failure to benchmark strictness or a hidden/test-side constraint only when
   the combined issue, reference-solution, and evaluation evidence supports
   that interpretation.

### Phase 3: synthesis

7. **Failure labeling.** Synthesize all applicable evidence and assign the one
   primary observed failure mode with the clearest archived evidence link to
   the unsuccessful submission. If multiple unrecovered candidates have such a
   link, use chronology only as a deterministic tie-breaker. Do not separately
   count co-occurring or downstream problems.

## Fields to complete

Do not modify the prefilled `task_id`, `model`, or `trial` columns. Complete:

| Column | Required content |
|---|---|
| `category` | One of `P1`, `P2`, `L1`, `S1`, `S2`, `S3`, `I1`, `V1`, `V2`, `V3`, `V4`, or `OTHER` |
| `failure_reason` | A concise explanation tied to concrete evidence in this trial |
| `earliest_link` | One of `SUPPORTED`, `NOT_SUPPORTED`, or `INDETERMINATE` using the rules below |
| `notes` | Optional ambiguity, competing category, missing evidence, or codebook feedback |

Every row must contain a category, a failure reason, and an `earliest_link`
decision. Write all human-entered text in English so the locked sheets can be
released without a later translation step that might alter the coding
rationale.

## Decision rule

First enumerate the observable deviations and exclude those that the agent
demonstrably corrected before submission. Among the remaining candidates,
select the failure mode with the clearest archived evidence link to the
unsuccessful submission. Use chronology only to break a tie between multiple
directly supported candidates. Temporal precedence, trajectory prose, a patch
difference, or a failed outcome alone is insufficient.

Use `OTHER` rather than forcing a case into an existing category when the
evidence supports a distinct observed mode. Explain the proposed mode in
`failure_reason` and, if useful, propose a short category name in `notes`.

The codebook contains the boundary rules for L1/S1, S2/V3, V1/V2, I1/other,
P1/P2, and V4/other. In particular, use S2 when the repair strategy itself
leaves the target behavior or project constraint unresolved. Use V3 when the
target repair is otherwise achieved but retained evidence confirms a regression
in previously valid state, types, contracts, or behavior.

## Earliest-link decision

This field audits the previously stated chronological attribution rule; it does
not assert causality.

| Value | Use when |
|---|---|
| `SUPPORTED` | The selected primary mode is the earliest observable unrecovered deviation, and archived patch, repository-state, tool, or evaluation evidence directly traces its retained effect to the unsuccessful submission. |
| `NOT_SUPPORTED` | The evidence identifies an earlier unrecovered deviation with an equally or more direct link to the unsuccessful submission than the selected mode, or contradicts the selected mode's proposed link. |
| `INDETERMINATE` | Missing evidence, multiple similarly supported explanations, or an unclear sequence prevents a defensible judgment. |

Do not use `NOT_SUPPORTED` merely because evidence is missing; use
`INDETERMINATE`. Explain a non-obvious decision in `failure_reason` or `notes`.

## Independence and submission

Do not discuss individual cases with the other coder before both files are
complete. Procedural questions may be sent to the coordinator, but the answer
must not reveal a canonical or peer label. Submit the completed CSV as a locked
snapshot; subsequent corrections must be recorded rather than silently
overwriting the submitted version.

