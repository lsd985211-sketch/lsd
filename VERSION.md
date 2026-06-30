# Versioning

Current version: `0.1.0`

## Policy

- Use Semantic Versioning.
- Bump `MAJOR` for breaking public API changes.
- Bump `MINOR` for new backward-compatible features.
- Bump `PATCH` for bug fixes and doc-only maintenance.
- Never rewrite a released tag; publish a new release instead.

## Truth source

- `VERSION.md` explains the policy.
- `CHANGELOG.md` records the historical notes.
- `releases/<version>.md` holds the draft release notes for the next publish.

## Release flow

1. Update `VERSION.md`, `CHANGELOG.md`, and `releases/<version>.md`.
2. Tag the release.
3. Create a GitHub release with notes.
4. Keep previous releases immutable.
