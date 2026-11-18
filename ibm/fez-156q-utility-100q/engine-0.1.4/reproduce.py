#!/usr/bin/env python3
"""Rebuild the IBM Fez utility-scale engine 0.1.4 tables from counts and receipts.

The prepared tables under reproduced/ are outputs. This script does not read them.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
CIRCUITS = ("mirror_brickwork_d8", "clifford_ising_trotter_d6", "ghz_ladder_local_zz")
WIDTHS = (50, 80, 100)
WEIGHTS = ("Z", "ZZ", "ZZZZ")
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
PROVIDER_SHA = "249cf82cd9b2137980b920afac9009873081c5b49577656275e2045710fc08f0"
WIDTH_MEANS = {
    50: ("0.216833", "0.115087", "0.0891778", "0.0463885", "0.0442466"),
    80: ("0.198532", "0.137404", "0.0632484", "0.0300838", "0.0451668"),
    100: ("0.171007", "0.114083", "0.0562958", "0.0428317", "0.0401012"),
}
CIRCUIT_MEANS = {
    "mirror_brickwork_d8": ("0.278935", "0.222392", "9.8587e-06", "1e-06", "1e-06"),
    "clifford_ising_trotter_d6": ("0.202962", "0.125667", "0.179798", "0.110476", "0.120282"),
    "ghz_ladder_local_zz": ("0.104474", "0.018515", "0.0289138", "0.00882671", "0.00923194"),
}
WEIGHT_MEANS = {
    "Z": ("0.0542354", "0.0340117", "0.00683859", "0.00451599", "0.00213397"),
    "ZZ": ("0.233706", "0.148894", "0.0757422", "0.0437228", "0.0443089"),
    "ZZZZ": ("0.29843", "0.183669", "0.126141", "0.0710652", "0.0830717"),
}
HEAD_TO_HEAD = {
    "provider_target_card": (65, 16, 0),
    "in_session_card": (76, 5, 0),
}


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
                "db" + "uf",
                "znepro_" + "free",
                "cr" + "n:v1",
                "Api" + "Key-",
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


def check_cards(rounds: int) -> None:
    for round_number in range(1, rounds + 1):
        provider = read_json(HERE / "cards" / f"r{round_number}" / "provider_target_card.json")
        session = read_json(HERE / "cards" / f"r{round_number}" / "in_session_card.json")
        if provider.get("card_name") != "provider_target_card" or provider.get("calibration_sha256") != PROVIDER_SHA:
            fail(f"provider card witness mismatch in round {round_number}")
        if session.get("card_name") != "in_session_card" or session.get("calibration_sha256") != content_sha(session):
            fail(f"in-session card witness mismatch in round {round_number}")
        if len(provider["qubits"]) != 103 or len(session["qubits"]) != 103:
            fail(f"card does not cover 103 active qubits in round {round_number}")
        for card in (provider, session):
            for row in card["qubits"]:
                for key in ("error_1q", "t1_us", "t2_us", "prob_meas1_prep0", "prob_meas0_prep1"):
                    if key not in row:
                        fail(f"card qubit is missing {key}")
            for edge in card["edges"]:
                if "error_2q" not in edge:
                    fail("card edge is missing error_2q")


def score(cases: list[dict], physicals: list[int]) -> list[dict]:
    rows = []
    for case in cases:
        group = case["measurement_groups"][0]
        for round_number in (1, 2, 3):
            prepared, flipped = load_readout(round_number, physicals)
            path = HERE / "counts" / f"r{round_number}" / f"{case['case_id']}__g0.json"
            stored = read_json(path)
            local_id = f"r{round_number}/{case['case_id']}/g0"
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
            for observable in group["observables"]:
                label = str(observable["label"])
                reference = float(observable["reference"])
                raw = expectation(counts, label)
                values = {"raw": raw, "m3_in_session": assignment_expectation(counts, label, prepared_logical, flipped_logical)}
                for arm, folder in FOLDERS.items():
                    receipt = read_json(HERE / "receipts" / folder / f"r{round_number}" / f"{case['case_id']}__g0" / f"{label}.json")
                    receipt_id = f"r{round_number}/{case['case_id']}/g0/{label}"
                    if receipt.get("local_id") != receipt_id or receipt.get("observable") != label or receipt.get("target_observable") != label:
                        fail(f"receipt identity mismatch for {receipt_id}")
                    if receipt.get("status") != "COMPLETED" or receipt.get("engine_version") != "0.1.4":
                        fail(f"receipt is not COMPLETED on engine 0.1.4 for {receipt_id}")
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
                    values[arm] = float(receipt["mitigated_expectation"])
                row = {
                    "case_id": case["case_id"],
                    "circuit": case["circuit"],
                    "round": round_number,
                    "weight": str(observable["weight"]),
                    "width": int(case["width"]),
                }
                for arm in ("raw",) + ARMS:
                    row[f"{arm}_absolute_error"] = abs(float(values[arm]) - reference)
                rows.append(row)
    return rows


def cells(rows: list[dict], predicate) -> tuple[str, ...]:
    selected = [row for row in rows if predicate(row)]
    if len(selected) != 27:
        fail("a published group does not have 27 case-rounds")
    output = []
    for arm in ("raw",) + ARMS:
        values = [float(row[f"{arm}_absolute_error"]) for row in selected]
        output.append(fmt(sum(values) / len(values)))
    return tuple(output)


def wins(rows: list[dict], arm: str) -> tuple[int, int, int, int]:
    bins = [0, 0, 0, 0]
    grouped: dict[tuple, list[dict]] = {}
    for row in rows:
        grouped.setdefault((row["case_id"], row["weight"]), []).append(row)
    if len(grouped) != 27:
        fail("expected 27 observables")
    for items in grouped.values():
        better = sum(1 for item in items if float(item[f"{arm}_absolute_error"]) < float(item["raw_absolute_error"]))
        bins[better] += 1
    return bins[3], bins[2], bins[1], bins[0]


def head_to_head(rows: list[dict], arm: str) -> tuple[int, int, int]:
    lower = higher = tied = 0
    for row in rows:
        arm_error = float(row[f"{arm}_absolute_error"])
        other = float(row["m3_in_session_absolute_error"])
        if arm_error < other:
            lower += 1
        elif arm_error > other:
            higher += 1
        else:
            tied += 1
    return lower, higher, tied


def write_tables(rows: list[dict]) -> None:
    lines = [
        "# Recomputed utility-scale tables",
        "",
        "These tables were rebuilt from counts/ and receipts/ in this directory.",
        "",
        "## By width",
        "",
        "| width | raw | m3_in_session | zero_telemetry | provider_target_card | in_session_card |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for width in WIDTHS:
        lines.append(f"| `{width}` | {' | '.join(cells(rows, lambda row, width=width: row['width'] == width))} |")
    lines.extend(["", "## By circuit", "", "| circuit | raw | m3_in_session | zero_telemetry | provider_target_card | in_session_card |", "| --- | ---: | ---: | ---: | ---: | ---: |"])
    for circuit in CIRCUITS:
        lines.append(f"| `{circuit}` | {' | '.join(cells(rows, lambda row, circuit=circuit: row['circuit'] == circuit))} |")
    lines.extend(["", "## By observable weight", "", "| weight | raw | m3_in_session | zero_telemetry | provider_target_card | in_session_card |", "| --- | ---: | ---: | ---: | ---: | ---: |"])
    for weight in WEIGHTS:
        lines.append(f"| `{weight}` | {' | '.join(cells(rows, lambda row, weight=weight: row['weight'] == weight))} |")
    lines.append("")
    output = HERE / "reproduced"
    output.mkdir(exist_ok=True)
    (output / "TABLES.md").write_text("\n".join(lines), encoding="utf-8")
    (output / "results.json").write_text(
        json.dumps(
            {
                "head_to_head_versus_m3": {arm: list(HEAD_TO_HEAD[arm]) for arm in HEAD_TO_HEAD},
                "observables_better_in_all_three_rounds": 27,
                "receipts": 243,
                "shots": 135168,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    guard()
    manifest = read_json(HERE / "manifest.json")
    cases = manifest["cases"]
    if len(cases) != 9 or manifest.get("device") != "IBM Fez (156Q Heron r2)":
        fail("the manifest is not the 9-circuit Fez utility study")
    if manifest.get("engine_version") != "0.1.4" or int(manifest.get("rounds")) != 3:
        fail("the manifest is not engine 0.1.4 across three rounds")
    if int(manifest.get("shots_per_task")) != 4096 or int(manifest.get("benchmark_tasks")) != 27:
        fail("the manifest task budget is not 27 tasks of 4096 shots")
    if int(manifest.get("benchmark_shots")) != 110592 or int(manifest.get("total_shots")) != 135168:
        fail("the manifest shot budget is not 110592 benchmark shots and 135168 total shots")
    if int(manifest.get("readout_calibration_tasks")) != 6 or len(manifest.get("active_physical_qubits") or []) != 103:
        fail("the manifest does not record 6 readout tasks on 103 active qubits")
    if max(int(case["cz_count"]) for case in cases) != 732:
        fail("the largest circuit does not have 732 cz gates")
    check_cards(3)
    physicals = [int(qubit) for qubit in manifest["active_physical_qubits"]]
    count_files = list((HERE / "counts").rglob("*.json"))
    receipt_files = list((HERE / "receipts").rglob("*.json"))
    if len(count_files) != 33 or len(receipt_files) != 243:
        fail("expected 33 count files and 243 receipts")
    shot_total = 0
    for path in count_files:
        shot_total += sum(int(value) for value in read_json(path)["counts"].values())
    if shot_total != 135168:
        fail(f"stored shots are {shot_total}, not 135168")
    rows = score(cases, physicals)
    if len(rows) != 81:
        fail("expected 81 observable rounds")
    for width, expected in WIDTH_MEANS.items():
        if cells(rows, lambda row, width=width: row["width"] == width) != expected:
            fail(f"width mean mismatch for {width}")
    for circuit, expected in CIRCUIT_MEANS.items():
        if cells(rows, lambda row, circuit=circuit: row["circuit"] == circuit) != expected:
            fail(f"circuit mean mismatch for {circuit}")
    for weight, expected in WEIGHT_MEANS.items():
        if cells(rows, lambda row, weight=weight: row["weight"] == weight) != expected:
            fail(f"weight mean mismatch for {weight}")
    for arm in ARMS:
        if wins(rows, arm) != (27, 0, 0, 0):
            fail(f"win count is not 27 of 27 for {arm}")
    for arm, expected in HEAD_TO_HEAD.items():
        if head_to_head(rows, arm) != expected:
            fail(f"head-to-head mismatch for {arm}")
    write_tables(rows)
    print(json.dumps({"in_session_lower_than_m3": 76, "provider_lower_than_m3": 65, "receipts": 243, "shots": 135168, "wins_all_three": 27}, sort_keys=True))


if __name__ == "__main__":
    main()
