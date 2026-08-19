# Contributing

Arcana Academy uses an issue-first pull-request workflow. The repository is intentionally public so both the application and the engineering process are inspectable.

## Development workflow

1. Start from a GitHub issue with scope and acceptance criteria.
2. Branch from `main` using a focused prefix such as `feat/`, `fix/`, `test/`, `docs/`, or `chore/`.
3. Keep database migrations, tests, and documentation with the behavior they support.
4. Run the local quality checks below.
5. Open a pull request that links the issue and identifies release impact.
6. Merge only after CI passes and review comments are resolved.

## Quality checks

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m compileall -q app
npm --prefix react-vite ci
npm --prefix react-vite run lint
npm --prefix react-vite run build
```

Deployment-sensitive changes should also verify the Docker image and smoke-test the affected authenticated/adventure flow.

## Definition of done

A change is done when the implementation is complete, automated coverage protects important behavior, CI is green, schema changes include migrations, documentation is current, and the PR explains validation and release impact.

Never commit secrets, production database URLs, Cloudinary credentials, `.env` files, or real user data.
