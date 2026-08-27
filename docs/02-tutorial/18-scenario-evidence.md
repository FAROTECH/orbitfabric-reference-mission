# 18, Scenario Evidence

Status: tutorial draft  
Scope: reading simulation JSON reports and scenario logs as engineering evidence

## Purpose

This step explains how to read scenario evidence.

The previous step introduced generated artifacts as reproducible outputs. This step focuses specifically on scenario execution evidence.

Scenario evidence has two complementary forms:

| Evidence form | Role |
|---|---|
| simulation JSON report | Machine-readable scenario evidence produced by Core. |
| plain-text log | Human-readable timeline for engineering review. |

Plain-text logs are not just console output.

They are human-readable evidence that the Reference Mission contract produced the expected operational behavior.

Simulation JSON reports are the stronger downstream surface because they can be indexed, counted and consumed by later Core-owned reports.

The current evidence logs are:

```text
generated/logs/nominal_payload_acquisition.txt
generated/logs/eclipse_low_power_payload_suspension.txt
generated/logs/adcs_degraded_pointing_payload_inhibit.txt
generated/logs/delayed_sband_downlink_backlog_pending.txt
```

The corresponding simulation JSON reports should be generated under:

```text
generated/reports/
```

## Source of truth

The source of truth remains:

```text
mission/
scenarios/
```

Scenario JSON reports and logs are generated evidence derived from those inputs.

This means they should be read as reproducible execution records, not hand-authored documentation.

If evidence contradicts the model or scenario, the project should fix the model, scenario or simulator behavior. It should not manually edit generated output.

!!! note "Machine-readable first"
    Downstream tooling should consume simulation JSON reports, not plain-text logs. Logs are for human review.

## Log structure

Each current scenario log follows the same high-level structure:

```text
OrbitFabric Scenario Simulator 1.0.0

Scenario: <scenario_id>
Mission: of-rm-1

Timeline:
  <time-stamped evidence lines>

Result: PASSED
```

This structure matters because it gives each log three layers:

| Layer | Meaning |
|---|---|
| Header | Identifies simulator, scenario and mission. |
| Timeline | Shows ordered operational evidence. |
| Result | Summarizes whether the scenario expectation passed. |

The timeline is the main human-readable evidence surface.

## Evidence line types

The current logs use a compact set of evidence line types:

| Line type | Example | Meaning |
|---|---|---|
| `MODE` | `MODE=NOMINAL` | Current spacecraft mode. |
| `COMMAND` | `COMMAND payload.start_acquisition -> ACCEPTED` | Command execution or dispatch result. |
| `EVENT` | `EVENT payload.acquisition_started severity=INFO` | Event emitted by the scenario execution. |
| `TELEMETRY` | `TELEMETRY radiation_payload.acquisition_active=true` | Observed telemetry value. |
| `INJECT` | `INJECT eps.battery.state_of_charge=28.0` | Scenario-injected telemetry value. |
| `MODE TRANSITION` | `MODE TRANSITION NOMINAL -> PAYLOAD_ACTIVE reason=payload.acquisition_started` | Spacecraft posture change and reason. |
| `PAYLOAD` | `PAYLOAD radiation_event_payload LIFECYCLE=ACQUIRING` | Payload lifecycle state. |
| `DATA_PRODUCT` | `DATA_PRODUCT radiation_histogram CONTRACT_EVIDENCE_RECORDED` | Data product evidence recorded. |
| `DATA_FLOW` | `DATA_FLOW radiation_histogram EXPECTATION_MET` | Data-flow expectation satisfied. |
| `SCENARIO` | `SCENARIO PASSED` | Scenario-level expectation result. |

This vocabulary is deliberately simple.

It is enough to review mission behavior without reading simulator internals.

## Simulation JSON report role

A simulation JSON report should be used when evidence needs to be consumed by tools.

It can support:

- scenario run indexing;
- expectation accounting;
- coverage summary generation;
- dashboard-ready status surfaces;
- repeatable CI inspection.

A plain-text log is easier for a person to read.

A simulation JSON report is safer for a tool to consume.

That boundary must remain explicit.

## Reading the nominal evidence path

The nominal payload acquisition evidence proves the end-to-end science path.

The core evidence chain is:

```text
COMMAND payload.start_acquisition -> ACCEPTED
EVENT payload.acquisition_started severity=INFO
PAYLOAD radiation_event_payload LIFECYCLE=ACQUIRING
MODE TRANSITION NOMINAL -> PAYLOAD_ACTIVE reason=payload.acquisition_started
COMMAND payload.request_histogram -> ACCEPTED
EVENT payload.histogram_generated severity=INFO
DATA_PRODUCT radiation_histogram CONTRACT_EVIDENCE_RECORDED
DATA_FLOW radiation_histogram EXPECTATION_MET
COMMAND comms.start_sband_downlink -> ACCEPTED
MODE TRANSITION PAYLOAD_ACTIVE -> DOWNLINK reason=comms.sband_downlink_started
DATA_FLOW radiation_histogram EXPECTATION_MET
COMMAND comms.stop_sband_downlink -> ACCEPTED
MODE TRANSITION DOWNLINK -> NOMINAL reason=comms.sband_downlink_completed
Result: PASSED
```

This chain proves that the scenario is not just a command sequence.

It links payload acquisition, data product creation, downlink flow and final return to nominal posture.

## Reading the low-power evidence path

The low-power evidence proves protective behavior from EPS evidence.

The core evidence chain is:

