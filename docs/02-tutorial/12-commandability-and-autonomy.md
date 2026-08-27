# 12, Commandability and Autonomy

Status: tutorial draft  
Scope: twelfth step of the progressive Reference Mission tutorial

## Purpose

This step introduces commandability and autonomy.

After defining commands, faults, data products and contact assumptions, the next question is:

```text
Who is allowed to request an operation, under which conditions, and what may happen automatically?
```

The command contract described what commands exist.

The commandability contract describes which sources may dispatch them, where contact is required, which modes are allowed, which confirmation semantics apply and which autonomous actions are expected during protective behavior.

In the Reference Mission, commandability is defined in:

```text
mission/commandability.yaml
```

## Operational reason

A command is incomplete if the model does not explain who can issue it.

Some commands are ground-driven. Some protective actions may be dispatched by onboard autonomy. Some commands require ground contact. Some are valid only in specific spacecraft modes.

Commandability makes these constraints explicit.

It connects:

```text
command
-> source
-> allowed mode
-> confirmation semantics
-> expected events
-> expected effects
```

## Current command sources

The current Reference Mission defines two command sources:

| Source | Type | Requires contact | Tutorial role |
|---|---|---|---|
| `ground_ops` | `ground` | `true` | Ground operator source during contact windows. |
| `onboard_autonomy` | `autonomous` | `false` | Onboard source for protective commands. |

This distinction is essential.

The ground can intentionally request operations during contact.

Onboard autonomy can perform protective actions without waiting for contact.

## Current commandability rules

The current model defines five commandability rules:

| Rule | Command | Sources | Tutorial role |
|---|---|---|---|
| `enter_nominal_rule` | `obc.enter_nominal` | `ground_ops` | Ground-confirmed transition into nominal operations. |
| `enter_safe_mode_rule` | `obc.enter_safe_mode` | `ground_ops`, `onboard_autonomy` | Safe-mode transition with explicit confirmation semantics. |
| `start_payload_acquisition_rule` | `payload.start_acquisition` | `ground_ops` | Ground-driven start of payload acquisition from nominal mode. |
| `stop_payload_acquisition_rule` | `payload.stop_acquisition` | `ground_ops`, `onboard_autonomy` | Ground or autonomous stop of payload acquisition. |
| `start_sband_downlink_rule` | `comms.start_sband_downlink` | `ground_ops` | Ground-driven S-band downlink start during contact. |

These rules do not replace the command definitions.

They refine how commands are allowed to be dispatched in operational context.

## Confirmation semantics

The commandability model includes confirmation semantics such as:

| Confirmation | Tutorial meaning |
|---|---|
| `required` | The operation requires explicit confirmation semantics. |
| `hinted` | The operation carries lighter confirmation expectations. |

This is not a ground-system implementation.

It is a contract-level hint that the operation has different operational handling depending on risk and context.

## Example: payload acquisition start

Starting payload acquisition is ground-driven.

The rule says:

```text
command: payload.start_acquisition
source: ground_ops
allowed mode: NOMINAL
confirmation: required
expected effect: mode PAYLOAD_ACTIVE
```

This means payload acquisition is not treated as an arbitrary automatic action.

It requires an explicit operational source and spacecraft posture.

## Example: payload acquisition stop

Stopping payload acquisition can be performed by either:

```text
ground_ops
onboard_autonomy
```

That is deliberate.

The ground may stop acquisition intentionally.

The onboard system may stop acquisition protectively when a fault recovery path requires it.

This preserves the earlier separation:

```text
fault decides recovery posture
command performs local payload action
commandability explains who may dispatch the command
```

## Autonomous action

The current model defines one autonomous action:

```text
auto_stop_payload_on_low_power
```

It is triggered by:

```text
eps.low_battery_warning
```

and dispatches:

```text
payload.stop_acquisition
```

from:

```text
onboard_autonomy
```

This is the core autonomy behavior in the current Reference Mission.

It allows the low-power scenario to show that payload activity can be stopped protectively without waiting for a ground contact.

## Recovery intent

The current model defines one recovery intent:

```text
recover_from_low_power
```

It connects:

```text
eps.low_battery_warning
-> target mode DEGRADED_POWER
-> payload.stop_acquisition
-> radiation_payload.acquisition_active false
```

This is not a complete FDIR implementation.

It is a contract-level statement of expected recovery behavior.

## Link to contact assumptions

Ground-command sources require contact.

That links this step to the previous contact and downlink assumptions:

```text
ground_ops
-> requires_contact: true
-> contact_profile: reference_ground_station
```

The Reference Mission can therefore distinguish between commands that need a ground opportunity and autonomous actions that do not.

## Link to scenario evidence

Commandability and autonomy are especially important for degraded scenarios.

A scenario can show:

```text
fault detected
-> autonomous action selected
-> command auto-dispatched
-> payload stops acquiring
-> spacecraft remains in degraded posture
```

This is more informative than simply saying that the payload stopped.

It explains why, by whom and under which contract rule.

## What is deliberately not modeled yet

This commandability contract does not define:

- authentication;
- encryption;
- role-based access control;
- command stack implementation;
- onboard scheduler implementation;
- full autonomy engine;
- complete FDIR execution logic;
- operator UI workflow.

Those are implementation and operations details.

At this stage, the Reference Mission only defines contract-level command authorization and autonomous intent.

## Modeling rule introduced in this step

The twelfth rule is:

```text
Separate command existence from commandability.
```

A command definition says what operation exists.

A commandability rule says who can dispatch it, when it is allowed and what evidence should confirm it.

Do not hide autonomy inside command effects.

Expose autonomous dispatch explicitly when scenario evidence needs to explain protective behavior.

## What comes next

The next tutorial steps move from model construction to scenario walkthroughs.

The first scenario will be nominal payload acquisition.
