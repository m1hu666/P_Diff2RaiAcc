# Failure-analysis inputs

This directory contains the curated inputs for the failure analysis. The
generated catalogue and statistics are stored under `result/`, so source
annotations remain separate from derived artifacts.

| File | Role |
|---|---|
| `FAILURE_CODEBOOK.md` | Human-readable category definitions and annotation rules |
| `failure_codebook.json` | Machine-readable version of the same taxonomy |
| `failure_annotations.csv` | One primary-category annotation for every failed trial |
| `failure_case_notes.json` | Task-level diagnostic notes for tasks containing at least one failed trial |

Rebuild and validate the derived failure outputs from the repository root:

```bash
python3 scripts/build_failure_analysis.py
```

The builder enforces one-to-one coverage of the archived `label=false` records,
checks retained evidence hashes, and writes the complete English report to
`result/analyse.md`.

The separate [taxonomy coder-check package](../taxonomy_methodology/README.md)
documents how the taxonomy was constructed and provides two label-blind coder
sheets plus the comparison procedure. Canonical final annotations do not
substitute for pre-discussion coder labels.
