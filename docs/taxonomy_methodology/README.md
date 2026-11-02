# Taxonomy construction and three-coder verification

This directory documents the taxonomy and provides three independent checks
of the authors' existing trial assignments. Coders receive the current label
and analysis for each trial in the readable
[verification packet](VERIFICATION_CASES.md), then inspect the linked materials
and record a decision in their own sheet. The authoritative source records
remain the [trial annotations](../failure_analysis/failure_annotations.csv) and
the [failure codebook](../failure_analysis/FAILURE_CODEBOOK.md).

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
   one primary observed failure mode per failed trial, with evidence limitations
   recorded in the diagnosis or case notes for assignments awaiting further
   verification. If
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

## Source repositories

The failed tasks in this taxonomy check come from
[Astropy](https://github.com/astropy/astropy),
[Django](https://github.com/django/django),
[Matplotlib](https://github.com/matplotlib/matplotlib),
[Requests](https://github.com/psf/requests),
[Pylint](https://github.com/pylint-dev/pylint),
[scikit-learn](https://github.com/scikit-learn/scikit-learn),
[Sphinx](https://github.com/sphinx-doc/sphinx), and
[SymPy](https://github.com/sympy/sympy).

## Three-coder verification of existing assignments

The check uses three blank response sheets:

- [coder_a.csv](coder_a.csv)
- [coder_b.csv](coder_b.csv)
- [coder_c.csv](coder_c.csv)

The sheets contain the same 242 failed trials, ordered by repository and then
by increasing task failure count. Each row shows the current category. The
verification packet adds the existing diagnosis and direct links to task
materials, benchmark test-ID lists, candidate patch, and trajectory without
the hash and path columns of the machine-readable annotation file. It is
regenerated with:

```bash
python3 scripts/build_taxonomy_review_packet.py
```

Following [CODING_GUIDE.md](CODING_GUIDE.md), each coder independently marks
`ACCEPT`, `CHANGE`, or `UNSURE`. `CHANGE` requires a proposed category from the
eleven codebook categories or `OTHER` and a concise reason. `UNSURE` requires a
reason describing what prevents a decision; it does not introduce a failure
category or change the retained assignment. `ACCEPT` may include an optional
note about wording. Each coder also fills `earliest_link` to judge whether the
displayed current category corresponds to the earliest observable unrecovered
deviation with a direct evidence link to the unsuccessful submission. Its
values are `SUPPORTED`, `NOT_SUPPORTED`, and `INDETERMINATE`; the latter two
require an explanation in the same `reason` column. The three coders work
separately and lock their sheets before seeing anyone else's responses or
discussing individual trials.

This is a post hoc verification of disclosed existing labels and analyses,
not de novo, label-blind coding. The original assignment is a shared reference,
not a fourth independent rating. Because the original open-code lists and
pre-reconciliation labels were not retained, this check cannot reconstruct
agreement during the original taxonomy construction. Coders may be influenced
by seeing the authors' labels and explanations.

After all three sheets are complete, run:

```bash
python3 scripts/taxonomy_coder_check.py compare
```

The command validates the locked sheets and creates a discussion table and
pre-discussion statistics. Report each coder's acceptance, proposed changes,
and unresolved decisions; the number accepted by all three; and pairwise
agreement on their chosen categories. The report also provides three-coder
agreement and task-cluster bootstrap intervals where defined. Category
agreement excludes rows with an `UNSURE` decision and states its denominator.
The chronological-link responses are compared separately, retaining all three
values and their denominators. Agreement with the current label measures
review concordance. It is not an estimate of independent agreement during
original coding.

Discuss every proposed change, `UNSURE` decision, and chronological-link
assessment other than `SUPPORTED`; inspect any additional comments on accepted
labels. Where the coders choose different categories or chronological-link
values, the comparison table keeps each pre-discussion response intact. The
canonical category changes only after an explicit reconciled decision. If the
category changes, reassess `final_earliest_link` for that final category.

After discussion fields and final decisions have been completed in the
comparison table, run:

```bash
python3 scripts/taxonomy_coder_check.py summarize
```

This reports the reconciled category distribution and the number and
percentage of trials rated `SUPPORTED`, `NOT_SUPPORTED`, or `INDETERMINATE`
for the final category. The `SUPPORTED` percentage over all failed trials
answers how often the chronological attribution convention is supported by
the retained evidence. An additional assessable-only percentage uses
`SUPPORTED / (SUPPORTED + NOT_SUPPORTED)`; `INDETERMINATE` is never counted as
`NOT_SUPPORTED`. The script resamples whole tasks for a 95% interval on the
all-trial supported proportion. These are observational evidence-link
judgments, not proof of a causal root cause. No agreement statistic should be
reported before the three coder sheets have actually been completed and
locked.

## Files created after coding

The comparison command writes:

- `docs/taxonomy_methodology/coder_comparison.csv`, the table used for
  discussion and reconciliation; and
- `result/Statistics results/taxonomy_reliability/agreement.json`, the numeric
  pre-discussion verification summary.

After reconciliation, the summarize command writes
`result/Statistics results/taxonomy_reliability/final_review_summary.json`.

The comparison table is created only after all three coder sheets are complete and
is not overwritten automatically after discussion fields have been edited.

## Methodological references

- Cohen, J. (1960). [A coefficient of agreement for nominal scales](https://doi.org/10.1177/001316446002000104).
- O'Connor, C., and Joffe, H. (2020). [Intercoder reliability in qualitative research: debates and practical guidelines](https://doi.org/10.1177/1609406919899220).

