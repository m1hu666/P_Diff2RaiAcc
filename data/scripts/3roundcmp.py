#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
from pathlib import Path


MODEL_DIR = "gpt-5-2025-08-07-medium-reasoning"


def load_round(round_num: int, base_dir: Path):
    path = base_dir / "data" / "data" / "verified" / MODEL_DIR / f"round{round_num}.json"
    with path.open("rb") as f:
        raw = f.read()
    text = raw.decode("utf-8", errors="ignore")
    return json.loads(text)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print patches of 3 rounds for one instance id (terminal view)"
    )
    parser.add_argument(
        "--i", required=True, help="instance id, e.g. django__django-7530"
    )
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parents[2]
    r1 = load_round(1, base_dir)
    r2 = load_round(2, base_dir)
    r3 = load_round(3, base_dir)

    iid = args.i
    obj1 = r1.get(iid)
    obj2 = r2.get(iid)
    obj3 = r3.get(iid)
    if not any([obj1, obj2, obj3]):
        print(f"Instance {iid} not found in any round.")
        return

    def patch(obj):
        return (obj or {}).get("model_patch", "").rstrip() or "<No patch>"

    print("=" * 80)
    print(f"Instance: {iid}")
    print("=" * 80)

    print("\n########## ROUND 1 ##########\n")
    print(patch(obj1))

    print("\n########## ROUND 2 ##########\n")
    print(patch(obj2))

    print("\n########## ROUND 3 ##########\n")
    print(patch(obj3))

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()