# 07, Event Contract

Status: tutorial draft  
Scope: seventh step of the progressive Reference Mission tutorial

## Purpose

This step introduces the event contract.

After defining telemetry and commands, the next question is:

```text
How does the mission make operational milestones visible?
```

Events are the narrative evidence of the mission contract. They mark that something relevant happened: a command completed, a mode changed, a payload activity started, a warning condition appeared or a downlink activity progressed.

In the Reference Mission, events are defined in:

```text
mission/events.yaml
```

## Operational reason

Telemetry describes values. Commands describe requested actions. Events describe operational facts.

A scenario is much easier to understand when it can show a timeline such as:

```text
payload acquisition started
histogram generated
S-band contact started
S-band downlink completed
```

This makes events different from telemetry.

A telemetry item may say that a value is true or above a threshold. An event says that a relevant operational milestone has occurred and should be recorded as evidence.

## Current event set

The current Reference Mission defines thirteen events:

| Event | Source | Severity | Tutorial role |
|---|---|---|---|
| `obc.health_check_completed` | `obc` | `info` | Marks successful health-check completion. |
| `obc.mode_changed` | `obc` | `info` | Marks spacecraft operational mode change. |
| `payload.acquisition_started` | `radiation_payload` | `info` | Marks start of payload acquisition. |
| `payload.acquisition_completed` | `radiation_payload` | `info` | Marks completion of payload acquisition. |
| `payload.histogram_generated` | `radiation_payload` | `info` | Marks generation of a science histogram product. |
| `payload.radiation_burst_detected` | `radiation_payload` | `warning` | Marks a high event-rate science condition. |
| `eps.low_power_warning_raised` | `eps` | `warning` | Marks low-power warning threshold crossing. |
| `payload.acquisition_suspended` | `radiation_payload` | `warning` | Marks suspension of payload acquisition due to a constraint. |
| `adcs.pointing_degraded` | `adcs` | `warning` | Marks degraded or not-ready pointing state. |
| `comms.sband_contact_started` | `sband_radio` | `info` | Marks start of scheduled S-band contact. |
| `comms.sband_downlink_started` | `sband_radio` | `info` | Marks start of S-band science downlink. |
| `comms.sband_downlink_completed` | `sband_radio` | `info` | Marks completion of S-band science downlink. |
| `storage.near_full` | `data_storage` | `warning` | Marks storage usage above warning threshold. |

This set is intentionally compact.

It focuses on events that are useful in the first operational scenarios and in later Studio-style evidence navigation.

## What each event declares

Each event declares a small contract-level surface:

| Property | Role |
|---|---|
| `id` | Stable machine-readable event identifier. |
| `source` | Subsystem that emits or owns the event. |
| `severity` | Event severity category. |
| `description` | Human-readable operational meaning. |
| `downlink_priority` | Relative priority for downlink handling. |
| `persistence` | Whether the event should be stored and downlinked. |

This is enough for the event to appear in generated documentation, scenario traces and future navigation surfaces.

## Events versus telemetry

Events and telemetry must stay separate.

Telemetry answers:

```text
What value or state is being observed?
```

Events answer:

```text
What operational milestone or condition was recorded?
```

For example, `eps.battery.state_of_charge` is telemetry. `eps.low_power_warning_raised` is an event.

The telemetry value can explain the condition. The event records that the condition mattered operationally.

## Events versus commands

Events and commands must also stay separate.

A command is a requested action. An event is evidence that something happened.

For example, `payload.request_histogram` is a command. `payload.histogram_generated` is an event.

The command expresses intent. The event records the outcome that the scenario can later inspect.

## Why severity matters

Severity gives the model a lightweight operational signal.

The current Reference Mission uses:

| Severity | Meaning in this tutorial |
|---|---|
| `info` | Normal operational milestone or expected progress. |
| `warning` | Operational condition that deserves attention but does not by itself define full recovery behavior. |

Critical recovery behavior will be introduced in the fault contract, not overloaded into events.

This separation is deliberate.

## What is deliberately not modeled yet

This event contract does not define:

- binary event packet formats;
- ground alarm rules;
- notification routing;
- operator acknowledgement workflow;
- full incident management;
- full FDIR implementation.

Those are implementation or operations details.

At this stage, events are model-level evidence markers.

## Link to later model areas

Later tutorial steps will use events to explain:

- fault triggers and recovery intent;
- payload lifecycle transitions;
- data product generation;
- downlink scenario evidence;
- scenario timeline readability;
- future Studio navigation.

Events are the bridge between model behavior and human-readable mission evidence.

## Modeling rule introduced in this step

The seventh rule is:

```text
Use events to record operational milestones, not to hide recovery logic.
```

Do not turn every telemetry change into an event.

Add events when a scenario, generated evidence surface or future review path needs to show that something operationally relevant happened.

## What comes next

The next step introduces faults.

Faults will define conditions that require recovery intent, degraded behavior or protective action.
