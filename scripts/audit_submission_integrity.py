"""Compare archived trajectories, final patches, and evaluation reports offline.

The script reads all 900 saved attempts and writes metadata-only integrity tables
under ``result/Statistics results/submission_integrity``. It never changes source
data, trajectories, patches, evaluation reports, or labels.
"""

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "result" / "Statistics results" / "submission_integrity"


def normalized(text):
    return (text or "").replace("\r\n", "\n").replace("\r", "\n").strip()


def sha256(text):
    return hashlib.sha256((text or "").encode()).hexdigest()


def write_csv(name, rows):
    if not rows:
        return
    with (OUT / name).open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    inventory = []
    report_conflicts = []
    for model_dir in sorted((ROOT / "data/data/verified").iterdir()):
        if not model_dir.is_dir():
            continue
        model = model_dir.name
        for trial in (1, 2, 3):
            round_name = f"round{trial}"
            predictions = json.loads((model_dir / f"{round_name}.json").read_text())
            report_dir = ROOT / "data/traj" / model / "sb-cli-reports"
            suffix = (f"gemini{trial}.json" if model.startswith("gemini") else
                      f"round{trial}_run.json" if model.startswith("gpt") else
                      f"round{trial}.json")
            report_path = report_dir / f"swe-bench_verified__test__{suffix}"
            evaluation = json.loads(report_path.read_text())
            for task, prediction in sorted(predictions.items()):
                patch = prediction.get("model_patch") or ""
                path = ROOT / "data/traj" / model / round_name / task / f"{task}.traj.json"
                label = prediction.get("label")
                eval_label = (True if task in evaluation.get("resolved_ids", []) else
                              False if task in evaluation.get("unresolved_ids", []) else None)
                row = {"model": model, "round": round_name, "task": task,
                       "label": label, "evaluation_label": eval_label,
                       "trajectory_path": str(path.relative_to(ROOT)),
                       "exit_status": None, "submission_chars": None,
                       "verified_patch_chars": len(patch), "steps": None,
                       "recorded_cost": None, "cost_limit": None,
                       "timeout": None, "priority_issue": "",
                       "patch_comparison": None, "trajectory_submission_sha256": None,
                       "verified_patch_sha256": sha256(patch)}
                if label is not eval_label:
                    report_conflicts.append({"model": model, "round": round_name,
                                             "task": task, "label": label,
                                             "evaluation_label": eval_label})
                if not path.exists():
                    row["priority_issue"] = "missing_trajectory"
                    row["patch_comparison"] = "missing_trajectory"
                else:
                    data = json.loads(path.read_text())
                    info = data.get("info", {})
                    submission = info.get("submission") or ""
                    config = info.get("config", {})
                    row.update({"exit_status": info.get("exit_status"),
                                "submission_chars": len(submission),
                                "steps": sum(m.get("role") == "assistant" for m in data.get("messages", [])),
                                "recorded_cost": info.get("model_stats", {}).get("instance_cost"),
                                "cost_limit": config.get("agent", {}).get("cost_limit"),
                                "timeout": config.get("environment", {}).get("timeout"),
                                "trajectory_submission_sha256": sha256(submission)})
                    if info.get("exit_status") != "Submitted":
                        row["priority_issue"] = "not_submitted"
                    elif not submission.strip():
                        row["priority_issue"] = "submitted_with_empty_content"
                    if normalized(submission) == normalized(patch):
                        row["patch_comparison"] = "identical_after_outer_whitespace_and_newlines"
                    elif not submission.strip():
                        row["patch_comparison"] = "empty_submission_vs_nonempty_verified_patch"
                    else:
                        row["patch_comparison"] = "nonempty_patch_text_difference"
                inventory.append(row)
    priority = [r for r in inventory if r["priority_issue"]]
    differences = [r for r in inventory if r["patch_comparison"] == "nonempty_patch_text_difference"]
    by_model = {}
    for model in sorted({r["model"] for r in inventory}):
        group = [r for r in inventory if r["model"] == model]
        by_model[model] = {"expected": len(group),
                           "exit_status": dict(Counter(str(r["exit_status"]) for r in group)),
                           "priority_issues": dict(Counter(r["priority_issue"] or "none" for r in group)),
                           "patch_comparison": dict(Counter(r["patch_comparison"] for r in group))}
    summary = {"expected": len(inventory), "by_model": by_model,
               "priority_records": priority, "nonempty_patch_text_difference_count": len(differences),
               "evaluation_label_conflicts": report_conflicts,
               "interpretation": "Submitted denotes the agent termination marker, not a nonempty patch or a passing evaluation. A nonempty final patch alongside an empty archived submission requires provenance reconciliation; its cause cannot be established from this comparison."}
    (OUT / "submission_audit.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    write_csv("submission_inventory.csv", inventory)
    write_csv("priority_rerun_candidates.csv", priority)
    write_csv("nonempty_patch_text_differences.csv", differences)
    print(json.dumps({"expected": len(inventory), "priority_records": priority,
                      "nonempty_patch_text_difference_count": len(differences),
                      "evaluation_label_conflict_count": len(report_conflicts)}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
