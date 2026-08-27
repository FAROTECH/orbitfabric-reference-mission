# 19, Runtime-Facing Contract Bindings

Status: tutorial draft  
Scope: generated runtime-facing contract artifacts

## Purpose

This step explains the runtime-facing artifacts that OrbitFabric Core can generate from the Reference Mission.

The previous step showed how scenario evidence makes operational causality reviewable.

This step shows a different capability:

```text
Mission Model
-> validated contract
-> generated runtime-facing bindings
```

Runtime-facing bindings are useful because they make the mission contract easier to inspect from the perspective of onboard software integration.

They are not flight software.

!!! warning "Boundary"
    The generated runtime-facing artifacts are contract bindings. They do not implement schedulers, drivers, telemetry polling, command dispatch logic, RTOS integration, fault-management runtime or hardware behavior.

## Source of truth

The source of truth remains:

```text
mission/
```

The generated runtime files are derived from the Mission Model.

If a generated runtime artifact disagrees with the Mission Model, fix the model or the generator.

Do not manually edit the generated artifact as if it were the authoritative contract.

## Command

Generate runtime-facing artifacts with:

```bash
orbitfabric gen runtime mission/
```

The current runtime generation profile is:

```text
cpp17
```

A fully explicit command can be written as:

```bash
orbitfabric gen runtime mission/ \
  --output-dir generated/runtime \
  --profile cpp17
```

## Expected output area

The generated output is written under:

```text
generated/runtime/
```

The current profile-specific area is:

```text
generated/runtime/cpp17/
```

The exact generated file list belongs to OrbitFabric Core.

The tutorial should focus on the engineering meaning of the output, not on treating generated file names as hand-authored source files.

## What the runtime contract represents

The runtime-facing contract can expose model-derived definitions such as:

- modes;
- telemetry identifiers;
- command identifiers;
- event identifiers;
- fault identifiers;
- packet identifiers;
- payload identifiers;
- data product identifiers;
- runtime contract manifest metadata.

This matters because onboard software discussions often suffer from duplicated definitions.

OrbitFabric reduces that ambiguity by deriving runtime-facing contract artifacts from the same Mission Model used for documentation, linting, scenario evidence and structured inspection.

## Why C++17 matters here

The `cpp17` profile is not presented as a complete onboard framework.

It is useful because many embedded and onboard software teams can review C++ header-level or binding-level artifacts more naturally than generic JSON alone.

The engineering value is:

```text
same contract
-> reviewable by software engineers
-> comparable with onboard implementation choices
-> reproducible from the model
```

## How to review generated runtime artifacts

A reviewer should ask:

- Do generated identifiers match the Mission Model?
- Are telemetry, commands, events and faults visible as contract entities?
- Are payload and data product entities visible where expected?
- Does the manifest identify the mission and generation profile?
- Is the generated output clearly derived and reproducible?
- Is there any accidental implication that the artifact is flight software?

The last question is critical.

A generated runtime-facing artifact is valuable precisely because it remains a contract surface, not an implementation claim.

## Relation to scenarios

Runtime-facing bindings do not execute scenarios.

They complement scenario evidence.

The relationship is:

```text
Mission Model defines the contract.
Scenario evidence exercises selected behavior.
Runtime-facing bindings expose contract identifiers toward onboard integration review.
```

This means a command such as:

```text
payload.start_acquisition
```

can appear consistently in:

- the command contract;
- scenario YAML;
- scenario evidence;
- relationship manifests;
- generated runtime-facing artifacts.

That continuity is the point.

## What this step proves

This step proves that OrbitFabric is not limited to documentation.

It can also produce contract-facing artifacts that are closer to software integration.

The correct claim is:

```text
OrbitFabric can generate runtime-facing contract bindings from the Mission Model.
```

The incorrect claim is:

```text
OrbitFabric generates flight software.
```

## What this step does not prove

This step does not prove:

- flight runtime correctness;
- real command dispatch behavior;
- telemetry acquisition behavior;
- task scheduling behavior;
- RTOS or Linux integration;
- driver integration;
- memory safety of downstream user code;
- hardware readiness.

Those topics belong to actual onboard software engineering.

OrbitFabric stays at the Mission Data Contract boundary.

## Modeling rule introduced in this step

The nineteenth rule is:

```text
Generated runtime-facing artifacts expose the contract toward software integration, but they are not the runtime.
```

## What comes next

The next tutorial step introduces ground-facing integration artifacts.

That step explains the same principle from the opposite side of the mission system: ground-facing dictionaries and review surfaces, not a live ground segment.
