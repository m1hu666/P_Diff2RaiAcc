"""Extract token, interaction, cost, prompt, and saved-setting audit data.

Inputs are the archived trajectories and verified labels under ``data/``.
Outputs are reproducible CSV/JSON files under ``result/Statistics results`` by
default. The script is offline, reads archived experiment data without changing
it, and uses no model or provider APIs.
"""

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
DEFAULT_OUTPUT = ROOT / "result" / "Statistics results"
MODELS = ["claude-sonnet-4-5-20250929", "gemini-3-pro-preview",
          "gpt-5-2025-08-07-medium-reasoning"]
SHORT = dict(zip(MODELS, ["Claude", "Gemini", "GPT"]))
FIELDS = ["prompt_tokens", "completion_tokens", "total_tokens",
          "prompt_tokens_details.cached_tokens", "cache_read_input_tokens",
          "cache_creation_input_tokens", "prompt_tokens_details.cache_creation_tokens",
          "prompt_tokens_details.text_tokens", "completion_tokens_details.reasoning_tokens",
          "completion_tokens_details.text_tokens"]
PARAMETERS = ["temperature", "top_p", "top_k", "max_tokens", "max_completion_tokens",
              "max_output_tokens", "reasoning", "reasoning_effort", "thinking",
              "thinking_config", "seed", "stop", "frequency_penalty", "presence_penalty",
              "n", "stream", "tools", "tool_choice", "parallel_tool_calls",
              "response_format", "verbosity", "drop_params"]
METRICS = ["steps", "prompt_tokens", "completion_tokens", "recorded_cost_usd"]
ABSENT = object()


