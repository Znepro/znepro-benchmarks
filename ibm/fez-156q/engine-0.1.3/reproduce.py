#!/usr/bin/env python3
"""Rebuild the IBM Fez engine 0.1.3 tables from counts and receipts in this directory.

The prepared tables under reproduced/ are outputs. This script does not read them.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
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
ARMS = (
    "m3_in_session",
    "single_run_zero_telemetry",
    "provider_target_card",
    "in_session_card",
)
FOLDERS = {
    "single_run_zero_telemetry": "zero_telemetry",
    "provider_target_card": "provider_target_card",
    "in_session_card": "in_session_card",
}
FIELDS = (
    "raw_absolute_error",
    "m3_in_session_absolute_error",
    "single_run_zero_telemetry_absolute_error",
    "provider_target_card_absolute_error",
    "in_session_card_absolute_error",
)
PROVIDER_SHA = "c61ebc1290d2dba44fdbeb33cb559c6df443caf937c7792567fd0011e689a943"
FAMILIES_25 = {
    "control_diagnostics": ("0.105976", "0.0568953", "0.108119", "0.0443351", "0.0451908"),
    "vqe_molecular": ("0.0590805", "0.0428005", "0.056069", "0.0228104", "0.01934"),
    "qaoa_maxcut": ("0.0795912", "0.0485778", "0.0459166", "0.0339785", "0.0260004"),
    "ising_dynamics": ("0.0771301", "0.0780851", "0.0872858", "0.078083", "0.0844625"),
    "parametric_circuits": ("0.0144851", "0.0100233", "0.0110456", "0.0168846", "0.00800908"),
}
FAMILIES_30 = {
    "control_diagnostics": ("0.0899996", "0.0497782", "0.0960277", "0.0449622", "0.0431305"),
    "vqe_molecular": ("0.0521241", "0.0360766", "0.0495921", "0.0197086", "0.0163276"),
    "qaoa_maxcut": ("0.0708292", "0.0435122", "0.0426158", "0.0317467", "0.0243611"),
    "ising_dynamics": ("0.102645", "0.0865742", "0.109184", "0.0854079", "0.0901401"),
    "parametric_circuits": ("0.0142413", "0.00885704", "0.0103938", "0.015942", "0.00703244"),
}
WINS_25 = {
    "m3_in_session": (20, 1, 1, 3, 20),
    "single_run_zero_telemetry": (19, 0, 3, 3, 20),
    "provider_target_card": (16, 1, 6, 2, 18),
    "in_session_card": (19, 4, 0, 2, 22),
}
WINS_30 = {
    "m3_in_session": (24, 1, 1, 4, 24),
    "single_run_zero_telemetry": (23, 0, 3, 4, 24),
    "provider_target_card": (19, 2, 6, 3, 22),
    "in_session_card": (23, 4, 0, 3, 26),
}
HEAD_25 = {"provider_target_card": (50, 25, 17), "in_session_card": (55, 20, 17)}
HEAD_30 = {"provider_target_card": (53, 37, 18), "in_session_card": (64, 26, 21)}
H2 = (
    ("h2_sto3g_trial_00", 1, "-1.10312", "-1.1192", "-1.10331", "-1.11608", "-1.11745"),
    ("h2_sto3g_trial_00", 2, "-1.09616", "-1.11472", "-1.09619", "-1.10942", "-1.11457"),
    ("h2_sto3g_trial_00", 3, "-1.09969", "-1.11989", "-1.09987", "-1.11289", "-1.11791"),
    ("h2_sto3g_trial_01", 1, "-1.02386", "-1.03809", "-1.025", "-1.06094", "-1.06234"),
    ("h2_sto3g_trial_01", 2, "-1.03021", "-1.04698", "-1.03131", "-1.06648", "-1.07086"),
    ("h2_sto3g_trial_01", 3, "-1.0255", "-1.04356", "-1.02678", "-1.06254", "-1.06787"),
    ("h2_sto3g_trial_02", 1, "-1.0545", "-1.06962", "-1.05518", "-1.09189", "-1.09315"),
    ("h2_sto3g_trial_02", 2, "-1.04356", "-1.06072", "-1.04404", "-1.08045", "-1.08519"),
    ("h2_sto3g_trial_02", 3, "-1.04229", "-1.06077", "-1.04287", "-1.07921", "-1.08399"),
    ("h2_sto3g_trial_03", 1, "-0.987281", "-1.00033", "-0.993889", "-1.02119", "-1.0226"),
    ("h2_sto3g_trial_03", 2, "-0.989682", "-1.00502", "-0.997561", "-1.02248", "-1.02641"),
    ("h2_sto3g_trial_03", 3, "-0.976872", "-0.992938", "-0.996838", "-1.01032", "-1.01434"),
    ("h2_sto3g_trial_04", 1, "-1.05568", "-1.07076", "-1.05635", "-1.09323", "-1.09502"),
    ("h2_sto3g_trial_04", 2, "-1.04264", "-1.06011", "-1.04336", "-1.08176", "-1.08623"),
    ("h2_sto3g_trial_04", 3, "-1.05522", "-1.0742", "-1.0557", "-1.0926", "-1.09733"),
    ("h2_sto3g_trial_05", 1, "-1.03272", "-1.04701", "-1.0333", "-1.06814", "-1.06947"),
    ("h2_sto3g_trial_05", 2, "-1.01779", "-1.03422", "-1.01937", "-1.05412", "-1.05828"),
    ("h2_sto3g_trial_05", 3, "-1.01955", "-1.03724", "-1.02098", "-1.05606", "-1.0604"),
)


def fail(message: str) -> None:
    raise SystemExit(message)


def read_json(path: Path) -> dict:
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        fail(f"expected an object in {path.name}")
    return document


def guard() -> None:
    for name in ("ZNEPRO_API_KEY", "ZNEPRO_API_URL", "IBM_QUANTUM_TOKEN", "IBM_QUANTUM_INSTANCE"):
        if os.environ.get(name):
            fail("unset API credentials before this offline command")
    if (HERE / ".env").exists():
        fail("remove .env from the study directory before this offline command")
    blocked = re.compile(
        "|".join(
            (
                "http" + "s?://",
                "arn:" + "aws",
                "db" + "tr",
                "db" + "ts",
                "znepro_" + "free",
                "cr" + "n:v1",
                "/" + "Users" + "/",
                "Znepro_" + "final" + "tests",
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


def fmt(value: float) -> str:
    return f"{float(value):.6g}"


def expectation(counts: dict[str, int], label: str) -> float:
    total = sum(counts.values())
    if total <= 0:
        fail("empty counts")
    signed = 0
    for bitstring, count in counts.items():
        if len(bitstring) != len(label):
            fail("bitstring width does not match the observable")
        sign = 1
        for index, letter in enumerate(label):
            if letter != "I" and bitstring[index] == "1":
                sign = -sign
        signed += sign * int(count)
    return signed / total


def assignment_rates(counts: dict[str, int], qubits: int) -> list[float]:
    total = sum(counts.values())
    if total != 4096:
        fail("readout calibration does not have 4096 shots")
    ones = [0] * qubits
    for bitstring, count in counts.items():
        if len(bitstring) != qubits or any(bit not in "01" for bit in bitstring):
            fail("readout bitstring does not match the active register")
        for index, bit in enumerate(bitstring):
            if bit == "1":
                ones[index] += int(count)
    return [count / total for count in ones]


def assignment_expectation(counts: dict[str, int], label: str, prepared: list[float], flipped: list[float]) -> float:
    indexes = [index for index, letter in enumerate(label) if letter != "I"]
    gammas = []
    deltas = []
    for index in indexes:
        gamma = 1.0 - prepared[index] - flipped[index]
        if gamma == 0.0:
            fail(f"readout channel on qubit {index} is singular")
        gammas.append(gamma)
        deltas.append(flipped[index] - prepared[index])
    total = sum(counts.values())
    accumulator = 0.0
    for bitstring, count in counts.items():
        product = 1.0
        for index, delta in zip(indexes, deltas):
            measured = 1.0 if bitstring[index] == "0" else -1.0
            product *= measured - delta
        accumulator += product * int(count)
    denominator = 1.0
    for gamma in gammas:
        denominator *= gamma
    return (accumulator / total) / denominator


def logical_rates(record: dict, physicals: list[int], prepared: list[float], flipped: list[float]) -> tuple[list[float], list[float]]:
    index_of = {int(qubit): index for index, qubit in enumerate(physicals)}
    layout = {int(logical): int(physical) for logical, physical in record["logical_to_physical"].items()}
    prepared_logical = []
    flipped_logical = []
    for logical in range(int(record["measured_qubits"])):
        slot = index_of[layout[logical]]
        prepared_logical.append(prepared[slot])
        flipped_logical.append(flipped[slot])
    return prepared_logical, flipped_logical


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


def content_sha(card: dict) -> str:
    body = json.dumps({"edges": card["edges"], "qubits": card["qubits"]}, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(body).hexdigest()


def load_readout(round_number: int, physicals: list[int]) -> tuple[list[float], list[float]]:
    zeros = read_json(HERE / "counts" / f"r{round_number}" / "__readout_all_zero.json")
    ones = read_json(HERE / "counts" / f"r{round_number}" / "__readout_all_one.json")
    for name, document in (("all_zero", zeros), ("all_one", ones)):
        if document.get("local_id") != f"r{round_number}/__readout/{name}":
            fail(f"readout identity mismatch for round {round_number}")
        if document.get("bit_order") != "q0_left" or document.get("source_bit_order") != "qiskit":
            fail(f"readout bit order mismatch for round {round_number}")
        if document.get("kind") != "readout" or document.get("status") != "COMPLETED":
            fail(f"readout record is not complete for round {round_number}")
        if document.get("physical_qubits") != physicals or int(document.get("shots")) != 4096:
            fail(f"readout register mismatch for round {round_number}")
    prepared = assignment_rates({str(key): int(value) for key, value in zeros["counts"].items()}, len(physicals))
    flipped = [1.0 - rate for rate in assignment_rates({str(key): int(value) for key, value in ones["counts"].items()}, len(physicals))]
    return prepared, flipped


def score_rounds(cases: list[dict], physicals: list[int]) -> list[list[dict]]:
    scored: list[list[dict]] = []
    for case in cases:
        rounds = []
        for round_number in (1, 2, 3):
            prepared, flipped = load_readout(round_number, physicals)
            raw_values: dict[str, float] = {}
            arm_values = {arm: {} for arm in ARMS}
            for group in case["measurement_groups"]:
                path = HERE / "counts" / f"r{round_number}" / f"{case['case_id']}__{group['group_id']}.json"
                stored = read_json(path)
                local_id = f"r{round_number}/{case['case_id']}/{group['group_id']}"
                if stored.get("local_id") != local_id or stored.get("case_id") != case["case_id"]:
                    fail(f"counts identity mismatch for {local_id}")
                if stored.get("bit_order") != "q0_left" or stored.get("source_bit_order") != "qiskit":
                    fail(f"counts bit order mismatch for {local_id}")
                if stored.get("status") != "COMPLETED" or stored.get("kind") != "benchmark":
                    fail(f"counts are not a completed benchmark record for {local_id}")
                digest = hashlib.sha256(str(group["qasm"]).encode("utf-8")).hexdigest()
                if stored.get("qasm_sha256") != digest:
                    fail(f"circuit hash mismatch for {local_id}")
                counts = {str(key): int(value) for key, value in stored["counts"].items()}
                if sum(counts.values()) != 4096 or int(stored.get("shots")) != 4096:
                    fail(f"shot record mismatch for {local_id}")
                prepared_logical, flipped_logical = logical_rates(stored, physicals, prepared, flipped)
                for label in group["observables"]:
                    label = str(label)
                    raw_values[label] = expectation(counts, label)
                    arm_values["m3_in_session"][label] = assignment_expectation(counts, label, prepared_logical, flipped_logical)
                    for arm, folder in FOLDERS.items():
                        receipt = read_json(HERE / "receipts" / folder / f"r{round_number}" / f"{case['case_id']}__{group['group_id']}" / f"{label}.json")
                        receipt_id = f"r{round_number}/{case['case_id']}/{group['group_id']}/{label}"
                        if receipt.get("local_id") != receipt_id or receipt.get("observable") != label or receipt.get("target_observable") != label:
                            fail(f"receipt identity mismatch for {receipt_id}")
                        if receipt.get("status") != "COMPLETED" or receipt.get("engine_version") != "0.1.3":
                            fail(f"receipt is not COMPLETED on engine 0.1.3 for {receipt_id}")
                        if receipt.get("arm") != arm or int(receipt.get("total_shots")) != 4096:
                            fail(f"receipt arm or shots mismatch for {receipt_id}")
                        if arm == "single_run_zero_telemetry":
                            if receipt.get("calibration_applied") is not False or "calibration_sha256" in receipt:
                                fail(f"zero-telemetry receipt carries a card for {receipt_id}")
                        else:
                            card = read_json(HERE / "cards" / f"r{round_number}" / f"{arm}.json")
                            if receipt.get("calibration_applied") is not True or receipt.get("card_name") != arm:
                                fail(f"card receipt mismatch for {receipt_id}")
                            if receipt.get("calibration_sha256") != card.get("calibration_sha256"):
                                fail(f"card witness mismatch for {receipt_id}")
                        arm_values[arm][label] = float(receipt["mitigated_expectation"])
            reference = case["recorded_primary"]
            raw = combine(case, raw_values)
            raw_error = absolute_error(raw, reference)
            row = {
                "case_id": case["case_id"],
                "cohort": case["cohort"],
                "family_id": case["family_id"],
                "raw": raw,
                "raw_absolute_error": raw_error,
            }
            for arm in ARMS:
                value = combine(case, arm_values[arm])
                error = absolute_error(value, reference)
                row[arm] = value
                row[f"{arm}_absolute_error"] = error
                row[f"{arm}_reduction"] = raw_error - error
            rounds.append(row)
        scored.append(rounds)
    return scored


def family_cells(cases: list[dict], scored: list[list[dict]], cohort: str | None, family_id: str) -> tuple[str, ...]:
    members = [index for index, case in enumerate(cases) if case["family_id"] == family_id and (cohort is None or case["cohort"] == cohort)]
    cells = []
    for field in FIELDS:
        values = [float(scored[index][round_index][field]) for index in members for round_index in range(3)]
        cells.append(fmt(sum(values) / len(values)))
    return tuple(cells)


def wins(cases: list[dict], scored: list[list[dict]], cohort: str | None, arm: str) -> tuple[int, int, int, int, int]:
    bins = [0, 0, 0, 0]
    mean_lower = 0
    for index, case in enumerate(cases):
        if cohort is not None and case["cohort"] != cohort:
            continue
        better = 0
        arm_errors = []
        raw_errors = []
        for round_index in range(3):
            row = scored[index][round_index]
            if float(row[f"{arm}_absolute_error"]) < float(row["raw_absolute_error"]):
                better += 1
            arm_errors.append(float(row[f"{arm}_absolute_error"]))
            raw_errors.append(float(row["raw_absolute_error"]))
        bins[better] += 1
        if sum(arm_errors) / 3 < sum(raw_errors) / 3:
            mean_lower += 1
    return bins[3], bins[2], bins[1], bins[0], mean_lower


def head_to_head(cases: list[dict], scored: list[list[dict]], cohort: str | None, arm: str) -> tuple[int, int, int]:
    lower = higher = mean_lower = 0
    for index, case in enumerate(cases):
        if cohort is not None and case["cohort"] != cohort:
            continue
        arm_errors = []
        other_errors = []
        for round_index in range(3):
            row = scored[index][round_index]
            arm_error = float(row[f"{arm}_absolute_error"])
            other_error = float(row["m3_in_session_absolute_error"])
            if arm_error < other_error:
                lower += 1
            elif arm_error > other_error:
                higher += 1
            arm_errors.append(arm_error)
            other_errors.append(other_error)
        if sum(arm_errors) / 3 < sum(other_errors) / 3:
            mean_lower += 1
    return lower, higher, mean_lower


def check_cards(rounds: int) -> None:
    for round_number in range(1, rounds + 1):
        provider = read_json(HERE / "cards" / f"r{round_number}" / "provider_target_card.json")
        session = read_json(HERE / "cards" / f"r{round_number}" / "in_session_card.json")
        if provider.get("card_name") != "provider_target_card" or provider.get("calibration_sha256") != PROVIDER_SHA:
            fail(f"provider card witness mismatch in round {round_number}")
        if session.get("card_name") != "in_session_card" or session.get("calibration_sha256") != content_sha(session):
            fail(f"in-session card witness mismatch in round {round_number}")
        for card in (provider, session):
            for row in card["qubits"]:
                for key in ("error_1q", "t1_us", "t2_us", "prob_meas1_prep0", "prob_meas0_prep1"):
                    if key not in row:
                        fail(f"card qubit is missing {key}")
            for edge in card["edges"]:
                if "error_2q" not in edge:
                    fail("card edge is missing error_2q")


def write_tables(cases: list[dict], scored: list[list[dict]]) -> None:
    lines = [
        "# Recomputed Fez tables",
        "",
        "These tables were rebuilt from counts/ and receipts/ in this directory.",
        "",
        "## Families, preregistered 25",
        "",
        "| family | raw | m3_in_session | zero_telemetry | provider_target_card | in_session_card |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for family in FAMILIES:
        cells = " | ".join(family_cells(cases, scored, "main_25", family))
        lines.append(f"| `{family}` | {cells} |")
    lines.extend(["", "## Families, all 30", "", "| family | raw | m3_in_session | zero_telemetry | provider_target_card | in_session_card |", "| --- | ---: | ---: | ---: | ---: | ---: |"])
    for family in FAMILIES:
        cells = " | ".join(family_cells(cases, scored, None, family))
        lines.append(f"| `{family}` | {cells} |")
    lines.extend(["", "## H2 STO-3G energy", "", "| trial | round | raw | m3_in_session | zero_telemetry | provider_target_card | in_session_card |", "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"])
    by_id = {case["case_id"]: index for index, case in enumerate(cases)}
    for case_id, round_number, *_rest in H2:
        row = scored[by_id[case_id]][round_number - 1]
        lines.append(
            f"| `{case_id}` | {round_number} | {fmt(row['raw'])} | {fmt(row['m3_in_session'])} | {fmt(row['single_run_zero_telemetry'])} | {fmt(row['provider_target_card'])} | {fmt(row['in_session_card'])} |"
        )
    lines.append("")
    output = HERE / "reproduced"
    output.mkdir(exist_ok=True)
    (output / "TABLES.md").write_text("\n".join(lines), encoding="utf-8")
    (output / "results.json").write_text(json.dumps({"h2": [list(row) for row in H2], "wins_25": WINS_25, "wins_30": WINS_30}, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    guard()
    manifest = read_json(HERE / "manifest.json")
    cases = manifest["cases"]
    if len(cases) != 30 or manifest.get("device") != "IBM Fez (156Q Heron r2)":
        fail("the manifest is not the 30-case Fez study")
    if manifest.get("engine_version") != "0.1.3" or int(manifest.get("rounds")) != 3:
        fail("the manifest is not engine 0.1.3 across three rounds")
    if int(manifest.get("shots_per_task")) != 4096 or int(manifest.get("benchmark_tasks")) != 162:
        fail("the manifest task budget is not 162 tasks of 4096 shots")
    if int(manifest.get("benchmark_shots")) != 663552 or int(manifest.get("total_shots")) != 688128:
        fail("the manifest shot budget is not 663552 benchmark shots and 688128 total shots")
    if int(manifest.get("readout_calibration_tasks")) != 6 or len(manifest.get("active_physical_qubits") or []) != 22:
        fail("the manifest does not record 6 readout tasks on 22 active qubits")
    main_count = sum(1 for case in cases if case["cohort"] == "main_25")
    examined_count = sum(1 for case in cases if case["cohort"] == "examined_5")
    if main_count != 25 or examined_count != 5:
        fail("the manifest cohorts are not 25 plus 5")
    if any(case["case_id"] in EXAMINED for case in cases if case["cohort"] == "main_25"):
        fail("an examined case is inside the preregistered 25")
    check_cards(3)
    physicals = [int(qubit) for qubit in manifest["active_physical_qubits"]]
    count_files = list((HERE / "counts").rglob("*.json"))
    receipt_files = list((HERE / "receipts").rglob("*.json"))
    if len(count_files) != 168 or len(receipt_files) != 1332:
        fail("expected 168 count files and 1332 receipts")
    shot_total = 0
    for path in count_files:
        shot_total += sum(int(value) for value in read_json(path)["counts"].values())
    if shot_total != 688128:
        fail(f"stored shots are {shot_total}, not 688128")
    scored = score_rounds(cases, physicals)
    for family, expected in FAMILIES_25.items():
        if family_cells(cases, scored, "main_25", family) != expected:
            fail(f"preregistered family mean mismatch for {family}")
    for family, expected in FAMILIES_30.items():
        if family_cells(cases, scored, None, family) != expected:
            fail(f"30-case family mean mismatch for {family}")
    for arm, expected in WINS_25.items():
        if wins(cases, scored, "main_25", arm) != expected:
            fail(f"preregistered win count mismatch for {arm}")
    for arm, expected in WINS_30.items():
        if wins(cases, scored, None, arm) != expected:
            fail(f"30-case win count mismatch for {arm}")
    for arm, expected in HEAD_25.items():
        if head_to_head(cases, scored, "main_25", arm) != expected:
            fail(f"preregistered head-to-head mismatch for {arm}")
    for arm, expected in HEAD_30.items():
        if head_to_head(cases, scored, None, arm) != expected:
            fail(f"30-case head-to-head mismatch for {arm}")
    by_id = {case["case_id"]: index for index, case in enumerate(cases)}
    for case_id, round_number, raw, m3, zero, provider, session in H2:
        row = scored[by_id[case_id]][round_number - 1]
        got = (
            fmt(row["raw"]),
            fmt(row["m3_in_session"]),
            fmt(row["single_run_zero_telemetry"]),
            fmt(row["provider_target_card"]),
            fmt(row["in_session_card"]),
        )
        if got != (raw, m3, zero, provider, session):
            fail(f"H2 energy mismatch for {case_id} round {round_number}")
    write_tables(cases, scored)
    print(json.dumps({"denominator_25_in_session_all_three": 19, "denominator_25_in_session_mean": 22, "denominator_30_in_session_mean": 26, "receipts": 1332, "shots": 688128}, sort_keys=True))


if __name__ == "__main__":
    main()
