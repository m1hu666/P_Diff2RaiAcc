# Taxonomy construction and three-coder verification

This directory documents the taxonomy and preserves three coder checks
of the authors' earlier trial assignments. The coders received the then-current
label and analysis, inspected the linked materials, and recorded decisions in
their own sheets. The [verification packet](VERIFICATION_CASES.md) is now
regenerated from the reconciled annotations and is useful as a current linked
case index; it is not a frozen copy of the exact packet shown before discussion.
The authoritative source records
remain the [trial annotations](../../FINAL-CODEBOOK/failure_annotations.csv) and
the [failure codebook](../../FINAL-CODEBOOK/FAILURE_CODEBOOK.md).

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
observed mode were initially grouped and refined into eleven subcategories.
During the post hoc coder discussion, all nine S3 assignments were reclassified
as V5 evaluation-infrastructure failures and S3 was retired from the final
taxonomy. The reconciled codebook therefore contains eleven final categories.
The subcategories were mapped to five broader stages
derived from the agent's YAML-configured repair workflow and the sequential
trajectory logs: problem understanding, localization, strategy and logic,
implementation and execution, and validation and harness constraints.

The subcategories were therefore induced from trial-level failure evidence,
while the broader stages were organized using a workflow-derived framework.
This is more accurately described as a hybrid inductive-deductive process than
as a wholly unconstrained inductive analysis.

All failures in the fixed experimental corpus were analyzed. Formal saturation
was not used to stop sampling. Intermediate open-code lists, category-change
logs, and independent coder labels from the original construction phase were
not retained; only its final analysis was preserved. The later three-coder
coder sheets are a separate post hoc check. The repository therefore does not support a
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

The submitted responses are provided as three English CSV transcriptions:

- [coder_a.csv](coder_a.csv)
- [coder_b.csv](coder_b.csv)
- [coder_c.csv](coder_c.csv)

The sheets contain the same 242 failed trials, with the earlier category in
each row. The rows use the same task order and are matched by task, model,
and trial. Chinese notes were translated into English without changing the
review judgments. Blank `earliest_link` cells were filled with
`INDETERMINATE` (75 in A, nine in B, none in C). The English synonym
`unsupported` was normalized to `NOT_SUPPORTED`; question marks and
conditional status entries became `INDETERMINATE`, with conditions retained
in the English `reason`. Other blank or informal review fields remain visible.
The current
verification packet adds the reconciled diagnosis and direct links to task
materials, benchmark test-ID lists, candidate patch, and trajectory without
the hash and path columns of the machine-readable annotation file. It is
regenerated with:

```bash
python3 scripts/build_taxonomy_review_packet.py
```

Following [CODING_GUIDE.md](CODING_GUIDE.md), the coders were asked to mark
`ACCEPT` or `CHANGE`. `CHANGE` requires a proposed category from the original
eleven codebook categories or `OTHER` and a concise reason. `ACCEPT` may
include an optional note about wording. Each coder also fills `earliest_link`
to judge whether the displayed current category corresponds to the earliest
observable unrecovered deviation with a direct evidence link to the
unsuccessful submission. Its values are `SUPPORTED`, `NOT_SUPPORTED`, and
`INDETERMINATE`; the latter two require an explanation in the same `reason`
column. The sheets preserve the submitted entries.

This is a post hoc verification of disclosed existing labels and analyses,
not de novo, label-blind coding. The original assignment is a shared reference,
not a fourth independent rating. Because the original open-code lists and
independent labels from the original taxonomy-construction phase were not
retained, this check cannot reconstruct
agreement during the original taxonomy construction. Coders may be influenced
by seeing the authors' labels and explanations.

The three CSVs record the pre-discussion responses. The agreed decisions
are in [talk.md](talk.md); the canonical labels and English diagnoses are in
the [trial annotations](../../FINAL-CODEBOOK/failure_annotations.csv). V5 was
created during reconciliation and was therefore not an option on the original
response sheets. The [verification packet](VERIFICATION_CASES.md) reflects the
reconciled annotations; the CSVs retain each coder's original
`current_category` and response.

## Final chronological-link judgments

The explicit final decisions are stored in
[earliest_link_decisions.csv](earliest_link_decisions.csv). For every failed
trial, apply these rules in order:

1. Use an explicit discussion or adjudication decision when available.
2. Otherwise, when the final primary category is unchanged, assign the status
   selected by at least two of the three coders.
3. Treat a majority of `INDETERMINATE` votes, a three-way split, or a changed
   category without reassessment as a provisional `INDETERMINATE` result.
4. Adjudicate every provisional result as `SUPPORTED` or `NOT_SUPPORTED`. For
   the current provisional V-category cases, assign `SUPPORTED` because the
   selected mode is at the final validation stage. For every non-V case, inspect
   its trajectory, candidate patch, repository state, and evaluation evidence
   to determine whether the selected category is the earliest directly linked
   unrecovered deviation.
5. Do not publish a final `INDETERMINATE` result; an unresolved provisional case
   is an incomplete adjudication and causes the aggregation script to fail.

The voting stage is symmetric over `SUPPORTED`, `NOT_SUPPORTED`, and
`INDETERMINATE`. A majority result requires two matching votes but need not be
unanimous. Explicit adjudication decisions supersede the vote. Assessments of
a replaced category cannot be applied automatically to its replacement, and
no aggregate status establishes or disproves a causal claim. The current
adjudication resolved 44 provisional cases: 21 V-category cases by the stated
validation-stage rule and 23 non-V cases by trial-specific evidence review.

Rebuild the final trial table, counts, and percentages with:

```bash
python3 scripts/summarize_earliest_links.py
```

The [result summary](../../result/Statistics%20results/taxonomy_reliability/README.md)
reports all three statuses. Its
[trial table](../../result/Statistics%20results/taxonomy_reliability/final_earliest_links.csv)
retains the three coder values and the final resolution basis; its
[grouped counts](../../result/Statistics%20results/taxonomy_reliability/earliest_link_summary.csv)
also report results by model and final category. Percentages use all 242 failed
trials in the overall row. `INDETERMINATE` includes missing or unresolved
assessments and does not mean `NOT_SUPPORTED`.

## Agreement statistics

The agreement analysis and all response-conversion rules are documented in
[ANNOTATION_AGREEMENT.md](ANNOTATION_AGREEMENT.md). Agreement is reported as
Fleiss' kappa over the three fixed reviewers: 0.742 overall (all 242 attempts)
and 0.795 for the 40 trials whose final reconciled label is V1 or V2.
The accompanying [`fleiss_kappa.py`](fleiss_kappa.py) reproduces both values
directly from the three reviewer sheets. These statistics use pre-discussion
responses and assess informed verification of existing assignments; they do
not reconstruct blind agreement during the original taxonomy construction.
The chronological-link counts above use a separate final-resolution rule.

## Methodological references

- Fleiss, J. L. (1971). [Measuring nominal scale agreement among many raters](https://doi.org/10.1037/h0031619).
- O'Connor, C., and Joffe, H. (2020). [Intercoder reliability in qualitative research: debates and practical guidelines](https://doi.org/10.1177/1609406919899220).

