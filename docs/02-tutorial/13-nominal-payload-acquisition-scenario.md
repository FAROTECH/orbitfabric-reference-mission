# 13, Nominal Payload Acquisition Scenario

Status: tutorial draft  
Scope: first scenario walkthrough of the progressive Reference Mission tutorial

## Purpose

This step introduces the first executable scenario walkthrough.

The previous tutorial steps built the mission contract incrementally: spacecraft identity, subsystems, modes, telemetry, commands, events, faults, payload lifecycle, data products, contact assumptions and commandability.

This scenario shows those pieces working together in a nominal operational flow.

The scenario is defined in:

```text
scenarios/nominal_payload_acquisition.yaml
```

## Scenario intent

The scenario answers one operational question:

```text
Can the Reference Mission describe a nominal payload acquisition, generate a science product, make that product eligible for downlink, and complete a representative S-band downlink flow?
```

This is the first end-to-end evidence path in the tutorial.

It connects science activity to product generation and product downlink.

## Scenario summary

The scenario performs this high-level sequence:

```text
NOMINAL mode
-> ground starts payload acquisition
-> payload becomes active
-> event-rate telemetry is observed
-> histogram is requested
-> histogram product is generated
-> product becomes eligible for science_priority_flow
-> S-band contact starts
-> downlink starts
-> spacecraft enters DOWNLINK
-> science product is associated with the contact window
-> downlink completes
-> spacecraft returns to NOMINAL
```

This is deliberately a nominal path.

No fault recovery or onboard protective action is expected in this scenario.

## Initial state

The scenario starts in:

```text
mode: NOMINAL
```

The initial telemetry is healthy and consistent with nominal payload acquisition:

| Telemetry | Initial value | Meaning |
|---|---:|---|
| `eps.battery.voltage` | `8.1` | Battery voltage is healthy. |
| `eps.battery.state_of_charge` | `72.0` | Battery state of charge is comfortably above payload-start threshold. |
| `eps.solar.input_power` | `4.5` | Solar input power is available. |
| `adcs.pointing_status` | `NOMINAL` | ADCS is suitable for payload acquisition. |
| `adcs.angular_rate` | `0.2` | Angular rate is low. |
| `sband_radio.link_state` | `IDLE` | S-band is not yet active. |
| `radiation_payload.acquisition_active` | `false` | Payload acquisition has not started. |
| `radiation_payload.event_rate` | `0.0` | No current science event rate. |
| `radiation_payload.histogram_ready` | `false` | No histogram is ready yet. |
| `radiation_payload.histogram_pending_bytes` | `0` | No histogram backlog exists yet. |

The key point is that the scenario starts from a valid, non-degraded spacecraft posture.

## Step 1, verify nominal posture

At `t: 0`, the scenario expects:

```text
NOMINAL
```

This verifies that the scenario starts from the intended operational posture.

It is not enough for the mission to have a `NOMINAL` mode in the model. The scenario must begin from it explicitly.

## Step 2, start payload acquisition

At `t: 5`, the scenario sends:

```text
payload.start_acquisition
```

with:

```text
duration_s: 300
```

This uses the command contract and commandability model introduced earlier.

The command is meaningful because:

- the spacecraft is in `NOMINAL`;
- ADCS pointing is `NOMINAL`;
- battery state of charge is above the payload-start threshold;
- the command is a ground-driven payload acquisition request.

## Step 3, observe payload acquisition start

At `t: 6`, the scenario expects:

```text
payload.acquisition_started
```

At `t: 7`, it expects:

```text
PAYLOAD_ACTIVE
```

This connects command intent to scenario evidence:

```text
payload.start_acquisition
-> payload.acquisition_started
-> PAYLOAD_ACTIVE
```

The event records the operational milestone.

The mode change records the spacecraft posture.

## Step 4, observe science activity

The scenario then injects payload telemetry:

```text
radiation_payload.acquisition_active: true
radiation_payload.event_rate: 42.0
```

