# Reconciled taxonomy decisions

This page records the final decisions from the three-coder discussion. The
coder responses and notes are available in the English `coder_a.csv`,
`coder_b.csv`, and `coder_c.csv` transcriptions. The canonical trial diagnoses are in
[`failure_annotations.csv`](../../FINAL-CODEBOOK/failure_annotations.csv).
Rows not listed below retain their pre-discussion category. `V5` was added
during reconciliation for evaluation-infrastructure failures; it was
not an option on the original coder sheets. These decisions concern recorded
unresolved trials and do not change their benchmark outcome labels.

| Task | Trials | Before | Final | Basis of final diagnosis |
| --- | --- | --- | --- | --- |
| `astropy__astropy-8872` | Claude, Gemini, GPT: trials 1–3 each | V3 | V5 | Coder C identified a dependency deprecation warning treated as an error during test collection. The candidate float16 behavior was not assessed by that run. |
| `django__django-10554` | Claude 1 | I1 | P1 | Coder C found that the submitted changes were only a reproduction and tests; the agent treated an earlier partial fix as if the reported ordering problem were already resolved. |
| `django__django-13023` | Claude 2 | V1 | P1 | Coders A and C found that the agent interpreted a model-field failure as a forms-field problem and changed the wrong component. |
| `django__django-16560` | Claude 1 | L1 | L1 | Final discussion retains the original scope diagnosis: the patch adds error-code support to core constraints but omits the PostgreSQL ExclusionConstraint subclass. |
| `django__django-16560` | Gemini 1 | L1 | I1 | Coder A traced an unintended `CheckConstraint.__repr__` edit: five placeholders receive four formatting arguments, leaving an unrecovered `TypeError`. |
| `django__django-16560` | Gemini 2–3 | L1 | V1 | Coder A identified the added field-based uniqueness assertion that retains `unique_together` despite a supplied custom code. |
| `django__django-16560` | GPT 1 | L1 | I1 | The verified patch changes an unchanged context line to mojibake, while the trajectory's final submission retains the original quotation marks. This concrete patch-state mismatch is assigned I1; it does not establish that the agent intended the corrupted line. |
| `django__django-16560` | GPT 2–3 | S1 / L1 | I1 | Coder A and/or C found unrecovered editing errors in the constructor signatures; GPT 2 changed a comment instead of the intended code, and GPT 3 used a replacement that missed the actual signature. |
| `matplotlib__matplotlib-26208` | Claude 2 | P2 | S1 | Coder C found that the patch preserves data limits but omits the required unit initialization for twinned axes. |
| `psf__requests-2931` | Gemini 1, Gemini 3, GPT 2, GPT 3 | S1 | V3 | Coder A identified that the patches establish the requested binary-body behavior but change the shared encoder's return type on the existing URL-parameter path. That path is previously supported behavior rather than an unimplemented part of the requested body change, so its confirmed compatibility regression is classified as V3 rather than S1. |
| `pylint-dev__pylint-8898` | GPT 2 | P1 | I1 | Coder A found that the submitted edit removes `_TYPE_TRANSFORMERS`, so normal option parsing fails before the new splitter runs. |
| `pylint-dev__pylint-4661` | Claude, Gemini, GPT: trials 1–3 each | S3 | V5 | Final discussion assigns V5 to all nine trials. The evaluation test imports `appdirs` unconditionally, but that dependency is unavailable in the sb-cli environment for these submissions, so collection stops before candidate path-resolution behavior is exercised. The data-versus-cache and abstraction differences from the reference remain unassessed rather than establishing S3. |
| `sphinx-doc__sphinx-11510` | Claude 2 | S2 | V2 | Coders A and C found an extra trailing newline in the emitted event text relative to the exact assertion. |

The discussion also settled the following chronological-link audits:

| Task | Trials | Final `earliest_link` |
| --- | --- | --- |
| `django__django-11532` | GPT 1 | `SUPPORTED` |
| `django__django-16502` | Claude 1, Claude 3, GPT 2 | `SUPPORTED` |
| `psf__requests-2931` | Gemini 1, Gemini 3, GPT 2, GPT 3 | `SUPPORTED` |
| `sympy__sympy-18211` | Gemini 3 | `NOT_SUPPORTED` |

These nine explicit statuses are the machine-readable inputs in
[earliest_link_decisions.csv](earliest_link_decisions.csv). The
[aggregation rules](README.md#final-chronological-link-judgments) determine the
remaining trial statuses.

For `django__django-11532` GPT 1, `SUPPORTED` records the reconciled judgment
of coders B and C. Coder C linked the local Message-ID conversion to Unicode
hostname state retained in the shared cache and later sending failures. The
retained per-test archive does not independently confirm that later-send
explanation; the final review judgment and this evidence limitation are both
preserved.

`earliest_link` concerns the earliest observable unrecovered deviation with a
direct archived evidence link. It does not establish a causal root cause.
