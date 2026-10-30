"""Summarize provider-reported prompt and completion tokens by outcome.

The model order is read from the summary header so that outcome columns cannot
be silently assigned to the wrong trajectory directory.
"""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SUMMARY_FILE = ROOT / "result" / "summary.txt"
OUTPUT_FILE = ROOT / "result" / "Statistics results" / "token_usage_stats.txt"
TRAJECTORY_ROOT = ROOT / "data" / "traj"


def read_outcomes(path: Path) -> tuple[list[str], list[tuple[str, dict[str, str]]]]:
    lines = [line.split() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines or lines[0][0] != "id" or lines[0][-1] != "difficulty":
        raise ValueError(f"Unexpected summary header: {path}")
    models = lines[0][1:-1]
    records = []
    for parts in lines[1:]:
        if len(parts) < len(models) + 2:
            raise ValueError(f"Incomplete summary row: {' '.join(parts)}")
        outcomes = dict(zip(models, parts[1:1 + len(models)]))
        if any(len(value) != 3 or set(value) - {"√", "×"} for value in outcomes.values()):
            raise ValueError(f"Invalid outcome string for {parts[0]}")
        records.append((parts[0], outcomes))
    return models, records


def trajectory_usage(path: Path) -> tuple[int, int]:
    document = json.loads(path.read_text(encoding="utf-8"))
    prompt = 0
    completion = 0
    for message in document.get("messages", []):
        if message.get("role") != "assistant":
            continue
        usage = message.get("extra", {}).get("response", {}).get("usage", {})
        prompt_value = usage.get("prompt_tokens")
        completion_value = usage.get("completion_tokens")
        if isinstance(prompt_value, (int, float)):
            prompt += int(prompt_value)
        if isinstance(completion_value, (int, float)):
            completion += int(completion_value)
    return prompt, completion


def main() -> None:
    models, records = read_outcomes(SUMMARY_FILE)
    stats = {
        model: {
            outcome: {"count": 0, "prompt": 0, "completion": 0}
            for outcome in ("success", "failure")
        }
        for model in models
    }

    for instance_id, outcomes in records:
        for model, result in outcomes.items():
            for trial, symbol in enumerate(result, 1):
                path = TRAJECTORY_ROOT / model / f"round{trial}" / instance_id / f"{instance_id}.traj.json"
                if not path.is_file():
                    raise FileNotFoundError(f"Missing trajectory: {path}")
                prompt, completion = trajectory_usage(path)
                group = stats[model]["success" if symbol == "√" else "failure"]
                group["count"] += 1
                group["prompt"] += prompt
                group["completion"] += completion

    lines = [
        "Provider-reported token usage by recorded outcome",
        "=" * 60,
        "Prompt and completion counts are summed over saved assistant responses.",
        "Outcome-conditioned values are descriptive and use different task sets.",
        "",
    ]
    for model in models:
        lines.extend([f"Model: {model}", "-" * 60])
        for outcome in ("success", "failure"):
            values = stats[model][outcome]
            count = values["count"]
            if count == 0:
                lines.append(f"  {outcome.title()} attempts: 0")
                continue
            prompt_mean = values["prompt"] / count
            completion_mean = values["completion"] / count
            lines.extend([
                f"  {outcome.title()} attempts: {count}",
                f"    Mean prompt tokens:     {prompt_mean:.2f}",
                f"    Mean completion tokens: {completion_mean:.2f}",
                f"    Mean combined tokens:   {prompt_mean + completion_mean:.2f}",
            ])
        lines.append("")

    expected_attempts = len(records) * len(models) * 3
    observed_attempts = sum(group["count"] for model in stats.values() for group in model.values())
    if observed_attempts != expected_attempts:
        raise ValueError(f"Outcome groups cover {observed_attempts} of {expected_attempts} attempts")
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
