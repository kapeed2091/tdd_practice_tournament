from django.db import models
from django_swagger_utils.drf_server.exceptions import BadRequest, NotFound

from tournament.constants.exception_messages import TOURNAMENT_DOES_NOT_EXIST_WITH_THE_GIVEN_TOURNAMENT_ID, \
    INVALID_USER_ID, INVALID_NUMBER_OF_ROUNDS, INVALID_START_DATETIME, USER_DOES_NOT_BELONG_TO_THE_TOURNAMENT, \
    OPPONENT_IS_NOT_YET_ASSIGNED
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
    def get_tournament(cls, tournament_id):
        return cls.objects.get(id=tournament_id)

    @classmethod
    def get_all_tournaments(cls):
        tournaments = cls.objects.all()
        return [each.convert_to_dict2() for each in tournaments]

    def is_final_round(self, round_number):
        if self.no_of_rounds == round_number:
            return True
        return False

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

    @classmethod
    def get_user_current_round(cls, user_id, tournament_id):
        from tournament.models import Match

        tournament = cls._get_tournament_v2(tournament_id)
        current_match = Match.get_user_current_match(
            user_id=user_id, tournament=tournament)
        cls._validate_user_current_tournament_match(current_match)
        return current_match.round

    @classmethod
    def get_opponent_user_profile(cls, user_id, tournament_round, tournament_id):
        from tournament.models import User, Match

        user = User.get_user(user_id)
        tournament = cls.get_tournament(tournament_id)
        user_match = Match.get_user_match_in_a_tournament_round(
            user=user,
            tournament_round=tournament_round,
            tournament=tournament
        )
        match_id = user_match.match_id

        opponent_user = Match.get_opponent_user_of_match(
            user=user,
            match_id=match_id
        )
        return cls._get_user_profile(opponent_user)

    @classmethod
    def get_winner_profile(cls, tournament_id):
        from tournament.models import Match

        tournament = cls.get_tournament(tournament_id)
        winner_match = Match.get_tournament_winner_match(tournament)
        winner = winner_match.user
        return cls._get_user_profile(winner)

    @classmethod
    def _get_tournament_v2(cls, tournament_id):
        try:
            return cls.get_tournament(tournament_id)
        except cls.DoesNotExist:
            raise NotFound(TOURNAMENT_DOES_NOT_EXIST_WITH_THE_GIVEN_TOURNAMENT_ID)

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
            raise BadRequest(INVALID_USER_ID)

    @staticmethod
    def _validate_no_of_rounds(no_of_rounds):
        if no_of_rounds <= 0:
            raise BadRequest(INVALID_NUMBER_OF_ROUNDS)

    @staticmethod
    def _validate_start_datetime(start_datetime):
        now = get_current_date_time()
        if start_datetime <= now:
            raise BadRequest(INVALID_START_DATETIME)

    def is_not_started(self):
        return not self._is_started()

    def _is_started(self):
        if self.status != TournamentStatus.YET_TO_START.value:
            return True
        return False

    @staticmethod
    def _validate_user_current_tournament_match(match):
        if match is None:
            raise NotFound(USER_DOES_NOT_BELONG_TO_THE_TOURNAMENT)

    @classmethod
    def _get_user_profile(cls, user):
        user_dict = user.convert_to_dict()
        user_profile = cls._remove_unnecessary_fields_for_user_profile(user_dict)
        return user_profile

    @staticmethod
    def _remove_unnecessary_fields_for_user_profile(user_dict):
        user_dict.pop('user_id')
        return user_dict

