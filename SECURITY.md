# Security Policy

## Reporting

Do not disclose unpatched vulnerabilities, authentication bypasses, exposed credentials, or cross-user data access in a public issue. Use GitHub private vulnerability reporting / Security Advisories when available and include reproduction steps, impact, and the affected route or component.

## Application boundaries

Arcana Academy uses Flask session authentication, CSRF protection, SQLAlchemy persistence, and Cloudinary-backed media workflows. Changes involving login/session behavior, user/player ownership, write APIs, uploads, database migrations, or deployment configuration require explicit security review and automated coverage where practical.

Production secrets, database URLs, Cloudinary credentials, and user data must be supplied outside source control.

## Supported version

The actively maintained `main` branch is the supported version. Security fixes should be validated through CI and released promptly with clear release notes.
