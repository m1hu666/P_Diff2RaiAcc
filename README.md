# P_Diff2RaiAcc

This repository is used to analyze and visualize different models' results and trajectories on SWE-bench Verified.

Below is a brief guide for two commonly used scripts: `data/scripts/inspector.py` and `data/scripts/datavis.py`.

## Environment Setup

It is recommended to use a virtual environment and install project dependencies:

```bash
cd P_Diff2RaiAcc
pip install -r requirements.txt
```

## 1. Terminal Trajectory Inspector: `inspector.py`

Script path: `data/scripts/inspector.py`

Purpose: browse a single `.traj.json` trajectory file step-by-step in the terminal, displaying one message at a time with simple color highlighting.

### Arguments

- `--m`: model name, corresponding to the directory name under `data/traj/{model}/...`.
- `--r`: round index, starting from 1, corresponding to `round{r}`.
- `--i`: instance ID / example name (file prefix), e.g. `astropy__astropy-7671`.
- positional `path` (optional): if `--m/--r/--i` are not used, you can pass a directory or a specific `.traj.json` file. The script will search for the first matching `.traj.json` in that directory.

When `--m/--r/--i` are provided, the script constructs the trajectory path as:

```text
data/traj/{m}/round{r}/{i}/{i}.traj.json
```

### Example: specify trajectory via model / round / instance ID

```bash
python data/scripts/inspector.py \
  --m gpt-5-2025-08-07-medium-reasoning \
  --r 1 \
  --i astropy__astropy-7671
```

### Interaction

After starting the script, the terminal shows the current step content and a command prompt at the bottom:

- `l` or Enter: next step
- `h`: previous step
- a number (e.g. `10`): jump to that step
- `q`: quit

Each message shows its `role` (system / user / assistant ¡ú mini-swe-agent) with different colors for quick visual distinction when reading trajectories.

## 2. Patch Export Tool: `datavis.py`

Script path: `data/scripts/datavis.py`

Purpose: batch-export gold patches, model-generated patches, and related metadata (test patch, problem statement, hints) for multiple instances and models, saving them under the `analyse/` directory for further offline analysis or visualization.

### Input File Layout

`datavis.py` reads result files from:

```text
data/data/verified/{model.replace('/', '_')}/round{r}.json
```

For example:

- model: `gpt-5-2025-08-07-medium-reasoning`
- round: `1`

The result file will be:

```text
data/data/verified/gpt-5-2025-08-07-medium-reasoning/round1.json
```

The JSON should use `instance_id` as keys, each storing the model's result for that instance.

### Instance ID Source

- The script reads instance IDs line by line from the repository root file:

  ```text
  id.txt
  ```

- Each non-empty line is treated as one `instance_id`, for example:

  ```text
  astropy__astropy-14182
  django__django-10554
  ...
  ```

### Fixed Model List

`datavis.py` currently processes three models:

- `claude-sonnet-4-5-20250929`
- `gemini-3-pro-preview`
- `gpt-5-2025-08-07-medium-reasoning`

For each model, it looks for `round1.json`, `round2.json`, and `round3.json` under the corresponding `data/data/verified/{model}/` directory.

### Data from SWE-bench Verified

For each `instance_id`, the script loads the entry from HuggingFace dataset `princeton-nlp/SWE-bench_Verified` (split `test`) and extracts:

- `patch` (gold patch)
- `test_patch`
- `problem_statement`
- `hints_text`

### Output Layout under `analyse/`

For each model and instance ID, the script creates a directory:

```text
analyse/{model}/{instance_id}/
```

and writes the following files:

- `{instance_id}_gold.patch` — gold patch (`patch` from SWE-bench Verified)
- `{round_num}{instance_id}_model.patch` — model-generated patch for each available round (1, 2, 3)
- `{instance_id}_test.patch` — `test_patch` from SWE-bench Verified
- `{instance_id}_problem_statement.txt` — `problem_statement` from SWE-bench Verified
- `{instance_id}_hints.txt` — `hints_text` from SWE-bench Verified

If some fields are missing in the dataset, the corresponding files are still created but may be empty.

### Usage

`datavis.py` no longer requires command-line arguments like `--m` or `--i`. It uses the fixed model list and the IDs from `id.txt`.

From the repository root:

```bash
python data/scripts/datavis.py
```

After running:

- The script loads the SWE-bench Verified `test` split from HuggingFace.
- For each model and instance ID, it reads local result JSONs, collects per-round `model_patch`, and fetches related fields from SWE-bench Verified.
- All patches and metadata are saved under the `analyse/` directory in a consistent file layout for downstream analysis.

---

If you run into issues with paths, dependencies, or encoding when using these scripts, first double-check:

- You are running commands from the repository root.
- The virtual environment is activated and `requirements.txt` dependencies are installed.
- The values of `--m/--r/--i` match the actual structure under the `data/` directory.

To further extend these scripts (e.g. add filters, batch browsing, etc.), you can add new utilities under `data/scripts/` or adapt the existing ones.