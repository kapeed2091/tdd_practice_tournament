from django.db import models

from tdd_practice.constants.general import TournamentStatus


class Tournament(models.Model):
    name = models.CharField(max_length=50)
    no_of_rounds = models.IntegerField()
    start_datetime = models.DateTimeField()
    username = models.CharField(max_length=50)
    status = models.CharField(max_length=20,
                              default=TournamentStatus.CAN_JOIN.value)
    winner = models.ForeignKey('tournament.User', null=True)

    def convert_tournament_to_dict(self):
        return {"no_of_rounds": self.no_of_rounds,
                "start_datetime": self.start_datetime,
                "id": self.id,
                "name": str(self.name),
                "status": str(self.status)
                }

    def validate_tournament_in_can_join_status(self):
        if self._is_tournament_not_in_can_join_status():
            raise Exception("User can not join in the tournament")

    @classmethod
    def get_tournament_winner_profile(cls, tournament_id):
        tournament = cls.get_tournament_by_id(tournament_id=tournament_id)

        tournament.validate_tournament_winner()

        from .user import User
        return User.get_user_profile(user_id=tournament.winner_id)

    @classmethod
    def validate_tournament_id(cls, tournament_id):
        cls.get_tournament_by_id(tournament_id=tournament_id)

    def _is_tournament_not_in_can_join_status(self):
        return not self._is_tournament_in_can_join_status()

    def _is_tournament_in_can_join_status(self):
        return self.status == TournamentStatus.CAN_JOIN.value

    def is_tournament_not_started(self):
        return not self._is_tournament_started()

    def _is_tournament_started(self):
        return self.status == TournamentStatus.IN_PROGRESS.value

    def update_status(self, status):
        self.status = status
        self.save()

    @classmethod
    def create_tournament(cls, create_tournament_details):
        from .user import User

        no_of_rounds = create_tournament_details['no_of_rounds']
        start_datetime = create_tournament_details['start_datetime']
        username = create_tournament_details['username']

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

    def validate_tournament_winner(self):
        from .user import User
        if User.is_user_id_null(self.winner_id):
            raise Exception("Tournament winner not yet declared")
