# Release Process

Arcana Academy uses semantic version tags and GitHub Releases to make shipped work easy to inspect.

## Release checklist

1. Work is linked to a GitHub issue and merged through a PR.
2. CI is green on `main`.
3. `CHANGELOG.md` describes notable changes.
4. Schema changes include reviewed Alembic migrations.
5. Auth/adventure/resource flows affected by the release receive a focused smoke test.
6. Deployment-sensitive changes verify the container and production configuration.

## Versioning

- `vX.Y.Z` patch: compatible bug/security fixes.
- `vX.Y.0` minor: backward-compatible features or meaningful gameplay/content additions.
- `vX.0.0` major: intentionally breaking API/schema/platform changes.

## Publishing

Push the intended semantic-version tag from `main`. The Release workflow reruns automated verification and uses the GitHub CLI to publish generated release notes. A failed verification prevents release publication.

GitHub release publication and production deployment are separate events; production should be smoke-tested after deployment and any remediation should be captured in a follow-up issue/PR.
