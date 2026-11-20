#!/usr/bin/env python3
"""Rebuild the Cepheus engine 0.1.4 comparison from sibling counts and local receipts.

The baseline directory is read only. Tables under reproduced/ are outputs.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "engine-0.1.3"
EXAMINED = (
    "diag_asymmetric_3q",
    "h2_sto3g_trial_00",
    "maxcut_cycle8_angles_a",
    "ising_4_end_step3",
    "param_hea_6",
)
FAMILIES = (
    "control_diagnostics",
    "vqe_molecular",
    "qaoa_maxcut",
    "ising_dynamics",
    "parametric_circuits",
)
PUBLISHED = {
    "control_diagnostics": ("0.27178138", "0.033285914"),
    "vqe_molecular": ("0.093121023", "0.025372676"),
    "qaoa_maxcut": ("0.57042544", "0.043746796"),
    "ising_dynamics": ("0.20993661", "0.016534359"),
    "parametric_circuits": ("0.036489691", "0.023908453"),
}


def fail(message: str) -> None:
    raise SystemExit(message)


def read_json(path: Path) -> dict:
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        fail(f"expected an object in {path.name}")
    return document


def guard() -> None:
    if os.environ.get("ZNEPRO_API_KEY") or os.environ.get("ZNEPRO_API_URL"):
        fail("unset ZNEPRO_API_KEY and ZNEPRO_API_URL before this offline command")
    if (HERE / ".env").exists():
        fail("remove .env from the study directory before this offline command")
    blocked = re.compile(
        "|".join(
            (
                "http" + "s?://",
                "arn:" + "aws",
                "Bear" + "er ",
                "znepro_" + "live_",
                "aws_" + "access_key",
                "/Us" + "ers/",
                "task-" + "[0-9a-fA-F]{8}-",
            )
        )
    )
    for path in HERE.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".json", ".py"}:
            continue
        if "reproduced" in path.relative_to(HERE).parts:
            continue
        if blocked.search(path.read_text(encoding="utf-8")):
            fail(f"blocked token in {path.relative_to(HERE)}")


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(str(path.relative_to(root)).encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def support(label: str) -> tuple[int, ...]:
    return tuple(index for index, letter in enumerate(label) if letter != "I")


def expectation(counts: dict[str, int], label: str) -> float:
    total = sum(counts.values())
    if total <= 0:
        fail("empty counts")
    signed = 0
    for bitstring, count in counts.items():
        if len(bitstring) < len(label):
            fail("bitstring is shorter than the observable")
        sign = 1
        for qubit in support(label):
            if bitstring[qubit] == "1":
                sign = -sign
        signed += sign * int(count)
    return signed / total


def combine(case: dict, values: dict[str, float]) -> float | dict[str, float]:
    if case["formula"] == "components":
        return {str(term["pauli"]): float(values[str(term["pauli"])]) for term in case["terms"]}
    total = float(case["constant"])
    for term in case["terms"]:
        total += float(term["coefficient"]) * float(values[str(term["pauli"])])
    return total


def absolute_error(value: float | dict[str, float], reference: object) -> float:
    if isinstance(value, dict):
        if not isinstance(reference, dict):
            fail("component reference is not an object")
        return sum(abs(float(value[key]) - float(reference[key])) for key in value) / len(value)
    return abs(float(value) - float(reference))


def counts_for(case_id: str, group_id: str, round_number: int) -> dict:
    path = BASE / "counts" / f"r{round_number}" / f"{case_id}__{group_id}.json"
    document = read_json(path)
    counts = {str(key): int(value) for key, value in document["counts"].items()}
    if document.get("bit_order") != "q0_left" or sum(counts.values()) != 1000:
        fail(f"shot record mismatch for {case_id} {group_id} r{round_number}")
    if document.get("status") != "COMPLETED" or document.get("data_type") != "real_qpu":
        fail(f"counts are not a completed real-QPU record for {case_id}")
    document["counts"] = counts
    return document


def baseline_receipt(case_id: str, group_id: str, round_number: int, label: str) -> dict:
    path = BASE / "receipts" / "zero_telemetry" / f"r{round_number}" / f"{case_id}__{group_id}" / f"{label}.json"
    document = read_json(path)
    if document.get("status") != "COMPLETED" or document.get("engine_version") != "0.1.3":
        fail(f"baseline receipt is not COMPLETED on engine 0.1.3 for {label}")
    if document.get("arm") != "single_run_zero_telemetry" or document.get("calibration_applied") is not False:
        fail(f"baseline arm mismatch for {label}")
    return document


def candidate_receipt(case_id: str, group_id: str, round_number: int, label: str) -> dict:
    path = HERE / "receipts" / f"r{round_number}" / f"{case_id}__{group_id}" / f"{label}.json"
    document = read_json(path)
    local_id = f"r{round_number}/{case_id}__{group_id}/{label}"
    if document.get("local_id") != local_id or document.get("observable") != label:
        fail(f"candidate identity mismatch for {local_id}")
    if document.get("target_observable") != label or document.get("bit_order") != "q0_left":
        fail(f"candidate binding mismatch for {local_id}")
    if document.get("status") != "COMPLETED" or document.get("engine_version") != "0.1.4":
        fail(f"candidate is not COMPLETED on engine 0.1.4 for {local_id}")
    if document.get("arm") != "single_run_zero_telemetry" or document.get("client_version") != "1.0.3":
        fail(f"candidate arm mismatch for {local_id}")
    if document.get("calibration_applied") is not False or document.get("readout_telemetry") is not False:
        fail(f"candidate telemetry flag mismatch for {local_id}")
    if int(document.get("total_shots")) != 1000 or int(document.get("round")) != round_number:
        fail(f"candidate shots mismatch for {local_id}")
    value = document.get("mitigated_expectation")
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        fail(f"candidate expectation missing for {local_id}")
    return document


def score_case(case: dict, round_number: int) -> dict:
    raw_values: dict[str, float] = {}
    old_values: dict[str, float] = {}
    new_values: dict[str, float] = {}
    for group in case["measurement_groups"]:
        stored = counts_for(case["case_id"], group["group_id"], round_number)
        for label in group["observables"]:
            label = str(label)
            raw_values[label] = expectation(stored["counts"], label)
            old = baseline_receipt(case["case_id"], group["group_id"], round_number, label)
            new = candidate_receipt(case["case_id"], group["group_id"], round_number, label)
            if new["mitigated_expectation"] != old["mitigated_expectation"]:
                fail(f"0.1.4 expectation differs from 0.1.3 for {case['case_id']} {label} r{round_number}")
            old_values[label] = float(old["mitigated_expectation"])
            new_values[label] = float(new["mitigated_expectation"])
    required = [str(term["pauli"]) for term in case["terms"]]
    if any(label not in raw_values for label in required):
        fail(f"missing observable for {case['case_id']} round {round_number}")
    raw_error = absolute_error(combine(case, raw_values), case["recorded_primary"])
    old_error = absolute_error(combine(case, old_values), case["recorded_primary"])
    new_error = absolute_error(combine(case, new_values), case["recorded_primary"])
    if old_error != new_error:
        fail(f"absolute error differs for {case['case_id']} round {round_number}")
    return {
        "raw_absolute_error": raw_error,
        "reduction": raw_error - new_error,
        "znepro_absolute_error": new_error,
    }


def fmt(value: float) -> str:
    return f"{float(value):.8g}"


def check_wording() -> None:
    for name in ("README.md", "SUMMARY.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        for phrase in (
            "20 of 25",
            "21 of 25",
            "diag_near_zero_2q",
            "ising_6_mag_step1",
            "162 tasks",
            "162,000",
            "calibration_applied",
            "readout",
            "93",
        ):
            if phrase not in text:
                fail(f"missing required phrase in {name}: {phrase}")


def write_tables(document: dict) -> None:
    lines = [
        "# Recomputed Cepheus 0.1.4 tables",
        "",
        "These tables were rebuilt from the sibling baseline counts and the receipts in this directory.",
        "Every 0.1.4 expectation matched the stored 0.1.3 expectation.",
        "",
        f"Main result: {document['all_three_better']} of 25 cases are better in all three rounds, and {document['mean_smaller']} of 25 have a lower three-round mean.",
        "",
        "Cases worse than raw in all three rounds: `diag_near_zero_2q` and `ising_6_mag_step1`.",
        "",
        "## Families of the 25",
        "",
        "| family | MAE | mean reduction | unit |",
        "| --- | ---: | ---: | --- |",
    ]
    for family in document["families"]:
        lines.append(
            f"| `{family['family_id']}` | {family['mae']} | {family['mean_reduction']} | {family['unit']} |"
        )
    lines.append("")
    output = HERE / "reproduced"
    output.mkdir(exist_ok=True)
    (output / "TABLES.md").write_text("\n".join(lines), encoding="utf-8")
    (output / "results.json").write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    guard()
    check_wording()
    if not (BASE / "manifest.json").is_file():
        fail("sibling engine 0.1.3 manifest is missing")
    before = tree_digest(BASE)
    status = read_json(HERE / "status.json")
    if status.get("engine_version") != "0.1.4" or status.get("arm") != "single_run_zero_telemetry":
        fail("status.json is not the zero-telemetry 0.1.4 record")
    if status.get("candidate_receipts") != 444 or status.get("planned_payloads") != 444:
        fail("status.json does not record 444 receipts")
    if status.get("main_all_three_better") != 20 or status.get("main_mean_smaller") != 21:
        fail("status.json headlines differ from 20 of 25 and 21 of 25")
    if status.get("missing_readout_telemetry_groups") != 162 or status.get("missing_coupling_telemetry_groups") != 93:
        fail("status.json telemetry gaps differ from 162 readout and 93 coupling")
    if status.get("zero_reference_cases") != ["diag_near_zero_2q", "ising_6_mag_step1"]:
        fail("status.json zero-reference cases differ")
    if status.get("bit_order") != "q0_left" or status.get("client_version") != "1.0.3":
        fail("status.json client or bit order differs")
    manifest = read_json(BASE / "manifest.json")
    cases = manifest["cases"]
    if len(cases) != 30:
        fail("the manifest does not contain 30 cases")
    receipts = list((HERE / "receipts").rglob("*.json"))
    if len(receipts) != 444:
        fail("candidate coverage is not 444 receipts")
    rows = []
    for case in cases:
        reductions = []
        errors = []
        for round_number in (1, 2, 3):
            scored = score_case(case, round_number)
            reductions.append(float(scored["reduction"]))
            errors.append(float(scored["znepro_absolute_error"]))
        rows.append(
            {
                "case_id": case["case_id"],
                "cohort": "examined_5" if case["case_id"] in EXAMINED else "main_25",
                "errors": errors,
                "family_id": case["family_id"],
                "mean": sum(reductions) / 3,
                "reductions": reductions,
                "rounds_better": sum(value > 0 for value in reductions),
                "unit": case["unit"],
            }
        )
    main = [row for row in rows if row["cohort"] == "main_25"]
    if len(main) != 25:
        fail("the main denominator is not 25")
    all_three = sum(row["rounds_better"] == 3 for row in main)
    mean_smaller = sum(row["mean"] > 0 for row in main)
    worse_all = sorted(row["case_id"] for row in main if row["rounds_better"] == 0)
    if all_three != 20 or mean_smaller != 21 or worse_all != ["diag_near_zero_2q", "ising_6_mag_step1"]:
        fail("rebuilt 25-case counts do not match the published result")
    families = []
    for family in FAMILIES:
        selected = [row for row in main if row["family_id"] == family]
        if not selected:
            fail(f"family has no main cases: {family}")
        errors = [value for row in selected for value in row["errors"]]
        mae = sum(errors) / len(errors)
        mean_reduction = sum(row["mean"] for row in selected) / len(selected)
        rendered = (fmt(mae), fmt(mean_reduction))
        if rendered != PUBLISHED[family]:
            fail(f"family table differs for {family}")
        families.append(
            {
                "family_id": family,
                "mae": rendered[0],
                "mean_reduction": rendered[1],
                "unit": selected[0]["unit"],
            }
        )
    if tree_digest(BASE) != before:
        fail("the engine 0.1.3 baseline changed during the rebuild")
    document = {
        "all_three_better": all_three,
        "expectations_matched": 444,
        "families": families,
        "mean_smaller": mean_smaller,
        "receipts": 444,
    }
    write_tables(document)
    print(json.dumps(document, sort_keys=True))


if __name__ == "__main__":
    main()
