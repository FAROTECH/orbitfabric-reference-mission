# OrbitFabric Reference Mission

**Contract-oriented engineering reference mission for OrbitFabric Core and OrbitFabric Studio.**

This repository contains a realistic small-spacecraft Reference Mission used to validate, demonstrate and evolve the OrbitFabric ecosystem.

It is not flight software, not a spacecraft simulator and not a real mission configuration. It is an engineering workspace for a representative CubeSat-style Mission Data Contract.

---

## Purpose

The Reference Mission shows how a small spacecraft team can move from operational intent to a structured, machine-readable mission contract, deterministic Core evidence and visual mission understanding in OrbitFabric Studio.

The intended flow is:

```text
mission concept
-> subsystem topology
-> operational states
-> telemetry and command contracts
-> events and recovery rules
-> payload and data products
-> contact and downlink assumptions
-> scenarios
-> generated evidence
-> runtime-facing contract artifacts
-> ground-facing contract artifacts
-> Core-owned structured surfaces
-> Studio mission exploration
```

The goal is a compact, credible and teachable reference mission that demonstrates one coherent OrbitFabric engineering workflow.

---

## Editorial Architecture

The validated mission model is the technical end-state. It is not the tutorial order.

The documentation is organized so that the reader can distinguish between progressive tutorial material and current-state reference material:

```text
docs/
  00-orientation/
  02-tutorial/
  03-reference-overview/
```

The tutorial reconstructs the mission forward from operational reasoning, completes the Core-facing evidence arc, then uses the current Studio Preview 1 to explore the same Core-owned facts visually.

Key rule:

```text
validated end-state
-> editorial decomposition
-> step-by-step construction path
-> Core evidence
-> Studio mission understanding
```

Start from:

```text
docs/00-orientation/00-purpose-and-reading-path.md
```

---

## Repository Layout

```text
.
├── mission/
├── scenarios/
├── docs/
└── mkdocs.yml
```

### `mission/`

Contains the OrbitFabric Mission Model files. This directory must remain compatible with the real OrbitFabric Core loader.

### `scenarios/`

Contains executable OrbitFabric scenario files.

### `docs/`

Contains the progressive tutorial, Studio exploration block and current reference overview.

### `mkdocs.yml`

Contains the local MkDocs Material navigation and rendering configuration for the tutorial site.

---

## Current Scenario Set

The current executable scenario set is:

1. `nominal_payload_acquisition`
2. `eclipse_low_power_payload_suspension`
3. `adcs_degraded_pointing_payload_inhibit`
4. `delayed_sband_downlink_backlog_pending`

The scenario set is intentionally compact. The priority is semantic consistency, not model size.

---

## Current Tutorial Coverage

The tutorial now covers:

- Mission Model construction;
- telemetry, command, event and fault contracts;
- payload lifecycle;
- data products and storage intent;
- contact windows and downlink flows;
- commandability and autonomy;
- executable scenario walkthroughs;
- generated Markdown documentation;
- simulation JSON reports and plain-text logs;
- `model_summary.json`;
- `entity_index.json`;
- `relationship_manifest.json`;
- runtime-facing C++17 contract bindings;
- ground-facing dictionaries and review artifacts;
- v1.1 candidate dashboard, scenario-run-index and coverage surfaces;
- current post-v1.1 candidate `mission_snapshot.json`;
- current additive explicit FDIR Relationship Manifest families;
- an explicit capability coverage matrix;
- OrbitFabric Studio Preview 1 mission opening and hydration boundary;
- Mission Atlas, Entity Explorer and Entity X-Ray;
- Relationship Explorer, Context Path and Context Map;
- low-power FDIR context exploration;
- Operational State Map and Mode Focus;
- the final Core + Studio engineering workflow boundary.

The Studio section documents only capabilities that are implemented in OrbitFabric Studio 0.15.0 Preview 1.

---

## Core Release Posture Used by the Tutorial

The tutorial distinguishes three layers:

```text
v1.0.0
  Stable Mission Data Contract baseline

v1.1.0
  Published candidate integration surface consolidation

current post-v1.1 Core development
  candidate Mission Snapshot
  additive explicit FDIR relationship families
```

The post-v1.1 additions are documented because they are implemented and directly relevant to the current Studio preview, but they are not retroactively described as part of v1.1.0.

---

## How to Validate with OrbitFabric Core

From an environment where the `orbitfabric` CLI is installed:

