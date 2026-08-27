# 11, Contact and Downlink Assumptions

Status: tutorial draft  
Scope: eleventh step of the progressive Reference Mission tutorial

## Purpose

This step introduces contact and downlink assumptions.

After defining data products and storage intent, the next question is:

```text
How does the mission express that stored products are eligible for downlink?
```

The Reference Mission does not simulate orbital geometry, RF propagation or ground-station scheduling.

It defines enough contact and downlink structure to connect data products to a representative communication opportunity.

In the Reference Mission, contact and downlink assumptions are defined in:

```text
mission/contacts.yaml
```

## Operational reason

A data product with downlink intent is still incomplete unless the mission can explain how that product is intended to leave the spacecraft.

The contact model answers:

```text
Which ground reference exists?
Which link profile is assumed?
Which contact window is available?
Which products are eligible for a downlink flow?
```

This is contract-level reasoning.

It is deliberately simpler than a real mission operations or RF planning system.

## Current contact profile

The current model defines one abstract contact profile:

| Contact profile | Target | Tutorial role |
|---|---|---|
| `reference_ground_station` | `reference_ground_segment` | Abstract ground station used by the Reference Mission tutorial. |

This is intentionally generic.

The Reference Mission needs a ground-side anchor for downlink reasoning, but it does not need a real ground-station network at this stage.

## Current link profiles

The current model defines two downlink link profiles:

| Link profile | Direction | Assumed rate | Tutorial role |
|---|---|---|---|
| `uhf_low_rate_downlink` | `downlink` | `9600` bps | Low-rate beacon and housekeeping assumption. |
| `sband_science_downlink` | `downlink` | `1000000` bps | Simplified S-band science downlink assumption. |

These rates are assumptions for tutorial-level reasoning.

They do not define modem configuration, coding, framing, antenna pointing or real link budget behavior.

## Current contact window

The current model defines one representative S-band contact window:

| Contact window | Link profile | Start | Duration | Assumed capacity |
|---|---|---|---|---|
| `sband_window_001` | `sband_science_downlink` | `2026-01-01T00:20:00Z` | `300` seconds | `1000000` bytes |

This window is used by the nominal payload acquisition scenario.

The exact timestamp is not the point of the tutorial.

The important point is that a scenario can refer to an explicit downlink opportunity instead of relying on an implicit or magical transfer.

## Current downlink flow

The current model defines one downlink flow:

| Downlink flow | Queue policy | Eligible products |
|---|---|---|
| `science_priority_flow` | `priority_then_age` | `radiation_histogram`, `critical_housekeeping`, `scenario_evidence_log` |

This flow connects product intent to contact assumptions.

It says that the Reference Mission expects science and operational evidence products to be eligible for a priority-based downlink path.

## Link to data products

The previous step introduced data products and downlink intent.

This step connects that intent to a flow:

```text
radiation_histogram
-> science product
-> high priority
-> eligible for science_priority_flow
-> carried during a representative S-band contact
```

This makes the science downlink explainable without modeling the full communication system.

## Link to operational modes

The downlink assumptions also connect to operational modes.

The spacecraft has a `DOWNLINK` mode, and the command contract includes S-band activity commands.

Together, the model can express:

```text
S-band contact available
-> downlink starts
-> spacecraft enters DOWNLINK posture
-> eligible products are considered for downlink
-> downlink completes
-> spacecraft returns toward NOMINAL
```

This is enough for scenario evidence.

## What is deliberately not modeled yet

This contact and downlink contract does not define:

- orbital propagation;
- pass prediction;
- antenna pointing;
- modulation or coding;
- real RF link budget;
- ground-station resource scheduling;
- packet-level protocol behavior;
- retransmission logic;
- CFDP or file-transfer implementation;
- complete mission operations planning.

Those are outside the current Reference Mission tutorial step.

At this stage, the model only needs a contract-level way to reason about downlink eligibility and representative contact opportunity.

## Why this level is enough

OrbitFabric is not pretending to be a full communication simulator here.

The useful contract-level questions are simpler:

- Does a data product exist?
- Is it intended for downlink?
- Which link family can carry it?
- Which flow makes it eligible?
- Which contact assumption makes the scenario explicit?
- Which evidence should show that downlink started or completed?

That is the correct level for this Reference Mission.

## Modeling rule introduced in this step

The eleventh rule is:

```text
Model contact and downlink assumptions only as far as needed to explain product flow.
```

Do not introduce RF or mission-operations detail before the tutorial needs it.

A contact model should make scenario evidence explicit, not replace a specialized communications simulator or ground scheduling system.

## What comes next

The next step introduces commandability and autonomy.

That step will explain which commands are ground-driven, which actions may be automatic, and how recovery behavior becomes visible in scenarios.
