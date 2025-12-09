import argparse
import json
from pathlib import Path
from typing import Dict, Set

from datasets import load_dataset


def label_to_mark(label):
    """label True/False/None -> √ / × / ?"""
    if label is True:
        return "√"
    if label is False:
        return "×"
    return "?"


def load_swebench_difficulty():
    """Load difficulty from SWE-bench_Verified (test split)."""
    ds = load_dataset("princeton-nlp/SWE-bench_Verified", split="test")
    return {item["instance_id"]: item.get("difficulty", "") for item in ds}


def load_round_results(base_dir: Path, model: str, round_num: int) -> Dict[str, dict]:
    """Load result dict for a given model and round. If file missing, return {}."""
    result_path = (
        base_dir
        / "data"
        / "data"
        / "verified"
        / model.replace("/", "_")
        / f"round{round_num}.json"
    )
    if not result_path.exists():
        return {}
    with result_path.open("r", encoding="utf-8", errors="replace") as f:
        return json.load(f)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Summarize multi-model 3-round results into one table."
    )
    parser.add_argument(
        "--models",
        "-m",
        type=str,
        nargs="+",
        required=True,
        help=(
            "Model names, e.g.: "
            "-m claude-sonnet-4-5-20250929 "
            "gpt-5-2025-08-07-medium-reasoning "
        ),
    )
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parents[2]

    print("Loading SWE-bench-Verified difficulties...")
    difficulties = load_swebench_difficulty()

    # 预加载每个模型、每一轮的结果
    print("Loading model round results...")
    # results[model][round_num] -> {instance_id: obj}
    results: Dict[str, Dict[int, Dict[str, dict]]] = {}
    all_ids: Set[str] = set()

    for model in args.models:
        results[model] = {}
        for r in (1, 2, 3):
            round_data = load_round_results(base_dir, model, r)
            results[model][r] = round_data
            all_ids.update(round_data.keys())

    # 输出目录和文件
    out_root = base_dir / "analyse" / "result"
    out_root.mkdir(parents=True, exist_ok=True)
    out_path = out_root / "summary.txt"

    # 表头：id + 每个模型一列（三字符，如 ×××/√××）+ difficulty
    header_cols = ["id"]
    for model in args.models:
        safe_name = model.replace("/", "_")
        header_cols.append(safe_name)
    header_cols.append("difficulty")

    with out_path.open("w", encoding="utf-8") as f:
        f.write("  ".join(header_cols) + "\n")

        # 为了稳定输出，按 id 排序
        for instance_id in sorted(all_ids):
            row = [instance_id]

            # 每个模型一列，内容为三轮拼接的紧凑字符串，如 "×××"、"√××"
            for model in args.models:
                marks = []
                for r in (1, 2, 3):
                    obj = results[model][r].get(instance_id)
                    label = obj.get("label") if obj is not None else None
                    marks.append(label_to_mark(label))
                row.append("".join(marks))

            # difficulty
            diff = difficulties.get(instance_id, "")
            row.append(diff)

            f.write("  ".join(row) + "\n")

    print("Summary written to", out_path)


if __name__ == "__main__":
    main()