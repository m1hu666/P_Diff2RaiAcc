# Annotation Agreement: Three-Coder Verification (Fleiss' kappa)

This page reports the three-coder agreement for the failure annotations as
Fleiss' kappa. The three authors independently verified the then-current
category and diagnosis for each of the 242 failed attempts and submitted their
responses before case-by-case reconciliation. The statistics therefore measure
agreement when verifying the proposed assignments, not blind agreement during
the original taxonomy construction.

## Response conversion

Each reviewer response is converted to one category or an unresolved state:

- `ACCEPT` -> the row's `current_category`.
- `CHANGE` with a single recognizable code -> that code.
- `CHANGE` with `OTHER-V5` -> `V5`.
- `CHANGE` with multiple, blank, or unrecognized codes -> unresolved.

## Method

Fleiss' kappa is computed over the three fixed reviewers on all 242 attempts
(or on the V1/V2 subset). With $N$ subjects and three raters,

$$
P_o=\frac{1}{N}\sum_{i=1}^{N}\frac{1}{3}\sum_{1\le r<s\le 3}\mathbf{1}(z_{ir}=z_{is}),
\qquad
P_e=\sum_g\left(\frac{n_g}{3N}\right)^2,
\qquad
\kappa=\frac{P_o-P_e}{1-P_e},
$$

where $z_{ir}$ is reviewer $r$'s converted category for subject $i$ and $n_g$
is the total number of ratings assigned to category $g$ across the three
reviewers.

A `CHANGE` response whose `proposed_category` does not yield a single code
(multiple, blank, or unrecognized) is treated as an unresolved rating. The 12
such ratings in the data (2 from reviewer A and 10 from reviewer B, each on a
distinct attempt) are placed in one common `UNRESOLVED` nominal state so that
all 242 attempts remain in the denominator. In the observed-agreement term
$P_o$, a pair agrees only when both ratings carry the same value: an
unresolved rating paired with a substantive category is therefore a
disagreement, while two unresolved ratings on the same attempt would agree
(this does not occur in the current data). In the chance-agreement term $P_e$,
the `UNRESOLVED` state contributes like any other category through its
marginal proportion $n_{\text{UNRESOLVED}}/(3N)$. The V1/V2 subset consists of
the trials whose prefilled `current_category` is `V1` or `V2`.

## Results

| Subset | N | Agreeing pairs | $P_o$ | $P_e$ | Fleiss' kappa |
| --- | ---: | ---: | ---: | ---: | ---: |
| Overall | 242 | 562 / 726 | 0.7741 | 0.1242 | 0.742 |
| V1/V2 trials | 38 | 110 / 114 | 0.9649 | 0.6236 | 0.907 |

## Reproduction

```bash
python docs/taxonomy_methodology/fleiss_kappa.py \
  docs/taxonomy_methodology/coder_a.csv \
  docs/taxonomy_methodology/coder_b.csv \
  docs/taxonomy_methodology/coder_c.csv
```

The script uses only the Python standard library.
