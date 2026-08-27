# Changelog

Notable changes are documented here and published through semantic-version GitHub Releases.

## Unreleased

### Added
- First automated regression suite for the turn-based game engine.
- Tactical Adventure combat rules with telegraphed enemy strike, heavy-attack, and guard intents.
- Distinct sword, spell, defend, and flee decisions with critical hits and an Arcane Blast cooldown.
- Adventure combat-rule regression tests covering tactical counters, progression costs, defeat loss, and dragon-boss tracking.
- GitHub Actions quality gates for Python tests/compile, frontend lint/build, and Docker image verification.
- Tag-driven GitHub Release automation.
- Structured issue forms, pull-request checklist, Dependabot, contribution guide, security policy, architecture docs, and release docs.

### Changed
- Adventure area unlocks now come from the backend so client and server progression rules stay aligned.
- Active Adventure encounters are restored after a page refresh and town actions are disabled during combat.
- Training cost now scales with level, defeat loss scales with carried gold, and dragon boss victories increment the displayed kill record.
- Adventure combat UI now surfaces enemy intent, round number, spell cooldown, attack/defense stats, and tactical action guidance.
- Frontend production `build` is now a one-shot Vite build; watch mode remains available as `build:watch`.
- Public project documentation is repositioned around Arcana Academy rather than the original starter template.

## Versioning

Patch releases contain compatible fixes. Minor releases contain backward-compatible features. Major releases are reserved for intentionally breaking API, schema, or platform behavior.
