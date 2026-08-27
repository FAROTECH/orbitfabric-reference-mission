# 17, Generated Artifacts

Status: tutorial draft aligned to current Core  
Scope: generated documentation, reports, logs, runtime-facing artifacts, ground-facing artifacts and current structured surfaces

## Purpose

This step explains the generated artifacts produced from the Reference Mission.

The previous tutorial steps built the mission model and walked through the four current scenarios. This step explains what OrbitFabric Core can generate or export from that material.

Generated artifacts turn the mission contract into reviewable evidence and downstream inspection surfaces.

They are not the source of truth.

The source of truth remains:

```text
mission/
scenarios/
```

!!! note "Source of truth"
    The Mission Model and scenario YAML files remain authoritative. Generated files must be regenerated from Core, not hand-edited to make the tutorial look right.

## Repository policy

The repository currently ignores:

```text
generated/
```

Generated output should therefore be treated as local reproducible evidence unless the project intentionally captures controlled snapshots for documentation or release evidence.

## Current generated artifact groups

The tutorial uses five local output groups:

```text
generated/docs/
generated/reports/
generated/logs/
generated/runtime/
generated/ground/
```

| Group | Role |
|---|---|
| `generated/docs/` | Human-reviewable Markdown generated from the mission model. |
| `generated/reports/` | Machine-readable JSON evidence and Core-owned inspection surfaces. |
| `generated/logs/` | Human-reviewable scenario timelines. |
| `generated/runtime/` | Runtime-facing contract bindings and manifests. |
| `generated/ground/` | Ground-facing dictionaries, manifests and review artifacts. |

The value is not file volume. The value is reuse of one mission contract across consistent engineering surfaces.

## Compatibility classification

The current tutorial must distinguish the release posture of these outputs.

| Surface class | Examples | Interpretation |
|---|---|---|
| Stable v1 compatibility-sensitive Core surfaces | lint JSON, simulation JSON, `model_summary.json`, `entity_index.json`, original v1 `relationship_manifest.json` families | Machine-readable Core evidence or inspection surfaces with the stable v1 baseline. |
| v1.1 candidate integration surfaces | `dashboard_summary.json`, `scenario_run_index.json`, `coverage_summary.json`, structured simulation expectation accounting | Additive published candidate surfaces introduced by the v1.1 integration consolidation. |
| Current post-v1.1 candidate development | `mission_snapshot.json`, additive explicit FDIR Relationship Manifest families | Implemented on current Core development after v1.1; not retroactively part of the v1.1 release. |
| Preview or disposable generated artifacts | generated Markdown, plain-text logs, C++17 runtime-facing bindings, ground dictionaries and manifests | Useful outputs, but not Mission Model source. |

!!! warning "Do not overclaim"
    Runtime-facing artifacts are not flight software. Ground-facing artifacts are not a ground segment. Candidate Core surfaces are not Studio APIs.

## Generated documentation

Generate human-reviewable documentation with:

```bash
orbitfabric gen docs mission/
orbitfabric gen data-flow mission/
```

The resulting Markdown provides a direct generated view of the current model domains and data-flow declarations.

Generated docs are useful for review, but they do not replace the tutorial. The tutorial explains why each contract area exists and how it participates in operational reasoning.

## Stable v1 inspection surfaces

The stable v1 inspection chain used throughout OrbitFabric is:

```text
model_summary.json
entity_index.json
relationship_manifest.json
```

Generate it with:

```bash
orbitfabric export model-summary mission/ \
  --json generated/reports/model_summary.json

orbitfabric export entity-index mission/ \
  --json generated/reports/entity_index.json

orbitfabric export relationship-manifest mission/ \
  --json generated/reports/relationship_manifest.json
```

### Model summary

`model_summary.json` provides a compact inventory of the loaded mission model.

For this Reference Mission, the modeled areas include spacecraft identity, seven subsystems, seven modes, telemetry, commands, events, faults, packets, payload, data products, contacts, downlink flow, commandability, autonomous action and recovery intent.

The exact generated counts should be rechecked during the final Core command-validation pass rather than copied manually into the tutorial as an immutable claim.

### Entity index

`entity_index.json` is the machine-readable catalog of domain-qualified mission entities.

