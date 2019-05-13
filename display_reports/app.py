from django.apps import AppConfig


class DisplayReportsAppConfig(AppConfig):
    name = "display_reports"

    def ready(self):
        from display_reports import signals # pylint: disable=unused-variable
