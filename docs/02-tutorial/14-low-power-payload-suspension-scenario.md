# 14, Low-Power Payload Suspension Scenario

Status: tutorial draft  
Scope: second scenario walkthrough of the progressive Reference Mission tutorial

## Purpose

This step introduces the first degraded operational scenario.

The nominal scenario showed a clean payload acquisition and downlink path. This scenario shows what happens when an otherwise nominal payload activity is interrupted by a low-power condition.

The scenario is defined in:

```text
scenarios/eclipse_low_power_payload_suspension.yaml
```

The generated scenario log is available in the provided generated artifact set as:

```text
generated/logs/eclipse_low_power_payload_suspension.txt
```

## Scenario intent

The scenario answers one operational question:

```text
Can the Reference Mission explain how low-power evidence leads to degraded-power posture and autonomous payload suspension?
```

This is not a failure of the mission contract.

It is a positive test of protective behavior.

The mission should not keep science acquisition active when power margin is no longer acceptable.

## Scenario summary

The scenario performs this high-level sequence:

```text
NOMINAL mode
-> ground starts payload acquisition
-> payload becomes ACQUIRING
-> payload event-rate telemetry is observed
-> EPS state of charge drops below warning threshold twice
-> low-power warning event is raised
-> spacecraft transitions to DEGRADED_POWER
-> onboard autonomy dispatches payload.stop_acquisition
-> payload acquisition completes
-> acquisition_active becomes false
-> payload lifecycle returns to READY
-> scenario passes
```

This scenario exercises debounce, fault recovery and autonomous command dispatch.

## Initial state

The scenario starts in:

```text
mode: NOMINAL
```

The initial state is healthy enough to allow payload acquisition, but already power-constrained compared with the nominal scenario:

| Telemetry | Initial value | Meaning |
|---|---:|---|
| `eps.battery.voltage` | `7.6` | Battery voltage is acceptable but lower than in the nominal scenario. |
| `eps.battery.state_of_charge` | `42.0` | State of charge is above the payload-start threshold. |
| `eps.solar.input_power` | `0.3` | Solar input is low, consistent with eclipse or constrained generation. |
| `adcs.pointing_status` | `NOMINAL` | ADCS is suitable for payload acquisition. |
| `sband_radio.link_state` | `IDLE` | S-band is inactive. |
| `radiation_payload.acquisition_active` | `false` | Payload acquisition has not started yet. |
| `radiation_payload.histogram_ready` | `false` | No histogram is ready. |
| `radiation_payload.histogram_pending_bytes` | `0` | No histogram backlog exists. |

The key point is that the scenario begins in a valid payload-acquisition posture.

The low-power condition is introduced later.

## Step 1, start payload acquisition

At `t: 5`, the scenario sends:

```text
payload.start_acquisition
```

with:

```text
duration_s: 600
```

At `t: 6`, it expects:

```text
payload.acquisition_started
```

At `t: 7`, it expects:

```text
PAYLOAD_ACTIVE
```

At `t: 10`, it expects the payload lifecycle to be:

```text
ACQUIRING
```

This confirms that the scenario really starts with successful payload acquisition.

The low-power response is therefore tested during active science operations, not before them.

## Step 2, observe payload activity

At `t: 30`, the scenario injects:

```text
radiation_payload.event_rate: 35.0
```

This represents ongoing science activity.

The exact value is not the point. The point is that the payload is actively acquiring when the EPS condition changes.

## Step 3, inject first low state-of-charge sample

At `t: 120`, the scenario injects:

```text
eps.battery.state_of_charge: 28.0
```

This is below the warning threshold defined by the EPS low-battery fault.

However, the scenario then expects the spacecraft to remain in:

```text
PAYLOAD_ACTIVE
```

This is important.

A single low sample is not enough to trigger the fault because the fault contract uses debounce.

## Step 4, inject second low state-of-charge sample

At `t: 122`, the scenario injects:

```text
eps.battery.state_of_charge: 27.0
```

This is the second consecutive low sample.

The fault contract requires:

```text
debounce_samples: 2
```

At this point, the low-power condition becomes operationally significant.

