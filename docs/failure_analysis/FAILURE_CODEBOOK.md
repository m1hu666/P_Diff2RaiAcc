# Failure annotation codebook

This codebook defines the stages and categories used in the failure analysis. The machine-readable version is [failure_codebook.json](failure_codebook.json). Category names and codes follow the manuscript; numeric codes provide the corresponding hierarchical notation.

The annotation unit is one failed model trial on one task. Each failed trial receives one primary observed failure-mode category so that category counts remain mutually exclusive. A task can contain trials with different categories, and a trial can contain co-occurring or downstream problems that are described without being counted again. The label is an evidence-supported diagnostic attribution, not an identified causal root cause.

## Stages and categories

| Stage | Code | Legacy code | Category | Operational interpretation |
|---|---|---|---|---|
| Problem Understanding | P1 | 1.1 | Misinterpretation / Domain Knowledge Lack | The diagnosis identifies an incorrect or incomplete interpretation of a requirement, domain rule, or architectural assumption. |
| Problem Understanding | P2 | 1.2 | Distracted by Hints / TODOs | The diagnosis links the chosen direction to a specific suggestion or TODO that leaves the required behavior unresolved. |
| Localization | L1 | 2.1 | Incomplete Scope / Wrong Layer | Required files, entry points, or subclasses are omitted, or the intervention is placed at an unsuitable architectural layer. |
| Strategy & Logic | S1 | 3.1 | Partial Fix / Incomplete Logic | The repair covers part of the required behavior but misses an operation, input combination, boundary case, or compatibility condition. |
| Strategy & Logic | S2 | 3.2 | Incorrect Strategy / Side Effects | The proposed algorithm, control flow, or repair strategy is unsuitable or introduces a behavioral conflict. |
| Strategy & Logic | S3 | 3.3 | Hardcoding / Bad Practices | A fixed or environment-specific assumption fails to satisfy required portability or repository conventions. |
| Implementation & Execution | I1 | 4.1 | Tool Failure / Silent State Hallucination | An operation fails or produces an unintended change, or the agent proceeds with an incorrect belief about the repository state. |
| Validation & Harness Constraints | V1 | 5.1 | Specification-Oracle Gap | The diagnosis identifies a difference between the behavior emphasized by the issue and an additional requirement enforced by the tests. |
| Validation & Harness Constraints | V2 | 5.2 | Strict Output Format Mismatch | The produced string, argument structure, serialized form, or attribute representation differs from the asserted representation. |
| Validation & Harness Constraints | V3 | 5.3 | Side Effects | The repair interferes with shared state, cached values, downstream contracts, or behavior checked by other tests. |
| Validation & Harness Constraints | V4 | 5.4 | Execution Timing Mismatch | Required state or a transformation is supplied at a different lifecycle point or processing stage from the expected one. |

## Evidence and interpretation

Interpret each annotation alongside the issue description, candidate patch, reference patch, test patch, and trajectory where available. A difference from the reference patch does not establish an error. Conversely, a failed benchmark label records the evaluation outcome without establishing the reason for failure. Keep the recorded outcome and the qualitative diagnosis separate.

Artifact paths identify the materials available in this repository. They are navigation and provenance aids, not evidence that every listed artifact was necessary for every annotation.

The published count tables summarize the canonical trial annotations. The existence of a coded dataset does not by itself establish independent-coder agreement, causal identification, or semantic correctness. No agreement coefficient should be inferred without a separate reliability study.

Apply the Failure Diagnosis Workflow in the manuscript: group and order tasks, compare candidate and reference patches, reconstruct the historical repository context when patch comparison is insufficient, trace the trajectory step by step, and inspect the benchmark harness when a self-generated reproduction succeeds but official evaluation fails. Enumerate observable deviations and exclude transient errors that the agent demonstrably recovered. Select the remaining failure mode with the clearest archived evidence link to the unsuccessful submission. If multiple candidates have such a link, use chronology only as a deterministic tie-breaker; temporal precedence alone is insufficient.

Retain selected successful cases as a separate comparison set. They illustrate alternative repairs or successful execution and receive no failure label. Exclude them from failure-category denominators.

## Category boundaries

**L1 and S1.** L1 concerns where the repair is attempted and whether all required implementation locations are covered. S1 concerns which required behaviors the selected logic handles. Omitting a subclass is a scope problem; handling creation but not later updates is incomplete behavioral coverage. Some cases can exhibit both. Select the mode with the clearest archived evidence link to the unsuccessful submission and explain the specific omission rather than applying an automatic category-priority rule.

**S2 and V3.** Use S2 when the repair strategy itself fails to satisfy the target behavior or project constraint. Use V3 when the target repair is otherwise achieved but a confirmed regression affects previously valid state, types, contracts, or behavior. A regression requires retained test or repository evidence and should not be inferred from patch breadth alone. V3 includes type and contract regressions and should not uniformly be described as environment pollution.

**V1 and V2.** V1 concerns the scope of required behavior; V2 concerns its concrete representation. A test that checks an additional exception case can motivate V1. An exact argument-list or string assertion can motivate V2. Neither label alone proves that the candidate is semantically equivalent to the reference or that the test is invalid: representations can form part of a public contract.

**I1 and other categories.** I1 requires observable tool or repository-state evidence. Suitable evidence includes a command error, an edit that was not executed, a file differing from the intended edit, or a claim that a change was applied when the saved state shows otherwise. A failed benchmark result or unrelated patch content alone does not establish a tool failure or state hallucination.

**P1 and P2.** P1 concerns the interpretation of the required behavior. P2 additionally requires an identifiable cue that the recorded diagnosis connects to the chosen repair direction. An observed connection does not establish that removing the cue would have changed the outcome.

**V4 and other categories.** A timing diagnosis should identify when a value or transformation is required and when the patch supplies it. A workaround that merely changes accepted input syntax does not establish a timing failure without a documented processing-stage distinction.

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

## Annotation policy

Do not invent supporting evidence or change a benchmark outcome without an applicable evaluation. Assign a category only when the archived issue, patches, trajectory, and evaluation requirements support the stated attribution. Keep outcome labels separate from qualitative diagnoses, and avoid stronger claims than the retained evidence supports.
