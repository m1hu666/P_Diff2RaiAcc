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

These nine statuses were the initial machine-readable discussion decisions.
After applying the majority-vote rule, 44 trials still had a provisional
`INDETERMINATE` result. A second adjudication reviewed the linked trajectories,
candidate patches, repository state, evaluation tests, and reconciled trial
diagnoses. Its grouped results are:

| Task | Trials | Category | Final `earliest_link` | Adjudication basis |
| --- | --- | --- | --- | --- |
| `astropy__astropy-8872` | all 9 | V5 | `SUPPORTED` | V-category validation-stage rule; collection is blocked before candidate behavior is assessed. |
| `django__django-12125` | Gemini 3 | S2 | `SUPPORTED` | The retained module-search strategy bypasses the required nested-type qualified-name serialization path. |
| `django__django-13023` | Claude 2 | P1 | `SUPPORTED` | The trajectory finds both DecimalField layers but chooses the forms layer for a model-save issue. |
| `django__django-16560` | Claude 1 | L1 | `SUPPORTED` | The first scope inventory omits PostgreSQL ExclusionConstraint and the final patch retains that omission. |
| `django__django-16560` | Gemini 1 | I1 | `NOT_SUPPORTED` | ExclusionConstraint is omitted before the later repr editing defect and has an equally direct test link. |
| `django__django-16560` | Gemini 2–3 | V1 | `SUPPORTED` | V-category validation-stage rule; the retained mismatch is the legacy unique_together assertion. |
| `django__django-16560` | GPT 1 | I1 | `NOT_SUPPORTED` | The model patch omits ExclusionConstraint before the later archived mojibake mismatch. |
| `django__django-16560` | GPT 2–3 | I1 | `SUPPORTED` | Failed automated edits leave constructor parameter references without a valid signature. |
| `django__django-10554` | Claude 1 | P1 | `SUPPORTED` | The trajectory mistakes an earlier partial fix for the requested production repair. |
| `django__django-16502` | Claude 2, Gemini 1–2 | P1 | `SUPPORTED` | The trajectories preserve an RFC-valid GET-equivalent length but never recover Django's selected policy of omitting automatically generated Content-Length metadata for consistent HEAD handling. |
| `matplotlib__matplotlib-21568` | GPT 1, GPT 3 | P1 | `SUPPORTED` | The trajectory interprets the spacing request as removal of the explicitly requested TeX wrapper. |
| `matplotlib__matplotlib-26208` | Claude 2 | S1 | `SUPPORTED` | The patch preserves limits but never initializes twin-axis units required by the evaluated behavior. |
| `pylint-dev__pylint-8898` | GPT 2 | I1 | `NOT_SUPPORTED` | An incorrect unmatched-delimiter splitting strategy predates the later table-removal edit defect. |
| `pylint-dev__pylint-4661` | all 9 | V5 | `SUPPORTED` | V-category validation-stage rule; the unavailable appdirs dependency stops test collection. |
| `sphinx-doc__sphinx-11510` | Claude 2 | V2 | `SUPPORTED` | V-category validation-stage rule; the retained trailing newline directly fails the exact assertion. |
| `sympy__sympy-18211` | Gemini 1–2, GPT 1 | S1 | `NOT_SUPPORTED` | The only failing test uses equalities; an unverified fallback fails its second equality rather than an omitted inequality. |
| `sympy__sympy-12489` | Claude 1–3, Gemini 3, GPT 3 | P1 | `SUPPORTED` | The trajectories reduce subclass preservation to `_af_new` paths and never generalize dynamic dispatch to every internal constructor, leaving hard-coded `Perm(...)` paths. |

Together, the initial nine decisions and these 44 adjudications produce 53
explicit statuses in
[earliest_link_decisions.csv](earliest_link_decisions.csv). The CSV records a
trial-specific reason for every decision. The underlying materials are linked
from the [verification packet](VERIFICATION_CASES.md), and the
[aggregation rules](README.md#final-chronological-link-judgments) require every
provisional result to be resolved before publication.

The `django__django-16502` decision does not assert that HTTP forbids a correct
`Content-Length` header on a HEAD response. It records a P1 domain-knowledge
judgment about the trajectories' failure to identify Django's selected
implementation policy: omit the automatically derived header rather than
retain it. The reference implementation and evaluation both enforce that
project-specific choice.

For `django__django-11532` GPT 1, `SUPPORTED` records the reconciled judgment
of coders B and C. Coder C linked the local Message-ID conversion to Unicode
hostname state retained in the shared cache and later sending failures. The
retained per-test archive does not independently confirm that later-send
explanation; the final review judgment and this evidence limitation are both
preserved.

`earliest_link` concerns the earliest observable unrecovered deviation with a
direct archived evidence link. It does not establish a causal root cause.
