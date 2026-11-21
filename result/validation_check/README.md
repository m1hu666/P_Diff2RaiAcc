# Evidence for the V1/V2 analysis

## Agreement on the 40 final V1/V2 cases

| Pre-discussion result | Value |
| --- | ---: |
| Final V1/V2 assignments | 40/242 (16.5%) |
| All three labels match the final category | 33/40 (82.5%) |
| At least two labels match the final category | 38/40 (95.0%) |
| Pairwise observed agreement A–B / A–C / B–C | 92.5% / 85.0% / 82.5% |
| Pairwise Cohen's kappa A–B / A–C / B–C | 0.815 / 0.636 / 0.599 |
| Overall pair agreement | 104/120 (86.7%) |
| Conger's kappa | 0.681 |
| V1 unanimous / at-least-two match | 4/10 (40.0%) / 8/10 (80.0%) |
| V2 unanimous / at-least-two match | 29/30 (96.7%) / 30/30 (100.0%) |

A sensitivity analysis gives 38/242 (15.7%) when only majority-supported
assignments are retained and 33/242 (13.6%) when unanimity is required. The
lower agreement for V1 is one reason not to interpret 16.5% as a
semantic-correctness rate.

## Selection of the external-evidence subset

The unit of selection is a task rather than an attempt because attempts for
the same task share the same issue-level semantic dispute. We screened all
nine tasks represented by the 40 V1/V2 attempts using the same eligibility
conditions:

1. **Independent provenance:** exclude the original issue, reference PR, gold
   commit/test, and documentation derived from that fix.
2. **Behavioral relevance:** require an authoritative artifact that directly
   specifies or executes the disputed type, exception, argument structure, or
   transformation; confirmation of only the underlying bug is insufficient.
3. **Maturity and reproducibility:** require a merged/released upstream
   artifact, an official executable test, or a final external specification.
   An open, unreviewed PR is not sufficient.
4. **Direction neutrality:** include qualifying evidence whether it supports
   the candidate, exposes a candidate limitation, or gives a mixed result.
5. **Shared task behavior:** count attempts only when they exhibit the same
   behavior addressed by the external artifact.

All qualifying tasks were retained. Thus, this is a post hoc, exhaustive
criterion-based subset rather than a random, preregistered, or representative
sample, and it is not used to estimate a semantic-correctness rate. Django
ticket fields such as *Accepted*, *Has patch*, and *Needs tests* record
workflow state; without independent review, a merged change, or executable
authoritative evidence, they are not treated as validation.

| Screened task | Category / attempts | Independent evidence after excluding task/reference provenance | Screening result |
| --- | ---: | --- | --- |
| `django__django-11790` | V2 / 5 | The test added by the independent, closed/fixed [Django #19423](https://code.djangoproject.com/ticket/19423) ([archived patch](https://code.djangoproject.com/attachment/ticket/19423/19423-1.diff)) asserts string-valued `widget.attrs["maxlength"]` for model-backed `CharField` widgets. | Eligible; supports the candidate representation, not whole-patch equivalence. |
| `django__django-13023` | V1 / 4 | CPython's executable Decimal tests at the immutable [Python 3.8.20 tag](https://github.com/python/cpython/blob/v3.8.20/Lib/test/test_decimal.py) assert that malformed tuples raise `ValueError`. | Eligible; exposes the candidates' omitted exception case. |
| `django__django-13406` | V1 / 4 | The relevant `values_list()` documentation and tests derive from the original issue/reference change. | Not eligible. |
| `django__django-14140` | V2 / 6 | [Django #32651](https://code.djangoproject.com/ticket/32651) independently reproduces the `Q`/`Exists` crash and confirms the upstream fix, but does not decide kwargs versus positional deconstruction. | Contextual only; fails exact-behavior criterion. |
| `django__django-14771` | V2 / 4 | [PEP 540](https://peps.python.org/pep-0540/) specifies `-X utf8`, and CPython's executable tests at the immutable [Python 3.9.19 tag](https://github.com/python/cpython/blob/v3.9.19/Lib/test/test_cmd_line.py) run the split `"-X", "utf8"` form. | Eligible; supports the candidate representation for the demonstrated option. |
| `django__django-16560` | V1 / 2 | Later [Django #37329](https://code.djangoproject.com/ticket/37329) and [PR #21933](https://github.com/django/django/pull/21933) directly propose honoring the supplied code, but the PR remains open and has no review. | Provisional only; fails maturity criterion. |
| `sphinx-doc__sphinx-11510` | V2 / 1 | Later issues [#11643](https://github.com/sphinx-doc/sphinx/issues/11643) and [#11648](https://github.com/sphinx-doc/sphinx/issues/11648), resolved by merged [PR #11657](https://github.com/sphinx-doc/sphinx/pull/11657), revise the include-event contract but do not decide the disputed trailing newline. | Qualifying context only; fails exact-behavior criterion. |
| `sphinx-doc__sphinx-7748` | V2 / 9 | A [later merged Sphinx change with tests](https://github.com/sphinx-doc/sphinx/commit/94b5607591cde699e95b8f7ec8a949adc312f98b) adopts consecutive signature scanning but still removes a present backslash. | Eligible; supports the scanning strategy but exposes the retained-backslash mismatch. |
| `sphinx-doc__sphinx-8056` | V2 / 5 | No later independent artifact decides the configuration-dependent combined-versus-split representation. | Not eligible. |

The resulting subset contains four of nine tasks and 22 of 40 attempts
(55.0%). Its results are deliberately mixed:

| External result | Tasks | Attempts |
| --- | --- | ---: |
| Supports an alternative candidate representation | `django__django-11790`, `django__django-14771` | 9 |
| Exposes a genuine candidate coverage gap | `django__django-13023` | 4 |
| Supports one part of the strategy but confirms the remaining mismatch | `sphinx-doc__sphinx-7748` | 9 |

These counts identify attempts for which an authoritative independent artifact
bears directly on the disputed behavior; they do not identify 22 semantically
correct patches. The evidence is task-level: it applies to attempts sharing
the stated behavior and is not a separate live execution of every archived
patch. The contextual and provisional records are disclosed but are not added
to the 22-attempt subset.

## Qualified formulation for the paper

> Manual failure analysis assigned 40 of 242 failed attempts (16.5%) to V1 or
> V2. In separate pre-discussion assessment of these 40 cases by three
> authors, all three labels matched the final category in 33 cases (82.5%),
> at least two matched in 38 cases (95.0%), and Conger's kappa was 0.681. We
> also conducted a post hoc screen of all nine represented tasks using uniform,
> outcome-independent provenance, relevance, maturity, and coverage criteria.
> Independent authoritative evidence was available for four tasks, covering 22 of the 40
> attempts: it supported the alternative representation in nine attempts,
> exposed an additional input-coverage gap in four, and supported only part of
> the strategy while confirming the remaining mismatch in nine. This
> criterion-based subset is not treated as representative, and its task-level
> evidence is not a whole-patch equivalence proof. Accordingly, 16.5% is
> reported as the incidence of two diagnostic categories, not as a
> semantic-correctness rate or a count of benchmark false negatives.
