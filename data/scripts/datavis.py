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


def save_patches(base_dir: str, model: str, instance_id: str, gold_patch: str, round_model_patches: dict,
                 test_patch: str = '', problem_statement: str = '', hints_text: str = '') -> None:
    """Save gold patch, per-round model patches and extra info under analyse/ directory.

    Directory: analyse/{model}/{instance_id}/
        - {instance_id}_gold.patch
        - {round_num}{instance_id}_model.patch
        - {instance_id}_test.patch
        - {instance_id}_problem_statement.txt
        - {instance_id}_hints.txt
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

    # Extra information from SWE-bench-verified
    if test_patch is not None:
        test_path = os.path.join(instance_dir, f"{instance_id}_test.patch")
        with open(test_path, 'w', encoding='utf-8') as f:
            f.write(test_patch or "")
    if problem_statement is not None:
        problem_path = os.path.join(instance_dir, f"{instance_id}_problem_statement.txt")
        with open(problem_path, 'w', encoding='utf-8') as f:
            f.write(problem_statement or "")
    if hints_text is not None:
        hints_path = os.path.join(instance_dir, f"{instance_id}_hints.txt")
        with open(hints_path, 'w', encoding='utf-8') as f:
            f.write(hints_text or "")


def main():
    """Batch export patches and metadata for fixed models and ids from id.txt."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Fixed model list
    models = [
        'claude-sonnet-4-5-20250929',
        'gemini-3-pro-preview',
        'gpt-5-2025-08-07-medium-reasoning',
    ]

    # Load instance ids from given file
    id_file = '/home/m1hu/P_Diff2RaiAcc/id.txt'
    if not os.path.exists(id_file):
        print(f"ID file not found: {id_file}")
        return

    with open(id_file, 'r', encoding='utf-8') as f:
        instance_ids = [line.strip() for line in f if line.strip()]

    if not instance_ids:
        print("No instance ids found in id.txt")
        return

    print("Loading SWE-bench-verified from HuggingFace...")
    sb_data = get_swebench_data()

    # Iterate over models and instances
    for model in models:
        print(f"Processing model: {model}")

        # Load all rounds (1..3) once per model
        results_by_round = {}
        for round_num in (1, 2, 3):
            result_path = get_result_path(model, round_num)
            if not os.path.exists(result_path):
                continue
            with open(result_path, 'r', encoding='utf-8', errors='replace') as f:
                results_by_round[round_num] = json.load(f)

        if not results_by_round:
            print(f"  No result files found for model {model}.")
            continue

        for instance_id in instance_ids:
            round_model_patches = {}

            # Collect patches from each round for this instance
            for round_num, result_data in results_by_round.items():
                instance_obj = result_data.get(instance_id)
                if not instance_obj:
                    continue
                model_patch = instance_obj.get('model_patch', '')
                round_model_patches[round_num] = model_patch

            if not round_model_patches:
                print(f"  Instance '{instance_id}' not found in any round results for model '{model}'.")
                continue

            sb_obj = sb_data.get(instance_id)
            if not sb_obj:
                print(f"  Instance '{instance_id}' not found in swe-bench-verified dataset.")
                gold_patch = ''
                test_patch = ''
                problem_statement = ''
                hints_text = ''
            else:
                gold_patch = sb_obj.get('patch', '')
                test_patch = sb_obj.get('test_patch', '')
                problem_statement = sb_obj.get('problem_statement', '')
                hints_text = sb_obj.get('hints_text', '')

            # Save patches and extra information to analyse directory
            save_patches(
                base_dir,
                model,
                instance_id,
                gold_patch,
                round_model_patches,
                test_patch=test_patch,
                problem_statement=problem_statement,
                hints_text=hints_text,
            )
            print(f"  Saved patches and metadata for model '{model}', instance '{instance_id}'.")

if __name__ == '__main__':
    main()