# Flight / Ground Reference Project

This is the executable project behind Engineering Story 01, **One Mission Contract Across Flight and Ground**.

It is not a toy example. It uses the canonical OrbitFabric Reference Mission, pinned public downstream products, native F Prime generation/build, the existing OpenC3 F Prime plugin, generated OpenC3 COSMOS verification code and a live command/telemetry loop.

## What it runs

The same canonical mission-level contract is consumed through two independent paths:

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

The paths converge downstream in OpenC3 COSMOS and a live F Prime target.

Canonical mission identities:

```text
command:   payload.stop_acquisition
telemetry: radiation_payload.acquisition_active
```

## Requirements

The project is validated on Ubuntu through GitHub Actions. For local reproduction you need:

- Git
- Python 3 with `venv` support; Python 3.12 matches the accepted proof environment
- a normal native build toolchain suitable for F Prime
- Docker with Docker Compose v2 for the `live` proof

The runner creates its own Python virtual environment and clones every pinned dependency under `.work/`. It does not modify the Reference Mission source.

## Quick start

From the repository root:

```bash
./engineering-stories/01-one-contract-flight-ground/reference-project/run_reference_project.sh static
```

This performs the complete non-runtime proof:

```text
canonical mission -> Core Integration Input Set
                  -> F Prime projection
                  -> native F Prime generate/build
                  -> native Dictionary
                  -> OpenC3 F Prime target generation
                  -> COSMOS verification projection
                  -> identity and executable-subset checks
```

To execute the live command/telemetry loop as well:

```bash
./engineering-stories/01-one-contract-flight-ground/reference-project/run_reference_project.sh live
```

Live mode additionally starts the pinned OpenC3 COSMOS runtime and the native F Prime target, waits for the real `FPRIME_INT` connection and runs the generated verification suite.

A successful run ends with either:

```text
[reference-project] static proof PASS
```

or:

```text
[reference-project] live proof PASS
```

Generated work products are kept under:

```text
reference-project/.work/
```

and local evidence under:

```text
reference-project/.work/evidence/
```

## Project layout

```text
run_reference_project.sh
    local static/live entry point

profiles/
    fprime.yaml
    cosmos.yaml

scripts/
    materialize_fprime_story.py
    configure_fprime_server_role.py
    generate_cosmos_fprime_target.py
    run_live_fprime_cosmos.sh

evidence/
    publication-grade retained evidence for the accepted baseline
```

The canonical verification scenario remains part of the Reference Mission itself:

```text
scenarios/payload_stop_acquisition_verification.yaml
```

It is intentionally richer than the current COSMOS projection surface.

## What is downstream-owned

The Reference Project deliberately keeps downstream behavior and deployment decisions downstream.

Its minimal F Prime command handler implements:

```text
OF_StopAcquisition
    -> write OF_AcquisitionActive = false
    -> command OK
```

This is Reference Project implementation behavior. It is not generated from OrbitFabric `expected_effects`.

F Prime also remains authoritative for native deployment resolution, telemetry packet placement and Dictionary identity. The existing OpenC3 F Prime plugin owns the F Prime-to-COSMOS dictionary/transport realization, while OpenC3 COSMOS owns runtime execution semantics.

## CI reproduction

The repository also retains two authoritative workflows:

- `R1 Flight Ground Proof`
- `R1 Live Flight Ground Proof`

They execute the same accepted architecture on pinned public baselines and publish detailed run artifacts.

## Read next

- [Engineering Story](../STORY.md)
- [Technical Deep Dive](../TECHNICAL-DEEP-DIVE.md)
- [Package entry point](../README.md)
