# 09, Payload Lifecycle

Status: tutorial draft  
Scope: ninth step of the progressive Reference Mission tutorial

## Purpose

This step introduces the payload lifecycle.

After defining telemetry, commands, events and faults, the next question is:

```text
How does the mission describe the operational state of the science payload?
```

The payload lifecycle gives the Reference Mission a compact vocabulary for science activity.

In the Reference Mission, the payload contract is defined in:

```text
mission/payloads.yaml
```

## Operational reason

The science payload is not just another subsystem.

It is the primary source of mission value in the current Reference Mission. It produces science telemetry, accepts payload commands, generates science events, can produce a histogram product and can be interrupted by operational constraints.

The lifecycle makes that behavior explicit.

Without a lifecycle, the model could show individual telemetry values and commands, but it would not clearly explain the payload's operational progression.

## Current payload

The current Reference Mission defines one payload:

| Payload | Connected subsystem | Profile | Tutorial role |
|---|---|---|---|
| `radiation_event_payload` | `radiation_payload` | `iod` | NanoSiPM-like radiation event payload used as the main science source. |

The payload is intentionally singular at this stage.

The tutorial should first make one payload contract understandable before introducing additional payloads or higher-volume science products.

## Lifecycle states

The current payload lifecycle defines six states:

| State | Tutorial meaning |
|---|---|
| `OFF` | Payload is not active. This is the initial lifecycle state. |
| `READY` | Payload is available for future acquisition. |
| `ACQUIRING` | Payload acquisition is active. |
| `HISTOGRAM_READY` | A science histogram product has been generated. |
| `DOWNLINK_PENDING` | Payload data is waiting for downlink handling. |
| `FAULT` | Payload is in a fault-related condition. |

The initial lifecycle state is:

```text
OFF
```

This is different from spacecraft mode.

The spacecraft may be in `NOMINAL`, while the payload lifecycle may be `READY` or `ACQUIRING` depending on payload activity.

## Payload-linked telemetry

The payload contract explicitly lists the telemetry it produces:

```text
radiation_payload.acquisition_active
radiation_payload.event_rate
radiation_payload.histogram_ready
radiation_payload.histogram_pending_bytes
```

These telemetry items make the lifecycle observable.

For example, `radiation_payload.acquisition_active` supports the distinction between ready and active acquisition behavior.

`radiation_payload.histogram_ready` supports the transition toward histogram-ready evidence.

`radiation_payload.histogram_pending_bytes` supports later backlog and downlink reasoning.

## Payload-linked commands

The payload accepts three commands:

```text
payload.start_acquisition
payload.stop_acquisition
payload.request_histogram
```

These commands drive the operational lifecycle:

| Command | Lifecycle role |
|---|---|
| `payload.start_acquisition` | Moves the payload toward active acquisition. |
| `payload.stop_acquisition` | Stops acquisition and returns the payload to a ready state. |
| `payload.request_histogram` | Requests generation of the histogram science product. |

The key rule from the command step still applies:

```text
Payload commands control payload state.
Fault and recovery logic controls spacecraft posture.
```

## Payload-linked events

The payload contract also lists the events it can generate:

```text
payload.acquisition_started
payload.acquisition_completed
payload.histogram_generated
payload.radiation_burst_detected
payload.acquisition_suspended
```

These events make payload progress visible in scenario evidence.

The payload lifecycle is therefore not hidden inside an implementation. It is visible through events and telemetry.

## Payload-linked fault

The current payload has one possible fault:

```text
payload.timeout
```

This fault represents a case where payload acquisition does not complete within the expected operational window.

It connects payload activity to protective behavior without requiring the tutorial to define a full onboard payload manager.

## Lifecycle versus spacecraft modes

Payload lifecycle and spacecraft modes are related, but they are not the same thing.

Spacecraft mode describes the posture of the spacecraft:

```text
NOMINAL
PAYLOAD_ACTIVE
DEGRADED_POWER
ADCS_DEGRADED
SAFE
```

Payload lifecycle describes the state of the payload activity:

```text
READY
ACQUIRING
HISTOGRAM_READY
DOWNLINK_PENDING
FAULT
```

Keeping them separate is essential.

A spacecraft can enter a degraded mode because of EPS or ADCS constraints while the payload lifecycle is moved back to `READY` by `payload.stop_acquisition`.

That separation preserves operational meaning.

## What is deliberately not modeled yet

This payload lifecycle does not define:

- payload firmware internals;
- detector electronics;
- SPI framing;
- binary histogram format;
- acquisition algorithms;
- calibration processing;
- science validation logic;
- detailed downlink scheduling.

Those are implementation or later data-product concerns.

At this stage, the Reference Mission only defines the mission-level lifecycle of the science payload.

## Link to later model areas

Later tutorial steps will use the payload lifecycle to explain:

- science data product generation;
- storage and downlink intent;
- nominal acquisition scenario evidence;
- low-power payload suspension;
- ADCS degraded payload inhibit;
- delayed downlink and backlog behavior.

The payload lifecycle is the bridge between mission operations and science data production.

## Modeling rule introduced in this step

The ninth rule is:

```text
Use payload lifecycle states to expose science activity at mission-contract level.
```

Do not hide payload state inside implementation details.

Expose only the states needed to explain commands, telemetry, events, faults and scenario evidence.

## What comes next

The next step introduces data products and storage.

That step will explain how generated science output becomes a contract-level object that can be stored, prioritized and prepared for downlink.
