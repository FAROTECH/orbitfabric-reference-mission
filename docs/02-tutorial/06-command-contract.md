# 06, Command Contract

Status: tutorial draft  
Scope: sixth step of the progressive Reference Mission tutorial

## Purpose

This step introduces the command contract.

After defining what the mission can observe through telemetry, the next question is:

```text
What can ground operators or onboard logic request the spacecraft to do?
```

Commands are the actionable side of the mission contract. They describe the operations that can be requested, the modes where they are allowed, the acknowledgement behavior, the expected effects and the operational risk level.

In the Reference Mission, commands are defined in:

```text
mission/commands.yaml
```

## Operational reason

A command is not just a function call.

In OrbitFabric, a command connects mission intent to expected behavior:

```text
request
-> target subsystem
-> allowed modes
-> preconditions
-> acknowledgement
-> emitted events
-> expected effects
```

That connection is what makes the model useful for validation, documentation and scenario evidence.

## Current command groups

The current Reference Mission defines nine commands across three operational groups:

| Group | Commands | Tutorial role |
|---|---|---|
| OBC | `obc.request_health_check`, `obc.enter_nominal`, `obc.enter_safe_mode` | Spacecraft-level health and posture control. |
| Payload | `payload.start_acquisition`, `payload.stop_acquisition`, `payload.request_histogram` | Science acquisition and data-product generation. |
| Communications | `comms.mark_sband_contact_started`, `comms.start_sband_downlink`, `comms.stop_sband_downlink` | Contact and S-band downlink activity. |

This set is intentionally small.

It is enough to drive the first tutorial scenarios without turning the model into a complete spacecraft operations manual.

## What each command declares

Each command can declare several contract-level properties:

| Property | Role |
|---|---|
| `id` | Stable machine-readable command identifier. |
| `target` | Subsystem that receives or owns the operation. |
| `description` | Human-readable operational meaning. |
| `arguments` | Input parameters, if the command needs them. |
| `allowed_modes` | Spacecraft modes where the command may be accepted. |
| `preconditions` | Model-level conditions required before execution. |
| `requires_ack` | Whether the command expects acknowledgement. |
| `timeout_ms` | Expected command-response timeout. |
| `risk` | Operational risk category. |
| `emits` | Events expected from the command. |
| `expected_effects` | Mode, telemetry, payload or data-product changes expected from the command. |

The important point is that a command carries both operational constraints and expected evidence.

## Example: starting payload acquisition

The payload acquisition command is allowed from `NOMINAL` mode.

It also has explicit preconditions:

```text
adcs.pointing_status == NOMINAL
eps.battery.state_of_charge > 30
```

This makes the command contract depend on telemetry and spacecraft posture.

The expected effects include:

- transition toward `PAYLOAD_ACTIVE`;
- payload lifecycle becoming `ACQUIRING`;
- `radiation_payload.acquisition_active` becoming `true`;
- emission of payload and mode-change events.

This is exactly the kind of chain the scenario layer can later exercise.

## Example: stopping payload acquisition

The stop-acquisition command is deliberately narrower than recovery logic.

It stops the payload and updates payload-related evidence:

```text
payload lifecycle -> READY
radiation_payload.acquisition_active -> false
```

It does not decide that the spacecraft must return to `NOMINAL`.

That distinction is important.

A payload command should control payload state. Fault and recovery logic should control spacecraft posture.

This prevents degraded scenarios from being incorrectly hidden by a command effect.

## Example: S-band downlink

The S-band commands make contact and downlink activity explicit:

- contact start marks the link as ready;
- downlink start transitions toward `DOWNLINK` and sets the link to `DOWNLINKING`;
- downlink stop returns the link to `IDLE` and transitions back toward nominal operations.

This keeps downlink behavior visible in the model without pretending that OrbitFabric is a full RF simulator or scheduler.

## What is deliberately not modeled yet

This command contract does not define:

- binary telecommand packets;
- authentication or encryption;
- ground procedure tooling;
- onboard dispatcher implementation;
- task scheduling;
- retry algorithms;
- low-level radio protocol details.

Those are implementation or operations details.

At this stage, the Reference Mission only defines command-level mission intent and expected evidence.

## Link to later model areas

Later tutorial steps will use commands to explain:

- event generation;
- fault recovery actions;
- payload lifecycle transitions;
- data product generation;
- downlink scenario evidence;
- commandability and autonomy.

Commands are where the mission contract starts to become actionable.

## Modeling rule introduced in this step

The sixth rule is:

```text
A command should describe requested behavior and expected evidence, not implementation internals.
```

Do not add a command only because a software function exists.

Add a command when the mission needs an explicit operation that can be constrained, acknowledged, simulated or reviewed.

## What comes next

The next step introduces events.

Events will make command outcomes and operational milestones visible in scenario evidence.
