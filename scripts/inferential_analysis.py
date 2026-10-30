"""Run task-paired inference for repeated-trial model comparisons.

The input is ``per_attempt.csv`` produced by ``audit_token_methodology.py``;
comparison CSVs and the analysis-design record are written to
``result/Statistics results`` by default. The task is the independent sampling
unit and three trials are averaged within each model/task. The script is offline
and requires no third-party packages.
"""

import argparse
import csv
import hashlib
import itertools
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
DEFAULT_OUTPUT = ROOT / "result" / "Statistics results"
RESOURCE_METRICS = ("steps", "prompt_tokens", "completion_tokens")
PREFERRED_MODELS = ("claude-sonnet-4-5-20250929", "gemini-3-pro-preview",
                    "gpt-5-2025-08-07-medium-reasoning")


def percentile(values, probability):
    ordered = sorted(values)
    offset = (len(ordered) - 1) * probability
    lower = int(offset)
    upper = min(lower + 1, len(ordered) - 1)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (offset - lower)


def interval(values):
    observed = [value for value in values if value is not None]
    return ((percentile(observed, .025), percentile(observed, .975))
            if observed else (None, None))


def holm_adjust(p_values):
    """Holm step-down adjusted p-values, preserving input order."""
    adjusted = [None] * len(p_values)
    previous = 0.0
    for rank, index in enumerate(sorted(range(len(p_values)), key=p_values.__getitem__)):
        previous = max(previous, min(1.0, (len(p_values) - rank) * p_values[index]))
        adjusted[index] = previous
    return adjusted


def exact_signed_sum_p_value(differences):
    """Exact two-sided task-swap test for integer paired differences.

    Under the exchangeability null, each complete model/task block can be
    swapped independently. Zero differences do not change the distribution.
    """
    observed = abs(sum(differences))
    magnitudes = [abs(int(value)) for value in differences if value]
    distribution = {0: 1}
    for value in magnitudes:
        updated = Counter()
        for total, count in distribution.items():
            updated[total + value] += count
            updated[total - value] += count
        distribution = updated
    return sum(count for total, count in distribution.items()
               if abs(total) >= observed) / (2 ** len(magnitudes))


def exact_mcnemar_p_value(left_only, right_only):
    """Two-sided exact binomial test on discordant task-level indicators."""
    discordant = left_only + right_only
    if not discordant:
        return 1.0
    tail = sum(math.comb(discordant, count)
               for count in range(min(left_only, right_only) + 1)) / (2 ** discordant)
    return min(1.0, 2 * tail)


def resource_swap_p_values(difference_vectors, repetitions, seed):
    """Share task-level signs across resource outcomes in each permutation.

    Each vector contains integer differences in three-trial totals. Scaling
    these totals to trial means leaves the two-sided statistic unchanged.
    The plus-one correction prevents a zero Monte Carlo p-value.
    """
    rng = random.Random(seed)
    n_tasks = len(difference_vectors[0])
    observed = [abs(sum(vector)) for vector in difference_vectors]
    exceedances = [0] * len(difference_vectors)
    for _ in range(repetitions):
        mask = rng.getrandbits(n_tasks)
        permuted = [0] * len(difference_vectors)
        for task in range(n_tasks):
            sign = 1 if (mask >> task) & 1 else -1
            for metric, vector in enumerate(difference_vectors):
                permuted[metric] += sign * vector[task]
        for metric, total in enumerate(permuted):
            exceedances[metric] += abs(total) >= observed[metric]
    return [(count + 1) / (repetitions + 1) for count in exceedances]


def portable_name(path):
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.name


