# 20, Ground-Facing Integration Artifacts

Status: tutorial draft  
Scope: generated ground-facing contract artifacts

## Purpose

This step explains the ground-facing artifacts that OrbitFabric Core can generate from the Reference Mission.

The previous step introduced runtime-facing bindings.

This step looks at the opposite integration direction:

```text
Mission Model
-> validated contract
-> generated ground-facing artifacts
```

Ground-facing artifacts are useful because they make telemetry, command, event, fault and data-product definitions easier to inspect from a ground integration perspective.

They are not a ground segment.

!!! warning "Boundary"
    The generated ground-facing artifacts are contract exports. They do not implement a telemetry archive, command uplink service, operator console, station automation, database, transport layer or mission control system.

## Source of truth

The source of truth remains:

```text
mission/
```

The generated ground files are derived from the Mission Model.

If a generated ground artifact disagrees with the Mission Model, fix the model or the generator.

Do not manually edit generated ground artifacts as if they were the authoritative contract.

## Command

Generate ground-facing artifacts with:

```bash
orbitfabric gen ground mission/
```

The current ground generation profile is:

```text
generic
```

A fully explicit command can be written as:

```bash
orbitfabric gen ground mission/ \
  --output-dir generated/ground \
  --profile generic
```

## Expected output area

The generated output is written under:

```text
generated/ground/
```

The current profile-specific area is:

```text
generated/ground/generic/
```

The generated package may include:

- a ground contract manifest;
- JSON dictionaries;
- CSV dictionaries;
- Markdown review artifacts.

The exact generated file list belongs to OrbitFabric Core.

The tutorial should focus on why these artifacts matter, not on treating them as hand-authored integration files.

## Why ground-facing artifacts matter

Ground systems need consistent knowledge of what the spacecraft contract contains.

At minimum, engineering teams often need to review:

- telemetry identifiers;
- command identifiers;
- event identifiers;
- fault identifiers;
- packet definitions;
- data product identifiers;
- downlink intent;
- commandability constraints.

Without a model-first approach, these definitions tend to be duplicated across spreadsheets, documents, scripts and operator notes.

OrbitFabric keeps the Mission Model as the source of truth and emits ground-facing artifacts as reproducible outputs.

## Dictionary-oriented view

A dictionary-oriented artifact is useful because it allows a ground-side reviewer to ask:

```text
Which telemetry items exist?
Which commands exist?
Which events and faults can appear?
Which data products should be expected?
```

This does not mean OrbitFabric is decoding binary packets.

It means OrbitFabric is exporting the contract-facing description of declared mission data entities.

## Review artifact view

Markdown review artifacts are useful for human engineering review.

CSV and JSON dictionaries are useful for downstream processing.

The correct split is:

| Artifact style | Best used for |
|---|---|
| Markdown | Human review and documentation. |
| CSV | Spreadsheet-style inspection and simple exchange. |
| JSON | Tool consumption and automation. |
| Manifest | Generation metadata and contract package inspection. |

## Relation to generated documentation

Generated documentation and ground-facing artifacts are related, but not identical.

Generated documentation explains the Mission Model domains in human-readable Markdown.

Ground-facing artifacts package contract definitions in formats that are more useful for integration review.

The same Mission Model drives both.

## Relation to runtime-facing artifacts

Runtime-facing and ground-facing artifacts serve different sides of the system boundary.

```text
runtime-facing artifacts -> onboard software integration review
ground-facing artifacts  -> ground integration review
```

Both remain derived contract surfaces.

Neither one becomes the implementation itself.

## Relation to scenarios

Ground-facing artifacts do not execute scenarios.

They complement scenario evidence.

The relationship is:

```text
Mission Model defines declared data and behavior.
Scenarios exercise selected operational chains.
Ground-facing artifacts expose declared contract entities for ground-side review.
```

For example, a data product such as:

```text
radiation_histogram
```

can appear consistently in:

- the data product contract;
- downlink flow assumptions;
- scenario evidence;
- relationship manifests;
- generated ground-facing dictionaries.

That continuity is the point.

## What this step proves

This step proves that OrbitFabric can support integration discussion beyond internal documentation.

The correct claim is:

```text
OrbitFabric can generate ground-facing contract artifacts from the Mission Model.
```

The incorrect claim is:

```text
OrbitFabric generates a ground segment.
```

## What this step does not prove

This step does not prove:

- binary telemetry decoding;
- binary telecommand encoding;
- CCSDS, PUS or CFDP compliance;
- XTCE export;
- Yamcs integration;
- OpenC3 integration;
- live command uplink;
- telemetry archive behavior;
- operator console behavior;
- ground station scheduling.

Those topics require separate implementation work and explicit future scope.

OrbitFabric stays at the Mission Data Contract boundary.

## Modeling rule introduced in this step

The twentieth rule is:

```text
Generated ground-facing artifacts expose the contract toward ground integration, but they are not the ground segment.
```

## What comes next

The next tutorial step introduces dashboard and coverage foundations.

That step explains how Core-owned structured reports can support future dashboards and Studio views without moving Mission Data Contract semantics into the UI.
