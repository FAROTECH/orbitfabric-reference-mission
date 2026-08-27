# 03, Subsystem Topology

Status: tutorial draft  
Scope: third step of the progressive Reference Mission tutorial

## Purpose

This step introduces the spacecraft subsystem topology.

After defining the spacecraft identity, the next question is:

```text
Which onboard elements participate in the mission contract?
```

The answer is not a full spacecraft architecture. It is the minimum subsystem set needed to explain the first operational scenarios.

In the Reference Mission, the topology is defined in:

```text
mission/subsystems.yaml
```

## Operational reason

A mission data contract must connect behavior to responsible elements.

Telemetry needs a source. Commands need a target. Events need an origin. Faults need a subsystem context. Data products need producers and storage assumptions.

Without subsystem topology, the model would only contain disconnected names.

The topology turns the spacecraft identity into a set of operational participants.

## Current subsystem set

The current Reference Mission defines seven subsystem-level elements:

| Subsystem | Role in the tutorial |
|---|---|
| `obc` | Coordinates mission operations, command handling, supervision and evidence storage. |
| `eps` | Provides power state, battery telemetry and low-power constraints. |
| `adcs` | Provides pointing state and payload acquisition readiness. |
| `uhf_radio` | Provides low-rate beacon and housekeeping downlink. |
| `sband_radio` | Provides higher-rate science downlink during scheduled contacts. |
| `radiation_payload` | Produces radiation event-rate telemetry and histogram data products. |
| `data_storage` | Stores science, housekeeping and evidence-oriented products before downlink. |

This set is intentionally compact.

It is large enough to exercise meaningful cross-subsystem behavior, but small enough to remain teachable.

## Why these subsystems exist

Each subsystem exists because at least one early scenario needs it.

| Subsystem | Scenario pressure |
|---|---|
| `obc` | Needed to coordinate commands, mode changes and evidence. |
| `eps` | Needed to explain low-power behavior and payload suspension. |
| `adcs` | Needed to explain pointing constraints on payload acquisition. |
| `uhf_radio` | Needed for essential low-rate communication assumptions. |
| `sband_radio` | Needed for science downlink assumptions. |
| `radiation_payload` | Needed as the main science source. |
| `data_storage` | Needed to explain backlog, persistence and deferred downlink. |

This is the main modeling point of this step:

```text
A subsystem is introduced when mission behavior needs an accountable source, target or constraint.
```

## What is deliberately not modeled yet

The topology does not yet describe:

- electrical interfaces;
- bus protocols;
- physical harnessing;
- processor allocation;
- task layout;
- packet binary formats;
- RF implementation details;
- storage filesystem details.

Those details may matter in a real spacecraft project, but they are not needed for this Reference Mission step.

OrbitFabric is modeling the mission contract, not the implementation wiring.

## Link to later model areas

This topology will be used by later tutorial steps:

- telemetry items will reference subsystem sources;
- commands will target subsystem elements;
- events will be emitted by subsystem sources;
- faults will be attached to subsystem contexts;
- payload contracts will connect to the payload subsystem;
- data products will identify producers and storage intent.

The topology therefore acts as a semantic backbone for the rest of the mission contract.

## Modeling rule introduced in this step

The third rule is:

```text
Introduce subsystems only when they explain mission behavior.
```

Subsystems are not inventory items. They are operational participants.

## What comes next

The next step introduces operational modes.

Modes describe the spacecraft posture in which these subsystem interactions become meaningful.
