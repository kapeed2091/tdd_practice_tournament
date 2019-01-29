from django.db import models


class Tournament(models.Model):
    total_rounds = models.IntegerField()
    start_datetime = models.DateTimeField()

    @classmethod
    def create_tournament(cls, total_rounds, start_datetime_str):
        start_datetime = cls._get_start_datetime_object(start_datetime_str)
        cls.objects.create(total_rounds=total_rounds,
                           start_datetime=start_datetime)

    @classmethod
    def _get_start_datetime_object(cls, start_datetime_str):
        from ib_common.date_time_utils.convert_string_to_local_date_time \
            import convert_string_to_local_date_time
        from ib_tournament.constants.general import DEFAULT_DATE_TIME_FORMAT
        return convert_string_to_local_date_time(
            start_datetime_str, DEFAULT_DATE_TIME_FORMAT)
