# Architecture

Arcana Academy is a Flask + React full-stack fantasy application that combines authenticated CRUD/resource systems with an adventure loop and a turn-based game-engine prototype.

```text
Browser
  └─ React / Redux / React Router / GSAP
       ├─ landing + authenticated navigation
       ├─ player, spell, potion, sword resource flows
       ├─ adventure + battle interfaces
       └─ /api requests
            └─ Flask
                 ├─ Flask-Login + CSRF
                 ├─ resource/adventure blueprints
                 ├─ game service
                 └─ SQLAlchemy / Alembic
                      └─ SQLite development / PostgreSQL production
```

## Major code boundaries

**Frontend:** `react-vite/src/` contains routed React surfaces, Redux modules, adventure/battle UI, resource CRUD forms, and visual interaction components.

**API:** `app/api/` separates authentication, player, spell, potion, sword, game, and adventure endpoints.

**Domain/data:** `app/models/` contains users, players, equipment/content, adventure state, and supporting entities. `migrations/` provides explicit schema history.

**Turn engine:** `app/game/engine.py` is an in-memory, testable turn-based engine with map rules, action points, movement, attack range/damage, turn progression, basic AI, and a serialized client contract.

**Media:** Cloudinary upload support is isolated behind the API upload helper rather than mixed into UI state.

## Quality strategy

The first automated regression layer targets the pure game rules because those are deterministic and high-value. CI also compiles Python sources, lints the React application, builds the frontend from source, and verifies the existing Docker image. Future coverage should add Flask route integration tests and focused React component tests.

## Deployment note

The current Dockerfile still performs migrations/seeding during image creation and relies on the committed frontend bundle. Modernizing that boundary is intentionally tracked in issue #2 so production behavior can be changed and verified independently from this workflow/documentation baseline.
