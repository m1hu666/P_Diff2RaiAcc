# Failure annotation codebook

This codebook defines the stages and categories used in the failure analysis. The machine-readable version is [failure_codebook.json](failure_codebook.json). The category codes retain the study's hierarchical notation; the S2 and V3 names clarify their behavioral boundary.

The annotation unit is one failed model trial on one task. Each failed trial retains one primary observed failure-mode category so that category counts remain mutually exclusive. A task can contain trials with different categories, and a trial can contain co-occurring or downstream problems that are described without being counted again. The labels are diagnostic attributions, not identified causal root causes. Where an existing assignment still needs verification, retain its category and state the evidence limitation in the diagnosis or case notes rather than treating that assignment as newly confirmed.

## Stages and categories

| Stage | Code | Legacy code | Category | Operational interpretation |
|---|---|---|---|---|
| Problem Understanding | P1 | 1.1 | Misinterpretation / Domain Knowledge Lack | The diagnosis identifies an incorrect or incomplete interpretation of a requirement, domain rule, or architectural assumption. |
| Problem Understanding | P2 | 1.2 | Distracted by Hints / TODOs | The diagnosis links the chosen direction to a specific suggestion or TODO that leaves the required behavior unresolved. |
| Localization | L1 | 2.1 | Incomplete Scope / Wrong Layer | Required files, entry points, or subclasses are omitted, or the intervention is placed at an unsuitable architectural layer. |
| Strategy & Logic | S1 | 3.1 | Partial Fix / Incomplete Logic | The repair covers part of the required behavior but misses an operation, input combination, boundary case, or compatibility condition. |
| Strategy & Logic | S2 | 3.2 | Incorrect Strategy | An incorrect algorithm, transformation, or workaround prevents the patch from satisfying the behavior required by the reported issue. |
| Implementation & Execution | I1 | 4.1 | Tool Failure / Silent State Hallucination | An operation fails, the agent acts on an incorrect repository state, or the archived evaluated patch differs concretely from the recorded final submission. |
| Validation & Harness Constraints | V1 | 5.1 | Specification-Oracle Gap | The diagnosis identifies a difference between the behavior emphasized by the issue and an additional requirement enforced by the tests. |
| Validation & Harness Constraints | V2 | 5.2 | Strict Output Format Mismatch | The produced string, argument structure, serialized form, or attribute representation differs from the asserted representation. |
| Validation & Harness Constraints | V3 | 5.3 | Regression of Existing Behavior | The patch successfully resolves the issue-reported problem but introduces a regression in previously correct behavior. |
| Validation & Harness Constraints | V4 | 5.4 | Execution Timing Mismatch | Required state or a transformation is supplied at a different lifecycle point or processing stage from the expected one. |
| Validation & Harness Constraints | V5 | 5.5 | Evaluation Infrastructure Failure | An evaluation dependency or test-collection environment prevents the submitted behavior from being assessed reliably. |

## Evidence and interpretation

Interpret each annotation alongside the issue description, candidate patch, reference patch, test patch, and trajectory where available. A difference from the reference patch does not establish an error. Conversely, a failed benchmark label records the evaluation outcome without establishing the reason for failure. Keep the recorded outcome and the qualitative diagnosis separate.

Artifact paths identify the materials available in this repository. They are navigation and provenance aids, not evidence that every listed artifact was necessary for every annotation.

The published count tables summarize the canonical trial annotations. The existence of a coded dataset does not by itself establish independent-coder agreement, causal identification, or semantic correctness. No agreement coefficient should be inferred without a separate reliability study.

Apply the Failure Diagnosis Workflow in the manuscript: group and order tasks, compare candidate and reference patches, reconstruct the historical repository context when patch comparison is insufficient, trace the trajectory step by step, and inspect the benchmark harness when a self-generated reproduction succeeds but official evaluation fails. Enumerate observable deviations and exclude transient errors that the agent demonstrably recovered. Select the remaining failure mode with the clearest archived evidence link to the unsuccessful submission. If multiple candidates have such a link, use chronology only as a deterministic tie-breaker; temporal precedence alone is insufficient.

Retain selected successful cases as a separate comparison set. They illustrate alternative repairs or successful execution and receive no failure label. Exclude them from failure-category denominators.

## Category boundaries

