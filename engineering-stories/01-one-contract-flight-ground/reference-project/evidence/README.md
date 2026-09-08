# Retained evidence

This directory contains the stable, publication-grade evidence selected from the accepted Reference Project baseline.

It is intentionally **not** a history of development runs. The public package keeps the smallest durable set of facts needed to inspect the Engineering Story after transient GitHub Actions artifacts expire.

## Accepted baseline

`accepted-baseline.json` is the provenance index for the post-packaging Reference Project acceptance. It records the exact project commit, pinned downstream baselines, canonical/native identities, workflow acceptance and artifact digests.

## Retained artifacts

```text
accepted-baseline.json
    accepted Reference Project provenance and exact baselines

openc3-fprime-dry-run.json
    native F Prime Dictionary -> OpenC3 F Prime identity handoff

cosmos-verification-plan.json
    exact canonical Scenario accounting and executable-subset projection

cosmos-verification.py
    exact generated COSMOS procedure used by the accepted proof

live-proof.json
    compact live-loop result produced by the runtime harness

fprime-runtime.txt
    selected native F Prime connection and command-dispatch evidence

cosmos-runtime.txt
    selected OpenC3 interface-readiness and Script Runner result

evidence-set.json
    portable OrbitFabric Evidence Set Manifest for the retained runtime evidence

SHA256SUMS
    SHA-256 digests for the retained files above
```

The complete native Dictionary and verbose runtime logs remain reproducible through the Reference Project and are also published by the acceptance workflows. They are deliberately not duplicated here because they add volume without improving the public architectural claim.

## Evidence Set boundary

`evidence-set.json` uses the candidate generic OrbitFabric `orbitfabric.evidence_set_manifest / 0.1-candidate` contract.

It deliberately indexes only these retained evidence objects:

```text
fprime-runtime.txt
cosmos-runtime.txt
live-proof.json
```

The other retained files remain useful, but they have different roles:

```text
accepted-baseline.json        Story acceptance/provenance record
openc3-fprime-dry-run.json    identity-handoff characterization
cosmos-verification-plan.json projection artifact
cosmos-verification.py        generated artifact
SHA256SUMS                    byte-integrity inventory
```

File presence therefore does not make a file generic evidence. Evidence inclusion and subject-correlation claims are curator-owned and explicit in the manifest.

The manifest correlates retained evidence to exact upstream identities from the accepted R1 proof, including the canonical Scenario SHA, Core-normalized Scenario atom ids, exact Integration Result SHA-256 values and selected Result mapping/artifact ids. The Integration Result files themselves do not need to be duplicated into this retained evidence bundle because their exact SHA-256 values are the subject identities.

Producer-specific fields such as `status`, native target names and Script Runner results remain inside their producer-owned content. The generic manifest does not promote those fields into a universal OrbitFabric verdict.

## Evidence policy

The evidence directory preserves **accepted facts**, not CI archaeology. A failed run is included only when a specific falsification is necessary to explain an architectural lesson in the Technical Deep Dive.
