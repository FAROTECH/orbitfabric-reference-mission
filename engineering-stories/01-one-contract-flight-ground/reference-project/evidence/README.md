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

SHA256SUMS
    SHA-256 digests for the retained files above
```

The complete native Dictionary and verbose runtime logs remain reproducible through the Reference Project and are also published by the acceptance workflows. They are deliberately not duplicated here because they add volume without improving the public architectural claim.

## Evidence policy

The evidence directory preserves **accepted facts**, not CI archaeology. A failed run is included only when a specific falsification is necessary to explain an architectural lesson in the Technical Deep Dive.
