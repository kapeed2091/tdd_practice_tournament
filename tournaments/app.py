from django.apps import AppConfig


class TournamentAppConfig(AppConfig):
    name = "tournaments"

    def ready(self):
        from tournaments import signals # pylint: disable=unused-variable
