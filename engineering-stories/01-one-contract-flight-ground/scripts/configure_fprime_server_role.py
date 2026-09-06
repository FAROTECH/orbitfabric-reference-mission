#!/usr/bin/env python3
"""Configure the R1 Story-owned F Prime fixture as the TCP server endpoint.

The pinned F Prime Ref application uses ``Drv.TcpClient`` because its normal GDS
arrangement expects the flight application to connect outward to a ground server.
The pinned OpenC3 F Prime plugin also owns a TCP client interface. For the R1 live
proof the Story-owned deployment therefore selects F Prime's native ``Drv.TcpServer``
as its communications realization.

This changes only downstream deployment topology. It does not alter OrbitFabric
mission semantics, adapter output, command/telemetry identities, or the native
Dictionary after F Prime generates it.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise RuntimeError(f"{path}: expected exactly one transport-role anchor: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    args = parser.parse_args()

    project = args.project.resolve()
    deployment = project / "Ref"
    instances = deployment / "Top/instances.fpp"
    manifest_path = project / "ENGINEERING_STORY_FIXTURE.json"

    if not instances.is_file():
        raise RuntimeError(f"missing F Prime instances file: {instances}")
    if not manifest_path.is_file():
        raise RuntimeError(f"missing Story fixture manifest: {manifest_path}")

    replace_once(
        instances,
        "  instance comDriver: Drv.TcpClient base id 0x10025000\n",
        "  instance comDriver: Drv.TcpServer base id 0x10025000\n",
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["communications_realization"] = {
        "instance": "comDriver",
        "component": "Drv.TcpServer",
        "listen_address": "0.0.0.0",
        "port": 50000,
        "peer_role": "OpenC3 F Prime plugin TCP client",
        "ownership": "F Prime deployment fixture",
        "reason": (
            "The pinned F Prime Ref deployment and the pinned OpenC3 F Prime plugin "
            "both default to TCP client roles. R1 assigns the native F Prime side the "
            "server role so exactly one runtime endpoint owns listen/accept."
        ),
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print("configured R1 F Prime communications role: Drv.TcpServer on port 50000")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
