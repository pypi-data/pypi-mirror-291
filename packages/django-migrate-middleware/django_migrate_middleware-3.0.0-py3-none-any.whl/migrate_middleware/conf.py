from django.conf import settings

MIGRATE_MIDDLEWARE_COLOR_OUTPUT = getattr(
    settings, "MIGRATE_MIDDLEWARE_STDOUT_NO_COLOR", False
)
