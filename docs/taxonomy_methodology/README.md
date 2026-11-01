# Taxonomy construction and coder check

This directory contains the materials for checking whether two additional
coders can independently apply the final failure taxonomy. It complements the
[failure codebook](../failure_analysis/FAILURE_CODEBOOK.md) and the current
canonical [trial annotations](../failure_analysis/failure_annotations.csv).

## How the taxonomy was constructed

The annotation unit was one unresolved model trial. Trial diagnosis followed
the three-phase Failure Diagnosis Workflow reported in the manuscript:

1. **Task preparation and triage:** tasks were grouped by repository and, within
   each repository, ordered by ascending total failure count across the nine
   attempts.
2. **Diagnostic iteration:** all failed generated patches for a task were
   compared with the developer reference patch. When this comparison was
   insufficient, the historical repository context was reconstructed from the
   task's base commit. The sequential trajectory was then traced to enumerate
   observable deviations, determine whether they were later recovered, and
   connect retained effects to the submitted patch. When a self-generated
   reproduction succeeded but official evaluation failed, the benchmark test
   patch and evaluation requirements were also inspected.
3. **Synthesis:** the issue specification, patch evidence, repository context,
   evaluation requirements, and trajectory evidence were combined to select
   one primary evidence-supported observed failure mode per failed trial. If
   multiple unrecovered candidates had a direct archived evidence link to the
   unsuccessful submission, chronology was used only as a deterministic
   tie-breaker. Co-occurring or downstream problems were not counted again.

Trial-level attribution statements describing the same or closely related
observed mode were then grouped and refined into the eleven subcategories in
the final codebook. The subcategories were mapped to five broader stages
derived from the agent's YAML-configured repair workflow and the sequential
trajectory logs: problem understanding, localization, strategy and logic,
implementation and execution, and validation and harness constraints.

The subcategories were therefore induced from trial-level failure evidence,
while the broader stages were organized using a workflow-derived framework.
This is more accurately described as a hybrid inductive-deductive process than
as a wholly unconstrained inductive analysis.

All failures in the fixed experimental corpus were analyzed. Formal saturation
was not used to stop sampling. Intermediate open-code lists, category-change
logs, and pre-reconciliation coder labels were not retained; only the final
analysis was preserved. The repository therefore does not support a
retrospective claim that formal saturation or a particular level of original
intercoder agreement was reached.

The trajectories are observational records. No intermediate decision was
experimentally manipulated and no counterfactual trajectory was evaluated.
The labels therefore represent diagnostic attributions supported by the
archived evidence, not identified causal root causes.

## Two-coder check

The new check uses two files:

- [coder_a.csv](coder_a.csv)
- [coder_b.csv](coder_b.csv)

Both files contain the same 242 trial identifiers but omit the canonical
category and canonical diagnosis. Each coder fills `category`,
`failure_reason`, and `earliest_link` independently by following
[CODING_GUIDE.md](CODING_GUIDE.md). The allowed categories are the eleven
codebook labels plus `OTHER`. Their row order implements the manuscript's task
triage rule: repository grouping followed by ascending task failure count.

The coders must not view the canonical annotation file, the generated failure
catalogue, `result/analyse.md`, or the other coder's sheet before submitting
their locked file. Removing the answer columns from the sheets is insufficient
if a coder can inspect those other repository files. Provide a separate
read-only evidence package when practical. The study is label-blind and
coder-independent; it should not be described as model-blind because model
identity may be apparent from the trajectories.

After both sheets are complete, run:

```bash
python3 scripts/taxonomy_coder_check.py compare
```

The command validates the two sheets, computes pre-discussion A-B agreement,
and creates a comparison table containing the canonical, Coder A, and Coder B
decisions. Discussion and any final category or rationale changes happen only
after this table has been generated.

All category or `earliest_link` disagreements require discussion. Cases with
the same values but materially different attribution rationales should also be
reviewed when reading the side-by-side reasons; text equivalence is not inferred
automatically.

The primary reliability results are A-B exact agreement and unweighted Cohen's
kappa. Because multiple trials belong to the same task, 95% intervals are
computed by resampling complete task clusters. Category agreement and
`earliest_link` agreement are reported separately. Agreement between either
coder and the canonical category is secondary concordance, not a third
independent rating and not a reconstruction of the original coding process.

After discussion fields and final decisions have been completed in the
comparison table, run:

```bash
python3 scripts/taxonomy_coder_check.py summarize
```

This reports the reconciled `SUPPORTED`, `NOT_SUPPORTED`, and `INDETERMINATE`
counts. A `SUPPORTED` result means that the archived artifacts directly support
the chronological attribution convention; it does not establish a causal root
cause. Counts and percentages describe the fixed 242-trial corpus. The summary
also provides a task-cluster bootstrap interval for the supported proportion
when a task-level generalization is desired; failed trials must not be treated
as independent Bernoulli observations.

## Files created after coding

The comparison command writes:

- `docs/taxonomy_methodology/coder_comparison.csv`, the table used for
  discussion and reconciliation; and
- `result/Statistics results/taxonomy_reliability/agreement.json`, the numeric
  pre-discussion agreement summary.

After reconciliation, the summarize command writes
`result/Statistics results/taxonomy_reliability/final_attribution_summary.json`.

The comparison table is created only after both coder sheets are complete and
is not overwritten automatically after discussion fields have been edited.

## Methodological references

- Cohen, J. (1960). [A coefficient of agreement for nominal scales](https://doi.org/10.1177/001316446002000104).
- O'Connor, C., and Joffe, H. (2020). [Intercoder reliability in qualitative research: debates and practical guidelines](https://doi.org/10.1177/1609406919899220).

