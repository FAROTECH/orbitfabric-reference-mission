#!/usr/bin/env python3
"""Verify that an Integration Result bundle is replayable from its own root."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any


def _load_result(result_path: Path) -> dict[str, Any]:
    if not result_path.is_file():
        raise ValueError("missing integration_result.json at bundle root")

    try:
        value = json.loads(result_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read integration_result.json: {exc}") from exc

    if not isinstance(value, dict):
        raise ValueError("integration_result.json root must be an object")
    if value.get("kind") != "orbitfabric.integration_result":
        raise ValueError("integration_result.json has an unexpected kind")
    if not isinstance(value.get("artifacts"), list):
        raise ValueError("integration_result.json artifacts must be an array")
    return value


def _contained_artifact_path(bundle_root: Path, raw_path: Any) -> tuple[str, Path]:
    if not isinstance(raw_path, str) or not raw_path:
        raise ValueError("artifact path must be a non-empty string")

    relative = PurePosixPath(raw_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"artifact path escapes bundle root: {raw_path}")

    target = (bundle_root / Path(*relative.parts)).resolve()
    try:
        target.relative_to(bundle_root.resolve())
    except ValueError as exc:
        raise ValueError(f"artifact path escapes bundle root: {raw_path}") from exc
    return raw_path, target


def verify_bundle(bundle_root: Path) -> list[tuple[str, str, str]]:
    root = bundle_root.resolve()
    result = _load_result(root / "integration_result.json")
    verified: list[tuple[str, str, str]] = []
    failures: list[str] = []

    for index, artifact in enumerate(result["artifacts"]):
        if not isinstance(artifact, dict):
            failures.append(f"artifact at index {index} must be an object")
            continue

        artifact_id = artifact.get("id")
        label = artifact_id if isinstance(artifact_id, str) and artifact_id else f"index {index}"
        declared_sha256 = artifact.get("sha256")

        try:
            relative, target = _contained_artifact_path(root, artifact.get("path"))
        except ValueError as exc:
            failures.append(f"invalid artifact {label}: {exc}")
            continue

        if not target.is_file():
            failures.append(f"missing artifact {label}: {relative}")
            continue

        if not isinstance(declared_sha256, str) or len(declared_sha256) != 64:
            failures.append(f"invalid declared SHA-256 for artifact {label}: {relative}")
            continue

        actual_sha256 = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual_sha256.lower() != declared_sha256.lower():
            failures.append(
                f"SHA-256 mismatch for artifact {label}: {relative}; "
                f"declared {declared_sha256}, actual {actual_sha256}"
            )
            continue

        verified.append((label, relative, actual_sha256))

    if failures:
        raise ValueError("\n".join(failures))
    return verified


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle_root", type=Path)
    args = parser.parse_args()

    try:
        verified = verify_bundle(args.bundle_root)
    except ValueError as exc:
        print(f"replayable Integration Result bundle FAIL:\n{exc}", file=sys.stderr)
        return 1

    for artifact_id, path, digest in verified:
        print(f"verified {artifact_id}: {path} sha256={digest}")
    print(f"replayable Integration Result bundle PASS: {len(verified)} artifacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