def encoded(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(encoded(value).encode()).hexdigest()


def numeric(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def nested(value, name):
    for key in name.split("."):
        if not isinstance(value, dict):
            return ABSENT
        value = value.get(key, ABSENT)
    return value


def normalized_patch(value):
    return (value or "").replace("\r\n", "\n").replace("\r", "\n").strip()


def utc(value):
    return datetime.fromtimestamp(value, timezone.utc).isoformat() if numeric(value) else None


def dump_json(out, name, value):
    (out / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def dump_csv(out, name, rows, fieldnames=None):
    if fieldnames is None:
        fieldnames = list(dict.fromkeys(k for row in rows for k in row))
    with (out / name).open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: encoded(v) if isinstance(v, (dict, list)) else v for k, v in row.items()})


def percentile(values, p):
    ordered = sorted(values)
    offset = (len(ordered) - 1) * p
    lower = int(offset)
    upper = min(lower + 1, len(ordered) - 1)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (offset - lower)


def summarize(rows, cohort, group):
    result = []
    for model in MODELS:
        selected = [r for r in rows if r["model"] == model]
        for metric in METRICS:
            values = [r[metric] for r in selected if numeric(r.get(metric))]
            result.append({"cohort": cohort, "group": group, "model": model,
                           "metric": metric, "attempts": len(selected), "observed": len(values),
                           "mean": mean(values) if values else None,
                           "median": median(values) if values else None,
                           "q25": percentile(values, .25) if values else None,
                           "q75": percentile(values, .75) if values else None,
                           "min": min(values) if values else None,
                           "max": max(values) if values else None,
                           "sum": sum(values) if values else None})
    return result


def audit(root, out):
    attempts, calls, anomalies, initial_rows, variants = [], [], [], [], {}
    task_ids = None
    coverage = defaultdict(Counter)
    values = defaultdict(Counter)
    parameter_counts = defaultdict(Counter)
    setting_counts = defaultdict(Counter)
    initial_groups = defaultdict(list)
    templates = {}
    file_manifest = []
    images = defaultdict(set)
    for model in MODELS:
        for trial in (1, 2, 3):
            round_name = f"round{trial}"
            labels_path = root / "data/data/verified" / model / f"{round_name}.json"
            label_bytes = labels_path.read_bytes()
            predictions = json.loads(label_bytes)
            file_manifest.append({"path": str(labels_path.relative_to(root)),
                                  "sha256": hashlib.sha256(label_bytes).hexdigest()})
            if task_ids is None:
                task_ids = set(predictions)
            if set(predictions) != task_ids:
                anomalies.append({"model": model, "round": round_name, "task": "",
                                  "kind": "task_set_mismatch", "details": sorted(set(predictions) ^ task_ids)})
            for task, prediction in sorted(predictions.items()):
                path = root / "data/traj" / model / round_name / task / f"{task}.traj.json"
                key = {"model": model, "round": round_name, "task": task}
                if not path.exists():
                    anomalies.append(key | {"kind": "missing_trajectory", "details": str(path.relative_to(root))})
                    continue
                raw = path.read_bytes()
                try:
                    data = json.loads(raw)
                except (ValueError, UnicodeError) as exc:
                    anomalies.append(key | {"kind": "invalid_json", "details": str(exc)})
                    continue
                file_manifest.append({"path": str(path.relative_to(root)),
                                      "sha256": hashlib.sha256(raw).hexdigest()})
                info, messages = data["info"], data["messages"]
                config = info["config"]
                agent, model_cfg, environment = (config[k] for k in ("agent", "model", "environment"))
                kwargs = model_cfg.get("model_kwargs", {})
                template = {k: v for k, v in agent.items() if k.endswith("template")}
                template_hash = digest(template)
                templates[template_hash] = template
                compact = {"agent_non_templates": {k: v for k, v in agent.items() if not k.endswith("template")},
                           "templates_sha256": template_hash, "model": model_cfg,
                           "environment_without_image": {k: v for k, v in environment.items() if k != "image"},
                           "agent_type": config.get("agent_type"), "model_type": config.get("model_type"),
                           "environment_type": config.get("environment_type"),
                           "mini_version_recorded": info.get("mini_version")}
                config_hash = digest(compact)
                variant = variants.setdefault(config_hash, {"configuration": compact, "members": []})
                variant["members"].append(key)
                initial = [{"role": m["role"], "content": m["content"]} for m in messages[:2]]
                initial_groups[task].append(key | {"sha256": digest(initial)})
                images[task].add(environment.get("image"))
                for parameter in PARAMETERS:
                    parameter_counts[(model, parameter)][encoded(kwargs[parameter]) if parameter in kwargs else "<not explicitly set>"] += 1
                recorded_settings = {
                    'requested_model': model_cfg.get('model_name'),
                    'framework_version': info.get('mini_version'),
                    'step_limit': agent.get('step_limit'),
                    'cost_limit_usd': agent.get('cost_limit'),
                    'shell_timeout_seconds': environment.get('timeout'),
                    'cache_control': model_cfg.get('set_cache_control'),
                    'agent_wrapper': config.get('agent_type'),
                    'interactive_mode': agent.get('mode', '<not applicable>'),
                    'confirm_exit': agent.get('confirm_exit', '<not applicable>'),
                }
                for parameter, value in recorded_settings.items():
                    setting_counts[(model, parameter)][encoded(value)] += 1
                submission = info.get("submission") or ""
                verified = prediction.get("model_patch") or ""
                patch_match = normalized_patch(submission) == normalized_patch(verified)
                row = key | {"label": prediction.get("label"), "exit_status": info.get("exit_status"),
                             "trajectory_path": str(path.relative_to(root)), "trajectory_sha256": hashlib.sha256(raw).hexdigest(),
                             "config_sha256": config_hash, "initial_prompt_sha256": digest(initial),
                             "templates_sha256": template_hash, "requested_model": model_cfg["model_name"],
                             "agent_type": config.get("agent_type"), "step_limit": agent.get("step_limit"),
                             "cost_limit_usd": agent.get("cost_limit"), "shell_timeout_seconds": environment.get("timeout"),
                             "container_lifetime": environment.get("container_timeout"),
                             "cost_tracking_recorded": model_cfg.get("cost_tracking", "<not recorded>"),
                             "cache_control_recorded": model_cfg.get("set_cache_control"),
                             "reasoning_recorded": kwargs.get("reasoning"),
                             "reasoning_effort_recorded": kwargs.get("reasoning_effort"),
                             "recorded_cost_usd": info.get("model_stats", {}).get("instance_cost"),
                             "api_calls_recorded": info.get("model_stats", {}).get("api_calls"),
                             "submission_nonempty": bool(submission.strip()), "patch_text_matches": patch_match,
                             "steps": 0, "shell_action_attempts": 0, "format_error_responses": 0,
                             "command_timeouts": 0, "length_responses": 0, "multiple_choice_responses": 0,
                             "native_tool_call_responses": 0, "visible_output_characters": 0,
                             "unrecognized_user_feedback": 0, "manual_intervention_messages": 0}
                totals, observed = Counter(), Counter()
                response_models, timestamps = Counter(), []
                format_template = agent.get("format_error_template", "").split("{{", 1)[0]
                timeout_template = agent.get("timeout_template", "").split("{{", 1)[0]
                for message_index, message in enumerate(messages):
                    if message["role"] == "user" and message_index > 1 and message_index != len(messages) - 1:
                        content = message.get("content") or ""
                        if any(x in content for x in ("Interrupted by user:", "The user added a new task:", "The user rejected your command")):
                            row["manual_intervention_messages"] += 1
                        recognized = ((format_template and content.startswith(format_template)) or
                                      (timeout_template and content.startswith(timeout_template)) or
                                      content.startswith("<returncode>"))
                        if not recognized:
                            row["unrecognized_user_feedback"] += 1
                    if message["role"] != "assistant":
                        continue
                    row["steps"] += 1
                    content = message.get("content") or ""
                    row["visible_output_characters"] += len(content)
                    action_blocks = re.findall(r"```bash\s*\n(.*?)\n```", content, re.DOTALL)
                    if len(action_blocks) == 1:
                        row["shell_action_attempts"] += 1
                    else:
                        row["format_error_responses"] += 1
                    following = messages[message_index + 1] if message_index + 1 < len(messages) else {}
                    timed_out = following.get("role") == "user" and "timed out and has been killed" in (following.get("content") or "")
                    row["command_timeouts"] += timed_out
                    response = message.get("extra", {}).get("response", {})
                    usage = response.get("usage")
                    if not isinstance(usage, dict):
                        anomalies.append(key | {"kind": "missing_usage", "details": message_index})
                        usage = {}
                    choices = response.get("choices", [])
                    finishes = Counter(str(c.get("finish_reason")) for c in choices)
                    length = finishes["length"] > 0
                    tools = any((c.get("message") or {}).get("tool_calls") or (c.get("message") or {}).get("function_call") for c in choices)
                    row["length_responses"] += length
                    row["multiple_choice_responses"] += len(choices) > 1
                    row["native_tool_call_responses"] += tools
                    response_model = response.get("model")
                    response_models[str(response_model)] += 1
                    created = response.get("created")
                    if numeric(created):
                        timestamps.append(created)
                    call = key | {"step": row["steps"], "message_index": message_index,
                                  "response_model": response_model, "response_created_utc": utc(created),
                                  "choice_count": len(choices), "finish_reasons": dict(finishes),
                                  "length_response": length, "visible_output_characters": len(content),
                                  "parsed_single_bash_block": len(action_blocks) == 1,
                                  "command_timeout": timed_out, "native_tool_call": bool(tools)}
                    for field in FIELDS:
                        value = nested(usage, field)
                        state = ("missing" if value is ABSENT else "null" if value is None else
                                 "numeric" if numeric(value) else "other")
                        coverage[(model, field)][state] += 1
                        call[field] = value if numeric(value) else None
                        call[field + ".state"] = state
                        if numeric(value):
                            coverage[(model, field)]["sum_observed"] += value
                            coverage[(model, field)]["zero" if value == 0 else "nonzero"] += 1
                            totals[field] += value
                            observed[field] += 1
                    p, c, t = (usage.get(k) for k in ("prompt_tokens", "completion_tokens", "total_tokens"))
                    if all(numeric(v) for v in (p, c, t)) and p + c != t:
                        anomalies.append(key | {"kind": "token_total_mismatch", "details": call["step"]})
                    reasoning = nested(usage, "completion_tokens_details.reasoning_tokens")
                    cache = nested(usage, "prompt_tokens_details.cached_tokens")
                    if numeric(reasoning) and numeric(c):
                        values[model]["completion_on_reasoning_observed_responses"] += c
                        values[model]["reasoning_tokens_reported"] += reasoning
                        values[model]["reasoning_subdivision_checked_responses"] += 1
                        values[model]["reasoning_exceeds_completion"] += reasoning > c
                        visible = nested(usage, "completion_tokens_details.text_tokens")
                        if numeric(visible):
                            values[model]["reasoning_plus_text_checked_responses"] += 1
                            values[model]["reasoning_plus_text_equals_completion"] += reasoning + visible == c
                    if numeric(cache) and numeric(p):
                        values[model]["prompt_on_cache_observed_responses"] += p
                        values[model]["cache_subdivision_checked_responses"] += 1
                        values[model]["cache_exceeds_prompt"] += cache > p
                    if length:
                        values[(model, "length_completion_counts")][str(c)] += 1
                    calls.append(call)
                row["response_models"] = dict(response_models)
                row["first_response_utc"] = utc(min(timestamps)) if timestamps else None
                row["last_response_utc"] = utc(max(timestamps)) if timestamps else None
                for field in FIELDS:
                    row[field + ".reported_sum"] = totals[field] if observed[field] else None
                    row[field + ".observed_responses"] = observed[field]
                    row[field + ".complete"] = observed[field] == row["steps"] and row["steps"] > 0
                    row[field] = totals[field] if row[field + ".complete"] else None
                row["prompt_tokens_per_step"] = row["prompt_tokens"] / row["steps"] if row["prompt_tokens"] is not None and row["steps"] else None
                if row["steps"] != row["api_calls_recorded"]:
                    anomalies.append(key | {"kind": "step_counter_mismatch", "details": [row["steps"], row["api_calls_recorded"]]})
                if row["exit_status"] != "Submitted" or not row["submission_nonempty"]:
                    anomalies.append(key | {"kind": "submission_problem", "details": row["exit_status"]})
                attempts.append(row)
    for task, group in sorted(initial_groups.items()):
        initial_rows.append({"task": task, "attempts": len(group),
                             "initial_prompt_variants": len({r["sha256"] for r in group}),
                             "image_string_variants": len(images[task]), "members": group})
    solved_tasks = {task for task in task_ids if len([r for r in attempts if r["task"] == task]) == 9
                    and all(r["label"] is True for r in attempts if r["task"] == task)}
    aligned = defaultdict(list)
    for row in attempts:
        if row["cost_limit_usd"] == 3 and row["shell_timeout_seconds"] == 60:
            aligned[(row["task"], row["round"])].append(row)
    aligned_rows = [r for group in aligned.values() if {r["model"] for r in group} == set(MODELS) for r in group]
    cohorts = {"all_archived_900": attempts,
               "all_models_solved_all_three_trials": [r for r in attempts if r["task"] in solved_tasks],
               "matched_task_rounds_cost3_timeout60": aligned_rows}
    summaries = []
    for name, group in cohorts.items():
        summaries.extend(summarize(group, name, "all"))
        for label, state in ((True, "success"), (False, "failure")):
            summaries.extend(summarize([r for r in group if r["label"] is label], name, state))
    coverage_rows = [{"model": model, "field": field, "responses": sum(coverage[(model, field)][k] for k in ("numeric", "null", "missing", "other")),
                      **{k: coverage[(model, field)][k] for k in ("numeric", "null", "missing", "other", "zero", "nonzero", "sum_observed")}}
                     for model in MODELS for field in FIELDS]
    parameters = [{"model": model, "parameter": parameter,
                   "value": '' if value == '<not explicitly set>' else value,
                   "status": 'unset' if value == '<not explicitly set>' else 'explicit',
                   "n_attempts": count}
                  for model in MODELS for parameter in PARAMETERS
                  for value, count in parameter_counts[(model, parameter)].items()]
    recorded_settings = [dict(row, scope='client API configuration') for row in parameters]
    recorded_settings.extend({"model": model, "parameter": parameter, "value": value,
                              "status": 'recorded', "n_attempts": count,
                              "scope": 'agent configuration'}
                             for (model, parameter), counter in setting_counts.items()
                             for value, count in counter.items())
    configuration_rows = [{"sha256": key, "count": len(v["members"]),
                           "counts_by_model": dict(Counter(r["model"] for r in v["members"])),
                           "counts_by_round": dict(Counter(r["round"] for r in v["members"])), **v}
                          for key, v in variants.items()]
    requests_by_attempt = {(r["model"], r["round"], r["task"]): r["requested_model"] for r in attempts}
    mapping = Counter((c["model"], requests_by_attempt[(c["model"], c["round"], c["task"])], c["response_model"]) for c in calls)
    mapping_rows = [{"model_group": key[0], "requested_model": key[1], "returned_model": key[2], "responses": count} for key, count in mapping.items()]
    audit = {"generated_utc": datetime.now(timezone.utc).isoformat(), "expected_attempts": len(task_ids) * 9,
             "observed_attempts": len(attempts), "tasks": len(task_ids), "recorded_responses": len(calls),
             "exit_statuses": dict(Counter(r["exit_status"] for r in attempts)),
             "initial_prompt_mismatch_tasks": [r["task"] for r in initial_rows if r["initial_prompt_variants"] != 1],
             "template_variants": len(templates), "patch_text_difference_attempts": sum(not r["patch_text_matches"] for r in attempts),
             "cohorts": {name: {"attempts": len(group), "tasks": len({r["task"] for r in group}),
                                "by_model": dict(Counter(r["model"] for r in group))} for name, group in cohorts.items()},
             "usage_detail_checks": {model: dict(values[model]) for model in MODELS},
             "length_completion_counts": {model: dict(values[(model, "length_completion_counts")]) for model in MODELS},
             "anomalies": anomalies,
             "limitations": ["Usage objects are normalized provider/gateway reports, not measured FLOPs or invoices.",
                             "Missing/null optional details are not zero; partial detail sums are not complete trajectory totals."]}
    for name, rows in (("per_attempt.csv", attempts), ("per_response.csv", calls),
                       ("usage_field_coverage.csv", coverage_rows), ("parameter_inventory.csv", parameters),
                       ("settings.csv", recorded_settings),
                       ("prompt_consistency.csv", initial_rows), ("summary_metrics.csv", summaries),
                       ("response_model_mapping.csv", mapping_rows),
                       ("anomalies.csv", anomalies)):
        dump_csv(out, name, rows, ["model", "round", "task", "kind", "details"] if name == "anomalies.csv" else None)
    dump_json(out, "audit.json", audit)
    dump_json(out, "configuration_variants.json", configuration_rows)
    dump_json(out, "prompt_templates.json", templates)
    dump_json(out, "input_manifest.json", file_manifest)
    print(f"Extracted {len(attempts)} attempts and {len(calls)} saved responses; {len(anomalies)} structural anomalies.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=ROOT, help="Repository containing data/traj and data/data/verified")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    audit(args.data_root.resolve(), args.output)


if __name__ == "__main__":
    main()
