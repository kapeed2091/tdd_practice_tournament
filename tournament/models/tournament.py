from django.db import models


class Tournament(models.Model):
    STATUS_MAX_LENGTH = 20
    NAME_MAX_LENGTH = 50

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    user_id = models.PositiveIntegerField()
    total_rounds = models.PositiveIntegerField()
    start_datetime = models.DateTimeField()
    status = models.CharField(max_length=STATUS_MAX_LENGTH)

    @classmethod
    def create_tournament(cls, user_id, total_rounds, start_datetime):
        cls._validate_user_id(user_id=user_id)

        cls._validate_total_rounds(total_rounds=total_rounds)

        cls._validate_start_datetime(start_datetime=start_datetime)

        from ..constants.general import TournamentStatus
        Tournament.objects.create(
            user_id=user_id,
            total_rounds=total_rounds,
            start_datetime=start_datetime,
            status=TournamentStatus.CAN_JOIN.value
        )

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

    @classmethod
    def get_tournament_by_id(cls, tournament_id):
        obj = cls.objects.get(id=tournament_id)
        return obj

    @staticmethod
    def validate_tournament_status(status):
        from ..constants.general import TournamentStatus
        from ..exceptions.exceptions import InvalidFullYetToStartRegister, \
            InvalidInProgresstRegister, InvalidCompletedRegister

        if status == TournamentStatus.FULL_YET_TO_START.value:
            raise InvalidFullYetToStartRegister

        elif status == TournamentStatus.IN_PROGRESS.value:
            raise InvalidInProgresstRegister

        elif status == TournamentStatus.COMPLETED.value:
            raise InvalidCompletedRegister

    def update_status(self, status):
        self.status = status
        self.save()

    @staticmethod
    def _validate_user_id(user_id):
        from .user import User
        user_exists = User.objects.filter(id=user_id).exists()
        if not user_exists:
            from ..exceptions.exceptions import InvalidUserId
            raise InvalidUserId

    @classmethod
    def get_all_tournament_details(cls):
        details = []
        for each_obj in cls.objects.all():
            details.append(each_obj.convert_to_dict())
        details = sorted(details, key=lambda k: k['start_datetime'])
        return details

    def convert_to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "total_rounds": self.total_rounds,
            "start_datetime": self.start_datetime,
            "status": self.status
        }
