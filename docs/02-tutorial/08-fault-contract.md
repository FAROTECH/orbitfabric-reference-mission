# 08, Fault Contract

Status: tutorial draft  
Scope: eighth step of the progressive Reference Mission tutorial

## Purpose

This step introduces the fault contract.

After telemetry, commands and events, the next question is:

```text
Which conditions require degraded behavior, recovery intent or protective action?
```

Faults are not just warning messages. A fault connects an observable condition to an operational response.

In the Reference Mission, faults are defined in:

```text
mission/faults.yaml
```

## Operational reason

Telemetry can show a value. Events can record a milestone. Faults explain when a condition becomes operationally significant enough to require a response.

A fault connects:

```text
condition
-> emitted event
-> recovery intent
-> optional automatic command
```

This is the first point in the tutorial where protective behavior becomes explicit.

## Current fault set

The current Reference Mission defines five faults:

| Fault | Source | Severity | Tutorial role |
|---|---|---|---|
| `eps.battery_critical` | `eps` | `critical` | Critical battery condition leading to `SAFE`. |
| `eps.low_battery_warning` | `eps` | `warning` | Low-power warning leading to `DEGRADED_POWER`. |
| `adcs.control_degraded` | `adcs` | `warning` | Pointing not suitable for payload acquisition, leading to `ADCS_DEGRADED`. |
| `payload.timeout` | `radiation_payload` | `error` | Payload acquisition did not complete within the expected window. |
| `data_storage.near_full` | `data_storage` | `warning` | Storage usage above warning threshold. |

This set is intentionally compact.

It is enough to exercise power protection, pointing constraints, payload timeout behavior and storage-pressure evidence.

## What each fault declares

Each fault can declare several contract-level properties:

| Property | Role |
|---|---|
| `id` | Stable machine-readable fault identifier. |
| `source` | Subsystem associated with the fault. |
| `severity` | Operational severity of the condition. |
| `description` | Human-readable explanation. |
| `condition` | Telemetry or event condition that triggers the fault. |
| `emits` | Event or events emitted when the fault is raised. |
| `recovery` | Intended operational response. |
| `mode_transition` | Mode transition associated with recovery intent. |
| `auto_commands` | Commands automatically dispatched as part of recovery. |

The important point is that the fault contract links detection, evidence and response.

## Telemetry-based faults

Most current faults are based on telemetry conditions.

Example:

```text
eps.battery.state_of_charge < 30.0
```

This condition raises the low-battery warning fault after debounce and leads to a degraded-power posture.

Another example:

```text
adcs.pointing_status != NOMINAL
```

This condition raises the ADCS degraded fault and inhibits payload-oriented behavior.

## Debounce

Several faults use:

```text
debounce_samples: 2
```

This means the condition must persist for two samples before the fault is considered active.

That matters because the tutorial should not treat every single telemetry fluctuation as a mission-level fault.

Debounce makes the model more realistic without turning it into a full flight-software implementation.

## Recovery intent

Each fault can declare a recovery intent.

For example:

| Fault | Recovery mode | Automatic command |
|---|---|---|
| `eps.battery_critical` | `SAFE` | `payload.stop_acquisition` |
| `eps.low_battery_warning` | `DEGRADED_POWER` | `payload.stop_acquisition` |
| `adcs.control_degraded` | `ADCS_DEGRADED` | `payload.stop_acquisition` |
| `payload.timeout` | `NOMINAL` | `payload.stop_acquisition` |
| `data_storage.near_full` | `NOMINAL` | none |

This does not mean the model implements a full FDIR system.

It means the mission contract exposes the expected recovery posture and the automatic actions that scenario evidence can inspect.

## Why fault recovery is separate from command effects

This distinction is critical.

A command such as `payload.stop_acquisition` should stop the payload and update payload evidence.

It should not decide the spacecraft recovery mode.

The fault decides the recovery posture:

```text
low battery fault -> DEGRADED_POWER
ADCS degraded fault -> ADCS_DEGRADED
battery critical fault -> SAFE
```

The command performs the local action:

```text
payload.stop_acquisition -> payload no longer acquiring
```

This separation prevents degraded scenarios from being incorrectly collapsed back into nominal behavior.

## Faults versus events

Faults and events must remain separate.

Events record operational milestones or warning evidence.

Faults define conditions that require recovery intent or protective behavior.

For example:

```text
eps.low_power_warning_raised
```

is an event.

```text
eps.low_battery_warning
```

is a fault.

The event is evidence. The fault is the model-level condition that carries recovery intent.

## What is deliberately not modeled yet

This fault contract does not define:

- complete FDIR design;
- voting logic;
- redundancy management;
- detailed recovery scripts;
- operator escalation procedures;
- implementation-level watchdog behavior;
- hardware-specific reset lines.

Those are outside the current tutorial step.

At this stage, the Reference Mission only defines contract-level fault semantics.

## Link to later model areas

Later tutorial steps will use faults to explain:

- payload lifecycle interruption;
- commandability constraints;
- autonomous command dispatch;
- low-power degraded scenario evidence;
- ADCS degraded scenario evidence;
- future Studio navigation from event to fault to recovery.

Faults are where the mission contract starts to show protective behavior.

## Modeling rule introduced in this step

The eighth rule is:

```text
Use faults to connect observable conditions to recovery intent.
```

Do not use faults as generic log messages.

A fault should explain why the spacecraft changes posture, dispatches an automatic command or records degraded behavior.

## What comes next

The next step introduces the payload lifecycle.

The payload lifecycle will show how science activity moves between ready, acquiring, histogram-ready and interrupted states.
