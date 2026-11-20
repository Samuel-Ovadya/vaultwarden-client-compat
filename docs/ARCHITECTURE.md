# Architecture

## Source of truth

The canonical data is the compatibility result set produced by CI. From it, the project generates:

1. `registry/latest.json` — latest approved Bitwarden client version and official upstream URL per platform.
2. `registry/history.json` — historical test outcomes and the tested version pairs.
3. The generated README compatibility table.

The registry does not distribute client binaries.

## Event triggers

- Bitwarden clients release: test the new candidate against the supported Vaultwarden versions.
- Vaultwarden release: retest supported Bitwarden client versions, including previously failing versions.
- Scheduled reconciliation: discover missed releases and refresh stale results.
- Manual dispatch: run a selected or full compatibility matrix.

## Approval

A client release is approved only when its required platform-specific tests pass under the current policy. Failed or unknown candidates must never replace the last approved registry entry.

## Update-source setup

Before writing setup scripts, verify the actual updater behavior for each official distribution. Firefox, Windows desktop, and Linux desktop may have different mechanisms and constraints. A setup helper must not imply that an app's built-in updater has been redirected unless that is demonstrably supported.
