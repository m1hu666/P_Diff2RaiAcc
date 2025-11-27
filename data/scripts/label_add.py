import json
from pathlib import Path


def main() -> None:
	base_dir = Path(__file__).resolve().parents[1]

	report_path = base_dir / "traj" / "gemini-3-pro-preview" / "sb-cli-reports" / "swe-bench_verified__test__gemini3.json"
	data_path = base_dir / "data" / "verified" / "gemini-3-pro-preview" / "round3.json"

	with report_path.open("r", encoding="utf-8") as f:
		report = json.load(f)

	resolved_ids = set(report.get("resolved_ids", []))
	unresolved_ids = set(report.get("unresolved_ids", []))

	with data_path.open("r", encoding="utf-8") as f:
		data = json.load(f)

	for iid, obj in data.items():
		if iid in resolved_ids:
			obj["label"] = True
		elif iid in unresolved_ids:
			obj["label"] = False

	with data_path.open("w", encoding="utf-8") as f:
		json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)


if __name__ == "__main__":
	main()
