# 04, Operational Modes

Status: tutorial draft  
Scope: fourth step of the progressive Reference Mission tutorial

## Purpose

This step introduces operational modes.

After defining the spacecraft identity and subsystem topology, the next question is:

```text
Which spacecraft postures matter for the mission contract?
```

Modes are not just software labels. In this tutorial, modes describe the operational posture of the spacecraft: what kind of activity is allowed, constrained or expected.

In the Reference Mission, modes are defined in:

```text
mission/modes.yaml
```

## Operational reason

The same command or telemetry value can have different meaning depending on the spacecraft mode.

For example, payload activity is expected in `PAYLOAD_ACTIVE`, but not in `SAFE`. S-band activity is expected in `DOWNLINK`, but not in normal payload acquisition. A power constraint can move the spacecraft out of a science posture and into a reduced-power posture.

Modes therefore give the mission contract a controlled vocabulary for spacecraft behavior.

## Current modes

The current Reference Mission defines seven modes:

| Mode | Tutorial meaning |
|---|---|
| `STANDBY` | Initial post-boot operational mode before nominal mission activities are enabled. |
| `NOMINAL` | Standard operating posture with housekeeping, beaconing and monitoring active. |
| `PAYLOAD_ACTIVE` | Science acquisition posture where the radiation payload is enabled. |
| `DOWNLINK` | Contact-oriented posture where stored telemetry and science products are downlinked. |
| `DEGRADED_POWER` | Reduced-power posture entered after low battery or constrained energy conditions. |
| `ADCS_DEGRADED` | Reduced pointing capability posture where payload acquisition may be inhibited. |
| `SAFE` | Survival-oriented posture with payload acquisition disabled and only essential telemetry active. |

The initial mode is:

```text
STANDBY
```

This means the model starts from a controlled post-boot posture before nominal mission activities are enabled.

## Mode transitions

The model also defines the main transitions between modes.

| From | To | Reason |
|---|---|---|
| `STANDBY` | `NOMINAL` | `commissioning_health_check_passed` |
| `NOMINAL` | `PAYLOAD_ACTIVE` | `payload_acquisition_command_accepted` |
| `PAYLOAD_ACTIVE` | `NOMINAL` | `payload_acquisition_completed` |
| `PAYLOAD_ACTIVE` | `DEGRADED_POWER` | `low_power_threshold_reached` |
| `NOMINAL` | `DOWNLINK` | `sband_contact_window_started` |
| `DOWNLINK` | `NOMINAL` | `sband_contact_window_ended` |
| `PAYLOAD_ACTIVE` | `ADCS_DEGRADED` | `pointing_not_ready` |
| `NOMINAL` | `SAFE` | `critical_fault_detected` |

These transitions are intentionally limited.

They are the transitions needed to explain the first Reference Mission scenarios, not a complete spacecraft mode table.

## Why modes are introduced now

Modes are introduced before telemetry, commands and faults because they provide context.

Later tutorial steps will use modes to explain:

- where a command is allowed;
- when a payload activity is expected;
- why a fault changes the spacecraft posture;
- why a downlink activity is treated differently from nominal operations;
- why protective behavior matters during constrained conditions.

Without modes, the model could list commands and telemetry, but it could not explain operational posture.

## What is deliberately not modeled yet

This step does not introduce:

- detailed onboard state machines;
- scheduling logic;
- flight-software tasks;
- transition guards implemented in code;
- full FDIR design;
- operator procedures.

Those are implementation or operations details.

The Reference Mission only needs the mode vocabulary required by the contract and by the initial scenarios.

## Modeling rule introduced in this step

The fourth rule is:

```text
Use modes to describe spacecraft posture, not implementation internals.
```

A mode should help explain what the spacecraft is doing and why a behavior is valid or constrained.

## What comes next

The next step introduces the telemetry contract.

Telemetry will make the mode transitions and operational conditions observable.
