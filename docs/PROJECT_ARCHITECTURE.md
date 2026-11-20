# Project Architecture --- Vaultwarden Client Compatibility

**Status:** Development baseline\
**Branch:** `dev`\
**Repository:**
https://github.com/Samuel-Ovadya/vaultwarden-client-compat\
**Architecture discussion:**
https://chatgpt.com/share/6b000ebe-fb4c-83eb-aad5-eb3d808d028e

> This document records the project constraints and architectural
> decisions currently established for development. It is not a
> replacement for the detailed specifications in `docs/ARCHITECTURE.md`,
> `docs/TESTING.md`, `compatibility/policy.yml`, or
> `compatibility/results.schema.json`. Those files remain authoritative
> for their respective technical details. Where a detail has not yet
> been verified against the original architecture discussion, this
> document deliberately leaves it unspecified rather than inventing a
> decision.

## 1. Purpose

The project evaluates and records compatibility between **official,
unmodified Bitwarden clients** and **Vaultwarden**.

The output is a structured, maintainable compatibility registry that
communicates which tested client/server combinations are compatible,
along with the evidence and history defined by the project's schemas and
policy.

The project is a compatibility-testing and reporting system. It is not a
client distribution service or a fork of the Bitwarden clients.

## 2. Product boundaries

### In scope

-   Test official, unmodified Bitwarden client releases against
    Vaultwarden.
-   Record compatibility outcomes in the project's defined result
    format.
-   Maintain the generated/current compatibility registry and its
    history.
-   Automate repeatable testing and registry maintenance through GitHub.
-   Preserve enough test evidence to explain and audit reported
    outcomes, following the existing testing specification.

### Explicitly out of scope

-   Modified or unofficial Bitwarden clients.
-   Mirroring, repackaging, or redistributing client binaries.
-   Hosting a permanent Vaultwarden instance or other persistent project
    infrastructure.
-   Requiring a separately operated server for routine development or
    automated testing.

A test must not silently substitute a modified client or a mirrored
binary for the official client release under evaluation.

## 3. Execution and infrastructure model

**GitHub is the project's development and automation platform.**

-   Source code, specifications, compatibility policy, schemas, and
    registry data are maintained in the GitHub repository.
-   Automated execution uses **GitHub Actions with GitHub-hosted
    runners**.
-   Test infrastructure is created temporarily within a workflow run, on
    its runner.
-   Any Vaultwarden instance and supporting test state required by a
    test run are ephemeral: they exist for the duration of that run and
    are torn down when the run ends.
-   Test execution must not depend on a permanently running VPS, home
    server, Proxmox guest, self-hosted runner, or externally hosted test
    service.
-   Workflow logs and artifacts are retained through GitHub Actions
    according to the workflow's retention configuration and repository
    policy.
-   The compatibility registry and its history are stored in the
    repository.

GitHub-hosted runners are temporary compute environments provided by
GitHub. This means the project does use GitHub's hosted CI compute, but
it does **not** operate or maintain its own persistent hosting
infrastructure.

## 4. High-level workflow

The intended lifecycle is:

1.  **Discover candidate versions** of the official Bitwarden clients
    and Vaultwarden, using the release/version sources and rules
    specified by the project.
2.  **Prepare an isolated test run** on a GitHub-hosted runner.
3.  **Start temporary test infrastructure** required for that run.
4.  **Run compatibility checks** against the official, unmodified client
    version and the selected Vaultwarden version.
5.  **Collect and validate results** against
    `compatibility/results.schema.json` and the rules in
    `compatibility/policy.yml`.
6.  **Preserve test evidence** using GitHub Actions logs/artifacts as
    specified by the testing design.
7.  **Update registry data** only through the project's defined
    registry-generation and validation process.
8.  **Tear down temporary resources**, regardless of success or failure.

The detailed test cases, version-selection rules, result semantics,
registry update rules, and failure-handling behavior must be taken from
the existing specifications. This overview does not redefine them.

## 5. Repository and branch workflow

-   `main` is the stable branch and must not be used for day-to-day
    development.
