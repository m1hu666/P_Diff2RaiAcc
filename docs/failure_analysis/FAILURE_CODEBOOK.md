# Failure annotation codebook

This codebook defines the stages and categories used in the failure analysis. The machine-readable version is [failure_codebook.json](failure_codebook.json). Category names and codes follow the manuscript; numeric codes provide the corresponding hierarchical notation.

The annotation unit is one failed model trial on one task. Each failed trial has one primary category, chosen as the earliest causally dominant unrecovered breakdown supported by the archived evidence. A task can contain trials with different categories. Secondary manifestations may appear in a trial's explanation without generating additional category counts.

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

The published count tables summarize the canonical trial annotations. The existence of a coded dataset does not by itself establish independent-coder agreement, causal priority, or semantic correctness. No agreement coefficient should be inferred without a separate reliability study.

Apply the manuscript's Failure Diagnosis Workflow: compare candidate and reference patches, reconstruct historical context when necessary, trace the trajectory, inspect the evaluation requirements, and identify the earliest causally dominant unrecovered breakdown. A transient error that is subsequently recovered is not the primary failure.

Retain selected successful cases as a separate comparison set. They illustrate alternative repairs or successful execution and receive no failure label. Exclude them from failure-category denominators.

## Category boundaries

**L1 and S1.** L1 concerns where the repair is attempted and whether all required implementation locations are covered. S1 concerns which required behaviors the selected logic handles. Omitting a subclass is a scope problem; handling creation but not later updates is incomplete behavioral coverage. Some cases can exhibit both. Use the earliest causally dominant breakdown and explain the specific omission rather than applying an automatic priority rule.

**S2 and V3.** S2 concerns the suitability of the repair strategy itself. V3 concerns broader consequences for state or contracts exercised beyond the immediate reproduced scenario. A faulty strategy can also cause a regression, so these are not inherently exclusive mechanisms. Use the primary failure mechanism for the single-label assignment. V3 includes type and contract regressions and should not uniformly be described as environment pollution.

**V1 and V2.** V1 concerns the scope of required behavior; V2 concerns its concrete representation. A test that checks an additional exception case can motivate V1. An exact argument-list or string assertion can motivate V2. Neither label alone proves that the candidate is semantically equivalent to the reference or that the test is invalid: representations can form part of a public contract.

**I1 and other categories.** I1 requires observable tool or repository-state evidence. Suitable evidence includes a command error, an edit that was not executed, a file differing from the intended edit, or a claim that a change was applied when the saved state shows otherwise. A failed benchmark result or unrelated patch content alone does not establish a tool failure or state hallucination.

**P1 and P2.** P1 concerns the interpretation of the required behavior. P2 additionally requires an identifiable cue that the recorded diagnosis connects to the chosen repair direction. An observed connection does not establish that removing the cue would have changed the outcome.

**V4 and other categories.** A timing diagnosis should identify when a value or transformation is required and when the patch supplies it. A workaround that merely changes accepted input syntax does not establish a timing failure without a documented processing-stage distinction.

## Annotation policy

Do not invent supporting evidence or change a benchmark outcome without an applicable evaluation. Assign a category only when the archived issue, patches, trajectory, and evaluation requirements support the stated mechanism. Keep outcome labels separate from qualitative diagnoses, and avoid stronger claims than the retained evidence supports.
