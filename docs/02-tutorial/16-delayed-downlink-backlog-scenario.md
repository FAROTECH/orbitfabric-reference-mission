# 16, Delayed Downlink Backlog Scenario

Status: tutorial draft  
Scope: fourth scenario walkthrough of the progressive Reference Mission tutorial

## Purpose

This step introduces the delayed S-band downlink backlog scenario.

The nominal scenario showed a science product generated and associated with a downlink opportunity. The degraded scenarios showed protective payload suspension. This scenario focuses on a different operational question: what happens when a science product is generated but no S-band downlink is executed during the scenario.

The scenario is defined in:

```text
scenarios/delayed_sband_downlink_backlog_pending.yaml
```

The generated scenario log is available in the provided generated artifact set as:

```text
generated/logs/delayed_sband_downlink_backlog_pending.txt
```

## Scenario intent

The scenario answers one operational question:

```text
Can the Reference Mission preserve explicit evidence that a science product exists, is eligible for downlink, but remains pending because no downlink occurred?
```

This is not a communication scenario.

It is a persistence and evidence scenario.

The key result is not downlink completion. The key result is that the backlog remains visible and explainable.

## Scenario summary

The scenario performs this high-level sequence:

```text
NOMINAL mode
-> ground starts payload acquisition
-> payload becomes ACQUIRING
-> event-rate telemetry is observed
-> histogram is requested
-> histogram is generated
-> payload lifecycle becomes HISTOGRAM_READY
-> histogram pending bytes become 4096
-> S-band remains IDLE
-> radiation_histogram data-flow expectation is met
-> after elapsed time, pending bytes are still 4096
-> S-band is still IDLE
-> spacecraft remains PAYLOAD_ACTIVE
-> scenario passes
```

This scenario proves that a data product can remain explicitly pending without being lost from the mission contract.

## Initial state

The scenario starts in:

```text
mode: NOMINAL
```

The initial telemetry is compatible with nominal payload acquisition and later histogram generation:

| Telemetry | Initial value | Meaning |
|---|---:|---|
| `eps.battery.voltage` | `8.0` | Battery voltage is healthy. |
| `eps.battery.state_of_charge` | `74.0` | Battery state of charge is healthy. |
| `eps.solar.input_power` | `4.8` | Solar input is available. |
| `data_storage.used_percent` | `41.0` | Storage is already used, but not near full. |
| `adcs.pointing_status` | `NOMINAL` | ADCS supports payload acquisition. |
| `sband_radio.link_state` | `IDLE` | S-band is inactive. |
| `radiation_payload.acquisition_active` | `false` | Payload acquisition has not started. |
| `radiation_payload.histogram_ready` | `false` | No histogram is ready. |
| `radiation_payload.histogram_pending_bytes` | `0` | No backlog exists yet. |

The key point is that the spacecraft is healthy enough for nominal science activity.

The scenario does not introduce degraded behavior.

## Step 1, start payload acquisition

At `t: 5`, the scenario sends:

```text
payload.start_acquisition
```

with:

