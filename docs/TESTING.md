# Testing policy

## Test dimensions

Each result must identify:

- Bitwarden client version
- Platform and artifact/build variant
- Vaultwarden server version
- Test-suite revision
- Run timestamp
- Result (`pass`, `fail`, or `error`)
- Relevant logs/artifact references

## Minimum smoke-test goals

The test plan should cover, where supported by the client:

- Server URL configuration and connection
- Authentication
- Vault unlock
- Initial vault sync
- Create, read, update and delete an item
- Sync after changes
- Logout and re-authentication

Tests must use disposable test accounts and synthetic data. Never use a real vault or real credentials in CI.

## Compatibility summary rules

A `>=` minimum is valid only when the minimum and all relevant newer tested versions pass, with no known failing gaps in the declared range. If results are non-monotonic, represent explicit ranges/exceptions. For a failing client, report its latest known working Vaultwarden version only when that exact pair has passed.

A missing test result is unknown, not pass.
