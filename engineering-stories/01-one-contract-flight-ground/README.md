# Engineering Story 01 - One Mission Contract Across Flight and Ground

This package is the public entry point for the first OrbitFabric Engineering Story.

It is organized in three layers so readers can choose how deep they want to go:

```text
STORY.md
    the engineering problem, the architectural thesis, the project and the result

TECHNICAL-DEEP-DIVE.md
    detailed identities, projections, downstream ownership boundaries and evidence

reference-project/
    the reproducible project that implements and proves the demonstrated vertical slice
```

## The demonstrated slice

One canonical OrbitFabric Reference Mission contract is used as the semantic root for two independent downstream paths:

```text
payload.stop_acquisition
radiation_payload.acquisition_active
```

The flight-side path is realized natively in F Prime. The ground-side path is projected independently into an OpenC3 COSMOS verification procedure. The paths converge through the existing F Prime to OpenC3 integration and execute one live command/telemetry verification loop.

The final public Story is intentionally bounded to this demonstrated vertical slice.

## Choose your path

- **Read the Story:** [`STORY.md`](STORY.md)
- **Go deeper technically:** [`TECHNICAL-DEEP-DIVE.md`](TECHNICAL-DEEP-DIVE.md)
- **Inspect or run the project:** [`reference-project/`](reference-project/)

The Story and Technical Deep Dive are being finalized only after the executable Reference Project and its retained evidence have been stabilized.
