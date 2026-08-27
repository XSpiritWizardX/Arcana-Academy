# Arcana Academy LoGD Release Closeout — 2026-08-27

## Release status

The Legend of the Green Dragon-style Arcana Academy gameplay release is merged into `main` and has passed the repository's release gates.

### Shipped
- LoGD-style forest → master → dragon prestige loop.
- Adventure progression schema migration.
- Updated production frontend bundle committed in `react-vite/dist` for the existing Docker deployment path.
- GitHub Actions maintenance for checkout, Python setup, and Node setup.
- Passing Python regression tests and compile checks.
- Passing frontend lint and production build.
- Passing Docker image build and migration/seed verification.

## Deferred from this release

The following work was intentionally not included in this release and is not required to deploy the current version:

- Flask route integration tests and focused React component coverage (issue #7).
- LoGD parity phase 2 systems such as specialties, inn, graveyard expansion, PvP, mounts, and clans (issue #18).

Those items may be reopened or recreated as future milestones when work on the next phase begins. They are being closed now so the current release has no stale deployment-blocking tickets.

## Deployment handoff

`main` is the release source of truth. The current Docker architecture remains unchanged. The deployment target should build from the latest `main` commit and use the committed production frontend bundle.
