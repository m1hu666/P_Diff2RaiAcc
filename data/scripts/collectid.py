import json
import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data', 'verified')
    round1_path = os.path.join(data_dir, 'gpt-5-2025-08-07-medium-reasoning', 'round1.json')
    output_path = os.path.join(data_dir, 'instance_id_list.json')

    with open(round1_path, 'r', encoding='gbk') as f:
        data = json.load(f)

    instance_ids = []
    for v in data.values():
        iid = v.get("instance_id")
        if iid and iid not in instance_ids:
            instance_ids.append(iid)

    with open(output_path, 'w', encoding='gbk') as f:
        json.dump(instance_ids, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()