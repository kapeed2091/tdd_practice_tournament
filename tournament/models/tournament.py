from django.db import models


class Tournament(models.Model):
    user_id = models.PositiveIntegerField()
    total_rounds = models.PositiveIntegerField()
    start_datetime = models.DateTimeField()

    @classmethod
    def create_tournament(cls, user_id, total_rounds, start_datetime):

        from .user import User
        user_exists = User.objects.filter(id=user_id).exists()
        if not user_exists:
            from ..exceptions.exceptions import InvalidUserId
            raise InvalidUserId

        cls._validate_total_rounds(total_rounds=total_rounds)

        cls._validate_start_datetime(start_datetime=start_datetime)

        obj = Tournament.objects.create(
            user_id=user_id,
            total_rounds=total_rounds,
            start_datetime=start_datetime
        )
        return obj

    @staticmethod
    def _validate_start_datetime(start_datetime):
        from datetime import datetime
        now = datetime.now()

        from ib_common.date_time_utils.convert_datetime_to_local_string \
            import convert_datetime_to_local_string
        date_time_format = '%Y-%m-%d %H:%M:%S'

        start_datetime_string = convert_datetime_to_local_string(
            start_datetime, date_time_format
        )
        now_str = convert_datetime_to_local_string(
            now, date_time_format
        )
        if start_datetime_string <= now_str:
            from ..exceptions.exceptions import InvalidStartDateTime
            raise InvalidStartDateTime

    @staticmethod
    def _validate_total_rounds(total_rounds):
        if total_rounds < 1:
            from ..exceptions.exceptions import InvalidTotalRounds
            raise InvalidTotalRounds

    @classmethod
    def validate_tournament_id(cls, tournament_id):
        tournament_exists = cls.objects.filter(id=tournament_id).exists()

        if not tournament_exists:
            from ..exceptions.exceptions import InvalidTournamentId
            raise InvalidTournamentId
