from django.db import models
from django_swagger_utils.drf_server.exceptions import BadRequest

from tournament.constants.general import TournamentStatus
from tournament.utils.date_time_utils import get_current_date_time


class KoTournament(models.Model):
    USER_ID_LENGTH = 20
    NAME_LENGTH = 20
    STATUS_LENGTH = 20

    created_user_id = models.CharField(max_length=USER_ID_LENGTH)
    name = models.CharField(max_length=NAME_LENGTH)
    no_of_rounds = models.PositiveIntegerField()
    start_datetime = models.DateTimeField()
    status = models.CharField(max_length=STATUS_LENGTH)

    @classmethod
    def create_tournament(cls, created_user_id, name,
                          no_of_rounds, start_datetime,
                          status=TournamentStatus.YET_TO_START.value):
        cls._validate_request(no_of_rounds=no_of_rounds,
                              start_datetime=start_datetime,
                              user_id=created_user_id)
        tournament = cls.objects.create(
            created_user_id=created_user_id,
            name=name,
            no_of_rounds=no_of_rounds,
            start_datetime=start_datetime,
            status=status
        )
        return tournament.convert_to_dict()

    @classmethod
    def get_all_tournaments(cls):
        tournaments = cls.objects.all()
        return [each.convert_to_dict2() for each in tournaments]

    @classmethod
    def _validate_request(cls, no_of_rounds, start_datetime, user_id):
        cls._validate_user_id(user_id)
        cls._validate_no_of_rounds(no_of_rounds)
        cls._validate_start_datetime(start_datetime)

    @staticmethod
    def _validate_user_id(user_id):
        from tournament.models import User

        try:
            User.get_user(user_id=user_id)
        except User.DoesNotExist:
            raise BadRequest('Invalid user_id')

    @staticmethod
    def _validate_no_of_rounds(no_of_rounds):
        if no_of_rounds <= 0:
            raise BadRequest('Invalid number of rounds')

    @staticmethod
    def _validate_start_datetime(start_datetime):
        now = get_current_date_time()
        if start_datetime <= now:
            raise BadRequest('Invalid start_datetime')

    def convert_to_dict(self):
        return {
            "created_user_id": self.created_user_id,
            "name": self.name,
            "no_of_rounds": self.no_of_rounds,
            "start_datetime": self.start_datetime,
            "status": self.status
        }

    def convert_to_dict2(self):
        return {
            "id": self.id,
            "name": self.name,
            "no_of_rounds": self.no_of_rounds,
            "start_datetime": self.start_datetime,
            "status": self.status
        }