```text
INJECT eps.battery.state_of_charge=28.0
INJECT eps.battery.state_of_charge=27.0
EVENT eps.low_power_warning_raised severity=WARNING
MODE TRANSITION PAYLOAD_ACTIVE -> DEGRADED_POWER reason=eps.low_battery_warning
COMMAND payload.stop_acquisition -> AUTO_DISPATCHED
EVENT payload.acquisition_completed severity=INFO
PAYLOAD radiation_event_payload LIFECYCLE=READY
TELEMETRY radiation_payload.acquisition_active=false
Result: PASSED
```

This chain proves three important things:

1. The fault does not trigger from a single low sample.
2. The spacecraft enters `DEGRADED_POWER`, not `NOMINAL`.
3. The payload stop is auto-dispatched as protective behavior.

This is exactly the distinction the fault and commandability steps introduced earlier.

## Reading the ADCS-degraded evidence path

The ADCS-degraded evidence proves protective behavior from pointing evidence.

The core evidence chain is:

```text
INJECT adcs.pointing_status=DEGRADED
INJECT adcs.pointing_status=DEGRADED
EVENT adcs.pointing_degraded severity=WARNING
MODE TRANSITION PAYLOAD_ACTIVE -> ADCS_DEGRADED reason=adcs.control_degraded
COMMAND payload.stop_acquisition -> AUTO_DISPATCHED
EVENT payload.acquisition_completed severity=INFO
PAYLOAD radiation_event_payload LIFECYCLE=READY
TELEMETRY radiation_payload.acquisition_active=false
Result: PASSED
```

This chain is intentionally similar to the low-power case.

The protective command is the same, but the degraded posture is different:

```text
EPS low battery -> DEGRADED_POWER
ADCS degraded pointing -> ADCS_DEGRADED
```

Scenario evidence preserves that difference.

## Reading the delayed-backlog evidence path

The delayed-backlog evidence proves persistence of a generated product when no downlink occurs.

The core evidence chain is:

```text
COMMAND payload.request_histogram -> ACCEPTED
EVENT payload.histogram_generated severity=INFO
PAYLOAD radiation_event_payload LIFECYCLE=HISTOGRAM_READY
DATA_PRODUCT radiation_histogram CONTRACT_EVIDENCE_RECORDED
TELEMETRY radiation_payload.histogram_ready=true
TELEMETRY radiation_payload.histogram_pending_bytes=4096
TELEMETRY sband_radio.link_state=IDLE
DATA_FLOW radiation_histogram EXPECTATION_MET
TELEMETRY radiation_payload.histogram_pending_bytes=4096
TELEMETRY sband_radio.link_state=IDLE
Result: PASSED
```

This chain proves that absence of downlink is not absence of data.

The product exists, the data-flow expectation is met, the link remains idle and the pending bytes remain visible.

## Evidence versus narrative

The tutorial narrative explains why each scenario matters.

The generated evidence shows what actually happened during generated execution.

Both are needed:

| Layer | Role |
|---|---|
| Tutorial walkthrough | Explains operational intent and engineering meaning. |
| Scenario YAML | Defines expectations and injected conditions. |
| Simulation JSON report | Records machine-readable execution evidence. |
| Scenario log | Records human-readable execution evidence. |

A good Reference Mission should keep all four aligned.

## Evidence versus verification

Scenario evidence is not full spacecraft verification.

It does not prove:

- flight software correctness;
- timing correctness;
- binary packet validity;
- hardware behavior;
- RF performance;
- operator procedure correctness;
- real mission safety.

It proves something narrower and still valuable:

```text
The mission contract, scenario expectations and generated behavior are coherent at model level.
```

That is the correct claim.

## Evidence and traceability

Scenario evidence makes traceability reviewable.

A reviewer can move from:

```text
scenario file
-> command
-> event
-> mode transition
-> payload lifecycle
-> data product
-> telemetry evidence
-> final result
```

This is the foundation for future Studio exploration.

Studio should eventually make these chains easier to navigate, but the Core evidence already exists before Studio.

## Current evidence coverage matrix

| Scenario | Main evidence chain | Final result |
|---|---|---|
| `nominal_payload_acquisition` | Payload acquisition, histogram generation, S-band downlink, return to nominal. | `PASSED` |
| `eclipse_low_power_payload_suspension` | EPS low-power warning, degraded-power transition, auto stop payload. | `PASSED` |
| `adcs_degraded_pointing_payload_inhibit` | ADCS degraded pointing, ADCS-degraded transition, auto stop payload. | `PASSED` |
| `delayed_sband_downlink_backlog_pending` | Histogram generated, data-flow expectation met, backlog remains pending. | `PASSED` |

This matrix is compact, but it captures the current behavioral coverage of the Reference Mission.

## What to look for when reviewing a new scenario

A new scenario evidence package should make these questions easy to answer:

- What was the initial mode?
- Which command started the behavior?
- Which telemetry was injected or observed?
- Which event confirmed the milestone?
- Did a mode transition occur?
- Did a payload lifecycle state change?
- Was a data product recorded?
- Was a data-flow expectation met?
- Was an automatic command dispatched?
- Did the final result pass?
- Is the same evidence available in machine-readable JSON?

If the answer is not visible in generated evidence, the scenario may not yet be good evidence.

## Modeling rule introduced in this step

The eighteenth rule is:

```text
Scenario evidence should make operational causality reviewable and tool-consumable.
```

A scenario log should not merely show that steps executed.

A simulation JSON report should not merely exist as a file.

Together, they should make it possible to understand why the mission behavior changed, which model entities participated and which evidence can be reused by Core-owned downstream surfaces.

## What comes next

The next tutorial step introduces runtime-facing contract bindings.

That step explains what OrbitFabric can generate toward runtime integration while preserving a strict boundary: generated bindings are not flight software.
