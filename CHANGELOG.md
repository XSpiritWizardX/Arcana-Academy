# Changelog

Notable changes are documented here and published through semantic-version GitHub Releases.

## Unreleased

### Added
- Legend of the Green Dragon-inspired Adventure progression loop with limited game-day forest fights.
- Normal, thrillseeking, and slumming forest hunts with level-relative creatures, gem drops, random events, and flawless-fight bonus turns.
- Multi-round combat controls: Fight, Fight 5, Fight 10, Fight to the End, and forest fleeing.
- Academy Master challenges as the required path to level advancement instead of automatic leveling.
- Level-15 Emerald Archdragon hunt with Dragon Kill prestige resets and permanent Dragon Point allocation.
- Weapon and armor shops with tiered upgrades and trade-in value.
- Gold-based healer, death penalties, protected bank gold, bank interest, and automatic game-day resurrection/refresh.
- Persistent gems, equipment tiers, game-day state, death state, Dragon Points, and permanent Dragon bonuses.
- Classic browser-RPG town/forest interface with responsive sidebar stats and event log.
- Automated regression tests for forest progression, equipment, death, game days, master/dragon rules, and permanent Dragon bonuses.
- First automated regression suite for the turn-based game engine.
- GitHub Actions quality gates for Python tests/compile, frontend lint/build, and Docker image verification.
- Tag-driven GitHub Release automation.
- Structured issue forms, pull-request checklist, Dependabot, contribution guide, security policy, architecture docs, and release docs.

### Changed
- Adventure is now centered on a fast repeatable town → forest → gear/heal → master → dragon gameplay cycle rather than automatic area-based stat grinding.
- `turns` now represents forest fights remaining in the current Arcana game day and refreshes on a six-hour game-day cadence.
- Death now removes carried gold, reduces experience, preserves banked gold, and sends the player to the graveyard until a new game day.
- Frontend production `build` is now a one-shot Vite build; watch mode remains available as `build:watch`.
- Public project documentation is repositioned around Arcana Academy rather than the original starter template.

## Versioning

Patch releases contain compatible fixes. Minor releases contain backward-compatible features. Major releases are reserved for intentionally breaking API, schema, or platform behavior.
