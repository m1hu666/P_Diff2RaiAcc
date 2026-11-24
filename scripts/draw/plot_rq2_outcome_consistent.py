#!/usr/bin/env python3
"""RQ2: Repository -> difficulty, separated into successful and failed attempts.

Input files (place both in --data-dir):
  per_attempt.csv: task, model, round, repository, difficulty, label,
                   steps, recorded_cost_usd
  task_metadata.csv: task, repository, difficulty (cross-check only)

Statistics:
  First average attempts WITH THE SAME OUTCOME within each task and model.
  Then give each qualifying task equal weight within repository x difficulty.
  The same task may contribute once to Success and once to Failure if the
  model's three trials had mixed outcomes. Missing combinations stay blank.
  Each model uses one fixed filled marker across both panels and both figures.

Outputs: two PDFs sized for one column, with panel captions and no point labels.
Defaults read result/Statistics results/data and write to full/figures.
Run from any directory:
  python /path/to/scripts/draw/plot_rq2_outcome_consistent.py
"""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, FormatStrFormatter, MultipleLocator

ROOT = Path(__file__).resolve().parents[2]
STATS_ROOT = ROOT / 'result' / 'Statistics results'

parser = argparse.ArgumentParser()
parser.add_argument('--data-dir', type=Path, default=STATS_ROOT / 'data')
parser.add_argument('--out-dir', type=Path, default=STATS_ROOT / 'full' / 'figures')
args = parser.parse_args()
args.out_dir.mkdir(parents=True, exist_ok=True)

MODELS = ['Claude', 'Gemini', 'GPT']
MODEL_MAP = {
    'claude-sonnet-4-5-20250929': 'Claude',
    'gemini-3-pro-preview': 'Gemini',
    'gpt-5-2025-08-07-medium-reasoning': 'GPT',
}
REPO_NAMES = {
    'django/django': 'Django',
    'sphinx-doc/sphinx': 'Sphinx',
    'matplotlib/matplotlib': 'Matplotlib',
    'sympy/sympy': 'SymPy',
    'scikit-learn/scikit-learn': 'scikit-learn',
    'astropy/astropy': 'Astropy',
    'pytest-dev/pytest': 'pytest',
    'pylint-dev/pylint': 'Pylint',
    'pydata/xarray': 'Xarray',
    'pallets/flask': 'Flask',
    'psf/requests': 'Requests',
}
DIFFICULTIES = [
    ('<15 min fix', '<15m'),
    ('15 min - 1 hour', '15–60m'),
    ('1-4 hours', '1–4h'),
]
STYLE = {
    'Claude': ('#0072B2', 'o', 22),
    'Gemini': ('#D55E00', 's', 21),
    'GPT': ('#171717', '^', 25),
}
OUTCOMES = ['Success', 'Failure']

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'Liberation Serif', 'Nimbus Roman', 'DejaVu Serif'],
    'font.size': 7.2,
    'axes.labelsize': 7.2,
    'xtick.labelsize': 7.0,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'axes.linewidth': 0.6,
})

# ------------ Read and verify the saved experiment records ------------
df = pd.read_csv(args.data_dir / 'per_attempt.csv')
meta = pd.read_csv(args.data_dir / 'task_metadata.csv')
df['model'] = df['model'].replace(MODEL_MAP)
required = ['task', 'model', 'round', 'repository', 'difficulty', 'label',
            'steps', 'recorded_cost_usd']
assert df[required].notna().all().all(), 'Missing required values'
assert len(df) == 900 and df.task.nunique() == 100
assert df.model.isin(MODELS).all()
assert df.groupby(['task', 'model']).size().eq(3).all()
assert set(df.label.unique()) == {True, False}
assert meta['task'].is_unique
check = df[['task', 'repository', 'difficulty']].drop_duplicates().merge(
    meta, on='task', validate='one_to_one', suffixes=('_record', '_meta'))
assert len(check) == 100
for field in ['repository', 'difficulty']:
    assert check[f'{field}_record'].eq(check[f'{field}_meta']).all()

df['outcome'] = np.where(df['label'], 'Success', 'Failure')

# ------------ Condition on outcome, THEN aggregate trials to tasks ------------
by_task = df.groupby(
    ['repository', 'difficulty', 'task', 'model', 'outcome'],
    as_index=False,
).agg(
    steps=('steps', 'mean'),
    cost=('recorded_cost_usd', 'mean'),
    qualifying_trials=('steps', 'size'),
)

# Equal weight per task that has this outcome for this model.
by_group = by_task.groupby(
    ['repository', 'difficulty', 'model', 'outcome'],
    as_index=False,
).agg(
    steps=('steps', 'mean'),
    cost=('cost', 'mean'),
    n_tasks=('task', 'nunique'),
    n_trials=('qualifying_trials', 'sum'),
)

lookup = by_group.set_index(['repository', 'difficulty', 'model', 'outcome'])

# Row totals describe the sampled tasks in each repo/difficulty group,
# NOT the number of tasks with a specific outcome/model.
task_info = df[['repository', 'difficulty', 'task']].drop_duplicates()
group_n = task_info.groupby(['repository', 'difficulty']).size()
repo_n = task_info.groupby('repository').size()
repos = sorted(repo_n.index, key=lambda r: (-int(repo_n[r]), r))
assert len(repos) == 11 and len(group_n) == 24

