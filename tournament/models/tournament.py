from django.db import models

from tdd_practice.constants.general import TournamentStatus


class Tournament(models.Model):
    name = models.CharField(max_length=50)
    no_of_rounds = models.IntegerField()
    start_date_time = models.DateTimeField()
    username = models.CharField(max_length=50)
    status = models.CharField(max_length=20,
                              default=TournamentStatus.CAN_JOIN.value)

    def convert_tournament_to_dict(self):
        start_datetime_str = \
            self.start_date_time.strftime("%Y-%m-%d %H:%M:%S")

        return {"no_of_rounds": self.no_of_rounds,
                "start_datetime": start_datetime_str,
                "id": self.id,
                "name": self.name,
                "status": self.status
                }

    @classmethod
    def create_tournament(cls, no_of_rounds, start_date_time, username):
        from .user import User

        cls.validate_start_datetime(start_datetime=start_date_time)
        cls.validate_no_of_rounds(no_of_rounds=no_of_rounds)
        User.validate_username(username=username)

        tournament_obj = cls.objects.create(
            no_of_rounds=no_of_rounds,
            start_date_time=start_date_time, username=username)

        return tournament_obj.convert_tournament_to_dict()

    @classmethod
    def validate_start_datetime(cls, start_datetime):
        from datetime import datetime
        if datetime.now() > start_datetime:
            raise Exception("Expected future date time")

    @classmethod
    def validate_no_of_rounds(cls, no_of_rounds):
        if no_of_rounds <= 0:
            raise Exception("Invalid no of rounds")

    @classmethod
    def get_all_tournaments(cls):
        tournament_objs = cls.objects.all().order_by('-start_date_time')

        tournaments = []

        for tournament_obj in tournament_objs:
            tournaments.append(tournament_obj.convert_tournament_to_dict())

        return tournaments

