"""Synchronize one verified-result label file with its evaluation report.

This maintenance utility reads the configured SWE-bench report and **modifies**
the corresponding verified JSON by setting boolean ``label`` values. The current
configuration targets GPT round 2; review both paths before running it.
"""

import json
from pathlib import Path
import chardet

def main() -> None:
    root = Path(__file__).resolve().parent.parent
    report_path = root / "data" / "traj" / "gpt-5-2025-08-07-medium-reasoning" / "sb-cli-reports" / "swe-bench_verified__test__round2_run.json"
    data_path = root / "data" / "data" / "verified" / "gpt-5-2025-08-07-medium-reasoning" / "round2.json"

    with report_path.open("r", encoding="utf-8") as f:
        report = json.load(f)

    resolved_ids = set(report.get("resolved_ids", []))
    unresolved_ids = set(report.get("unresolved_ids", []))

    # Detect the source encoding before reading the archived file.
    with data_path.open("rb") as f:
        raw_data = f.read()
        encoding_result = chardet.detect(raw_data)
        actual_encoding = encoding_result['encoding']
        print(f"Detected file encoding: {actual_encoding}")

    # Read with the detected encoding and write normalized UTF-8 JSON.
    with data_path.open("r", encoding=actual_encoding) as f:
        data = json.load(f)

    for iid, obj in data.items():
        if iid in resolved_ids:
            obj["label"] = True
        elif iid in unresolved_ids:
            obj["label"] = False

    with data_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)

if __name__ == "__main__":
    main()
