"""Shared output locations and archived task metadata (no external lookups)."""

from pathlib import Path

COHORTS = ("full", "without_django")
DJANGO = "django/django"
SHARED = {
    **dict.fromkeys(("per_attempt.csv", "per_response.csv", "task_metadata.csv"), "data"),
    **dict.fromkeys(("usage_field_coverage.csv", "token_usage_stats.txt", "token_accounting.md",
                     "accounting_coverage.md", "output_limit_diagnostics.md",
                     "missing_usage_shapes.csv", "missing_usage_examples.json", "MISSINGNESS.md"), "accounting"),
    **dict.fromkeys(("settings.csv", "parameter_inventory.csv", "configuration_variants.json",
                     "prompt_consistency.csv", "prompt_templates.json", "response_model_mapping.csv",
                     "settings.md", "runtime_source_evidence.json", "source_settings.csv"), "settings"),
    **dict.fromkeys(("audit.json", "anomalies.csv", "input_manifest.json"), "audits/extraction"),
    **dict.fromkeys(("failure_analysis_inputs.json", "failure_analysis_validation.json"), "audits/failures"),
    "failure_boundary_checks.json": "audits",
    "validation.json": "audits",
}
PER_COHORT = {
    **dict.fromkeys(("summary_metrics.csv", "resource_comparisons.csv", "estimated_cost_comparisons.csv",
                     "resource_usage.md", "resource_inference.md", "estimated_cost.md"), "resources"),
    **dict.fromkeys(("success_comparisons.csv", "stability_comparisons.csv", "success_stability_summary.csv",
                     "success_inference.md", "stability_inference.md", "success_stability.md"), "outcomes"),
    **dict.fromkeys(("failure_trial_catalog.csv", "failure_model_summary.csv", "failure_stage_summary.csv",
                     "failure_taxonomy_summary.csv", "failure_task_summary.csv", "category_inference.csv",
                     "category_uncertainty.csv"), "failures"),
    "analysis_design.json": "",
}


def artifact(root, name, cohort="full"):
    if name in SHARED:
        return Path(root) / SHARED[name] / name
    if name in PER_COHORT:
        if cohort not in COHORTS:
            raise ValueError(f"Unknown cohort: {cohort}")
        return Path(root) / cohort / PER_COHORT[name] / name
    raise ValueError(f"Unregistered analysis artifact: {name}")


def repository(task):
    return task.rsplit("-", 1)[0].replace("__", "/")


def task_metadata(path):
    lines = [line.split() for line in Path(path).read_text().splitlines() if line.strip()]
    if not lines or lines[0][0] != "id" or lines[0][-1] != "difficulty":
        raise ValueError(f"Invalid archived task summary: {path}")
    offset = len(lines[0]) - 1
    result = {}
    for parts in lines[1:]:
        task = parts[0]
        if task in result or len(parts) <= offset:
            raise ValueError(f"Duplicate task or missing difficulty: {task}")
        result[task] = {"task": task, "repository": repository(task),
                        "difficulty": " ".join(parts[offset:])}
    return result
