# Security Policy

## Supported scope

The OrbitFabric Reference Mission is a public engineering reference model and documentation workspace. It is not flight software, a spacecraft simulator, a ground segment, an authentication service or an operational spacecraft control system.

Security-sensitive maintenance applies to the current public `main` branch.

## Reporting a vulnerability

Do not report suspected security vulnerabilities through public issues, discussions or pull requests.

Use GitHub private vulnerability reporting when available, or contact the maintainers through a private channel.

A useful report should identify:

- the affected repository commit or workflow;
- the affected file, dependency or automation path;
- the observed behavior;
- the security impact;
- reproducible steps using synthetic or otherwise safe data;
- any known mitigation.

Do not include proprietary mission data, private spacecraft information, operational logs, credentials, tokens, export-controlled material, NDA-protected details or other confidential information in a vulnerability report.

## Security boundary

Relevant reports for this repository may include issues involving:

- GitHub Actions and repository automation;
- dependency handling for documentation builds;
- unsafe repository file or path handling;
- accidental exposure of sensitive information in the published documentation or repository history;
- malicious or unsafe content that can materially affect the Reference Mission publication workflow.

Issues in OrbitFabric Core parsing, validation, generation or simulation should be reported against the Core project. Issues in the OrbitFabric Studio application should be reported against Studio.

Security reporting does not relax the clean-room requirement: do not use a vulnerability report as a channel for sharing material that you are not authorized to disclose.
