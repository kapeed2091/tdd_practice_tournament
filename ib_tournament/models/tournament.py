from django.db import models
from ib_tournament.constants.general import TournamentStatus


class Tournament(models.Model):
    total_rounds = models.IntegerField()
    start_datetime = models.DateTimeField()
    name = models.CharField(max_length=50)
    status = models.CharField(
        max_length=50, default=TournamentStatus.CAN_JOIN.value)

    @classmethod
    def create_tournament(cls, total_rounds, start_datetime_str, name):
        start_datetime = cls._get_start_datetime_object(start_datetime_str)
        cls._validate_start_datetime(start_datetime)
        cls._validate_total_rounds(total_rounds)
        tournament = cls._create_tournament_object(
            total_rounds, start_datetime, name)
        return tournament.id

    @classmethod
    def get_all_tournaments(cls):
        tournaments = cls._get_all_tournament_objects()
        ordered_tournaments = cls._order_tournaments(tournaments)
        return cls._get_tournament_details(ordered_tournaments)

    def get_tournament_dict(self):
        from ib_common.date_time_utils.convert_datetime_to_local_string import \
            convert_datetime_to_local_string
        from ib_tournament.constants.general import DEFAULT_DATE_TIME_FORMAT
        return {
            'tournament_id': self.id,
            'name': self.name,
            'status': self.status,
            'start_datetime': convert_datetime_to_local_string(
                self.start_datetime, DEFAULT_DATE_TIME_FORMAT),
            'total_rounds': self.total_rounds
        }

    @classmethod
    def subscribe_to_tournament(cls, tournament_id, player_id):
        from ib_tournament.models import TournamentPlayer, Player

        Player.get_player_by_id(player_id)
        tournament = cls.get_tournament(tournament_id)
        cls._validate_tournament_state_to_subscribe(tournament.status)
        cls._validate_player_already_subscribed(tournament_id, player_id)
        TournamentPlayer.create_tournament_player(tournament_id, player_id)
        tournament.update_status_to_full_yet_to_start()
        return

    @classmethod
    def get_tournament(cls, tournament_id):
        try:
            return cls.objects.get(id=tournament_id)
        except cls.DoesNotExist:
            from django_swagger_utils.drf_server.exceptions import BadRequest
            from ib_tournament.constants.exception_messages import \
                INVALID_TOURNAMENT
            raise BadRequest(*INVALID_TOURNAMENT)

    def update_status_to_full_yet_to_start(self):
        from ib_tournament.constants.general import TournamentStatus
        if self._get_max_participants_count_reached():
            self._update_tournament_status(
                TournamentStatus.FULL_YET_TO_START.value)
        return

    @classmethod
    def create_tournament_by_player(cls, player_id, tournament_details):
        from ib_tournament.models import Player
        Player.get_player_by_id(player_id)

        total_rounds = tournament_details['total_rounds']
        start_datetime = cls._get_start_datetime_object(
            tournament_details['start_datetime_str'])
        cls._validate_start_datetime(start_datetime)
        cls._validate_total_rounds(total_rounds)
        tournament = cls._create_tournament_object(
            total_rounds, start_datetime, tournament_details['name'])
        return tournament.id

    @classmethod
    def _get_start_datetime_object(cls, start_datetime_str):
        from ib_common.date_time_utils.convert_string_to_local_date_time \
            import convert_string_to_local_date_time
        from ib_tournament.constants.general import DEFAULT_DATE_TIME_FORMAT
        return convert_string_to_local_date_time(
            start_datetime_str, DEFAULT_DATE_TIME_FORMAT)

    @classmethod
    def _validate_start_datetime(cls, start_datetime):
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        from ib_tournament.constants.exception_messages import INVALID_DATETIME
        from django_swagger_utils.drf_server.exceptions import BadRequest

        curr_datetime = get_current_local_date_time()
        if start_datetime <= curr_datetime:
            raise BadRequest(*INVALID_DATETIME)
        return

    @classmethod
    def _validate_total_rounds(cls, total_rounds):
        from django_swagger_utils.drf_server.exceptions import BadRequest
        from ib_tournament.constants.exception_messages import \
            INVALID_TOTAL_ROUNDS
        if total_rounds <= 0:
            raise BadRequest(*INVALID_TOTAL_ROUNDS)
        return

    @classmethod
    def _create_tournament_object(cls, total_rounds, start_datetime, name):
        tournament = cls.objects.create(total_rounds=total_rounds,
                                        start_datetime=start_datetime,
                                        name=name)
        return tournament

    @classmethod
    def _get_all_tournament_objects(cls):
        return cls.objects.all()

    @classmethod
    def _order_tournaments(cls, tournaments):
        tournaments = tournaments.order_by('status', 'start_datetime')

        from ib_tournament.constants.general import TournamentStatus
        ordered_status = [TournamentStatus.FULL_YET_TO_START.value,
                          TournamentStatus.CAN_JOIN.value,
                          TournamentStatus.IN_PROGRESS.value,
                          TournamentStatus.COMPLETED.value]
        ordered_tournaments = sorted(
            tournaments, key=lambda x: ordered_status.index(x.status))
        return ordered_tournaments

    @classmethod
    def _get_tournament_details(cls, tournaments):
        return [tournament.get_tournament_dict()
                for tournament in tournaments]

    @staticmethod
    def _validate_tournament_state_to_subscribe(status):
        from ib_tournament.constants.general import TournamentStatus
        from django_swagger_utils.drf_server.exceptions import BadRequest
        from ib_tournament.constants.exception_messages import \
            INVALID_TOURNAMENT_STATE

        if status != TournamentStatus.CAN_JOIN.value:
            raise BadRequest(*INVALID_TOURNAMENT_STATE)
        return

    @classmethod
    def _validate_player_already_subscribed(cls, tournament_id, player_id):
        from ib_tournament.models import TournamentPlayer
        from django_swagger_utils.drf_server.exceptions import BadRequest
        from ib_tournament.constants.exception_messages import \
            CAN_NOT_SUBSCRIBE_AGAIN
        if TournamentPlayer.get_tournament_player_exists(
                tournament_id, player_id):
            raise BadRequest(CAN_NOT_SUBSCRIBE_AGAIN)
        return

    def _get_max_participants_count_reached(self):
        from ib_tournament.models import TournamentPlayer
        total_tournament_players = \
            TournamentPlayer.get_tournament_players_count(self.id)
        return total_tournament_players == \
               self._get_maximum_players_in_tournament()

    def _update_tournament_status(self, status):
        self.status = status
        self.save()

    def _get_maximum_players_in_tournament(self):
        total_rounds = self.total_rounds
        return 2 ** total_rounds
