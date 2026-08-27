# 27, Core and Studio: One Engineering Workflow

Status: final ecosystem tutorial step  
Scope: closing the Reference Mission as an end-to-end Core + Studio engineering example

## Purpose

The Reference Mission began with a mission need rather than with YAML.

It then progressively introduced the Mission Data Contract, executable scenarios, generated evidence and downstream integration surfaces.

The final step answers the ecosystem-level question:

```text
What does the complete OrbitFabric workflow look like when Core and Studio are used together?
```

## The complete tutorial arc

The Reference Mission now demonstrates this path:

```text
mission need
        ↓
operational reasoning
        ↓
Mission Data Contract
        ↓
Core validation and lint
        ↓
scenario evidence
        ↓
generated documentation
runtime-facing artifacts
ground-facing artifacts
        ↓
Core-owned machine-readable surfaces
        ↓
Studio mission understanding
```

The important point is that the arrows do not transfer semantic ownership away from the Mission Model and Core.

## Define once

The authored source remains:

```text
mission/
scenarios/
```

The mission model declares the entities and contract-level relationships used throughout the tutorial.

The scenarios declare deterministic evidence inputs.

Everything downstream must remain traceable to those sources and to Core processing.

## Core validates, computes and emits

OrbitFabric Core is the semantic authority.

Across this tutorial it provides or generates:

- Mission Model loading and validation;
- semantic lint findings;
- generated Markdown documentation;
- simulation JSON reports;
- human-readable scenario logs;
- `model_summary.json`;
- `entity_index.json`;
- `relationship_manifest.json`;
- runtime-facing C++17 contract bindings;
- ground-facing dictionaries and review artifacts;
- v1.1 candidate dashboard, scenario-run-index and coverage surfaces;
- post-v1.1 candidate Mission Snapshot;
- additive explicit FDIR Relationship Manifest families.

These outputs have different compatibility classifications and should not be flattened into one promise.

The common rule is simpler:

```text
Core owns mission facts and deterministic derived evidence.
```

## Studio makes the mission understandable

OrbitFabric Studio Preview 1 consumes a focused set of Core-owned surfaces:

```text
Mission Snapshot
Entity Index
Relationship Manifest including explicit FDIR extensions
lint JSON
```

It then provides complementary human-facing lenses:

```text
Mission Atlas
Entity Explorer
Entity X-Ray
Relationship Explorer
Context Path
Context Map
Validation Findings
Operational State Map
Mode Focus
```

Studio may organize, normalize, group, label, route and lay out those facts.

It must not become a second semantic authority.

## One fact, multiple useful surfaces

Consider the low-power protection behavior used throughout the Reference Mission.

At source level, the Mission Model declares telemetry, a fault, a recovery target, a payload-stop command, autonomous action and recovery intent.

Core can validate those declarations and emit explicit relationship records.

Scenario evidence can exercise the protective path.

Studio can then let the engineer inspect the fault, follow its explicit relationship context and understand the surrounding operational modes.

The same engineering intent is therefore reused across multiple surfaces without being redefined independently:

```text
source declaration
-> validation
-> machine-readable relationship
-> scenario evidence
-> visual navigation
```

That is the central OrbitFabric thesis demonstrated by this repository.

## What Studio Preview 1 deliberately does not add

This tutorial must stop at the real Preview 1 boundary.

The following Studio capabilities remain deferred:

- Data Product Journey;
- Scenario Catalog;
- Scenario Replay / Evidence;
- Experiment Mode;
- Compare;
- Coverage UI;
- Generated Output Center;
- Mission Model editing;
- live telemetry;
- command uplink;
- mission-control behavior.

Some related Core surfaces already exist or are candidates, but that does not mean Preview 1 renders them.

The Reference Mission should evolve when those Studio capabilities become real and stable enough to teach accurately.

## What this Reference Mission now proves

A reader who completes the tutorial should be able to state the following accurately:

```text
OrbitFabric is a Mission Data Contract framework.

The mission contract is authored once, validated by Core, reused across deterministic evidence and generated integration artifacts, and explored visually in Studio without moving semantic ownership into the UI.
```

The Reference Mission therefore serves simultaneously as:

- a progressive OrbitFabric modeling tutorial;
- a realistic sanitized engineering example;
- an executable scenario evidence set;
- a Core capability demonstration;
- a Studio engineering acceptance mission;
- an end-to-end ecosystem reference workflow.

## What it does not prove

The Reference Mission is not:

- flight software;
- a spacecraft simulator;
- an RF simulator;
- a ground segment;
- mission control;
- a formal verification environment;
- a flight-readiness certification package;
- a protocol implementation;
- a hidden graph-inference engine.

Those boundaries are part of the credibility of the reference.

## Final engineering rule

The twenty-seventh and final rule is:

```text
Define mission meaning once.
Let Core own the fact.
Let downstream tools make that fact useful without redefining it.
```

## Reader takeaway

The final reading path can now be summarized as:

```text
Understand the mission need.
Build the contract progressively.
Validate it.
Exercise it.
Generate evidence.
Inspect integration surfaces.
See the mission in Studio.
Trace every visible fact back to Core-owned semantics.
```

That closes the current OrbitFabric Reference Mission tutorial.
