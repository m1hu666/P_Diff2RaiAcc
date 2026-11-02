# Failure-analysis inputs

This directory contains the curated inputs for the failure analysis. The
generated catalogue and statistics are stored under `result/`, so source
annotations remain separate from derived artifacts.

| File | Role |
|---|---|
| `FAILURE_CODEBOOK.md` | Human-readable category definitions and annotation rules |
| `failure_codebook.json` | Machine-readable version of the same taxonomy |
| `failure_annotations.csv` | One retained primary-category annotation for every failed trial |
| `failure_case_notes.json` | Task-level diagnostic notes for tasks containing at least one failed trial |

Rebuild and validate the derived failure outputs from the repository root:

```bash
python3 scripts/build_failure_analysis.py
```

The builder enforces one-to-one coverage of the archived `label=false` records,
checks retained evidence hashes, and writes the complete English report to
`result/analyse.md`.

Assignments requiring further verification remain in their existing categories.
Their evidence limitations are recorded in the diagnoses and case notes;
retention does not mean that those attributions were newly confirmed.

Small baseline-versus-candidate checks supporting the S2/V3 boundary can be run
without model access or external packages:

```bash
python3 scripts/check_failure_boundary_examples.py
```

The script extracts archived source and patch hunks. Its Sphinx and printer
checks use dependency or dispatch stubs and do not rerun full historical test
suites. The optional equality-fallback check requires an unmodified
[historical SymPy checkout](https://github.com/sympy/sympy/tree/b4f1aa3540fe68d078d76e78ba59d022dd6df39f)
and `mpmath==1.3.0`:

```bash
python3 scripts/check_failure_boundary_examples.py \
  --sympy-root /path/to/historical-sympy
```

This checks both official target equality assertions and tests whether the
candidate's transformed condition admits an extraneous solution. It is a
diagnostic reproduction, not a new benchmark outcome. `--output PATH` saves
the check results as JSON.

The separate [taxonomy coder-check package](../taxonomy_methodology/README.md)
documents how the taxonomy was constructed and provides a readable
[verification packet](../taxonomy_methodology/VERIFICATION_CASES.md), three
independent coder sheets, and the comparison procedure. This check presents
the current labels and diagnoses to the coders; its results assess those
existing assignments rather than reconstructing the original coding process.
