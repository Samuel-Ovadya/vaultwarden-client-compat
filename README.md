# Vaultwarden Client Compatibility

A community-maintained compatibility registry for **official, unmodified Bitwarden clients** connecting to Vaultwarden.

This project tests client/server version combinations and publishes a small JSON registry identifying the newest approved Bitwarden client release for each supported platform. Client binaries remain hosted by their official upstream distributors.

> This project is independent of Bitwarden and Vaultwarden and is not endorsed by either project.

## MVP scope

- Firefox browser extension
- Linux desktop client
- Windows desktop client
- Automated monitoring of Bitwarden client and Vaultwarden releases
- Compatibility test matrix
- Generated compatibility table and JSON registry
- Setup guidance/scripts only where the official client or platform supports a genuine configurable update source

No APK, macOS, Chrome/Chromium, binary mirroring, or modified Bitwarden client builds in the MVP.

## Compatibility policy

Compatibility is a relationship between a specific Bitwarden client version, a specific platform/build, and a specific Vaultwarden server version.

- `PASS` means the client passed the defined tests against the displayed minimum Vaultwarden version and every tested newer version in the supported range.
- `FAIL` means the client did not pass the current test policy. The table reports the latest Vaultwarden version on which it passed, if one exists.
- Untested combinations are **unknown**, never assumed compatible.
- If results are not monotonic (a newer Vaultwarden version fails while an older one passes), the project must show an explicit range/exception rather than an inaccurate `>=` claim.
- A new Bitwarden release triggers tests for that candidate.
- A new Vaultwarden release triggers retesting of supported Bitwarden client versions, including previously failing candidates.

The README table and registry are generated from the same test-result data. Do not edit generated sections manually.

## Important update-source limitation

A compatibility registry can identify the approved client version and link to official upstream downloads. It cannot automatically redirect an installed application's updater unless that application/platform supports a configurable update source.

The setup scripts in this repository must only configure documented, supported mechanisms. Where no supported mechanism exists, provide instructions or a registry-backed update check; do not patch official binaries or claim to have changed their updater.

## Repository layout

```text
.github/workflows/     CI workflows (added after the test harness is validated)
compatibility/         Policy and result schemas
registry/              Generated public JSON registry
tests/                 Platform-specific compatibility tests
setup/                 Optional platform setup helpers
scripts/               Release discovery, matrix and generation utilities
docs/                  Design and operational documentation
```

## Status

Early development. No client version is currently certified by this repository.

## Development

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [docs/TESTING.md](docs/TESTING.md).
