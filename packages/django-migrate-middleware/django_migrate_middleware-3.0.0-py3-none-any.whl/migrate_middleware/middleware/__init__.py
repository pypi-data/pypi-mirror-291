from django.core.management import call_command

from ..conf import MIGRATE_MIDDLEWARE_COLOR_OUTPUT


class MigrateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Call migrate on every call
        kwargs = {"interactive": False}
        if MIGRATE_MIDDLEWARE_COLOR_OUTPUT:
            kwargs.update(force_color=True)
        else:
            kwargs.update(no_color=True)
        call_command("migrate", **kwargs)
        return self.get_response(request)
