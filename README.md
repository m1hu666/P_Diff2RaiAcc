# P_Diff2RaiAcc

This repository archives the model patches, trajectories, evaluation labels, and
reproducible analyses used to compare three coding agents on 100 SWE-bench
Verified tasks with three attempts per model/task.

Provider-specific token definitions, experimental settings, interaction counts,
cost estimates, and task-paired statistical methods are documented in
[docs/METHODS.md](docs/METHODS.md).

## Setup

Use Python 3.10 or newer. The main analysis pipelines use the Python standard
library. Optional inspection and export utilities require the packages listed in
`requirements.txt`.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Repository layout

```text
P_Diff2RaiAcc/
├── analyse/                       # Per-model patches and task text evidence
├── data/
│   ├── data/verified/             # Verified patches and Boolean outcomes
│   └── traj/                      # Saved trajectories and evaluation reports
├── docs/
│   ├── METHODS.md                 # Accounting, settings, and statistical design
│   └── failure_analysis/          # Final codebook, annotations, and case notes
├── result/
│   ├── analyse.md                 # Complete failure-analysis catalogue
│   ├── summary.txt                # Three-trial outcome summary
│   └── Statistics results/        # Generated statistics, tables, and audits
├── scripts/                       # Reproducible analysis and utility scripts
└── examples/                      # Selected task examples
```

## Reproduce the analyses

Run the quantitative resource, settings, outcome, and inferential analysis:

```bash
python3 scripts/run_analysis.py
```

Run the failure-analysis catalogue builder:

```bash
python3 scripts/build_failure_analysis.py
```

The canonical quantitative outputs are written under
`result/Statistics results/`; the complete failure report is written to
`result/analyse.md`. Validation records include input hashes and coverage checks
so the generated tables can be checked against the archived data.

To refresh the optional implementation-source evidence, provide a local agent
checkout explicitly:

```bash
python3 scripts/run_analysis.py --agent-root /path/to/mini-swe-agent
```

## Independent integrity checks

These checks write to separate output locations and do not alter trajectories,
patches, or labels:

```bash
python3 scripts/audit_submission_integrity.py
python3 scripts/audit_inference_usage.py
python3 scripts/cal.py
```

## Supporting utilities

Every script begins with its purpose, inputs, outputs, and mutation scope where
relevant.

| Script | Purpose |
|---|---|
| `scripts/inspector.py` | Interactively inspect one saved trajectory |
| `scripts/res_cmp.py` | Rebuild `result/summary.txt` from verified labels |
| `scripts/cal.py` | Independently summarize reported tokens by outcome |
| `scripts/datavis.py` | Export selected patches and task metadata listed in root `id.txt` |
| `scripts/collectid.py` | Rebuild the saved task-ID list |
| `scripts/label_add.py` | Synchronize one verified label file with its evaluation report; this utility mutates the selected label file |
| `scripts/audit_submission_integrity.py` | Compare submissions, verified patches, and evaluation labels |
| `scripts/audit_inference_usage.py` | Produce an independent trajectory-level usage audit |

Example trajectory inspection:

```bash
python3 scripts/inspector.py \
  --m gpt-5-2025-08-07-medium-reasoning \
  --r 1 \
  --i astropy__astropy-7671
```

Rebuilding `result/summary.txt` requires access to the Hugging Face SWE-bench
Verified dataset for difficulty metadata:

```bash
python3 scripts/res_cmp.py -m \
  claude-sonnet-4-5-20250929 \
  gpt-5-2025-08-07-medium-reasoning \
  gemini-3-pro-preview
```