It supports questions such as:

```text
Which commands exist?
Which telemetry items exist?
Which faults exist?
Which entities belong to each domain?
```

This surface is especially important for downstream navigation and Studio entity identity.

### Relationship manifest

`relationship_manifest.json` records explicit or deterministically derived relationship records between model entities.

The original v1 relationship families remain compatibility-sensitive.

Current post-v1.1 Core development adds seven explicit FDIR relationship families:

```text
autonomous_action_triggered_by_fault
autonomous_action_uses_command_source
fault_observes_telemetry
fault_recovery_dispatches_command
fault_recovery_targets_mode
recovery_intent_includes_command
recovery_intent_targets_mode
```

These additions are additive. They do not turn the manifest into an inferred graph engine and they do not authorize downstream tools to invent missing semantics.

For this Reference Mission, the FDIR additions make low-power and degraded-pointing protection context much more useful to Studio without private UI heuristics.

## Mission Snapshot

Current post-v1.1 Core development also provides a candidate Mission Snapshot surface:

```text
generated/reports/mission_snapshot.json
```

Generate it with a Core revision that includes the feature:

```bash
orbitfabric export mission-snapshot mission/ \
  --json generated/reports/mission_snapshot.json
```

Mission Snapshot is a versioned read-only envelope around the complete loaded `MissionModel`.

It is useful when a downstream consumer needs the full loaded semantic model rather than a summary or index.

It is not:

- a YAML syntax tree;
- a source editor representation;
- a second source of truth;
- a Studio-specific API.

Studio Preview 1 consumes Mission Snapshot as one of its Core-owned hydration surfaces.

## Scenario reports and logs

Scenario execution produces two complementary evidence forms:

| Artifact | Role |
|---|---|
| Simulation JSON report | Machine-readable scenario evidence. |
| Plain-text log | Human-readable deterministic scenario timeline. |

Run the four Reference Mission scenarios with explicit outputs:

```bash
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
```

Simulation JSON should be preferred for machine indexing and downstream evidence processing. Plain-text logs remain valuable during human review.

## Runtime-facing artifacts

Generate runtime-facing contract artifacts with:

```bash
orbitfabric gen runtime mission/
```

The current profile is C++17.

These outputs are contract-facing bindings for onboard software integration review. They are not flight software.

## Ground-facing artifacts

Generate ground-facing artifacts with:

```bash
orbitfabric gen ground mission/
```

The current generic profile produces contract-facing dictionaries, manifests and review artifacts.

These outputs can support downstream integration discussion. They are not a ground segment.

## v1.1 candidate integration surfaces

The published v1.1 candidate integration layer includes:

```text
dashboard_summary.json
scenario_run_index.json
coverage_summary.json
```

Generate them with a Core version that includes the v1.1 candidate surfaces:

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

These surfaces remain Core-owned downstream foundations.

Studio Preview 1 does not currently use this dashboard/index/coverage trio as its documented hydration contract. Its current inputs are Mission Snapshot, Entity Index, Relationship Manifest and lint JSON.

That distinction avoids turning every Core candidate surface into an implied Studio feature.

## What generated artifacts are not

Generated artifacts are not:

- the mission source of truth;
- hand-authored tutorial content;
- a replacement for `mission/*.yaml`;
- a replacement for `scenarios/*.yaml`;
- a guarantee of flight behavior;
- a runtime implementation;
- a ground segment;
- mission control;
- a Studio semantic layer.

They are derived evidence and integration surfaces.

## Why this step matters

Generated artifacts close the loop between model and review:

```text
model source
-> generated documentation
-> machine-readable reports
-> scenario evidence
-> runtime-facing bindings
-> ground-facing artifacts
-> Core-owned downstream surfaces
-> Studio exploration
```

This is the practical meaning of a model-first mission data fabric.

## Modeling rule introduced in this step

The seventeenth rule is:

```text
Treat generated artifacts as reproducible evidence, not as source material.
```

If generated content disagrees with the mission model, fix the model or the generator. Do not manually edit generated output to make the tutorial look right.

## What comes next

The next tutorial step focuses on scenario evidence and explains how to read simulation JSON reports and human-readable logs together.
