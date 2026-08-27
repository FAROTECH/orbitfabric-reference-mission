# 05, Telemetry Contract

Status: tutorial draft  
Scope: fifth step of the progressive Reference Mission tutorial

## Purpose

This step introduces the telemetry contract.

After defining spacecraft identity, subsystem topology and operational modes, the next question is:

```text
What does the mission need to observe in order to explain behavior?
```

Telemetry is the observable side of the mission contract. It turns subsystem state, payload activity, storage pressure and communication posture into named model elements.

In the Reference Mission, telemetry is defined in:

```text
mission/telemetry.yaml
```

## Operational reason

Telemetry exists because the mission needs evidence.

A mode transition is not enough by itself. The model must also expose the values that explain why a transition or operational outcome happened.

For example:

- EPS telemetry explains low-power behavior.
- ADCS telemetry explains pointing constraints.
- Payload telemetry explains acquisition and science data generation.
- Storage telemetry explains backlog and persistence pressure.
- Radio telemetry explains communication posture.

Telemetry is therefore not just a list of measurements. It is the observable basis for operational reasoning.

## Current telemetry domains

The current Reference Mission defines telemetry across six domains:

| Domain | Telemetry examples | Why it matters |
|---|---|---|
| EPS | `eps.battery.voltage`, `eps.battery.state_of_charge`, `eps.solar.input_power` | Explains power margin and low-power conditions. |
| OBC | `obc.cpu_load`, `obc.watchdog_reset_counter` | Provides coarse onboard computer health evidence. |
| Storage | `data_storage.used_percent` | Explains storage pressure and backlog context. |
| ADCS | `adcs.pointing_status`, `adcs.angular_rate` | Explains pointing readiness and payload constraints. |
| Communications | `uhf_radio.beacon_state`, `sband_radio.link_state` | Explains beacon and downlink posture. |
| Payload | `radiation_payload.acquisition_active`, `radiation_payload.event_rate`, `radiation_payload.histogram_ready`, `radiation_payload.histogram_pending_bytes` | Explains science acquisition, histogram generation and pending data. |

This set is intentionally compact.

It contains enough telemetry to support the first operational scenarios without turning the Reference Mission into a full spacecraft telemetry database.

## What each telemetry item declares

Each telemetry item can declare several contract-level properties:

| Property | Role |
|---|---|
| `id` | Stable machine-readable telemetry identifier. |
| `name` | Human-readable name. |
| `type` | Data type expected by the contract. |
| `unit` | Engineering unit or state category. |
| `source` | Subsystem that produces the telemetry. |
| `sampling` | Nominal observation cadence. |
| `criticality` | Operational importance of the item. |
| `persistence` | Whether and how the item is stored or downlinked. |
| `downlink_priority` | Relative priority for downlink handling. |
| `quality` | Basic quality expectation. |
| `limits` | Warning or critical thresholds, where applicable. |
| `enum` | Allowed state values, where applicable. |
| `description` | Human-readable operational meaning. |

The important point is that telemetry is not only a signal name. It carries enough metadata to be validated, documented and later explored.

## Example: power telemetry

The EPS telemetry items are critical because they explain constrained-energy behavior.

The battery state of charge telemetry includes warning and critical lower limits. This makes the low-power scenario explainable from the model instead of relying only on narrative text.

The model can therefore connect:

```text
battery state of charge
-> low-power condition
-> degraded-power posture
-> payload activity suspended
```

This is the kind of chain the tutorial will exercise later through scenarios.

## Example: payload telemetry

The radiation payload telemetry explains the science activity:

- whether acquisition is active;
- what event rate is being observed;
- whether a histogram is ready;
- how many histogram bytes are pending for downlink.

This supports both nominal science acquisition and delayed downlink reasoning.

A science product is not only generated. It also leaves observable evidence in the telemetry contract.

## What is deliberately not modeled yet

This telemetry contract does not define:

- binary packet layouts;
- sensor drivers;
- ADC conversion details;
- calibration models;
- database schema;
- ground ingestion implementation;
- alerting UI behavior.

Those are implementation concerns.

At this stage, the Reference Mission only defines the observable mission-level contract.

## Link to later model areas

Later tutorial steps will use telemetry to explain:

- command effects;
- event generation;
- fault thresholds;
- payload lifecycle state;
- data product generation;
- backlog and downlink expectations;
- scenario evidence.

Telemetry is the first place where the model becomes measurably connected to behavior.

## Modeling rule introduced in this step

The fifth rule is:

```text
Telemetry exists because an operational question needs observable evidence.
```

Do not add telemetry only because a real spacecraft could measure it.

Add telemetry when the mission contract needs it to explain behavior, validate an expectation or produce useful evidence.

## What comes next

The next step introduces the command contract.

Commands will define how ground operations and onboard logic request changes in spacecraft or payload behavior.
