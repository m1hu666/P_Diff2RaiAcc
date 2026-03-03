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

## 2. Patch Visualization Tool: `datavis.py`

Script path: `data/scripts/datavis.py`

Purpose: load the gold patch and model-generated patch for a given instance from the verified results JSON and open a desktop GUI window to compare them side by side, with copy/save support.

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

### Arguments

- `--m`: model name (must match the directory name of the result file).
- `--r`: round index.
- `--i`: instance ID (same as `instance_id` in SWE-bench Verified).
- `--key`: optional, multi-value argument. Print selected fields from both the result JSON and SWE-bench Verified for comparison.
- `--v`: if set, open a GUI window to visualize gold patch vs model patch, with copy/save support.

### Example: only print selected fields

```bash
python data/scripts/datavis.py \
  --m gpt-5-2025-08-07-medium-reasoning \
  --r 1 \
  --i astropy__astropy-7671 \
  --key model_patch patch
```

### Example: open GUI to compare patches

```bash
python data/scripts/datavis.py \
  --m "gpt-5-2025-08-07-medium-reasoning" \
  --r 1 \
  --i "astropy__astropy-7671" \
  --v
```

After running:

- The script loads the corresponding instance from HuggingFace dataset `princeton-nlp/SWE-bench_Verified`.
- Loads `model_patch` for that instance from the local result JSON.
- Opens a modern-styled Tk window showing Gold Patch and Model Patch side by side, and indicates whether they exactly match.
- Allows copying and saving both patches to local files.

---

If you run into issues with paths, dependencies, or encoding when using these scripts, first double-check:

- You are running commands from the repository root.
- The virtual environment is activated and `requirements.txt` dependencies are installed.
- The values of `--m/--r/--i` match the actual structure under the `data/` directory.

To further extend these scripts (e.g. add filters, batch browsing, etc.), you can add new utilities under `data/scripts/` or adapt the existing ones.