def write_csv(directory, name, rows, fieldnames):
    with (directory / name).open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_attempts(path):
    with path.open() as stream:
        rows = list(csv.DictReader(stream))
    grouped = defaultdict(lambda: defaultdict(list))
    seen = set()
    for row in rows:
        key = (row["task"], row["model"], row["round"])
        if key in seen:
            raise ValueError(f"Duplicate attempt identifier: {key}")
        seen.add(key)
        label = row["label"].strip().lower()
        if label not in ("true", "false"):
            raise ValueError(f"A Boolean success label is required for {key}")
        row["success"] = int(label == "true")
        for metric in RESOURCE_METRICS:
            value = float(row[metric])
            if not math.isfinite(value) or value < 0 or not value.is_integer():
                raise ValueError(f"A nonnegative integer {metric} is required for {key}")
            row[metric] = int(value)
        cost = row.get("recorded_cost_usd", "")
        row["cost"] = float(cost) if cost != "" else None
        if row["cost"] is not None and (not math.isfinite(row["cost"]) or row["cost"] < 0):
            raise ValueError(f"Invalid recorded cost for {key}")
        grouped[row["task"]][row["model"]].append(row)
    models = sorted({row["model"] for row in rows})
    if len(models) != 3 or not grouped:
        raise ValueError("Exactly three model groups and at least one task are required")
    if set(models) == set(PREFERRED_MODELS):
        models = list(PREFERRED_MODELS)
    for task, groups in grouped.items():
        if set(groups) != set(models) or any(len(group) != 3 for group in groups.values()):
            raise ValueError(f"Task {task} does not have three trials for every model")
    return rows, grouped, models, sorted(grouped)


