"""Run the complete offline quantitative-analysis and validation pipeline.

The command reads archived data from the repository, writes canonical statistics
and publication tables to ``result/Statistics results``, and optionally records
portable evidence from a supplied mini-SWE-agent checkout. It does not modify
trajectories, verified labels, patches, or manuscript files.
"""

import argparse
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
DEFAULT_OUTPUT = ROOT / 'result' / 'Statistics results'


def run(script, *arguments):
    print(f'Running {script}', flush=True)
    subprocess.run([sys.executable, str(BASE/script), *map(str, arguments)], check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--agent-root', type=Path, help='Optional agent source checkout')
    parser.add_argument('--adapter-root', type=Path, help='Optional litellm package source')
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--bootstrap-repetitions', type=int, default=10000)
    parser.add_argument('--permutations', type=int, default=19999)
    args = parser.parse_args()
    if args.adapter_root and not args.agent_root:
        parser.error('--adapter-root requires --agent-root')
    if args.bootstrap_repetitions < 1 or args.permutations < 1:
        parser.error('Resampling counts must be positive')
    run('audit_token_methodology.py', '--data-root', args.data_root, '--output', args.output)
    if args.agent_root:
        extra = ['--adapter-root', args.adapter_root] if args.adapter_root else []
        run('inspect_runtime_source.py', '--agent-root', args.agent_root, '--output', args.output, *extra)
    run('inferential_analysis.py', '--self-check')
    run('inferential_analysis.py', '--input', args.output/'per_attempt.csv', '--output', args.output,
        '--seed', args.seed, '--bootstrap-repetitions', args.bootstrap_repetitions,
        '--permutations', args.permutations)
    run('build_analysis_report.py', '--output', args.output)
    run('validate_analysis_outputs.py', '--data-root', args.data_root, '--output', args.output)


if __name__ == '__main__':
    main()
