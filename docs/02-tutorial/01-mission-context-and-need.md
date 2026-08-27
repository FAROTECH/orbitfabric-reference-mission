# 01, Mission Context and Need

Status: tutorial draft  
Scope: first step of the progressive Reference Mission tutorial

## Purpose

This document starts the reader-facing tutorial.

The goal is not to introduce YAML immediately. The goal is to explain why a Reference Mission needs a mission data contract at all.

OrbitFabric is useful when a small spacecraft team wants mission behavior to be explicit before implementation details dominate the work.

## Starting point

The Reference Mission begins from a simple operational need:

```text
A small spacecraft must operate a scientific payload, preserve the resulting data, react to constrained spacecraft conditions, and make the resulting evidence understandable from the ground.
```

This need is intentionally broad. It gives enough engineering pressure to justify a mission model without forcing the tutorial into vendor-specific implementation details.

## What the mission must make visible

The mission contract must make these questions answerable:

- Which spacecraft elements exist?
- Which operational states matter?
- Which telemetry values explain spacecraft behavior?
- Which commands are allowed in each situation?
- Which events make operational progress visible?
- Which data products are produced?
- Which scenario proves that the model is coherent?

At this stage, the exact YAML syntax is not the important part.

The important part is the engineering boundary.

## Reference Mission boundary

The mission is a fictional and sanitized 3U CubeSat-style scientific technology demonstrator.

It includes only the elements needed to support the initial tutorial path:

- spacecraft identity;
- subsystem topology;
- operational states;
- telemetry and command contracts;
- event and recovery semantics;
- payload lifecycle;
- data products;
- contact and downlink assumptions;
- executable scenarios.

It is not a full spacecraft design, not flight software, not an RF simulator and not a ground segment.

## Modeling rule introduced in this step

The first rule is:

```text
Operational behavior first, YAML second.
```

A model element should be introduced only when it supports an operational question, a scenario expectation or a generated evidence surface.

## What comes next

The next step introduces the spacecraft identity.

That is the smallest stable anchor for the rest of the mission contract.
