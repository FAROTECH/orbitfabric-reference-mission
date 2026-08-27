# 15, ADCS Degraded Payload Inhibit Scenario

Status: tutorial draft  
Scope: third scenario walkthrough of the progressive Reference Mission tutorial

## Purpose

This step introduces the ADCS degraded payload inhibit scenario.

The previous degraded scenario showed how low power interrupts payload acquisition. This scenario shows a different operational constraint: payload acquisition is interrupted because spacecraft pointing is no longer suitable.

The scenario is defined in:

```text
scenarios/adcs_degraded_pointing_payload_inhibit.yaml
```

The generated scenario log is available in the provided generated artifact set as:

```text
generated/logs/adcs_degraded_pointing_payload_inhibit.txt
```

## Scenario intent

The scenario answers one operational question:

```text
Can the Reference Mission explain how degraded pointing leads to ADCS-degraded posture and autonomous payload suspension?
```

This is not a power-protection scenario.

It is a pointing-constraint scenario.

The mission should not keep a pointing-sensitive payload acquisition active when ADCS is no longer in a nominal pointing state.

## Scenario summary

The scenario performs this high-level sequence:

```text
NOMINAL mode
-> ground starts payload acquisition
-> payload becomes ACQUIRING
-> payload event-rate telemetry is observed
-> ADCS pointing becomes DEGRADED twice
-> ADCS degraded event is raised
-> spacecraft transitions to ADCS_DEGRADED
-> onboard autonomy dispatches payload.stop_acquisition
-> payload acquisition completes
-> acquisition_active becomes false
-> payload lifecycle returns to READY
-> scenario passes
```

This scenario exercises the same protective structure as the low-power case, but with a different subsystem source and a different degraded posture.

## Initial state

The scenario starts in:

```text
mode: NOMINAL
```

The initial telemetry is compatible with a nominal payload acquisition:

| Telemetry | Initial value | Meaning |
|---|---:|---|
| `eps.battery.voltage` | `8.0` | Power state is healthy. |
| `eps.battery.state_of_charge` | `68.0` | Battery state of charge is well above the payload-start threshold. |
| `eps.solar.input_power` | `4.2` | Solar input is available. |
| `adcs.pointing_status` | `NOMINAL` | ADCS initially supports payload acquisition. |
| `adcs.angular_rate` | `0.4` | Angular rate is low enough for this scenario. |
| `sband_radio.link_state` | `IDLE` | S-band is inactive. |
| `radiation_payload.acquisition_active` | `false` | Payload acquisition has not started yet. |
| `radiation_payload.histogram_ready` | `false` | No histogram is ready. |
| `radiation_payload.histogram_pending_bytes` | `0` | No histogram backlog exists. |

The key point is that the initial state is not power-constrained.

The degraded condition comes from ADCS pointing readiness.

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

This confirms that the payload starts correctly before ADCS degradation is introduced.

## Step 2, observe payload activity

At `t: 30`, the scenario injects:

```text
radiation_payload.event_rate: 38.0
```

This represents ongoing science acquisition.

The exact value is not the focus. The focus is that payload acquisition is active when pointing becomes degraded.

## Step 3, inject first degraded pointing sample

At `t: 90`, the scenario injects:

```text
adcs.pointing_status: DEGRADED
```

At `t: 91`, it still expects:

```text
PAYLOAD_ACTIVE
```

This is deliberate.

A single degraded pointing sample is not enough to trigger the ADCS fault because the fault uses debounce.

## Step 4, inject second degraded pointing sample

At `t: 92`, the scenario injects again:

```text
adcs.pointing_status: DEGRADED
```

This is the second consecutive degraded pointing sample.

The fault contract requires:

```text
debounce_samples: 2
```

At this point, the degraded pointing condition becomes operationally significant.

## Step 5, observe ADCS degraded evidence

At `t: 93`, the scenario expects:

```text
adcs.pointing_degraded
```

The generated log confirms this milestone:

```text
[01:32] EVENT adcs.pointing_degraded severity=WARNING
```

This event records the operational evidence that ADCS pointing is no longer suitable for payload acquisition.

## Step 6, enter ADCS-degraded posture

At `t: 94`, the scenario expects:

```text
ADCS_DEGRADED
```

The generated log records the same transition:

```text
[01:32] MODE TRANSITION PAYLOAD_ACTIVE -> ADCS_DEGRADED reason=adcs.control_degraded
```

This is the central spacecraft posture result of the scenario.

The spacecraft does not return to `NOMINAL` automatically.

It enters a degraded posture that preserves the reason for payload inhibition.

## Step 7, auto-dispatch payload stop

At `t: 95`, the scenario expects an automatic command dispatch:

```text
payload.stop_acquisition
```

with:

```text
dispatch: AUTO
```

The generated log records:

```text
[01:32] COMMAND payload.stop_acquisition -> AUTO_DISPATCHED
```

This is the same autonomy pattern used in the low-power scenario, but the trigger is different.

The command is dispatched protectively because ADCS is degraded, not because EPS is low.

## Step 8, payload stops acquiring

At `t: 96`, the scenario expects:

```text
payload.acquisition_completed
```

At `t: 97`, it expects:

```text
radiation_payload.acquisition_active: false
```

At `t: 98`, it expects the payload lifecycle to be:

```text
READY
```

The generated log confirms the same sequence:

```text
[01:32] EVENT payload.acquisition_completed severity=INFO
[01:32] PAYLOAD radiation_event_payload LIFECYCLE=READY
[01:32] TELEMETRY radiation_payload.acquisition_active=false
```

The payload is placed in a safe, non-acquiring lifecycle state while the spacecraft remains in an ADCS-degraded posture.

## Step 9, scenario passes

At `t: 99`, the scenario expects:

```text
scenario_status: PASSED
```

The generated log ends with:

```text
Result: PASSED
```

This confirms that the degraded pointing behavior is expected and validated.

## What this scenario proves

This scenario proves that the Reference Mission can connect:

- payload acquisition start;
- payload lifecycle `ACQUIRING`;
- ADCS pointing telemetry;
- debounce behavior across two degraded samples;
- ADCS degraded event;
- `PAYLOAD_ACTIVE -> ADCS_DEGRADED` transition;
- onboard autonomous command dispatch;
- payload acquisition stop;
- `acquisition_active: false` telemetry;
- payload lifecycle return to `READY`;
- scenario pass status.

This is the second protective-behavior evidence path in the tutorial.

## What this scenario does not prove

This scenario does not prove:

- low-power behavior;
- critical battery safe-mode transition;
- payload timeout behavior;
- storage near-full behavior;
- science product downlink;
- RF or contact behavior;
- real ADCS control-loop implementation;
- full onboard FDIR implementation.

Those remain separate concerns.

This scenario focuses only on degraded pointing during active payload acquisition.

## Why this scenario matters

The scenario validates that the same autonomy pattern can be triggered by different operational constraints.

In the previous degraded scenario:

```text
EPS low battery -> DEGRADED_POWER -> auto stop payload
```

In this scenario:

```text
ADCS degraded pointing -> ADCS_DEGRADED -> auto stop payload
```

The local payload action is the same, but the spacecraft recovery posture is different.

That distinction is the core point.

## Modeling rule introduced in this step

The fifteenth rule is:

```text
Reuse protective actions without erasing the subsystem-specific degraded posture.
```

The same command can be auto-dispatched for different reasons.

The mission contract must preserve the reason and the resulting spacecraft posture.

## What comes next

The next scenario introduces delayed S-band downlink and backlog pending.

It will shift the focus from protective behavior to product persistence when a science product is generated but not downlinked immediately.
