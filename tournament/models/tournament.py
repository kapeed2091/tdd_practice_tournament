from django.db import models

from tdd_practice.constants.general import TournamentStatus


class Tournament(models.Model):
    name = models.CharField(max_length=50)
    no_of_rounds = models.IntegerField()
    start_datetime = models.DateTimeField()
    username = models.CharField(max_length=50)
    status = models.CharField(max_length=20,
                              default=TournamentStatus.CAN_JOIN.value)

    def convert_tournament_to_dict(self):
        return {"no_of_rounds": self.no_of_rounds,
                "start_datetime": self.start_datetime,
                "id": self.id,
                "name": str(self.name),
                "status": str(self.status)
                }

    @classmethod
    def validate_tournament_in_can_join_status(cls, tournament_id):
        try:
            cls.get_tournament(tournament_id=tournament_id,
                               status=TournamentStatus.CAN_JOIN.value)
        except Exception:
            raise Exception("User can not join in the tournament")

    @classmethod
    def validate_tournament_id(cls, tournament_id):
        cls.get_tournament_by_id(tournament_id=tournament_id)

    @classmethod
    def update_tournament_status(cls, tournament_id, status):
        tournament = cls.get_tournament_by_id(tournament_id=tournament_id)
        tournament.status = status
        tournament.save()

    @classmethod
    def create_tournament(cls, no_of_rounds, start_datetime, username):
        from .user import User

        cls.validate_start_datetime(start_datetime=start_datetime)
        cls.validate_no_of_rounds(no_of_rounds=no_of_rounds)
        User.validate_username(username=username)

        tournament_obj = cls.objects.create(
            no_of_rounds=no_of_rounds,
            start_datetime=start_datetime, username=username)

        return tournament_obj.convert_tournament_to_dict()

    @classmethod
    def validate_start_datetime(cls, start_datetime):
        from ib_common.date_time_utils.get_current_local_date_time \
            import get_current_local_date_time

        curr_datetime = get_current_local_date_time()

        if curr_datetime > start_datetime:
            raise Exception("Expected future date time")

    @classmethod
    def validate_no_of_rounds(cls, no_of_rounds):
        if no_of_rounds <= 0:
            raise Exception("Invalid no of rounds")

    @classmethod
    def get_all_tournaments(cls):
        tournament_objs = cls.objects.all().order_by('-start_datetime')

        tournaments = []

        for tournament_obj in tournament_objs:
            tournaments.append(tournament_obj.convert_tournament_to_dict())

        return tournaments

    @classmethod
    def get_tournament(cls, tournament_id, status):
        try:
            return cls.objects.get(id=tournament_id, status=status)
        except cls.DoesNotExist:
            raise Exception(
                "No tournament exists with given tournament id and status")

    @classmethod
    def get_tournament_by_id(cls, tournament_id):
        try:
            return cls.objects.get(id=tournament_id)
        except cls.DoesNotExist:
            raise Exception("Invalid tournament id")

    @classmethod
    def get_no_of_participants_can_join(cls, tournament_id):
        tournament = cls.get_tournament_by_id(tournament_id=tournament_id)

        return cls.calculate_no_participants(
            no_of_rounds=tournament.no_of_rounds)

    @classmethod
    def calculate_no_participants(cls, no_of_rounds):
        return 2**no_of_rounds