## Step 5, observe low-power evidence

At `t: 123`, the scenario expects:

```text
eps.low_power_warning_raised
```

This is the event-level evidence that the EPS warning condition has been raised.

The generated log confirms this same milestone:

```text
[02:02] EVENT eps.low_power_warning_raised severity=WARNING
```

This event is evidence.

The recovery intent is carried by the fault and commandability model.

## Step 6, enter degraded-power posture

At `t: 124`, the scenario expects:

```text
DEGRADED_POWER
```

The generated log records the same operational transition:

```text
[02:02] MODE TRANSITION PAYLOAD_ACTIVE -> DEGRADED_POWER reason=eps.low_battery_warning
```

This is the central mode-level result of the scenario.

The spacecraft does not return to `NOMINAL` automatically. It enters a reduced-power posture.

## Step 7, auto-dispatch payload stop

At `t: 125`, the scenario expects an automatic command dispatch:

```text
payload.stop_acquisition
```

with:

```text
dispatch: AUTO
```

The generated log records:

```text
[02:02] COMMAND payload.stop_acquisition -> AUTO_DISPATCHED
```

This is the commandability and autonomy model in action.

The ground did not issue the stop command in this scenario.

Onboard autonomy dispatched it as part of protective behavior.

## Step 8, payload stops acquiring

At `t: 126`, the scenario expects:

```text
payload.acquisition_completed
```

At `t: 127`, it expects:

```text
radiation_payload.acquisition_active: false
```

At `t: 128`, it expects the payload lifecycle to be:

```text
READY
```

The generated log confirms the same sequence:

```text
[02:02] EVENT payload.acquisition_completed severity=INFO
[02:02] PAYLOAD radiation_event_payload LIFECYCLE=READY
[02:02] TELEMETRY radiation_payload.acquisition_active=false
```

This shows why separating fault recovery from command effects matters.

The fault moves the spacecraft to `DEGRADED_POWER`.

The auto-dispatched command stops the payload and returns the payload lifecycle to `READY`.

## Step 9, scenario passes

At `t: 129`, the scenario expects:

```text
scenario_status: PASSED
```

The generated log ends with:

```text
Result: PASSED
```

This confirms that the degraded behavior is expected and validated.

## What this scenario proves

This scenario proves that the Reference Mission can connect:

- payload acquisition start;
- payload lifecycle `ACQUIRING`;
- EPS low state-of-charge telemetry;
- debounce behavior across two low samples;
- low-power warning event;
- `PAYLOAD_ACTIVE -> DEGRADED_POWER` transition;
- onboard autonomous command dispatch;
- payload acquisition stop;
- `acquisition_active: false` telemetry;
- payload lifecycle return to `READY`;
- scenario pass status.

This is the first protective-behavior evidence path in the tutorial.

## What this scenario does not prove

This scenario does not prove:

- critical battery safe-mode transition;
- ADCS degraded behavior;
- payload timeout behavior;
- storage near-full behavior;
- science product downlink;
- RF or contact behavior;
- real onboard FDIR implementation.

Those remain separate concerns.

This scenario focuses only on low-power warning recovery during active payload acquisition.

## Why this scenario matters

The scenario validates a subtle but important design choice:

```text
fault recovery posture and payload command effects are separate.
```

The spacecraft enters `DEGRADED_POWER` because the EPS fault recovery intent says so.

The payload stops acquiring because onboard autonomy dispatches `payload.stop_acquisition`.

Those are related, but not the same operation.

That separation keeps the mission contract readable and prevents protective behavior from being hidden inside a generic command effect.

## Modeling rule introduced in this step

The fourteenth rule is:

```text
A degraded scenario should prove protective behavior without collapsing the mission back to nominal.
```

The expected outcome is not always a return to `NOMINAL`.

Sometimes the correct outcome is a clear degraded posture with safe payload state and preserved evidence.

## What comes next

The next scenario introduces ADCS degraded payload inhibit.

It will reuse the same separation between operational constraint, payload stop behavior and degraded spacecraft posture, but the trigger will come from pointing readiness instead of power state.
