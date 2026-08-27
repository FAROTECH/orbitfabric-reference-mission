# 21, Dashboard and Coverage Foundation

Status: tutorial draft aligned to Core v1.1 and Studio Preview 1  
Scope: Core-owned dashboard, scenario-run-index and coverage foundations before downstream rendering

## Purpose

This step explains how OrbitFabric Core can support dashboard and coverage-oriented consumers without moving Mission Data Contract semantics into a UI.

The previous steps showed that OrbitFabric can generate:

```text
documentation
scenario evidence
runtime-facing artifacts
ground-facing artifacts
```

Core v1.1 adds a candidate structured integration layer:

```text
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
```

These are Core-owned machine-readable surfaces.

They are not Studio APIs.

!!! warning "Candidate v1.1 surfaces"
    These reports are additive candidate integration surfaces published with OrbitFabric Core v1.1.0. They do not change the original v1.0.0 stable Mission Data Contract baseline.

## Core rule

The rule remains strict:

```text
Core defines, computes and emits.
Downstream tools consume, link and render.
```

If a dashboard, index or coverage fact matters, Core should emit it as structured evidence rather than requiring a UI to reconstruct it from raw YAML, terminal text or human-oriented logs.

## Source of truth

The authored source remains:

```text
mission/
scenarios/
```

Dashboard and coverage reports are derived outputs. They must not become a second source of truth.

## Dashboard summary

Generate the dashboard summary with:

```bash
orbitfabric export dashboard-summary mission/ \
  --json generated/reports/dashboard_summary.json
```

The report answers:

```text
What dashboard-ready Core facts are available for this Mission Model?
```

It may aggregate facts such as mission identity, validation summary, domain inventory, entity inventory and relationship inventory.

It must not invent coverage or readiness claims that Core does not define.

## Scenario run index

Generate the scenario run index with:

```bash
orbitfabric export scenario-run-index \
  --simulation-reports generated/reports \
  --json generated/reports/scenario_run_index.json
```

The report answers:

```text
Which Core simulation JSON reports are present in this reports directory?
```

It indexes machine-readable simulation reports rather than parsing plain-text logs.

That preserves the rule:

```text
machine-readable evidence must come from machine-readable Core reports
```

## Coverage summary

Generate the coverage summary with:

```bash
orbitfabric export coverage-summary mission/ \
  --entity-index generated/reports/entity_index.json \
  --relationship-manifest generated/reports/relationship_manifest.json \
  --scenario-run-index generated/reports/scenario_run_index.json \
  --json generated/reports/coverage_summary.json
```

The coverage summary derives from structured Core-owned inputs and associated simulation JSON evidence.

It must not derive coverage semantics from:

- plain-text logs;
- human-oriented CLI output;
- generated Markdown;
- generated runtime bindings;
- generated ground dictionaries;
- UI state;
- downstream raw-YAML heuristics.

## What coverage means here

Coverage does not mean flight readiness.

Coverage means a limited Core-defined measurement of which declared Mission Data Contract entities or relationships have been exercised by scenario evidence.

Coverage percentages are valid only when Core owns both numerator and denominator.

No downstream tool should invent private percentages.

## Relation to current Studio Preview 1

These v1.1 surfaces remain relevant ecosystem foundations, but the current Studio Preview 1 must be described accurately.

Preview 1 documents its Core hydration inputs as:

```text
Mission Snapshot
Entity Index
Relationship Manifest including explicit FDIR additions
lint JSON
```

It does not currently advertise `dashboard_summary.json`, `scenario_run_index.json` or `coverage_summary.json` as its active product contract.

That distinction matters.

The correct relationship is:

```text
Core v1.1 dashboard/index/coverage surfaces
    -> valid downstream foundations and future Studio inputs where appropriate

Current Studio Preview 1
    -> Mission Snapshot + Entity Index + Relationship Manifest + lint JSON
```

A Core surface may exist before a Studio capability consumes it.

The existence of `coverage_summary.json`, for example, does not imply that Preview 1 includes a Coverage UI.

## Mission Snapshot is a different concern

Current post-v1.1 Core development also includes candidate `mission_snapshot.json`.

Mission Snapshot is not a dashboard or coverage report. It is a versioned read-only envelope around the complete loaded Mission Model.

It is one of the surfaces consumed by Studio Preview 1 and is discussed in Step 17 and the Studio block.

## Why this distinction improves the architecture

It is tempting to design Studio screens first and then backfill data contracts.

OrbitFabric deliberately follows the opposite order:

```text
Mission Model
-> Core validation and structured facts
-> downstream product needs
-> Studio rendering where implemented
```

That keeps Core reusable beyond Studio and prevents Studio from becoming a hidden semantic implementation.

## What this step proves

This step proves that OrbitFabric Core can emit structured dashboard, indexing and coverage foundations independently of a specific UI.

The correct claim is:

```text
Core can expose structured facts suitable for downstream dashboard and coverage experiences.
```

The incorrect claim is:

```text
Studio Preview 1 currently renders every Core candidate surface.
```

## What this step does not prove

This step does not prove:

- mission health scoring;
- model completeness scoring;
- formal verification;
- flight readiness;
- live telemetry behavior;
- relationship graph inference;
- plugin execution;
- a current Studio Coverage UI.

## Modeling rule introduced in this step

The twenty-first rule is:

```text
Downstream dashboards and coverage views must consume Core-owned structured facts and must not invent private mission semantics.
```

## What comes next

The next step reviews capability coverage across the Core-facing tutorial before the reader moves into Studio Preview 1.
