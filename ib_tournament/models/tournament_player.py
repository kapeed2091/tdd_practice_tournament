from django.db import models


class TournamentPlayer(models.Model):
    tournament = models.ForeignKey('ib_tournament.Tournament')
    player = models.ForeignKey('ib_tournament.Player')
    curr_round_no = models.IntegerField(default=1)

    class Meta:
        unique_together = ('tournament', 'player')

    @classmethod
    def get_tournament_player(cls, tournament_id, player_id):
        try:
            tournament_player = cls.objects.get(
                tournament_id=tournament_id, player_id=player_id)
            return tournament_player
        except cls.DoesNotExist:
            cls._raise_exception_for_player_not_in_tournament()

    @classmethod
    def create_tournament_player(cls, tournament_id, player_id):
        cls.objects.create(tournament_id=tournament_id, player_id=player_id)

    @classmethod
    def get_tournament_player_exists(cls, tournament_id, player_id):
        return cls.objects.filter(
            tournament_id=tournament_id, player_id=player_id).exists()

    @classmethod
    def get_tournament_players_count(cls, tournament_id):
        tournament_players = cls.get_tournament_players(tournament_id)
        return tournament_players.count()

    @classmethod
    def get_player_ids_of_tournament(cls, tournament_id):
        tournament_players = cls.get_tournament_players(tournament_id)
        return list(tournament_players.values_list('player_id', flat=True))

    @classmethod
    def get_tournament_players(cls, tournament_id):
        return cls.objects.filter(tournament_id=tournament_id)

    @classmethod
    def get_player_current_round(cls, tournament_id, player_id):
        tournament_player = cls.get_tournament_player(
            tournament_id, player_id)
        return tournament_player.curr_round_no

    @classmethod
    def update_player_current_round(cls, tournament_id, player_id, round_no):
        tournament_player = cls.get_tournament_player(
            tournament_id, player_id)
        cls._update_current_round_no(tournament_player, round_no)
        return

    @staticmethod
    def _raise_exception_for_player_not_in_tournament():
        from django_swagger_utils.drf_server.exceptions import BadRequest
        from ib_tournament.constants.exception_messages import \
            PLAYER_NOT_IN_TOURNAMENT
        raise BadRequest(*PLAYER_NOT_IN_TOURNAMENT)

    def _update_current_round_no(self, round_no):
        self.curr_round_no = round_no
        self.save()