```bash
orbitfabric lint mission/
orbitfabric gen docs mission/
orbitfabric gen data-flow mission/

orbitfabric export model-summary mission/ \
  --json generated/reports/model_summary.json

orbitfabric export entity-index mission/ \
  --json generated/reports/entity_index.json

orbitfabric export relationship-manifest mission/ \
  --json generated/reports/relationship_manifest.json

orbitfabric sim scenarios/nominal_payload_acquisition.yaml \
  --json generated/reports/nominal_payload_acquisition_report.json \
  --log generated/logs/nominal_payload_acquisition.txt

orbitfabric sim scenarios/eclipse_low_power_payload_suspension.yaml \
  --json generated/reports/eclipse_low_power_payload_suspension_report.json \
  --log generated/logs/eclipse_low_power_payload_suspension.txt

orbitfabric sim scenarios/adcs_degraded_pointing_payload_inhibit.yaml \
  --json generated/reports/adcs_degraded_pointing_payload_inhibit_report.json \
  --log generated/logs/adcs_degraded_pointing_payload_inhibit.txt

orbitfabric sim scenarios/delayed_sband_downlink_backlog_pending.yaml \
  --json generated/reports/delayed_sband_downlink_backlog_pending_report.json \
  --log generated/logs/delayed_sband_downlink_backlog_pending.txt

orbitfabric gen runtime mission/
orbitfabric gen ground mission/
```

Core v1.1 candidate surfaces:

```bash
orbitfabric export dashboard-summary mission/ \
  --json generated/reports/dashboard_summary.json

orbitfabric export scenario-run-index \
  --simulation-reports generated/reports \
  --json generated/reports/scenario_run_index.json

orbitfabric export coverage-summary mission/ \
  --entity-index generated/reports/entity_index.json \
  --relationship-manifest generated/reports/relationship_manifest.json \
  --scenario-run-index generated/reports/scenario_run_index.json \
  --json generated/reports/coverage_summary.json
```

Current post-v1.1 Mission Snapshot support:

```bash
orbitfabric export mission-snapshot mission/ \
  --json generated/reports/mission_snapshot.json
```

Generated outputs should generally stay out of version control unless they are intentionally captured as controlled documentation snapshots.

---

## Relationship to OrbitFabric Studio

This Reference Mission is the primary engineering acceptance mission for **OrbitFabric Studio 0.15.0 Preview 1**.

The current preview consumes these Core-owned machine-readable surfaces:

```text
Mission Snapshot
Entity Index
Relationship Manifest including explicit FDIR additions
lint JSON
```

and exposes them through complementary mission-understanding lenses:

```text
Open Mission
-> Mission Atlas
-> Entity Explorer / Entity X-Ray
-> Relations / Context Path / Context Map
-> Validation Findings
-> Operations / Operational State Map / Mode Focus
```

The Reference Mission tutorial uses real model examples such as `eps.low_battery_warning` and `PAYLOAD_ACTIVE` to show that workflow.

The boundary is strict:

```text
Core owns mission semantics.
Studio makes Core-owned facts understandable.
```

Studio Preview 1 remains read-only with respect to Mission Model source.

Capabilities such as Scenario Replay, Coverage UI, Compare, Generated Output Center and Mission Model editing remain deliberately outside the current tutorial because they are not part of Preview 1.

---

## Studio Tutorial Screenshots

The Studio tutorial uses five real Preview 1 screenshots under:

```text
docs/assets/studio/
```

The publication set is:

```text
01-mission-atlas.png
02-entity-xray-low-battery-warning.png
03-fdir-context-map.png
04-operational-state-map.png
05-mode-focus-payload-active.png
```

The figures were captured from the real Reference Mission in Studio Preview 1 and selected or cropped for editorial clarity. A separate application-open screenshot was intentionally omitted because it duplicated the Mission Atlas surface without adding engineering information.

---

## How to Render the Tutorial Locally

Install the documentation dependency and run MkDocs:

```bash
python -m pip install -r requirements-docs.txt
mkdocs serve
```

Then open:

```text
http://127.0.0.1:8000/
```

For strict validation:

```bash
mkdocs build --strict
```

---

## Working Rules

1. Do not invent YAML syntax outside the OrbitFabric Core schema.
2. Keep mission files compatible with the actual Core loader.
3. Prefer small, scenario-driven increments.
4. Keep real mission or project references out of public-facing material.
5. Do not confuse the validated overview with the progressive tutorial path.
6. Do not describe generated runtime-facing artifacts as flight software.
7. Do not describe generated ground-facing artifacts as a ground segment.
8. Preserve the release posture of stable, candidate and current post-release Core surfaces.
9. Do not document future Studio features as if they existed in Preview 1.
10. Do not let Studio reconstruct or invent Mission Data Contract semantics.
11. Every Studio relationship shown in the tutorial must be traceable to a Core-owned relationship record.
12. Use real Studio screenshots from the Reference Mission rather than mock UI.

---

## Ecosystem Role

This repository is not a replacement for OrbitFabric Core or OrbitFabric Studio.

It is the reference workspace used to exercise both projects:

- **OrbitFabric Core** validates, processes, simulates and generates deterministic artifacts from the mission contract.
- **OrbitFabric Studio** consumes structured Core-owned facts and makes the mission easier for an engineer to navigate and understand.

The complete boundary is:

```text
Mission Model defines the source contract.
Core owns semantic facts and evidence.
Studio consumes and renders those facts.
The engineer remains able to trace visible meaning back to Core-owned semantics.
```
