# Open-Source Package for *Characterizing the Failure Modes of LLMs in Resolving Real-World GitHub Issues*

This repository is the open-source replication package for the paper
*Characterizing the Failure Modes of LLMs in Resolving Real-World GitHub
Issues*. It archives the model patches, complete agent trajectories, evaluation
outcomes, qualitative annotations, and reproducible analyses for three models
evaluated with mini-SWE-agent on 100 SWE-bench Verified tasks, with three trials
per model and task (900 trials in total).

All analyses operate on the archived artifacts and do not require model API
access.

## Reviewer-requested replication materials

The reviews explicitly requested that the replication package contain the
following materials. These are the primary entry points.

| Requested material | Location in this repository |
|---|---|
| **Task IDs** | The complete 100-task list is [`data/data/verified/instance_id_list.json`](data/data/verified/instance_id_list.json). |
| **Final labels and annotation rationale** | Archived pass/fail outcomes and submitted patches are in [`data/data/verified/`](data/data/verified/). The final reconciled qualitative labels and trial-level diagnoses are in [`FINAL-CODEBOOK/failure_annotations.csv`](FINAL-CODEBOOK/failure_annotations.csv), with task-level rationale and interpretation notes in [`FINAL-CODEBOOK/failure_case_notes.json`](FINAL-CODEBOOK/failure_case_notes.json). [`FINAL-CODEBOOK/README.md`](FINAL-CODEBOOK/README.md) explains the fields and their scope. |
| **Complete qualitative-analysis protocol, coding guidelines, codebook, and category definitions** | The taxonomy-construction and verification procedure is documented in [`docs/taxonomy_methodology/README.md`](docs/taxonomy_methodology/README.md), and the coder protocol is in [`CODING_GUIDE.md`](docs/taxonomy_methodology/CODING_GUIDE.md). The authoritative category definitions, decision rules, and boundaries are in [`FAILURE_CODEBOOK.md`](FINAL-CODEBOOK/FAILURE_CODEBOOK.md), with a machine-readable version in [`failure_codebook.json`](FINAL-CODEBOOK/failure_codebook.json). |
| **mini-SWE-agent prompting strategy and interaction loop** | [`docs/METHODS.md`](docs/METHODS.md#experimental-settings-and-prompts) documents the agent version, prompting strategy, serial bash interaction loop, and prompt consistency across trials. Exact archived templates are in [`prompt_templates.json`](result/Statistics%20results/settings/prompt_templates.json), and the nine-attempt-per-task consistency audit is in [`prompt_consistency.csv`](result/Statistics%20results/settings/prompt_consistency.csv). Every archived trajectory under [`data/traj/`](data/traj/) retains its configuration and complete ordered message history. |

The qualitative label is an evidence-based diagnostic annotation and is
separate from the archived benchmark pass/fail outcome. “Final” means
reconciled for this fixed corpus; it does not imply causal identification,
universal taxonomy completeness, or formal saturation.

## Additional evidence for the revision

Other review comments asked for stronger methodological and empirical support,
although they did not explicitly require these materials to be placed in the
repository. The package also provides:

- three-coder, pre-discussion verification sheets, reconciliation records, and
  agreement analysis in
  [`docs/taxonomy_methodology/`](docs/taxonomy_methodology/)—see
  [`ANNOTATION_AGREEMENT.md`](docs/taxonomy_methodology/ANNOTATION_AGREEMENT.md)
  for the scope and limitations of the reported agreement;
- an independent review of all 40 V1/V2 cases in
  [`V1V2_recheck/`](V1V2_recheck/README.md);
- archived provider, agent, token-accounting, interaction-count, and prompt
  evidence in
  [`result/Statistics results/settings/`](result/Statistics%20results/settings/)
  and [`docs/METHODS.md`](docs/METHODS.md); and
- task-paired inference, repository-cluster sensitivity, Django-exclusion
  results, denominators, and output definitions in the
  [statistics catalogue](result/Statistics%20results/README.md).

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
.
├── data/
│   ├── data/verified/             # Task list, submitted patches, and outcome labels
│   └── traj/                      # Complete trajectories, configurations, and messages
├── analyse/                       # Per-model task artifacts and benchmark test IDs
├── FINAL-CODEBOOK/                # Canonical taxonomy, labels, diagnoses, and case notes
├── docs/
│   ├── METHODS.md                 # Experimental, accounting, and statistical methods
│   └── taxonomy_methodology/      # Coding protocol and three-coder verification
├── V1V2_recheck/                  # Independent validation of the 40 V1/V2 cases
├── result/
│   ├── analyse.md                 # Human-readable failure-analysis catalogue
│   ├── summary.txt                # Three-trial outcome summary
│   └── Statistics results/        # Generated tables, reports, settings, and audits
├── scripts/                       # Analysis, validation, and inspection entry points
└── examples/                      # Selected task examples
```

The experiments used
[mini-SWE-agent](https://github.com/SWE-agent/mini-swe-agent) version 1.15.0
from its v1 codebase; see the official
[v1 documentation](https://mini-swe-agent.com/v1/). The archived settings and
their provenance are described in
[`settings.md`](result/Statistics%20results/settings/settings.md).

## Reproduce the analyses

Run the complete offline token-accounting, resource, outcome, taxonomy,
inferential, and sensitivity-analysis pipeline:

```bash
python3 scripts/run_analysis.py
```

This rebuilds the full 100-task cohort and the 50-task Django-excluded cohort,
including repository and difficulty strata, repository-cluster sensitivity,
audits, and validation. Generated artifacts are written under
`result/Statistics results/`.

Refresh the linked qualitative-review packet after changing the canonical
annotations, or check that the existing packet is current:

```bash
python3 scripts/build_taxonomy_review_packet.py
python3 scripts/build_taxonomy_review_packet.py --check
```

The four editable and reconciled failure-coding sources are collected in
[`FINAL-CODEBOOK/`](FINAL-CODEBOOK/README.md). Generated reports and tables
under `result/` should be rebuilt from those sources rather than edited
directly.

Each script begins with a description of its purpose, inputs, outputs, and
mutation scope where relevant. Consult that opening documentation for usage;
the root README intentionally lists only the main entry points.