-   `dev` is the active integration and development branch.
-   Development changes are made and validated on `dev`.
-   Changes should not be merged into `main` until they have been
    reviewed and validated.
-   No public release or publication step should be introduced as part
    of ordinary development. Release/publishing behavior requires an
    explicit project decision.

## 6. Security and test isolation principles

-   Use synthetic test accounts and test data. Do not use personal or
    production Vaultwarden/Bitwarden accounts.
-   Do not commit credentials, access tokens, private keys, session
    material, or generated secrets.
-   Supply any unavoidable workflow secrets through GitHub Actions
    secrets, with the narrowest practical permissions. Prefer workflows
    that need no repository secrets.
-   Keep test data and temporary services isolated to the workflow run.
-   Do not expose a temporary Vaultwarden test service publicly unless
    an existing, explicitly approved test requirement makes that
    unavoidable. The default design is runner-local testing.
-   Clean up temporary containers, processes, files, and credentials
    even when tests fail.
-   Treat logs and uploaded artifacts as potentially sensitive; redact
    credentials and avoid storing vault contents or secret-bearing test
    data.

These are project-level guardrails. The detailed threat model and
concrete security controls should remain aligned with the existing
architecture and testing specifications.

## 7. Sources of truth and specification precedence

Use the following sources for their respective responsibilities:

  -----------------------------------------------------------------------------------------------------------------
  Source                                                                        Responsibility
  ----------------------------------------------------------------------------- -----------------------------------
  [Architecture                                                                 Original architectural decisions
  discussion](https://chatgpt.com/share/6b000ebe-fb4c-83eb-aad5-eb3d808d028e)   and rationale

  [`docs/ARCHITECTURE.md`](ARCHITECTURE.md)                                     Detailed technical architecture

  [`docs/TESTING.md`](TESTING.md)                                               Test strategy, execution, evidence,
                                                                                and test behavior

  [`compatibility/policy.yml`](../compatibility/policy.yml)                     Compatibility policy and decision
                                                                                rules

  [`compatibility/results.schema.json`](../compatibility/results.schema.json)   Machine-readable result contract

  [`registry/latest.json`](../registry/latest.json)                             Current published/generated
                                                                                registry snapshot

  [`registry/history.json`](../registry/history.json)                           Registry history

  [GitHub                                                                       Implemented source and current
  repository](https://github.com/Samuel-Ovadya/vaultwarden-client-compat)       project state
  -----------------------------------------------------------------------------------------------------------------

If this overview conflicts with a specific existing technical
specification, do not silently choose one. Record the discrepancy and
resolve it against the original architecture discussion before
implementation.

## 8. Decisions intentionally not invented here

The following details must be confirmed from the detailed specifications
and architecture discussion before implementation or modification:

-   Exact client platforms, release channels, and version-discovery
    mechanisms.
-   Exact Vaultwarden version-selection and deployment mechanism.
-   Exact compatibility test cases and pass/fail criteria.
-   Whether tests use a browser, desktop client, CLI, mobile emulator,
    or another execution mechanism for each client.
-   Matrix dimensions, scheduling cadence, retry behavior, and
    concurrency limits.
-   Exact registry generation, history, and commit automation semantics.
-   Exact artifact contents and retention periods.
-   Any required GitHub permissions, secrets, or external release APIs.

This list is intentional: an architecture document should preserve
established decisions, not turn assumptions into requirements.

## 9. Definition of an acceptable implementation

An implementation conforms to this project architecture when:

-   It tests only official, unmodified Bitwarden clients.
-   It runs through GitHub Actions on GitHub-hosted runners.
-   Any test server and supporting infrastructure are temporary and
    isolated to the workflow run.
-   It requires no persistent project-operated hosting or self-hosted
    runner.
-   It validates results against the repository's policy and schema.
-   It maintains registry data through the specified, auditable process.
-   It protects credentials and test data and cleans up temporary
    resources.
-   It respects the `dev`-first development workflow and does not change
    `main` as part of routine development.
