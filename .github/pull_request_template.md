## Summary

Explain the player-facing or engineering outcome and why it is needed.

## Linked issue

Closes #

## Validation

- [ ] Python regression tests pass (`python -m unittest discover -s tests -v`)
- [ ] Python source compilation passes
- [ ] Frontend lint passes (`npm run lint`)
- [ ] Frontend production build passes (`npm run build`)
- [ ] Docker build verified when deployment behavior changes
- [ ] Relevant auth/adventure/CRUD flow smoke-tested manually

## Review checklist

- [ ] New behavior includes automated coverage where practical
- [ ] Database changes include an Alembic migration
- [ ] Authorization and record ownership were considered
- [ ] No credentials, `.env` content, or production user data are committed
- [ ] README/docs/changelog are updated when behavior or workflow changes
- [ ] UI changes include screenshots or short video when useful

## Release impact

Patch / minor feature / breaking major / no release impact.
