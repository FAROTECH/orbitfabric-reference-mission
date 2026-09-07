#!/usr/bin/env python3
"""Generate and verify the OpenC3 F Prime target from a native F Prime dictionary."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

PLUGIN_COMMIT = "f80d6a2d112a9f2680ad9f404bca2ac116315d33"
EXPECTED_COMMAND = "Ref.payload.OF_StopAcquisition"
EXPECTED_PACKET = "Ref.payload.OF_AcquisitionActive"
EXPECTED_ITEM = "OF_AcquisitionActive"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plugin-root", type=Path, required=True)
    parser.add_argument("--dictionary", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    plugin_root = args.plugin_root.resolve()
    dictionary = args.dictionary.resolve()
    output_dir = args.output_dir.resolve()

    actual = subprocess.check_output(
        ["git", "-C", str(plugin_root), "rev-parse", "HEAD"], text=True
    ).strip()
    if actual != PLUGIN_COMMIT:
        raise RuntimeError(f"unexpected OpenC3 F Prime plugin checkout: {actual}")
    if not dictionary.is_file():
        raise RuntimeError(f"F Prime Dictionary.json not found: {dictionary}")

    work = output_dir / "plugin-work"
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    shutil.copytree(plugin_root, work)

    parser_script = work / "lib/fprime_parser.py"
    subprocess.run(
        [sys.executable, str(parser_script), "FPRIME", str(dictionary)],
        cwd=work,
        check=True,
    )

    cmd_path = work / "targets/FPRIME/cmd_tlm/cmd.txt"
    tlm_path = work / "targets/FPRIME/cmd_tlm/tlm.txt"
    if not cmd_path.is_file() or not tlm_path.is_file():
        raise RuntimeError("OpenC3 F Prime parser did not produce expected cmd/tlm files")

    cmd_text = cmd_path.read_text(encoding="utf-8")
    tlm_text = tlm_path.read_text(encoding="utf-8")

    expected_command_line = f"COMMAND <%= target_name %> {EXPECTED_COMMAND} "
    expected_packet_line = f"TELEMETRY <%= target_name %> {EXPECTED_PACKET} "
    expected_item_line = f"APPEND_ITEM {EXPECTED_ITEM} "

    if expected_command_line not in cmd_text:
        raise RuntimeError(f"generated COSMOS command identity missing: {EXPECTED_COMMAND}")
    if expected_packet_line not in tlm_text:
        raise RuntimeError(f"generated COSMOS telemetry packet missing: {EXPECTED_PACKET}")
    if expected_item_line not in tlm_text:
        raise RuntimeError(f"generated COSMOS telemetry item missing: {EXPECTED_ITEM}")

    retained = output_dir / "generated-target"
    retained.mkdir()
    retained_cmd = retained / "cmd.txt"
    retained_tlm = retained / "tlm.txt"
    shutil.copy2(cmd_path, retained_cmd)
    shutil.copy2(tlm_path, retained_tlm)

    evidence = {
        "kind": "orbitfabric.reference_mission.engineering_story_01.openc3_fprime_dry_run",
        "version": "0.1-candidate",
        "status": "passed",
        "plugin_commit": actual,
        "dictionary_sha256": sha256(dictionary),
        "generated": {
            "cmd_txt_sha256": sha256(retained_cmd),
            "tlm_txt_sha256": sha256(retained_tlm),
        },
        "resolved": {
            "target": "FPRIME",
            "command": EXPECTED_COMMAND,
            "telemetry_packet": EXPECTED_PACKET,
            "telemetry_item": EXPECTED_ITEM,
        },
        "assertions": {
            "native_fprime_command_identity_preserved": True,
            "native_fprime_telemetry_identity_preserved": True,
            "no_story_owned_identity_alias_required": True,
        },
    }
    (output_dir / "openc3-fprime-dry-run.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    shutil.rmtree(work)

    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
