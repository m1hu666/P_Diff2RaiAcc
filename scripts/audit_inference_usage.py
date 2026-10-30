"""Audit saved experimental settings and usage without querying a model API.

The script reads archived trajectories and verified labels, then writes an
independent trajectory-level cross-check under
``result/Statistics results/trajectory_audit``. Outputs contain metadata,
hashes, and aggregate counts, never prompt contents. Missing usage fields remain
missing rather than being interpreted as zero.
"""

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "result" / "Statistics results" / "trajectory_audit"


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def leaves(value, prefix=""):
    for key, item in value.items():
        name = f"{prefix}.{key}" if prefix else key
        if isinstance(item, dict):
            yield from leaves(item, name)
        else:
            yield name, item


def summarize(rows):
    result = {"n": len(rows)}
    metrics = ["steps", "prompt", "completion", "total", "reasoning", "cached",
               "cache_creation", "cache_read", "instance_cost", "format_errors", "timeouts"]
    for key in metrics:
        values = [r[key] for r in rows if r.get(key) is not None]
        result[key] = ({"n_observed": len(values), "sum": sum(values),
                        "mean": mean(values), "median": median(values),
                        "min": min(values), "max": max(values)} if values else None)
    return result


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    model_audit = {}
    missing_trajectories = []
    initials = defaultdict(dict)
    initial_texts = defaultdict(list)
    template_groups = defaultdict(list)
    normalized_env_groups = defaultdict(list)
    issues = []
    for model_dir in sorted((ROOT / "data/traj").iterdir()):
        if not model_dir.is_dir():
            continue
        model = model_dir.name
        counters = defaultdict(Counter)
        usage_fields = defaultdict(lambda: {"numeric_count": 0, "null_count": 0,
                                            "nonzero_count": 0, "sum": 0})
        variants = defaultdict(list)
        for round_n in (1, 2, 3):
            round_name = f"round{round_n}"
            labels_path = ROOT / "data/data/verified" / model / f"{round_name}.json"
            labels = json.loads(labels_path.read_text())
            for task, label in sorted(labels.items()):
                path = model_dir / round_name / task / f"{task}.traj.json"
                if not path.exists():
                    missing_trajectories.append({"model": model, "round": round_name,
                                                 "task": task, "label": label.get("label")})
                    continue
                data = json.loads(path.read_text())
                info = data["info"]
                cfg = info["config"]
                agent_cfg = cfg["agent"]
                env_cfg = cfg["environment"]
                templates = {k: v for k, v in agent_cfg.items() if k.endswith("template")}
                ref = f"{model}/{round_name}/{task}"
                template_groups[digest(templates)].append(ref)
                normalized_env_groups[digest({k: v for k, v in env_cfg.items() if k != "image"})].append(ref)
                initial = [{"role": m["role"], "content": m["content"]}
                           for m in data["messages"][:2]]
                initials[task][f"{model}/{round_name}"] = digest(initial)
                initial_texts[task].append((ref, initial))
                compact_cfg = {"model": cfg["model"],
                               "step_limit": agent_cfg.get("step_limit"),
                               "cost_limit": agent_cfg.get("cost_limit"),
                               "templates_sha256": digest(templates),
                               "environment": {k: v for k, v in env_cfg.items() if k != "image"},
                               "agent_type": cfg.get("agent_type"),
                               "model_type": cfg.get("model_type"),
                               "environment_type": cfg.get("environment_type"),
                               "mini_version": info.get("mini_version")}
                variants[canonical(compact_cfg)].append(f"{round_name}/{task}")
                counters["exit_status"][str(info.get("exit_status"))] += 1
                counters["mini_version"][str(info.get("mini_version"))] += 1
                messages = data["messages"]
                assistants = [m for m in messages if m["role"] == "assistant"]
                stats = info.get("model_stats", {})
                row = {"model": model, "round": round_name, "task": task,
                       "label": label.get("label"), "exit_status": info.get("exit_status"),
                       "steps": len(assistants), "length_responses": 0,
                       "multiple_choice_responses": 0,
                       "api_calls": stats.get("api_calls"),
                       "instance_cost": stats.get("instance_cost"),
                       "step_limit": agent_cfg.get("step_limit"),
                       "cost_limit": agent_cfg.get("cost_limit"),
                       "timeout": env_cfg.get("timeout"),
                       "config_sha256": digest(compact_cfg),
                       "initial_sha256": digest(initial),
                       "format_errors": sum(m["role"] == "user" and m["content"].startswith("Please always provide EXACTLY ONE action") for m in messages[2:]),
                       "timeouts": sum(m["role"] == "user" and "timed out and has been killed" in m["content"] for m in messages[2:]),
                       "usage_calls": 0}
                sums = Counter()
                observed = Counter()
                created = []
                for msg in assistants:
                    response = msg.get("extra", {}).get("response", {})
                    counters["response_model"][str(response.get("model"))] += 1
                    if isinstance(response.get("created"), (int, float)):
                        created.append(response["created"])
                    usage = response.get("usage")
                    if not isinstance(usage, dict):
                        issues.append({"path": ref, "issue": "assistant_without_usage"})
                        continue
                    row["usage_calls"] += 1
                    choices = response.get("choices", [])
                    row["length_responses"] += any(c.get("finish_reason") == "length" for c in choices)
                    row["multiple_choice_responses"] += len(choices) > 1
                    counters["completion_tokens_per_response"][str(usage.get("completion_tokens"))] += 1
                    for key, value in leaves(usage):
                        f = usage_fields[key]
                        if isinstance(value, (int, float)):
                            f["numeric_count"] += 1
                            f["sum"] += value
                            f["nonzero_count"] += value != 0
                        elif value is None:
                            f["null_count"] += 1
                    fields = {"prompt": usage.get("prompt_tokens"),
                              "completion": usage.get("completion_tokens"),
                              "total": usage.get("total_tokens"),
                              "reasoning": (usage.get("completion_tokens_details") or {}).get("reasoning_tokens"),
                              "cached": (usage.get("prompt_tokens_details") or {}).get("cached_tokens"),
                              "cache_creation": usage.get("cache_creation_input_tokens"),
                              "cache_read": usage.get("cache_read_input_tokens")}
                    for key, value in fields.items():
                        if isinstance(value, (int, float)):
                            sums[key] += value
                            observed[key] += 1
                    if all(isinstance(fields[k], (int, float)) for k in ("prompt", "completion", "total")):
                        counters["usage_checks"]["total_equals_prompt_plus_completion" if fields["total"] == fields["prompt"] + fields["completion"] else "total_mismatch"] += 1
                    if fields["reasoning"] is not None:
                        counters["usage_checks"]["reasoning_le_completion" if fields["reasoning"] <= fields["completion"] else "reasoning_gt_completion"] += 1
                    for choice in choices:
                        counters["finish_reason"][str(choice.get("finish_reason"))] += 1
                        message = choice.get("message", {})
                        for key in ("tool_calls", "function_call", "thinking_blocks", "reasoning_content"):
                            counters["message_fields"][f"{key}:nonempty" if message.get(key) else f"{key}:empty_or_absent"] += 1
                for key in ("prompt", "completion", "total", "reasoning", "cached", "cache_creation", "cache_read"):
                    row[key] = sums[key] if observed[key] == len(assistants) and assistants else None
                    row[f"reported_{key}_sum"] = sums[key] if observed[key] else None
                    row[f"{key}_observed_calls"] = observed[key]
                row["first_created"] = min(created) if created else None
                row["last_created"] = max(created) if created else None
                if row["steps"] != row["api_calls"]:
                    issues.append({"path": ref, "issue": "api_calls_differ_from_assistants",
                                   "steps": row["steps"], "api_calls": row["api_calls"]})
                if row["usage_calls"] != row["steps"]:
                    issues.append({"path": ref, "issue": "usage_calls_differ_from_assistants"})
                rows.append(row)
        model_rows = [r for r in rows if r["model"] == model]
        model_audit[model] = {
            "counters": {k: dict(v) for k, v in counters.items()},
            "usage_fields": dict(usage_fields),
            "config_variants": [{"configuration": json.loads(k), "count": len(v),
                                 "by_round": dict(Counter(x.split('/')[0] for x in v)),
                                 "examples": v[:3]} for k, v in variants.items()],
            "aggregates": {group: summarize([r for r in model_rows if group == "all" or r["label"] is (group == "success")])
                           for group in ("all", "success", "failure")},
            "rounds": {rnd: summarize([r for r in model_rows if r["round"] == rnd])
                       for rnd in ("round1", "round2", "round3")}}
    initial_mismatches = {task: entries for task, entries in initials.items() if len(set(entries.values())) > 1}
    mismatch_details = {}
    for task in initial_mismatches:
        refs_and_prompts = initial_texts[task]
        # Keep only first-difference metadata, not task text.
        base_ref, base = refs_and_prompts[0]
        differences = []
        for ref, candidate in refs_and_prompts[1:]:
            if candidate == base:
                continue
            for index, (b, c) in enumerate(zip(base, candidate)):
                if b != c:
                    btext, ctext = b["content"], c["content"]
                    first = next((i for i, (x, y) in enumerate(zip(btext, ctext)) if x != y), min(len(btext), len(ctext)))
                    differences.append({"reference": base_ref, "candidate": ref, "message_index": index,
                                        "reference_length": len(btext), "candidate_length": len(ctext),
                                        "first_different_character": first})
        mismatch_details[task] = differences
    all_task_models = defaultdict(dict)
    for row in rows:
        all_task_models[row["task"]].setdefault(row["model"], []).append(row)
    model_names = sorted(model_audit)
    common_success_tasks = [task for task, groups in all_task_models.items()
                            if set(groups) == set(model_names)
                            and all(len(v) == 3 and all(r["label"] is True for r in v) for v in groups.values())]
    all_complete_tasks = [task for task, groups in all_task_models.items()
                          if set(groups) == set(model_names) and all(len(v) == 3 for v in groups.values())]
    comparisons = {}
    for name, tasks in (("all_complete_tasks", all_complete_tasks), ("all_models_success_in_all_three_trials", common_success_tasks)):
        comparisons[name] = {"n_tasks": len(tasks), "by_model": {m: summarize([r for r in rows if r["model"] == m and r["task"] in tasks]) for m in model_names}}
    aligned_limits = defaultdict(list)
    for row in rows:
        if row["cost_limit"] == 3.0 and row["timeout"] == 60:
            aligned_limits[(row["task"], row["round"])].append(row)
    aligned_rows = [r for group in aligned_limits.values()
                    if {r["model"] for r in group} == set(model_names) for r in group]
    comparisons["matched_task_rounds_with_cost_limit_3_and_timeout_60"] = {
        "n_tasks": len({r["task"] for r in aligned_rows}), "n_task_rounds": len(aligned_rows) // len(model_names),
        "by_model": {m: summarize([r for r in aligned_rows if r["model"] == m]) for m in model_names}}
    comparisons["submitted_only"] = {
        "n_tasks": len({r["task"] for r in rows if r["exit_status"] == "Submitted"}),
        "by_model": {m: summarize([r for r in rows if r["model"] == m and r["exit_status"] == "Submitted"]) for m in model_names}}
    report = {"scope": "Saved trajectories only; successful logged API responses, not unlogged retries or invoices.",
              "trajectory_count": len(rows), "missing_trajectories": missing_trajectories,
              "issues": issues, "model_audit": model_audit,
              "initial_prompt_audit": {"n_tasks": len(initials), "mismatched_tasks": initial_mismatches,
                                       "difference_metadata": mismatch_details},
              "template_variants": [{"sha256": k, "count": len(v), "example": v[0]} for k, v in template_groups.items()],
              "environment_variants_excluding_image": [{"sha256": k, "count": len(v), "example": v[0]} for k, v in normalized_env_groups.items()],
              "matched_comparisons": comparisons}
    (OUT / "audit.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    with (OUT / "per_trajectory.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print("Saved", OUT.relative_to(ROOT))
    print("Trajectories:", len(rows), "missing:", missing_trajectories)
    print("Prompt mismatch tasks:", len(initial_mismatches), "template variants:", len(template_groups))
    print("Issues:", len(issues))
    for model, audit in model_audit.items():
        print("\nMODEL", model)
        for variant in audit["config_variants"]:
            cfg = variant["configuration"]
            print("CONFIG", variant["count"], variant["by_round"], cfg["model"],
                  "cost_limit", cfg["cost_limit"], "timeout", cfg["environment"].get("timeout"))
        for group, agg in audit["aggregates"].items():
            print(group, "n", agg["n"], {k: (round(agg[k]["mean"], 4) if agg[k] else None) for k in ("steps", "prompt", "completion", "reasoning", "cached", "instance_cost")})
        print("COUNTERS", audit["counters"])
    print("Matched cohorts", {k: v["n_tasks"] for k, v in comparisons.items()})


if __name__ == "__main__":
    main()
