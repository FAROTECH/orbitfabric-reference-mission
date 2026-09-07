#!/usr/bin/env python3
"""Materialize the R1 Reference Project F Prime runtime fixture.

This script does not generate flight behavior from OrbitFabric semantics. It composes
adapter-produced FPP declarations into a F Prime deployment fixture and supplies the
one explicit downstream behavior required by Engineering Story 01:

    OF_StopAcquisition -> OF_AcquisitionActive = false

The pinned F Prime Ref deployment is used only as a native infrastructure host. Demo
application components unrelated to the Story slice are removed *before* native F
Prime generation. The resulting F Prime dictionary is never filtered or rewritten.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

FPRIME_COMMIT = "8a62e455a90b6d4f498c332d45d65a2a819988d8"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise RuntimeError(f"{path}: expected one patch anchor: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def regex_remove_once(path: Path, pattern: str, *, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, "", text, count=1, flags=re.MULTILINE | re.DOTALL)
    if count != 1:
        raise RuntimeError(f"{path}: expected one removable {label}, found {count}")
    path.write_text(updated, encoding="utf-8")


def remove_line_once(path: Path, line: str) -> None:
    replace_once(path, line, "")


def remove_instance_block(path: Path, instance: str) -> None:
    # F Prime Ref instance declarations end at the first blank line. This deliberately
    # operates on the copied Reference Project fixture, never on the upstream checkout.
    regex_remove_once(
        path,
        rf"^  instance {re.escape(instance)}:.*?(?:\n\n)",
        label=f"instance block {instance}",
    )


def remove_packet(path: Path, packet: str) -> None:
    regex_remove_once(
        path,
        rf"^  packet {re.escape(packet)} id .*?^  \}}\n\n",
        label=f"telemetry packet {packet}",
    )


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
        "    // Reference Project target behavior. OrbitFabric does not generate this implementation.\n"
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


def narrow_ref_demo_content(deployment: Path) -> list[str]:
    """Remove upstream sample-application content unrelated to R1.

    The native framework/subtopology infrastructure remains intact. The removed
    components are F Prime Ref *demo payloads*, not runtime infrastructure needed for
    command dispatch, telemetry, time, scheduling, or communication.
    """

    instances = deployment / "Top/instances.fpp"
    topology = deployment / "Top/topology.fpp"
    packets = deployment / "Top/RefPackets.fppi"
    root_cmake = deployment / "CMakeLists.txt"

    removed: list[str] = []

    # TypeDemo exercises arrays of user-defined enums and many scalar types. It is
    # unrelated to R1 and independently exposed the downstream OpenC3 array parser
    # limitation observed while preparing the minimal Reference Project fixture.
    remove_instance_block(instances, "typeDemo")
    remove_line_once(topology, "    instance typeDemo\n")
    remove_line_once(root_cmake, 'add_fprime_subdirectory("${CMAKE_CURRENT_LIST_DIR}/TypeDemo/")\n')
    remove_packet(packets, "TypeDemo")
    removed.append("Ref.TypeDemo")

    # SignalGen is another Ref sample payload. Its PairHistory channels are arrays of
    # the user-defined Ref.SignalPair struct and independently reproduce the same
    # downstream OpenC3 array-resolution limitation. None of SG1..SG5 participates in
    # the R1 stop-acquisition proof.
    for instance in ("SG1", "SG2", "SG3", "SG4", "SG5"):
        remove_instance_block(instances, instance)
        remove_line_once(topology, f"    instance {instance}\n")

    remove_line_once(root_cmake, 'add_fprime_subdirectory("${CMAKE_CURRENT_LIST_DIR}/SignalGen/")\n')

    for connection in (
        "      rateGroup1Comp.RateGroupMemberOut[0] -> SG1.schedIn\n",
        "      rateGroup1Comp.RateGroupMemberOut[1] -> SG2.schedIn\n",
        "      rateGroup2Comp.RateGroupMemberOut[2] -> SG3.schedIn\n",
        "      rateGroup2Comp.RateGroupMemberOut[3] -> SG4.schedIn\n",
        "      rateGroup3Comp.RateGroupMemberOut[1] -> SG5.schedIn\n",
    ):
        remove_line_once(topology, connection)

    signal_data_product_block = """      ### Moved this out of DataProducts Subtopology --> anything specific to deployment should live in Ref connections
      # Synchronous request. Will have both request kinds for demo purposes, not typical
      SG1.productGetOut -> DataProducts.Subtopology.productGetIn
      # Asynchronous request
      SG1.productRequestOut -> DataProducts.Subtopology.productRequestIn
      DataProducts.Subtopology.productResponseOut -> SG1.productRecvIn
      # Send filled DP
      SG1.productSendOut -> DataProducts.Subtopology.productSendIn
