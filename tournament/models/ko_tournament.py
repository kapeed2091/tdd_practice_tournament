from django.db import models
from tournament.constants import TournamentStatus
from tournament.constants.general import T_ID_MAX_LENGTH


class KOTournament(models.Model):
    TOURNAMENT_NAME_MAX_LENGTH = 30
    TOURNAMENT_STATUS_MAX_LENGTH = 30

    t_id = models.CharField(max_length=T_ID_MAX_LENGTH, unique=True)
    name = models.CharField(max_length=TOURNAMENT_NAME_MAX_LENGTH)
    number_of_rounds = models.IntegerField()
    start_datetime = models.DateTimeField()
    status = models.CharField(max_length=TOURNAMENT_STATUS_MAX_LENGTH,
                              default=TournamentStatus.CAN_JOIN.value)

    @classmethod
    def create_tournament(cls, user_id, name, number_of_rounds,
                          start_datetime, status):
        cls.validate_create_request(
            user_id=user_id, number_of_rounds=number_of_rounds,
            start_datetime=start_datetime, status=status)

        t_id = cls.generate_t_id()
        tournament = cls.assign_t_id_to_tournament(
            t_id=t_id, name=name, number_of_rounds=number_of_rounds,
            start_datetime=start_datetime, status=status)

        return tournament.convert_to_dict()

    @classmethod
    def get_all_tournaments(cls, user_id):
        from tournament.models import UserProfile
        UserProfile.is_registered_user(user_id=user_id)

        tournaments = cls.all_tournaments()
        all_tournaments = cls.all_tournaments_list(tournaments=tournaments)

        return all_tournaments

    @staticmethod
    def generate_t_id():
        import uuid
        from tournament.constants.general import T_ID_MAX_LENGTH
        return str(uuid.uuid4())[0:T_ID_MAX_LENGTH]

    @classmethod
    def assign_t_id_to_tournament(cls, t_id, name, number_of_rounds,
                                  start_datetime, status):
        return cls.objects.create(
            t_id=t_id, name=name, number_of_rounds=number_of_rounds,
            start_datetime=start_datetime, status=status)

    @classmethod
    def validate_create_request(cls, user_id, number_of_rounds, start_datetime,
                                status):
        from tournament.models import UserProfile

        UserProfile.is_registered_user(user_id=user_id)
        cls.is_valid_number_of_rounds(number_of_rounds=number_of_rounds)
        cls.is_valid_start_datetime(start_datetime=start_datetime)
        cls.is_valid_creation_status(status=status)

    def convert_to_dict(self):
        return {'t_id': str(self.t_id), 'name': str(self.name),
                'number_of_rounds': self.number_of_rounds,
                'start_datetime': self.start_datetime,
                'status': str(self.status)}

    @classmethod
    def all_tournaments(cls):
        return cls.objects.all()

    @classmethod
    def all_tournaments_list(cls, tournaments):
        all_tournaments = list()
        for tournament in tournaments:
            all_tournaments.append(tournament.convert_to_dict())

        return all_tournaments

    @classmethod
    def is_valid_number_of_rounds(cls, number_of_rounds):
        cls.is_non_int_type(number_of_rounds=number_of_rounds)
        cls.is_non_positive(number_of_rounds=number_of_rounds)

    @staticmethod
    def is_valid_start_datetime(start_datetime):
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time

        if start_datetime < get_current_local_date_time():
            raise Exception('Start datetime is less than current time')

    @staticmethod
    def is_valid_creation_status(status):
        from tournament.constants import TournamentStatus
        if status != TournamentStatus.CAN_JOIN.value:
            raise Exception('Invalid Tournament Status at creation')

    @staticmethod
    def is_non_positive(number_of_rounds):
        if number_of_rounds <= 0:
            raise Exception('Non-positive number of rounds given')

    @staticmethod
    def is_non_int_type(number_of_rounds):
        if type(number_of_rounds) != int:
            raise Exception('Float type number of rounds given')

    @classmethod
    def validate_tournament(cls, tournament_id):
        try:
            cls.objects.get(t_id=tournament_id)
        except:
            from tournament.constants.exception_messages import \
                TOURNAMENT_DOES_NOT_EXIST
            raise Exception(*TOURNAMENT_DOES_NOT_EXIST)

    def is_tournament_started(self):
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time

        if self.start_datetime < get_current_local_date_time():
            raise Exception('Tournament has started')

    @classmethod
    def get_tournament(cls, tournament_id):
        return cls.objects.get(t_id=tournament_id)

    def is_valid_subscribe_status(self):
        if self.status != TournamentStatus.CAN_JOIN.value:
            raise Exception('Invalid Tournament Status to subscribe')

    @classmethod
    def get_max_users_count(cls, tournament_id):
        tournament = cls.get_tournament(tournament_id=tournament_id)
        return pow(2, tournament.number_of_rounds)

    @classmethod
    def change_tournament_status_to_full(cls, tournament_id):
        tournament = cls.get_tournament(tournament_id=tournament_id)
        tournament.status = TournamentStatus.FULL_YET_TO_START.value
        tournament.save()

    @classmethod
    def validate_subscribe_request(cls, tournament_id):
        cls.validate_tournament(tournament_id=tournament_id)
        tournament_obj = cls.get_tournament(tournament_id=tournament_id)
        tournament_obj.is_tournament_started()
        tournament_obj.is_valid_subscribe_status()

    @classmethod
    def validate_start_datetime(cls, tournament_id):
        tournament_obj = cls.get_tournament(tournament_id=tournament_id)
        if tournament_obj.is_start_datetime_in_future():
            from tournament.constants.exception_messages import \
                CANNOT_CREATE_MATCH_BEFORE_START_DATETIME
            raise Exception(*CANNOT_CREATE_MATCH_BEFORE_START_DATETIME)

    def is_start_datetime_in_future(self):
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        if self.start_datetime > get_current_local_date_time():
            return True
        else:
            return False

    @classmethod
    def validate_start_datetime_for_play_match(cls, tournament_id):
        tournament_obj = cls.get_tournament(tournament_id=tournament_id)
        if tournament_obj.is_start_datetime_in_future():
            from tournament.constants.exception_messages import \
                CANNOT_PLAY_MATCH_BEFORE_START_DATETIME
            raise Exception(*CANNOT_PLAY_MATCH_BEFORE_START_DATETIME)

    @classmethod
    def validate_tournament_for_create_match(cls, tournament_id):
        cls.validate_tournament(tournament_id=tournament_id)
        cls.validate_start_datetime(tournament_id=tournament_id)
