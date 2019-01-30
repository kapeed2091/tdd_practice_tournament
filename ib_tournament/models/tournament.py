from django.db import models


class Tournament(models.Model):
    total_rounds = models.IntegerField()
    start_datetime = models.DateTimeField()

    @classmethod
    def create_tournament(cls, total_rounds, start_datetime_str, name, status):
        start_datetime = cls._get_start_datetime_object(start_datetime_str)
        cls._validate_start_datetime(start_datetime)
        cls._validate_total_rounds(total_rounds)
        cls.objects.create(total_rounds=total_rounds,
                           start_datetime=start_datetime)

    @classmethod
    def get_all_tournaments(cls):
        return []

    @classmethod
    def _get_start_datetime_object(cls, start_datetime_str):
        from ib_common.date_time_utils.convert_string_to_local_date_time \
            import convert_string_to_local_date_time
        from ib_tournament.constants.general import DEFAULT_DATE_TIME_FORMAT
        return convert_string_to_local_date_time(
            start_datetime_str, DEFAULT_DATE_TIME_FORMAT)

    @classmethod
    def _validate_start_datetime(cls, start_datetime):
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        from ib_tournament.constants.exception_messages import INVALID_DATETIME
        from django_swagger_utils.drf_server.exceptions import BadRequest

        curr_datetime = get_current_local_date_time()
        if start_datetime <= curr_datetime:
            raise BadRequest(*INVALID_DATETIME)
        return

    @classmethod
    def _validate_total_rounds(cls, total_rounds):
        from django_swagger_utils.drf_server.exceptions import BadRequest
        from ib_tournament.constants.exception_messages import \
            INVALID_TOTAL_ROUNDS
        if total_rounds <= 0:
            raise BadRequest(*INVALID_TOTAL_ROUNDS)
        return
