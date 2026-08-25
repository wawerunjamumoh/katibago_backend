# KatibaGo Backend Agent Guide

## Project shape

- This is a Django 6 backend using Django REST Framework and SQLite for local development.
- The main domain app is `apps.content`; its models, API, admin, services, migrations, and tests live beneath that package.
- Project configuration and top-level routing are in `config/`; the versioned API is mounted at `/api/v1/` in `config/urls.py`.
- Prefer the learner workflow endpoints (`/learn/`, `/me/`, and article/decision workflow actions) for learner-facing behavior. DRF router resources are primarily content-management endpoints.

## Commands

Run commands from the repository root with the project virtual environment active:

```bash
source .venv/bin/activate
python manage.py check
python manage.py test
python manage.py test apps.content.tests.test_auth_api apps.content.tests.test_learner_workflow
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Run the narrowest relevant test after a change. Use `check` and the full suite before completing cross-cutting changes. Do not edit generated migration files by hand; change models, generate a migration, and review the generated result.

## Implementation conventions

- Keep business workflows in `apps/content/services/` and keep API views focused on HTTP concerns. Reuse services from admin actions and API actions instead of duplicating workflow logic.
- Keep serializers and API views under `apps/content/api/`; add version-specific routes under `apps/content/api/v1/`.
- Put model definitions in the existing per-model modules under `apps/content/models/`, and preserve the exports in `apps/content/models/__init__.py`.
- Add behavior-focused Django tests under `apps/content/tests/`. Use DRF `APIClient` for endpoint contracts and Django `TestCase` for service/model behavior.
- Preserve ownership and publication rules: learner endpoints are authenticated and user-scoped; inactive articles are unavailable to learners; article completion must use the existing progress and XP services.
- Use existing relationships and constraints before adding fields or abstractions. Check the relevant domain contract before changing model ownership or cardinality.

## Compatibility details

- Preserve established public spellings such as `SafteyShield`, `SafteyShieldViewset`, `saftey_shields`, and `/safteyshields/` unless a deliberate compatibility change is requested.
- The repository uses `Readme.md` and `docs/enginnering/` with those spellings; link to them as they exist rather than renaming them incidentally.
- Local development uses the checked-in `db.sqlite3`; tests create isolated test data. Avoid modifying the database as part of source changes.
- Treat the current development settings and secret as non-production configuration. Do not expose credentials or broaden production behavior while making an unrelated feature change.
- After every changes,run tests.

## References

- API usage and test commands: [Readme.md](Readme.md)
- Domain contracts: [docs/enginnering/contracts.txt](docs/enginnering/contracts.txt)
- Detailed entity contracts: [docs/enginnering/contracts/](docs/enginnering/contracts/)
- Domain design notes: [docs/enginnering/designs/](docs/enginnering/designs/)
- Curriculum and engineering documentation: [docs/](docs/)