rows, repo_spans = [], []
y = 0.
for repo in repos:
    start = y
    for diff, display in DIFFICULTIES:
        if (repo, diff) not in group_n.index:
            continue
        rows.append((repo, diff, display, int(group_n.loc[(repo, diff)]), y))
        y += 1.
    repo_spans.append((repo, start, y - 1.))
    y += 0.32


def draw(metric, name, xlabel, suggested_max, ticks, minor_interval, panel_caption):
    # Render at publication width so embedding at column width preserves fonts.
    fig = plt.figure(figsize=(3.4, 5.3), facecolor='white')
    gs = fig.add_gridspec(
        1, 6,
        width_ratios=[1.8, 1.42, 0.35, 1.95, 0.70, 1.95],
        left=0.055, right=0.985, top=0.900,
        bottom=0.115, wspace=0.075,
    )

    ax_repo, ax_diff, ax_suc, ax_fail = [
        fig.add_subplot(gs[0, i]) for i in [0, 1, 3, 5]
    ]
    axs = [ax_repo, ax_diff, ax_suc, ax_fail]
    for ax in axs:
        ax.set_ylim(y - 0.55, -0.57)
        ax.set_yticks([])
    for ax in (ax_repo, ax_diff):
        ax.set_xlim(0, 1)
        ax.axis('off')

    for repo, first, last in repo_spans:
        ax_repo.text(0.98, (first + last) / 2,
                     REPO_NAMES.get(repo, repo),
                     ha='right', va='center', fontsize=6.8, fontweight='bold')
        if repo != repos[-1]:
            for ax in axs:
                ax.axhline(last + 0.65, color='#D9DEE2', lw=0.55, zorder=0)

    for repo, diff, display, total_tasks, yy in rows:
        ax_diff.text(0.02, yy, f'{display} ({total_tasks})',
                     ha='left', va='center', fontsize=6.8, color='#303030')
        for ax, outcome in ((ax_suc, 'Success'), (ax_fail, 'Failure')):
            for model in MODELS:
                key = (repo, diff, model, outcome)
                if key not in lookup.index:
                    continue  # no matching attempts; NEVER draw a fake zero
                record = lookup.loc[key]
                color, marker, size = STYLE[model]
                # One fixed visual encoding per model across ALL subgroups:
                # Claude: blue circle, Gemini: orange square, GPT: dark triangle.
                # All models share the exact horizontal center of each row.
                ax.scatter(
                    record[metric], yy,
                    s=size, marker=marker,
                    facecolors=color,
                    edgecolors='white',
                    linewidths=0.35,
                    zorder={'Claude': 4, 'Gemini': 5, 'GPT': 6}[model],
                )

    for ax, heading in ((ax_suc, 'Success'), (ax_fail, 'Failure')):
        ax.set_xlim(0, suggested_max)
        ax.xaxis.set_major_locator(FixedLocator(ticks))
        ax.xaxis.set_minor_locator(MultipleLocator(minor_interval))
        ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f' if metric == 'cost' else '%d'))
        ax.set_title(heading, fontsize=7.5, pad=5)
        ax.set_xlabel(xlabel, labelpad=4)
        ax.grid(axis='x', color='#EAEDF0', lw=0.55)
        ax.set_axisbelow(True)
        for spine in ['left', 'top', 'right']:
            ax.spines[spine].set_visible(False)
        ax.tick_params(axis='y', length=0)
        ax.tick_params(axis='x', length=2.5, pad=2)
        ax.tick_params(axis='x', which='minor', length=1.4, width=0.4)

    ax_repo.text(0.98, -1.02, 'Repository', ha='right',
                 va='center', fontweight='bold', fontsize=7.0)
    ax_diff.text(0.02, -1.02, 'Difficulty (N)', ha='left',
                 va='center', fontweight='bold', fontsize=7.0)

    model_handles = [Line2D([], [], color=STYLE[m][0], marker=STYLE[m][1],
                            linestyle='none', markersize=4.0, label=m)
                     for m in MODELS]
    fig.legend(handles=model_handles, loc='upper center',
               bbox_to_anchor=(0.5, 0.995), ncol=3, frameon=False,
               fontsize=7.2, columnspacing=1.2, handletextpad=0.3)

    fig.text(0.5, 0.015, panel_caption, ha='center', va='bottom', fontsize=7.5)

    fig.savefig(args.out_dir / f'{name}.pdf')
    plt.close(fig)


draw('steps', 'rq2_steps_success_failure_consistent',
     'Steps / attempt', 120, [0, 25, 50, 75, 100], 5,
     '(a) Interaction steps')
draw('cost', 'rq2_cost_success_failure_consistent',
     'Est. cost (USD)', 2.5, [0, 0.5, 1.0, 1.5, 2.0], 0.1,
     '(b) Estimated API costs')

print('Saved:', args.out_dir.resolve())
print('Outcome-specific group/model cells:', len(by_group), '/ 144')
print('Empty cells:', 144 - len(by_group))
print('Cells with 1-2 qualifying tasks:', (by_group.n_tasks < 3).sum())
print('Trial counts:', df.groupby(['model', 'outcome']).size().to_dict())
