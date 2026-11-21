"""Shared paths, CSV loading, and typography for the offline plotting scripts."""

import argparse
import csv
from pathlib import Path

import matplotlib as mpl
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STATS_ROOT = ROOT / "result" / "Statistics results"
COHORTS = ("full", "without_django")
MODELS = {
    "Claude": "claude-sonnet-4-5-20250929",
    "Gemini": "gemini-3-pro-preview",
    "GPT": "gpt-5-2025-08-07-medium-reasoning",
}


def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError(f"No plotting data in {path}")
    return rows


def configure_style():
    # Prefer the original typeface, with a portable serif fallback.
    available = {font.name for font in font_manager.fontManager.ttflist}
    font = "Times New Roman" if "Times New Roman" in available else "DejaVu Serif"
    mpl.rcParams.update({
        "font.family": "serif",
        "font.serif": [font],
        "axes.unicode_minus": False,
        "mathtext.fontset": "stix",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })


def output_path(stats_root, cohort, filename, output=None):
    path = Path(output) if output is not None else Path(stats_root) / cohort / "figures" / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def parse_args(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--stats-root", type=Path, default=DEFAULT_STATS_ROOT,
                        help="Statistics directory (default: repository result/Statistics results)")
    parser.add_argument("--cohort", choices=COHORTS, default="full")
    parser.add_argument("--output", type=Path,
                        help="Output file; its extension selects PDF, PNG, or SVG format")
    return parser.parse_args()
