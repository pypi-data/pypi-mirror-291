# Django Migrate Middleware

Run migrations on every request

## Install

```bash
pip install django-migrate-middleware
```

In the django settings file add package to the middleware settings.

```python
INSTALLED_APPS = [
    ...
    "migrate_middleware"
    ...
]

MIDDLEWARE = [
    "migrate_middleware.MigrateMiddleware",
    ...
]
```
## Configuration

- MIGRATE_MIDDLEWARE_COLOR_OUTPUT: force color output
