# 02, Spacecraft Identity

Status: tutorial draft  
Scope: second step of the progressive Reference Mission tutorial

## Purpose

This step introduces the smallest stable anchor of the mission contract: the spacecraft identity.

Before adding subsystems, telemetry, commands or scenarios, the model needs one top-level mission object that every later element can belong to.

In the Reference Mission, this anchor is defined in:

```text
mission/spacecraft.yaml
```

## Operational reason

The spacecraft identity answers the first basic question:

```text
Which mission model are we talking about?
```

This matters because every later contract element must be interpreted inside a specific mission boundary.

A telemetry item is not just a generic signal. A command is not just a generic operation. A scenario is not just a script.

They all belong to one mission model.

## Current model fragment

The current Reference Mission identity is:

```yaml
spacecraft:
  id: of-rm-1
  name: OrbitFabric Reference Mission 1
  class: cubesat
  form_factor: 3U
  mission_type: scientific_technology_demonstrator
  model_version: 0.1.0-reference-skeleton
```

This is intentionally compact.

At this stage, the purpose is not to describe the whole spacecraft. The purpose is to establish a stable root for the model.

## Field meaning

| Field | Meaning in this tutorial |
|---|---|
| `id` | Stable machine-readable mission identifier. |
| `name` | Human-readable mission name. |
| `class` | Broad spacecraft class. |
| `form_factor` | Compact physical category for tutorial context. |
| `mission_type` | High-level operational intent. |
| `model_version` | Version of this Reference Mission model baseline. |

## Why not add more yet

A real spacecraft project could track many more details: orbit assumptions, mass properties, deployables, platform variants, supplier data and mission-specific constraints.

Those details are deliberately not introduced here.

The tutorial only adds detail when an operational scenario needs it.

That keeps the model teachable and prevents the first step from becoming a static spacecraft database.

## Modeling rule introduced in this step

The second rule is:

```text
Start with a stable mission anchor, then add only the elements needed by behavior.
```

The spacecraft identity is not the mission design. It is the root of the mission contract.

## What comes next

The next step introduces subsystem topology.

That is where the spacecraft identity becomes operationally useful, because the mission begins to expose the onboard elements that will produce telemetry, accept commands and participate in scenarios.