def analyze(args):
    rows, grouped, models, tasks = load_attempts(args.input)
    n_tasks = len(tasks)
    cost_available = all(row["cost"] is not None for row in rows)
    # Features are model/task means. The same task resample is used for every
    # model and outcome, preserving cross-model pairing and within-task trials.
    resource_names = list(RESOURCE_METRICS) + (["cost"] if cost_available else [])
    features = resource_names + ["resolution_rate", "instability"]
    feature_index = {name: index for index, name in enumerate(features)}
    width = len(features)
    task_vectors, success_counts = [], {}
    for task in tasks:
        vector = []
        for model in models:
            attempts = grouped[task][model]
            successes = sum(row["success"] for row in attempts)
            success_counts[(task, model)] = successes
            vector.extend(mean(row[metric] for row in attempts) for metric in resource_names)
            vector.extend((successes / 3, int(successes in (1, 2))))
        task_vectors.append(vector)
    dimension = len(models) * width
    observed_means = [mean(vector[index] for vector in task_vectors) for index in range(dimension)]
    bootstrap_means = [[] for _ in range(dimension)]
    rng = random.Random(args.seed)
    for _ in range(args.bootstrap_repetitions):
        indices = [rng.randrange(n_tasks) for _ in tasks]
        for index in range(dimension):
            bootstrap_means[index].append(sum(task_vectors[task][index] for task in indices) / n_tasks)

    resources, successes, stability, costs = [], [], [], []
    for pair_index, (left_index, right_index) in enumerate(itertools.combinations(range(len(models)), 2)):
        left, right = models[left_index], models[right_index]
        pair = {"left_model": left, "right_model": right, "n_tasks": n_tasks,
                "trials_per_model_task": 3}
        vectors = [[sum(row[metric] for row in grouped[task][left])
                    - sum(row[metric] for row in grouped[task][right]) for task in tasks]
                   for metric in RESOURCE_METRICS]
        p_values = resource_swap_p_values(vectors, args.permutations, args.seed + pair_index)
        for metric_index, metric in enumerate(resource_names):
            a = left_index * width + feature_index[metric]
            b = right_index * width + feature_index[metric]
            differences = [x-y for x, y in zip(bootstrap_means[a], bootstrap_means[b])]
            ratios = [x/y if y > 0 else None for x, y in zip(bootstrap_means[a], bootstrap_means[b])]
            diff_low, diff_high = interval(differences)
            ratio_low, ratio_high = interval(ratios)
            record = pair | {"metric": "recorded_cost_usd" if metric == "cost" else metric,
                             "left_mean": observed_means[a], "right_mean": observed_means[b],
                             "mean_difference": observed_means[a] - observed_means[b],
                             "difference_ci95_lower": diff_low, "difference_ci95_upper": diff_high,
                             "ratio_of_means": observed_means[a] / observed_means[b] if observed_means[b] > 0 else None,
                             "ratio_ci95_lower": ratio_low, "ratio_ci95_upper": ratio_high}
            if metric == "cost":
                costs.append(record)
            else:
                record["p_value"] = p_values[metric_index]
                resources.append(record)
        for feature, destination, multiplier in (("resolution_rate", successes, 100),
                                                  ("instability", stability, 100)):
            a = left_index * width + feature_index[feature]
            b = right_index * width + feature_index[feature]
            differences = [multiplier * (x-y) for x, y in zip(bootstrap_means[a], bootstrap_means[b])]
            low, high = interval(differences)
            record = pair | {"left_rate": observed_means[a], "right_rate": observed_means[b],
                             "difference_percentage_points": multiplier * (observed_means[a] - observed_means[b]),
                             "difference_ci95_lower_pp": low, "difference_ci95_upper_pp": high}
            if feature == "resolution_rate":
                differences = [success_counts[(task, left)] - success_counts[(task, right)] for task in tasks]
                record["p_value"] = exact_signed_sum_p_value(differences)
            else:
                indicators = [(success_counts[(task, left)] in (1, 2), success_counts[(task, right)] in (1, 2))
                              for task in tasks]
                left_only = sum(x and not y for x, y in indicators)
                right_only = sum(y and not x for x, y in indicators)
                record.update({"left_only_unstable_tasks": left_only, "right_only_unstable_tasks": right_only,
                               "p_value": exact_mcnemar_p_value(left_only, right_only)})
            destination.append(record)
    for family in (resources, successes, stability):
        adjusted = holm_adjust([row["p_value"] for row in family])
        for row, value in zip(family, adjusted):
            row["p_value_holm"] = value
            row["holm_family_size"] = len(family)
    all_tests = resources + successes + stability
    for row, value in zip(all_tests, holm_adjust([row['p_value'] for row in all_tests])):
        row['p_value_holm_global'] = value
        row['global_family_size'] = len(all_tests)

    summaries = []
    for model_index, model in enumerate(models):
        counts = Counter(success_counts[(task, model)] for task in tasks)
        a = model_index * width + feature_index["resolution_rate"]
        b = model_index * width + feature_index["instability"]
        success_low, success_high = interval(bootstrap_means[a])
        instability_low, instability_high = interval(bootstrap_means[b])
        summaries.append({"model": model, "n_tasks": n_tasks, "attempts": n_tasks*3,
                          "resolved_attempts": sum(k*v for k, v in counts.items()),
                          **{f"tasks_with_{k}_successes": counts[k] for k in range(4)},
                          "resolution_rate": observed_means[a],
                          "resolution_rate_ci95_lower": success_low, "resolution_rate_ci95_upper": success_high,
                          "unstable_tasks": counts[1]+counts[2], "instability_rate": observed_means[b],
                          "instability_rate_ci95_lower": instability_low,
                          "instability_rate_ci95_upper": instability_high})

    args.output.mkdir(parents=True, exist_ok=True)
    for filename, result in (("resource_comparisons.csv", resources), ("success_comparisons.csv", successes),
                             ("stability_comparisons.csv", stability), ("success_stability_summary.csv", summaries)):
        write_csv(args.output, filename, result, list(result[0]))
    cost_fields = ["left_model", "right_model", "n_tasks", "trials_per_model_task", "metric", "left_mean", "right_mean",
                   "mean_difference", "difference_ci95_lower", "difference_ci95_upper", "ratio_of_means",
                   "ratio_ci95_lower", "ratio_ci95_upper"]
    write_csv(args.output, "estimated_cost_comparisons.csv", costs, cost_fields)
    design = {
        "input": portable_name(args.input), "input_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
        "n_tasks": n_tasks, "n_attempts": len(rows), "models": models, "trials_per_model_task": 3,
        "sampling_unit": "task; all models and their three trials are kept together",
        "resource_estimand": "mean per-attempt usage after averaging trials within model/task; effects are left-minus-right means and ratios of arithmetic means",
        "bootstrap": {"method": "paired task-cluster percentile bootstrap", "repetitions": args.bootstrap_repetitions,
                      "seed": args.seed, "confidence_level": .95,
                      "intervals": "pointwise estimation intervals, not simultaneous intervals"},
        "resource_test": {"method": "two-sided Monte Carlo task-level sign-flip test", "permutations": args.permutations,
                          "p_value": "(extreme permutations + 1)/(permutations + 1)",
                          "null": "within each task, the two complete model outcome blocks are exchangeable; the statistic is the absolute mean paired difference",
                          "multiplicity": "Holm correction across all nine model-pair by resource-metric tests"},
        "success_test": {"method": "exact task-level sign-flip test by integer-sum dynamic programming",
                         "estimand": "difference in mean task success fractions, in percentage points",
                         "null": "within each task, the paired three-trial success counts are exchangeable between models",
                         "multiplicity": "Holm correction across three model pairs"},
        "stability_test": {"definition": "unstable task: exactly one or two successes out of three trials",
                           "method": "two-sided exact McNemar test on paired task-level instability indicators",
                           "null": "the discordant indicator orientations are equally probable under equal marginal instability rates",
                           "multiplicity": "Holm correction across three model pairs",
                           "interpretation": "agreement includes consistently failed tasks; it is not equivalent to successful reliability"},
        "cost": {"included": cost_available, "analysis": "exploratory paired task-bootstrap differences and ratios only; no hypothesis test",
                 "interpretation": "archived framework estimates, not paid invoices"},
        "global_multiplicity_sensitivity": "An additional Holm adjustment across all 15 resource, success and stability tests is reported alongside outcome-family adjustments.",
        "scope": "fixed archived routes and settings; observational model comparisons, not causal effects of matched decoding parameters",
        "outcome_splits": "success/failure resource summaries are descriptive; no within-outcome hypothesis tests",
        "unavailable_annotations": "failure-taxonomy category tests require per-attempt annotation labels; aggregate category totals do not preserve task dependence"
    }
    (args.output / "analysis_design.json").write_text(json.dumps(design, indent=2) + "\n")
    print(f"Analyzed {len(rows)} attempts in {n_tasks} paired task clusters.")
    for row in summaries:
        print(f"{row['model']}: resolution={100*row['resolution_rate']:.2f}%; unstable tasks={row['unstable_tasks']}/{n_tasks}")
    for row in successes:
        print(f"Success: {row['left_model']} - {row['right_model']}: {row['difference_percentage_points']:+.2f} pp, Holm p={row['p_value_holm']:.6g}")
    for row in stability:
        print(f"Instability: {row['left_model']} - {row['right_model']}: {row['difference_percentage_points']:+.2f} pp, Holm p={row['p_value_holm']:.6g}")