This makes the payload activity observable.

The scenario is not modeling detector physics. It is showing that the mission contract can represent active science acquisition and a representative event rate.

## Step 5, request histogram generation

At `t: 60`, the scenario sends:

```text
payload.request_histogram
```

At `t: 62`, it expects:

```text
payload.histogram_generated
```

Then it injects:

```text
radiation_payload.histogram_ready: true
radiation_payload.histogram_pending_bytes: 4096
```

This connects payload lifecycle, telemetry and data-product intent:

```text
histogram requested
-> histogram generated event
-> histogram_ready true
-> pending bytes 4096
```

The value `4096` matches the estimated size of the `radiation_histogram` data product.

## Step 6, verify data flow eligibility

At `t: 70`, the scenario expects a data-flow relationship:

```text
data_product: radiation_histogram
triggered_by_command: payload.request_histogram
eligible_downlink_flow: science_priority_flow
```

This is the core OrbitFabric-style evidence in the nominal scenario.

The scenario is not merely checking that a command ran. It verifies that a science product is connected to a downlink flow.

The chain is:

```text
payload.request_histogram
-> radiation_histogram
-> science_priority_flow
```

## Step 7, mark S-band contact start

At `t: 1200`, the scenario sends:

```text
comms.mark_sband_contact_started
```

At `t: 1201`, it expects:

```text
comms.sband_contact_started
```

This connects the scenario to the contact model.

The important point is not pass prediction. The important point is that downlink activity is tied to an explicit contact assumption.

## Step 8, start S-band downlink

At `t: 1205`, the scenario sends:

```text
comms.start_sband_downlink
```

At `t: 1206`, it expects:

```text
comms.sband_downlink_started
```

At `t: 1207`, it expects:

```text
DOWNLINK
```

This connects the communication command to spacecraft posture:

```text
start S-band downlink
-> downlink started event
-> DOWNLINK mode
```

## Step 9, verify contact-window data flow

At `t: 1210`, the scenario expects:

```text
data_product: radiation_histogram
eligible_downlink_flow: science_priority_flow
contact_window: sband_window_001
```

This is the final product-flow check.

The science product is not just generated. It is associated with a downlink flow and a representative contact window.

That is the operational evidence this scenario is meant to demonstrate.

## Step 10, stop S-band downlink

At `t: 1500`, the scenario sends:

```text
comms.stop_sband_downlink
```

At `t: 1501`, it expects:

```text
comms.sband_downlink_completed
```

At `t: 1502`, it expects:

```text
NOMINAL
```

This closes the nominal scenario:

```text
DOWNLINK
-> downlink completed
-> NOMINAL
```

The spacecraft returns to the normal operational posture after the downlink opportunity.

## What this scenario proves

This scenario proves that the Reference Mission can connect:

- spacecraft mode;
- healthy initial telemetry;
- ground-commanded payload acquisition;
- payload acquisition evidence;
- science telemetry;
- histogram generation;
- science data product eligibility;
- S-band contact assumption;
- downlink command sequence;
- final return to nominal operations.

It is the first complete mission-data path in the tutorial.

## What this scenario does not prove

This scenario does not prove:

- fault handling;
- low-power recovery;
- ADCS degraded behavior;
- backlog persistence when downlink is delayed;
- RF link performance;
- real ground-station scheduling;
- payload physics;
- binary packet exchange;
- onboard software implementation.

Those are intentionally outside the nominal scenario.

They are handled by later scenarios or outside OrbitFabric's current scope.

## Modeling rule introduced in this step

The thirteenth rule is:

```text
A scenario should prove an operational relationship, not just execute a sequence.
```

The nominal scenario is useful because it links payload activity, data product generation and downlink eligibility into one readable evidence path.

## What comes next

The next scenario introduces low-power payload suspension.

That scenario will reuse the same mission contract, but it will exercise the degraded-power path and onboard protective behavior.
