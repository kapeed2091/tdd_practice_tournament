from django.apps import AppConfig


class TournamentAppConfig(AppConfig):
    name = "tournament"

    def ready(self):
        from tournament import signals # pylint: disable=unused-variable
