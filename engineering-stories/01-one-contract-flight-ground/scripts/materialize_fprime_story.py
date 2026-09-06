#!/usr/bin/env python3
"""Materialize the R1 Story-owned F Prime runtime fixture.

This script does not generate flight behavior from OrbitFabric semantics. It composes
adapter-produced FPP declarations into a tiny F Prime project and supplies the one
explicit downstream behavior required by Engineering Story 01:

    OF_StopAcquisition -> OF_AcquisitionActive = false
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

FPRIME_COMMIT = "8a62e455a90b6d4f498c332d45d65a2a819988d8"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise RuntimeError(f"{path}: expected one patch anchor: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def append_before_last_brace(path: Path, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    pos = text.rfind("}\n")
    if pos < 0:
        raise RuntimeError(f"{path}: closing brace not found")
    path.write_text(text[:pos] + block + text[pos:], encoding="utf-8")


def materialize_payload_component(project: Path, projection: Path) -> None:
    root = project / "Ref" / "Reference" / "PayloadComponent"
    generated_root = root / "generated"
    generated_root.mkdir(parents=True, exist_ok=True)

    for filename in ("OF_Commands.fppi", "OF_Telemetry.fppi"):
        source = projection / "components/Reference_PayloadComponent" / filename
        if not source.is_file():
            raise RuntimeError(f"missing adapter-produced FPP fragment: {source}")
        shutil.copy2(source, generated_root / filename)

    (root / "PayloadComponent.fpp").write_text(
        "module Reference {\n"
        "  active component PayloadComponent {\n"
        "    time get port timeCaller\n"
        "    import Fw.Command\n"
        "    import Fw.Channel\n\n"
        '    include "generated/OF_Commands.fppi"\n'
        '    include "generated/OF_Telemetry.fppi"\n'
        "  }\n"
        "}\n",
        encoding="utf-8",
    )

    (root / "PayloadComponentComponentImpl.hpp").write_text(
        "#pragma once\n"
        "#include <Ref/Reference/PayloadComponent/PayloadComponentComponentAc.hpp>\n\n"
        "namespace Reference {\n"
        "class PayloadComponentComponentImpl final : public PayloadComponentComponentBase {\n"
        "  public:\n"
        "    explicit PayloadComponentComponentImpl(const char* const compName);\n"
        "    ~PayloadComponentComponentImpl();\n\n"
        "  private:\n"
        "    void OF_StopAcquisition_cmdHandler(FwOpcodeType opCode, U32 cmdSeq);\n"
        "};\n"
        "}  // namespace Reference\n",
        encoding="utf-8",
    )

    (root / "PayloadComponentComponentImpl.cpp").write_text(
        '#include "PayloadComponentComponentImpl.hpp"\n\n'
        "namespace Reference {\n"
        "PayloadComponentComponentImpl::PayloadComponentComponentImpl(const char* const compName)\n"
        "    : PayloadComponentComponentBase(compName) {}\n\n"
        "PayloadComponentComponentImpl::~PayloadComponentComponentImpl() {}\n\n"
        "void PayloadComponentComponentImpl::OF_StopAcquisition_cmdHandler(\n"
        "    FwOpcodeType opCode, U32 cmdSeq) {\n"
        "    // Story-owned target behavior. OrbitFabric does not generate this implementation.\n"
        "    this->tlmWrite_OF_AcquisitionActive(false);\n"
        "    this->cmdResponse_out(opCode, cmdSeq, Fw::CmdResponse::OK);\n"
        "}\n"
        "}  // namespace Reference\n",
        encoding="utf-8",
    )

    (root / "PayloadComponent.hpp").write_text(
        "#pragma once\n"
        '#include "Ref/Reference/PayloadComponent/PayloadComponentComponentImpl.hpp"\n\n'
        "namespace Reference {\n"
        "using PayloadComponent = PayloadComponentComponentImpl;\n"
        "}  // namespace Reference\n",
        encoding="utf-8",
    )

    (root / "CMakeLists.txt").write_text(
        "set(SOURCE_FILES\n"
        '  "${CMAKE_CURRENT_LIST_DIR}/PayloadComponent.fpp"\n'
        '  "${CMAKE_CURRENT_LIST_DIR}/PayloadComponentComponentImpl.cpp"\n'
        ")\n"
        "register_fprime_module()\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fprime-root", type=Path, required=True)
    parser.add_argument("--projection", type=Path, required=True)
    parser.add_argument("--output-project", type=Path, required=True)
    args = parser.parse_args()

    fprime_root = args.fprime_root.resolve()
    actual = subprocess.check_output(
        ["git", "-C", str(fprime_root), "rev-parse", "HEAD"], text=True
    ).strip()
    if actual != FPRIME_COMMIT:
        raise RuntimeError(f"unexpected F Prime checkout: {actual}")

    projection = args.projection.resolve()
    project = args.output_project.resolve()
    deployment = project / "Ref"

    if project.exists():
        shutil.rmtree(project)
    project.mkdir(parents=True)
    shutil.copytree(fprime_root / "Ref", deployment)

    (deployment / "settings.ini").write_text(
        "[fprime]\nproject_root: ..\n" f"framework_path: {fprime_root}\n",
        encoding="utf-8",
    )

    replace_once(
        deployment / "CMakeLists.txt",
        'find_package(FPrime REQUIRED PATHS "${CMAKE_CURRENT_LIST_DIR}/..")',
        'find_package(FPrime REQUIRED PATHS "${FPRIME_FRAMEWORK_PATH}")',
    )
    replace_once(
        deployment / "PingReceiver/PingReceiverComponentImpl.cpp",
        "#include <Ref/PingReceiver/PingReceiverComponentImpl.hpp>",
        '#include "PingReceiverComponentImpl.hpp"',
    )
    with (deployment / "Top/CMakeLists.txt").open("a", encoding="utf-8") as stream:
        stream.write(
            "\n# R1 Story fixture: prefer copied implementation headers.\n"
            'target_include_directories(Ref_Top BEFORE PRIVATE "${FPRIME_PROJECT_ROOT}")\n'
        )

    materialize_payload_component(project, projection)

    instances = deployment / "Top/instances.fpp"
    topology = deployment / "Top/topology.fpp"
    packets = deployment / "Top/RefPackets.fppi"
    root_cmake = deployment / "CMakeLists.txt"

    append_before_last_brace(
        instances,
        "\n  instance payload: Reference.PayloadComponent base id 0x10030000 \\\n"
        "    queue size Default.QUEUE_SIZE \\\n"
        "    stack size Default.STACK_SIZE \\\n"
        "    priority 18\n\n",
    )
    replace_once(
        topology,
        "    instance pingRcvr\n",
        "    instance pingRcvr\n    instance payload\n",
    )
    replace_once(
        packets,
        "\n} omit {\n",
        "\n  # Story-owned downstream packet allocation. OrbitFabric projects the\n"
        "  # channel declaration; the F Prime deployment owns packet placement.\n"
        "  packet PayloadTlm id 38 group 3 {\n"
        "    payload.OF_AcquisitionActive\n"
        "  }\n\n"
        "} omit {\n",
    )
    replace_once(
        root_cmake,
        'add_fprime_subdirectory("${CMAKE_CURRENT_LIST_DIR}/Top/")',
        'add_fprime_subdirectory("${CMAKE_CURRENT_LIST_DIR}/Reference/PayloadComponent/")\n'
        'add_fprime_subdirectory("${CMAKE_CURRENT_LIST_DIR}/Top/")',
    )

    manifest = {
        "kind": "orbitfabric.reference_mission.engineering_story_01.fprime_fixture",
        "version": "0.1-candidate",
        "fprime_commit": actual,
        "host_deployment": "Ref",
        "component": "Reference.PayloadComponent",
        "instance": "payload",
        "source_bindings": {
            "command": "payload.stop_acquisition",
            "telemetry": "radiation_payload.acquisition_active",
        },
        "resolved_expected_names": {
            "command": "Ref.payload.OF_StopAcquisition",
            "telemetry": "Ref.payload.OF_AcquisitionActive",
        },
        "fixture_behavior": (
            "On OF_StopAcquisition the Story-owned F Prime implementation writes "
            "OF_AcquisitionActive=false and returns command OK."
        ),
        "telemetry_packet_allocation": {
            "packet": "PayloadTlm",
            "id": 38,
            "group": 3,
            "channel": "payload.OF_AcquisitionActive",
            "ownership": "F Prime deployment fixture",
        },
        "ownership_note": (
            "The behavior and telemetry packet placement above are downstream example "
            "implementation choices, not behavior or packet allocation generated from "
            "OrbitFabric mission semantics."
        ),
    }
    (project / "ENGINEERING_STORY_FIXTURE.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print("materialized Engineering Story 01 F Prime fixture")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