def self_check():
    assert exact_signed_sum_p_value([0, 0]) == 1
    assert exact_signed_sum_p_value([1, -1]) == 1
    assert exact_signed_sum_p_value([1, 1]) == .5
    assert exact_signed_sum_p_value([1, 1, 1]) == .25
    assert exact_mcnemar_p_value(0, 0) == 1
    assert exact_mcnemar_p_value(5, 0) == .0625
    assert holm_adjust([.01, .04, .03]) == [.03, .06, .06]
    assert percentile([0, 10], .025) == .25
    assert resource_swap_p_values([[0, 0]], 19, 42) == [1]
    cases = 0
    for length in range(5):
        for differences in itertools.product(range(-2, 3), repeat=length):
            totals = [sum(sign*value for sign, value in zip(signs, differences))
                      for signs in itertools.product((-1, 1), repeat=length)]
            expected = sum(abs(total) >= abs(sum(differences)) for total in totals) / len(totals)
            assert exact_signed_sum_p_value(differences) == expected
            cases += 1
    print(f"Pure-function checks passed, including {cases} exact-test enumeration cases.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_OUTPUT / "per_attempt.csv")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--bootstrap-repetitions", type=int, default=10000)
    parser.add_argument("--permutations", type=int, default=19999)
    parser.add_argument("--self-check", action="store_true", help="Run pure-function checks and exit")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return
    if args.bootstrap_repetitions < 1 or args.permutations < 1:
        parser.error("Bootstrap repetitions and permutations must be positive")
    analyze(args)


if __name__ == "__main__":
    main()
