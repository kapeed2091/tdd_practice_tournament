from django.db import models
from tournament.constants import TournamentStatus


class KOTournament(models.Model):
    T_ID_MAX_LENGTH = 20
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
        cls.is_registered_user(user_id=user_id)
        tournaments = cls.all_tournaments()
        all_tournaments = cls.all_tournaments_list(tournaments=tournaments)

        return all_tournaments

    @classmethod
    def generate_t_id(cls):
        import uuid
        return str(uuid.uuid4())[0:cls.T_ID_MAX_LENGTH]

    @classmethod
    def assign_t_id_to_tournament(cls, t_id, name, number_of_rounds,
                                  start_datetime, status):
        return cls.objects.create(
            t_id=t_id, name=name, number_of_rounds=number_of_rounds,
            start_datetime=start_datetime, status=status)

    @classmethod
    def validate_create_request(cls, user_id, number_of_rounds, start_datetime,
                                status):
        cls.is_registered_user(user_id=user_id)
        cls.is_valid_number_of_rounds(number_of_rounds=number_of_rounds)
        cls.is_start_datetime_in_past(start_datetime=start_datetime)
        cls.is_valid_creation_status(status=status)

    def convert_to_dict(self):
        return {'t_id': str(self.t_id), 'name': str(self.name),
                'number_of_rounds': self.number_of_rounds,
                'start_datetime': self.start_datetime,
                'status': str(self.status)}

    @classmethod
    def is_valid_number_of_rounds(cls, number_of_rounds):
        cls.is_non_int_type(number_of_rounds=number_of_rounds)
        cls.is_non_positive(number_of_rounds=number_of_rounds)

    @staticmethod
    def is_start_datetime_in_past(start_datetime):
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
    def is_registered_user(user_id):
        from tournament.models import UserProfile
        try:
            UserProfile.get_user(user_id=user_id)
        except models.ObjectDoesNotExist:
            raise Exception('User not registered')

    @classmethod
    def all_tournaments(cls):
        return cls.objects.all()

    @classmethod
    def all_tournaments_list(cls, tournaments):
        all_tournaments = list()
        for tournament in tournaments:
            all_tournaments.append(tournament.convert_to_dict())

        return all_tournaments

    @staticmethod
    def is_non_positive(number_of_rounds):
        if number_of_rounds <= 0:
            raise Exception('Non-positive number of rounds given')

    @staticmethod
    def is_non_int_type(number_of_rounds):
        if type(number_of_rounds) != int:
            raise Exception('Float type number of rounds given')
