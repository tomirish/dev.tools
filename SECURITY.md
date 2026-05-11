# Security Policy

## Scope

This repository contains Python scripts that generate image assets locally using Playwright. There is no backend, no user data, no authentication, and no network-facing service.

Security issues worth reporting:
- A script fetching or executing remote content without disclosure
- A dependency with a known CVE that affects local execution

Not in scope:
- Issues that require physical access to the machine running the scripts
- Issues in Playwright, Pillow, or pytest themselves — report those upstream

## Reporting a Vulnerability

Open a [GitHub Security Advisory](https://github.com/tomirish/dev.tools/security/advisories/new) to report privately. I'll respond within a few days.