```text
duration_s: 900
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

The generated log confirms the same start sequence:

```text
[00:05] COMMAND payload.start_acquisition -> ACCEPTED
[00:05] EVENT payload.acquisition_started severity=INFO
[00:05] PAYLOAD radiation_event_payload LIFECYCLE=ACQUIRING
[00:05] MODE TRANSITION NOMINAL -> PAYLOAD_ACTIVE reason=payload.acquisition_started
```

This establishes a normal payload-acquisition context.

## Step 2, observe science activity

At `t: 30`, the scenario injects:

```text
radiation_payload.event_rate: 55.0
```

This indicates ongoing science acquisition.

The exact rate is not the point. The point is that the payload has meaningful science activity before the histogram is requested.

## Step 3, request histogram generation

At `t: 120`, the scenario sends:

```text
payload.request_histogram
```

At `t: 121`, it expects:

```text
payload.histogram_generated
```

At `t: 122`, it expects the payload lifecycle to be:

```text
HISTOGRAM_READY
```

The generated log confirms:

```text
[02:00] COMMAND payload.request_histogram -> ACCEPTED
[02:00] EVENT payload.histogram_generated severity=INFO
[02:00] PAYLOAD radiation_event_payload LIFECYCLE=HISTOGRAM_READY
[02:00] DATA_PRODUCT radiation_histogram CONTRACT_EVIDENCE_RECORDED
```

This is the core data-product creation evidence.

The product is now part of the mission contract evidence.

## Step 4, mark pending histogram bytes

At `t: 123`, the scenario injects:

```text
radiation_payload.histogram_pending_bytes: 4096
```

At `t: 124`, it expects:

```text
radiation_payload.histogram_ready: true
radiation_payload.histogram_pending_bytes: 4096
sband_radio.link_state: IDLE
```

The generated log confirms:

```text
[02:04] TELEMETRY radiation_payload.histogram_ready=true
[02:04] TELEMETRY radiation_payload.histogram_pending_bytes=4096
[02:04] TELEMETRY sband_radio.link_state=IDLE
```

This is the heart of the backlog scenario.

The histogram exists. The payload has pending bytes. S-band is still idle.

## Step 5, verify data-flow intent

At `t: 125`, the scenario expects a data-flow relationship:

```text
data_product: radiation_histogram
triggered_by_command: payload.request_histogram
storage_intent_declared: true
downlink_intent_declared: true
eligible_downlink_flow: science_priority_flow
```

The generated log records:

```text
[02:05] DATA_FLOW radiation_histogram EXPECTATION_MET
```

This proves that the data product is not an isolated telemetry value.

It has declared storage intent, downlink intent and eligibility for the science-priority flow.

## Step 6, verify backlog remains pending

At `t: 1800`, the scenario expects:

```text
radiation_payload.histogram_pending_bytes: 4096
sband_radio.link_state: IDLE
```

The generated log confirms:

```text
[30:00] TELEMETRY radiation_payload.histogram_pending_bytes=4096
[30:00] TELEMETRY sband_radio.link_state=IDLE
```

This is the delayed-downlink evidence.

No S-band downlink occurred during the scenario, so the backlog remains visible.

## Step 7, verify spacecraft posture

At `t: 1801`, the scenario expects:

```text
PAYLOAD_ACTIVE
```

This is intentional.

Unlike the low-power and ADCS degraded scenarios, this scenario does not trigger a fault recovery path.

The spacecraft does not enter `DEGRADED_POWER`, `ADCS_DEGRADED` or `SAFE`.

The issue is not a fault. The issue is that the product remains pending because no downlink was executed.

## Step 8, scenario passes

At `t: 1802`, the scenario expects:

```text
scenario_status: PASSED
```

The generated log ends with:

```text
Result: PASSED
```

This confirms that a pending backlog is an expected and valid mission state.

## What this scenario proves

This scenario proves that the Reference Mission can connect:

- payload acquisition start;
- payload lifecycle `ACQUIRING`;
- science event-rate telemetry;
- histogram generation;
- payload lifecycle `HISTOGRAM_READY`;
- `radiation_histogram` data-product evidence;
- pending histogram bytes;
- S-band link remaining `IDLE`;
- declared storage intent;
- declared downlink intent;
- eligibility for `science_priority_flow`;
- backlog persistence after elapsed time;
- scenario pass status.

This is the tutorial's first persistence and backlog evidence path.

## What this scenario does not prove

This scenario does not prove:

- successful S-band downlink;
- contact-window execution;
- low-power recovery;
- ADCS degraded recovery;
- payload timeout behavior;
- storage near-full behavior;
- RF link performance;
- real file-transfer behavior.

Those remain separate concerns.

This scenario focuses only on generated science product evidence and explicit pending backlog.

## Why this scenario matters

A mission model must be able to represent incomplete operational outcomes.

A product that is not downlinked immediately should not disappear from the evidence chain.

The correct model-level statement is:

```text
product generated
-> storage intent declared
-> downlink intent declared
-> eligible flow known
-> S-band idle
-> backlog still pending
```

That is exactly what this scenario demonstrates.

## Modeling rule introduced in this step

The sixteenth rule is:

```text
A pending product is still mission evidence.
```

Do not treat lack of downlink as absence of data.

If the product exists and remains pending, the mission contract should make that state explicit and reviewable.

## What comes next

The next tutorial step should consolidate generated artifacts.

Now that the model construction and four scenario walkthroughs are documented, the tutorial can explain the generated documentation, reports and logs as reproducible evidence surfaces.
