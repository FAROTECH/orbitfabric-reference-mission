# Flight / Ground Reference Project

This is the executable project behind Engineering Story 01, **One Mission Contract Across Flight and Ground**.

It is not a toy example. It uses the canonical OrbitFabric Reference Mission, pinned public downstream products, native F Prime generation/build, the existing OpenC3 F Prime plugin, generated OpenC3 COSMOS verification code and a live command/telemetry loop.

## What the project proves

For the demonstrated stop-acquisition vertical slice, the same canonical mission-level contract is consumed through two independent paths:

```text
Reference Mission / Core
    -> F Prime adapter
    -> native F Prime realization
    -> native F Prime Dictionary
    -> OpenC3 F Prime plugin

Reference Mission / Core
    -> OpenC3 COSMOS adapter
    -> generated verification procedure
```

The two paths converge downstream in OpenC3 COSMOS and a live F Prime target.

Canonical mission identities:

```text
command:   payload.stop_acquisition
telemetry: radiation_payload.acquisition_active
```

## Project layout

```text
profiles/
    fprime.yaml
    cosmos.yaml

scripts/
    materialize_fprime_story.py
    configure_fprime_server_role.py
    generate_cosmos_fprime_target.py
    run_live_fprime_cosmos.sh

evidence/
    retained public evidence for the accepted project baseline
```

The canonical verification scenario remains at repository level:

```text
scenarios/payload_stop_acquisition_verification.yaml
```

## Reproduction

The current authoritative reproduction is automated by the repository workflows:

- `R1 Flight Ground Proof` validates the canonical Core input, both projections, native F Prime generate/build, native Dictionary identities and the OpenC3 F Prime dictionary handoff.
- `R1 Live Flight Ground Proof` rebuilds the same path, starts native F Prime and OpenC3 COSMOS, waits for the real interface connection and runs the generated verification suite.

A streamlined local quick-start is being finalized as part of the public Reference Project packaging. The workflows remain the exact executable specification of the accepted proof.

## Ownership boundary

The project deliberately keeps downstream behavior and deployment choices downstream.

The Story-owned F Prime command handler implements only the behavior needed by this vertical slice:

```text
OF_StopAcquisition
    -> write OF_AcquisitionActive = false
    -> command OK
```

That implementation is not generated from OrbitFabric `expected_effects`.

Likewise, F Prime owns native deployment resolution and telemetry packet placement, while OpenC3 owns its native target, transport and execution semantics.

## Read next

- [Engineering Story](../STORY.md)
- [Technical Deep Dive](../TECHNICAL-DEEP-DIVE.md)
- [Package entry point](../README.md)