**L1 and S1.** L1 concerns where the repair is attempted and whether all required implementation locations are covered. S1 concerns which required behaviors the selected logic handles. Omitting a subclass is a scope problem; handling creation but not later updates is incomplete behavioral coverage. Some cases can exhibit both. Select the mode with the clearest archived evidence link to the unsuccessful submission and explain the specific omission rather than applying an automatic category-priority rule.

**S2 and V3.** First determine whether the patch successfully resolves the issue-reported problem. Assign S2 when an incorrect algorithm, transformation, or workaround leaves that required behavior unresolved. Assign V3 only when both conditions are supported: (1) a reproduction test or other behavioral evidence confirms that the reported issue is resolved, and (2) regression tests or a before-and-after behavioral comparison confirms that the patch breaks previously correct behavior, a caller contract, or a state lifecycle. If the reported issue remains unresolved, do not assign V3 even when the patch also introduces a regression; classify the trial by the primary unresolved mechanism, such as S2 for an incorrect strategy or S1 for incomplete repair logic.

The V3 regression must be directly linked to the same patch and may affect the same function, a repeated-call path, a type or caller contract, or a state lifecycle. An unrelated or recovered error does not qualify. Patch breadth, a difference from the reference patch, a failed outcome, or membership in `FAIL_TO_PASS` or `PASS_TO_PASS` alone does not establish either successful issue resolution or a regression.

**V1 and V2.** V1 concerns the scope of required behavior; V2 concerns its concrete representation. A test that checks an additional exception case can motivate V1. An exact argument-list or string assertion can motivate V2. Neither label alone proves that the candidate is semantically equivalent to the reference or that the test is invalid: representations can form part of a public contract.

**I1 and other categories.** I1 requires observable tool or repository-state evidence. Suitable evidence includes a command error, an edit that was not executed, a file differing from the intended edit, or a claim that a change was applied when the saved state shows otherwise. A failed benchmark result or unrelated patch content alone does not establish a tool failure or state hallucination.

An archived evaluated patch that differs concretely from the recorded final submission may also be coded I1 as a patch-state failure; identify the changed bytes and do not attribute the mismatch to model intent without evidence.

**P1 and P2.** P1 concerns the interpretation of the required behavior. P2 additionally requires an identifiable cue that the recorded diagnosis connects to the chosen repair direction. An observed connection does not establish that removing the cue would have changed the outcome.

**V4 and other categories.** A timing diagnosis should identify when a value or transformation is required and when the patch supplies it. A workaround that merely changes accepted input syntax does not establish a timing failure without a documented processing-stage distinction.

**V5 and patch-attributable categories.** Use V5 when the reconciled evidence places the recorded failure in the evaluation environment before the candidate behavior can be assessed reliably. State the concrete blocker, such as a test-collection dependency. V5 remains a recorded unresolved trial, but it is not evidence of a defect in the model's selected repair. Do not infer V5 solely from an unsuccessful outcome or from a missing local reproduction.

## Earliest-link audit

The separate `earliest_link` field evaluates whether the selected primary mode
also satisfies the study's chronological attribution convention. It is not a
causal label.

| Value | Decision rule |
|---|---|
| `SUPPORTED` | The selected mode is the earliest observable unrecovered deviation, and archived patch, repository-state, tool, or evaluation evidence directly traces its retained effect to the unsuccessful submission. |
| `NOT_SUPPORTED` | The evidence identifies an earlier unrecovered deviation with an equally or more direct link to the unsuccessful submission than the selected mode, or contradicts the selected mode's proposed link. |
| `INDETERMINATE` | Missing evidence, multiple similarly supported explanations, or an unclear sequence prevents a defensible judgment. |

An event does not qualify as `SUPPORTED` merely because it occurs first, appears
in the trajectory narrative, differs from the reference patch, or precedes a
failed benchmark outcome.

These definitions apply to individual assessments. The
[final aggregation rule](../docs/taxonomy_methodology/README.md#final-chronological-link-judgments)
uses any eligible negative assessment as a conservative flag and requires
three positive assessments for support, subject to explicit discussion
decisions. An aggregate negative flag does not imply coder consensus.

## Annotation policy

Do not invent supporting evidence or change a benchmark outcome without an applicable evaluation. Assign a category only when the archived issue, patches, trajectory, and evaluation requirements support the stated attribution. Keep outcome labels separate from qualitative diagnoses, and avoid stronger claims than the retained evidence supports.