"""
    replace_once(topology, signal_data_product_block, "")

    for packet in (
        "SigGenSum",
        "SigGen1Info",
        "SigGen2Info",
        "SigGen3Info",
        "SigGen4Info",
        "SigGen5Info",
        "SigGen1",
        "SigGen2",
        "SigGen3",
        "SigGen4",
        "SigGen5",
    ):
        remove_packet(packets, packet)
    removed.append("Ref.SignalGen (SG1..SG5)")

    # DpDemo is a data-product sample with multiple nested/array user-defined types.
    # The standard DataProducts subtopology is retained; only this sample producer is
    # removed because it has no role in R1.
    remove_instance_block(instances, "dpDemo")
    remove_line_once(topology, "    instance dpDemo\n")
    remove_line_once(root_cmake, 'add_fprime_subdirectory("${CMAKE_CURRENT_LIST_DIR}/DpDemo/")\n')
    remove_line_once(topology, "      rateGroup2Comp.RateGroupMemberOut[4] -> dpDemo.run\n")

    dp_demo_connections = """      # Synchronous request
      dpDemo.productGetOut -> DataProducts.Subtopology.productGetIn
      # Send filled DP
      dpDemo.productSendOut -> DataProducts.Subtopology.productSendIn
      # Asynchronous request
      dpDemo.productRequestOut -> DataProducts.Subtopology.productRequestIn
      DataProducts.Subtopology.productResponseOut -> dpDemo.productRecvIn
"""
    replace_once(topology, dp_demo_connections, "")
    removed.append("Ref.DpDemo")

    return removed


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
            "\n# R1 Reference Project fixture: prefer copied implementation headers.\n"
            'target_include_directories(Ref_Top BEFORE PRIVATE "${FPRIME_PROJECT_ROOT}")\n'
        )

    removed_demo_content = narrow_ref_demo_content(deployment)
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
        "\n  # Reference Project downstream packet allocation. OrbitFabric projects the\n"
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
        "version": "0.2-candidate",
        "fprime_commit": actual,
        "host_deployment": "Ref infrastructure, narrowed before native generation",
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
            "On OF_StopAcquisition the Reference Project F Prime implementation writes "
            "OF_AcquisitionActive=false and returns command OK."
        ),
        "telemetry_packet_allocation": {
            "packet": "PayloadTlm",
            "id": 38,
            "group": 3,
            "channel": "payload.OF_AcquisitionActive",
            "ownership": "F Prime deployment fixture",
        },
        "excluded_upstream_demo_content": {
            "components": removed_demo_content,
            "reason": (
                "Unrelated F Prime Ref sample-application content with no role in the R1 "
                "semantic slice. TypeDemo and SignalGen also exposed the qualified-array "
                "parser limitation observed during R1. Removal occurs before native F Prime "
                "generation; the resulting native dictionary is not filtered or patched."
            ),
        },
        "ownership_note": (
            "The behavior, telemetry packet placement, and narrowing of unrelated Ref "
            "demo content are Reference Project fixture choices, not behavior or "
            "deployment generated from OrbitFabric mission semantics."
        ),
    }
    (project / "ENGINEERING_STORY_FIXTURE.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print("materialized Engineering Story 01 Reference Project F Prime fixture")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
