# -*- coding: gbk -*-
import argparse
import json
import os
from datasets import load_dataset


def get_result_path(model: str, round_num: int) -> str:
    return os.path.join('data', 'data', 'verified', model.replace('/', '_'), f'round{round_num}.json')


def get_swebench_data():
    ds = load_dataset("princeton-nlp/SWE-bench_Verified", split="test")
    return {item['instance_id']: item for item in ds}


def save_patches(base_dir: str, model: str, instance_id: str, gold_patch: str, round_model_patches: dict) -> None:
    """Save gold patch and per-round model patches under analyse/ directory.

    Directory: analyse/{model}/{instance_id}/
        - {instance_id}_gold.patch
        - {round_num}{instance_id}_model.patch
    """
    analyse_root = os.path.join(base_dir, 'analyse', model)
    instance_dir = os.path.join(analyse_root, instance_id)
    os.makedirs(instance_dir, exist_ok=True)

    gold_path = os.path.join(instance_dir, f"{instance_id}_gold.patch")
    with open(gold_path, 'w', encoding='utf-8') as f:
        f.write(gold_patch or "")

    for round_num, model_patch in round_model_patches.items():
        file_path = os.path.join(instance_dir, f"{round_num}{instance_id}_model.patch")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(model_patch or "")

def main():
    parser = argparse.ArgumentParser(description='Visualize patch results and compare with gold standard')
    parser.add_argument('--m', type=str, required=True, help='Model name')
    parser.add_argument('--i', type=str, required=True, help='Instance ID')
    parser.add_argument('--key', type=str, nargs='*', help='Attributes to output')
    args = parser.parse_args()
    
    # Load all rounds (1..3) for this model & instance
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    round_model_patches = {}
    for round_num in (1, 2, 3):
        result_path = get_result_path(args.m, round_num)
        if not os.path.exists(result_path):
            continue
        with open(result_path, 'r', encoding='utf-8', errors='replace') as f:
            result_data = json.load(f)
        instance_obj = result_data.get(args.i)
        if not instance_obj:
            continue
        model_patch = instance_obj.get('model_patch', '')
        round_model_patches[round_num] = model_patch

    if not round_model_patches:
        print(f"Instance '{args.i}' not found in any round results.")
        return

    print("Loading SWE-bench-verified from HuggingFace...")
    sb_data = get_swebench_data()
    sb_obj = sb_data.get(args.i)
    if not sb_obj:
        print(f"Instance '{args.i}' not found in swe-bench-verified dataset.")
        gold_patch = ''
    else:
        gold_patch = sb_obj.get('patch', '')

    # Optional attribute printing (using last found instance_obj)
    if args.key:
        print("== From results (last round that contains instance) ==")
        for k in args.key:
            value = instance_obj.get(k, '<No such data>') if 'instance_obj' in locals() else '<No such data>'
            print(f"{k}: {value}")
        if sb_obj:
            print("== From swe-bench-verified ==")
            for k in args.key:
                print(f"{k}: {sb_obj.get(k, '<No such data>')}")

    # Save patches to analyse directory
    save_patches(base_dir, args.m, args.i, gold_patch, round_model_patches)
    print("Saved patches for instance:", args.i)

if __name__ == '__main__':
    main()