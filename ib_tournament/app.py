from django.apps import AppConfig


class IbTournamentAppConfig(AppConfig):
    name = "ib_tournament"

    def ready(self):
        from ib_tournament import signals # pylint: disable=unused-variable
