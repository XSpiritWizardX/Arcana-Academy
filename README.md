# Arcana Academy

[![CI](https://github.com/XSpiritWizardX/Arcana-Academy/actions/workflows/ci.yml/badge.svg)](https://github.com/XSpiritWizardX/Arcana-Academy/actions/workflows/ci.yml)

Arcana Academy is a full-stack fantasy application that combines authenticated character and equipment management with an adventure loop and turn-based combat systems. It began as a CRUD-focused Flask/React project and evolved into a larger game-oriented platform with player progression, spells, potions, swords, persistent adventure state, media uploads, and an experimental tactical engine.

This public repository is maintained as an engineering showcase: product work is tracked through GitHub issues, implemented on branches, validated by automated CI, reviewed through pull requests, and published through semantic-version GitHub Releases.

## Engineering highlights

- Flask API with Flask-Login sessions, CSRF protection, SQLAlchemy models, and Alembic migrations
- React 18 + Redux + React Router frontend with GSAP-driven interaction and fantasy-themed UI
- CRUD workflows for players, spells, potions, and swords, including image/media support through Cloudinary
- Persistent adventure state with dedicated adventure routes and database migrations
- Standalone turn-based engine with grid movement, action points, range/damage rules, turn progression, serialization, and basic enemy AI
- Automated regression coverage for deterministic game-engine behavior
- GitHub Actions quality gates for Python tests/compile, frontend lint/build, and Docker image verification
- Dependabot maintenance for Python, npm, and GitHub Actions dependencies
- Structured issues, pull-request Definition of Done, security policy, architecture documentation, and tag-driven releases

## Tech stack

| Layer | Technology |
| --- | --- |
| Frontend | React 18, Redux, React Router, Vite, GSAP, CSS |
| Backend | Flask, Flask-Login, Flask-WTF/CSRF, Flask-CORS |
| Data | SQLAlchemy, Alembic / Flask-Migrate, SQLite development database |
| Media | Cloudinary |
| Testing | Python `unittest`, source compilation, ESLint, production Vite build |
| Delivery | Docker, Gunicorn, GitHub Actions, GitHub Releases |

## Architecture

The browser owns routed UI and client state. Flask exposes authentication, player/content CRUD, adventure, and game endpoints. SQLAlchemy models provide persistence while Alembic tracks schema evolution. The tactical game engine is kept in `app/game/engine.py` so deterministic rules can be tested independently from UI behavior.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the system boundaries and quality strategy.

```text
React / Redux / Router
        |
        | /api
        v
Flask blueprints + auth/CSRF
        |
        +---- game/adventure services
        |
        v
SQLAlchemy models + Alembic migrations
        |
        v
SQLite / production database
```

## Core application areas

### Adventure and combat

`react-vite/src/components/Adventure/` and `Battle/` provide the player-facing adventure/combat surfaces. The backend exposes adventure state and game routes, while `app/game/engine.py` contains a compact turn-based rules engine used for tactical experimentation.

### Character and equipment systems

The application models and exposes players, spells, potions, swords, galleries/bags/books, stages, images, schedules/events, reviews, and related fantasy content. React forms and Redux modules handle the implemented resource workflows.

### Authentication and persistence

Flask-Login manages authenticated sessions. Flask-WTF provides CSRF protection. SQLAlchemy maps application records and `migrations/` preserves explicit database history, including later adventure-state changes.

### Media uploads

Cloudinary upload behavior is isolated behind the backend upload helper. Deployment credentials are supplied through environment variables and are never expected in source control.

## Repository layout

```text
app/
  api/                Flask blueprints for auth, resources, game, adventure
  forms/              Authentication and upload forms
  game/               Testable turn-based game engine
  models/             SQLAlchemy domain/data models
  seeds/              Development/demo seed commands
migrations/           Alembic schema history
react-vite/
  src/components/     UI, adventure, battle, CRUD surfaces
  src/redux/          Client state and API actions
  src/router/         Application routing
tests/                Automated Python regression tests
docs/                 Architecture and release documentation
.github/              CI, releases, issue forms, PR template, Dependabot
Dockerfile            Current production container definition
```

## Getting started

### Prerequisites

- Python 3.9
- Node.js 20+ and npm
- PostgreSQL for a production-like database, or the local SQLite configuration for development

### Backend

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
flask db upgrade
flask seed all
flask run
```

The checked-in `.flaskenv` identifies the Flask application for local development. Use environment variables for production secrets and service credentials.

### Frontend

```bash
cd react-vite
npm ci
npm run dev
```

For a one-shot production build:

```bash
npm run build
```

Watch-mode builds remain available separately as `npm run build:watch`.

## Testing and quality gates

Run the deterministic Python regression suite:

```bash
python -m unittest discover -s tests -v
```

Compile backend source:

```bash
python -m compileall -q app
```

Validate the frontend:

```bash
npm --prefix react-vite ci
npm --prefix react-vite run lint
npm --prefix react-vite run build
```

The CI workflow runs these checks for pull requests and pushes to `main` and also verifies the current Docker image can be built. The initial regression suite protects map boundaries, session ownership, movement rules, combat damage/action points, turn refresh behavior, and the serialized client contract.

## Development workflow

1. Create or link a GitHub issue with acceptance criteria.
2. Work on a focused branch from `main`.
3. Add or update tests and migrations alongside behavior changes.
4. Open a pull request using the repository checklist.
5. Merge only after CI is green and review concerns are resolved.
6. Record notable changes in `CHANGELOG.md`.
7. Publish semantic-version tags through the Release workflow.

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and [docs/RELEASES.md](docs/RELEASES.md).

## Release model

Tags matching `vMAJOR.MINOR.PATCH` trigger `.github/workflows/release.yml`. The workflow reruns automated verification before creating a GitHub Release with generated notes. Release publication and production deployment remain separate so a release can be verified without hiding deployment concerns.

## Known engineering follow-up

The current Dockerfile reflects an older deployment approach: it runs database migrations and seed commands while the image is being built and relies on the committed frontend bundle. That behavior is intentionally tracked as a separate issue so the container can be modernized and production-verified without mixing deployment risk into this workflow/documentation baseline.

## Security

Do not commit database URLs, Flask secrets, Cloudinary credentials, `.env` files, or real user data. Security-sensitive reports should use GitHub's private vulnerability-reporting path rather than a public issue. See [SECURITY.md](SECURITY.md).
