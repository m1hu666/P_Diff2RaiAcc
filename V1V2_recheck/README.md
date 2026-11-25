# V1/V2 Validation

## Purpose

To further validate our findings, three software developers independently review all 40 cases classified as V1 (Specification-Oracle Gap; 10 cases) or V2 (Strict Output Format Mismatch; 30 cases).

For each case, the reviewers assess two aspects:

1. **Q1 – Patch vs. issue:** Does the generated patch satisfy the behavior described in the issue report?
2. **Q2 – Benchmark vs. issue:** Does the benchmark impose additional requirements or constraints not explicitly specified in the issue report?

The reviewers independently examine the issue descriptions, generated patches, reference patches, and relevant benchmark test cases.

## Labels

For each case, record:

- `q1_patch_satisfies_issue_report` – `√` if the generated patch satisfies the
  behavior described in the issue report, `×` otherwise.
- `q2_benchmark_adds_unstated_constraints` – `√` if the benchmark imposes
  additional requirements or constraints not explicitly specified in the issue
  report, `×` otherwise.
- `final_judgment`:

  - `√` – Both Q1 and Q2 hold, confirming the case as a valid V1/V2 instance.
  - `×` – At least one of Q1 or Q2 does not hold.

- `note` – a short, evidence-based explanation of the judgment, especially when
  a label is `×`. For a negative judgment, specify whether Q1, Q2, or both do
  not hold.

Cases with insufficient evidence should be flagged for discussion rather than automatically confirmed.

## Case List and Source Materials

The 40 cases are listed in `v1v2_validation_form.csv`, with one row per case.

Each of the three reviewers independently completes their assigned file:

- `checker_a.csv`
- `checker_b.csv`
- `checker_c.csv`

The canonical category, diagnosis, and artifact paths (issue statement,
generated patch, reference patch, and benchmark test patch) for each case are
available in the
[failure trial catalogue](../result/Statistics%20results/full/failures/failure_trial_catalog.csv).
