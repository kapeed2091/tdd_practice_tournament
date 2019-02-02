from django.db import models
from ib_tournament.constants.general import TMPlayerStatus


class TMPlayer(models.Model):
    player = models.ForeignKey('ib_tournament.Player')
    tournament_match = models.ForeignKey('ib_tournament.TournamentMatch')
    status = models.CharField(max_length=50,
                              default=TMPlayerStatus.YET_TO_START.value)
    score = models.IntegerField(default=0)
    completed_datetime = models.DateTimeField(
        default=None, null=True, blank=True)

    class Meta:
        unique_together = ('player', 'tournament_match')

    @classmethod
    def add_players_to_matches(cls, tournament_id):
        from ib_tournament.models import TournamentPlayer, TournamentMatch
        player_ids = TournamentPlayer.get_player_ids_of_tournament(
            tournament_id)
        grouped_player_ids = cls._group_players_as_group_of_two(player_ids)
        tournament_match_ids = TournamentMatch.\
            get_tournament_match_ids_of_tournament(tournament_id)
        cls._add_grouped_players_to_match(
            grouped_player_ids, tournament_match_ids)
        return

    @classmethod
    def play_match(cls, player_id, tournament_match_id):
        from ib_tournament.constants.general import TMPlayerStatus
        tm_player = cls._get_tm_player(player_id, tournament_match_id)
        cls._validate_status_to_play(tm_player.status)
        cls._update_status(tm_player, TMPlayerStatus.IN_PROGRESS.value)
        return

    @classmethod
    def submit_score(cls, player_id, tournament_match_id, score):
        from ib_tournament.constants.general import TMPlayerStatus
        tm_player = cls._get_tm_player(player_id, tournament_match_id)
        cls._validate_status_to_submit_score(tm_player.status)
        cls._update_score(tm_player, score)
        cls._update_status(tm_player, TMPlayerStatus.COMPLETED.value)
        cls._update_completed_datetime(tm_player)
        cls._update_match_winner(tournament_match_id)
        return

    @staticmethod
    def _group_players_as_group_of_two(player_ids):
        return [player_ids[count: count + 2]
                for count in range(0, len(player_ids), 2)]

    @classmethod
    def _add_grouped_players_to_match(
            cls, grouped_player_ids, tournament_match_ids):
        tm_players_to_create = list()
        for index, player_ids in enumerate(grouped_player_ids):
            tournament_match_id = tournament_match_ids[index]
            tm_players_to_create.extend(cls._initialise_tm_players(
                player_ids, tournament_match_id))
        cls.objects.bulk_create(tm_players_to_create)
        return

    @classmethod
    def _initialise_tm_players(cls, player_ids, t_match_id):
        return [cls(player_id=player_id, tournament_match_id=t_match_id)
                for player_id in player_ids]

    @classmethod
    def _validate_status_to_play(cls, status):
        from ib_tournament.constants.general import TMPlayerStatus
        from django_swagger_utils.drf_server.exceptions import BadRequest
        from ib_tournament.constants.exception_messages import \
            TM_PLAYER_NOT_IN_YET_TO_START
        if status != TMPlayerStatus.YET_TO_START.value:
            raise BadRequest(*TM_PLAYER_NOT_IN_YET_TO_START)

    @classmethod
    def _get_tm_player(cls, player_id, tournament_match_id):
        try:
            return cls.objects.get(player_id=player_id,
                                   tournament_match_id=tournament_match_id)
        except cls.DoesNotExist:
            from django_swagger_utils.drf_server.exceptions import BadRequest
            from ib_tournament.constants.exception_messages import \
                PLAYER_NOT_IN_MATCH
            raise BadRequest(*PLAYER_NOT_IN_MATCH)

    def _update_status(self, status):
        self.status = status
        self.save()

    def _update_score(self, score):
        self.score = score
        self.save()

    def _update_completed_datetime(self):
        self.completed_datetime = self._get_now()
        self.save()

    @staticmethod
    def _get_now():
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        return get_current_local_date_time()

    @classmethod
    def _validate_status_to_submit_score(cls, status):
        from ib_tournament.constants.general import TMPlayerStatus
        from django_swagger_utils.drf_server.exceptions import BadRequest
        from ib_tournament.constants.exception_messages import \
            SUBMIT_WHEN_STATUS_IS_IN_PROGRESS
        if status != TMPlayerStatus.IN_PROGRESS.value:
            raise BadRequest(*SUBMIT_WHEN_STATUS_IS_IN_PROGRESS)

    @classmethod
    def _update_match_winner(cls, tournament_match_id):
        from ib_tournament.models import TMPlayer, TournamentMatch

        tm_players = TMPlayer.objects.filter(
            tournament_match_id=tournament_match_id)
        if cls._can_update_winner(tm_players):
            winner_id = cls._get_winner_by_score(tm_players)
            TournamentMatch.update_winner(tournament_match_id, winner_id)
        return

    @classmethod
    def _can_update_winner(cls, tm_players):
        players_status_list = cls._get_players_status_list(tm_players)
        if cls._is_status_other_than_completed(players_status_list):
            return False
        return True

    @classmethod
    def _get_players_status_list(cls, tm_players):
        return [tm_player.status for tm_player in tm_players]

    @staticmethod
    def _is_status_other_than_completed(player_status_list):
        from ib_tournament.constants.general import TournamentStatus
        if list(set(player_status_list)) != [TournamentStatus.COMPLETED.value]:
            return True

    @classmethod
    def _get_winner_by_score(cls, tm_players):
        tm_player_1 = tm_players[0]
        tm_player_2 = tm_players[1]

        if tm_player_1.score > tm_player_2.score:
            return tm_player_1.player_id
        elif tm_player_2.score > tm_player_1.score:
            return tm_player_2.player_id
        else:
            return cls._get_winner_by_completed_datetime(tm_players)

    @classmethod
    def _get_winner_by_completed_datetime(cls, tm_players):
        tm_player_1 = tm_players[0]
        tm_player_2 = tm_players[1]

        if tm_player_1.completed_datetime < tm_player_2.completed_datetime:
            return tm_player_1.player_id
        else:
            return tm_player_2.player_id
