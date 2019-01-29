import datetime

from django.db import models
from django_swagger_utils.drf_server.exceptions import BadRequest


class Tournament(models.Model):
    CUSTOMER_ID_LENGTH = 20

    created_user_id = models.CharField(max_length=CUSTOMER_ID_LENGTH)
    no_of_rounds = models.PositiveIntegerField()
    start_datetime = models.DateTimeField()

    @classmethod
    def create_tournament(cls, created_user_id, no_of_rounds, start_datetime):
        cls.validate_request(no_of_rounds=no_of_rounds,
                             start_datetime=start_datetime)
        tournament = cls.objects.create(
            created_user_id=created_user_id,
            no_of_rounds=no_of_rounds,
            start_datetime=start_datetime
        )
        return tournament.convert_to_dict()

    @classmethod
    def validate_request(cls, no_of_rounds, start_datetime):
        cls.validate_no_of_rounds(no_of_rounds)
        cls.validate_start_datetime(start_datetime)

    @staticmethod
    def validate_no_of_rounds(no_of_rounds):
        if no_of_rounds <= 0:
            raise BadRequest('Invalid number of rounds')

    @staticmethod
    def validate_start_datetime(start_datetime):
        now = datetime.datetime.now()
        if start_datetime <= now:
            raise BadRequest('Invalid start_datetime')

    def convert_to_dict(self):
        return {
            "created_user_id": self.created_user_id,
            "no_of_rounds": self.no_of_rounds,
            "start_datetime": self.start_datetime
        }
