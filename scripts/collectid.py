"""Collect unique task IDs from the saved GPT round-1 verified results.

The script reads ``data/data/verified/.../round1.json`` and writes the compact
ID list to ``data/data/verified/instance_id_list.json``. It does not modify the
source result file.
"""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

def main():
    data_dir = ROOT / 'data' / 'data' / 'verified'
    round1_path = data_dir / 'gpt-5-2025-08-07-medium-reasoning' / 'round1.json'
    output_path = data_dir / 'instance_id_list.json'

    with round1_path.open('r', encoding='utf-8') as f:
        data = json.load(f)

    instance_ids = []
    for v in data.values():
        iid = v.get("instance_id")
        if iid and iid not in instance_ids:
            instance_ids.append(iid)

    with output_path.open('w', encoding='utf-8') as f:
        json.dump(instance_ids, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()
