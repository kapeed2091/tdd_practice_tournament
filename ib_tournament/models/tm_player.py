from django.db import models
from ib_tournament.constants.general import TMPlayerStatus


class TMPlayer(models.Model):
    player = models.ForeignKey('ib_tournament.Player')
    tournament_match = models.ForeignKey('ib_tournament.TournamentMatch')
    status = models.CharField(max_length=50,
                              default=TMPlayerStatus.YET_TO_START.value)

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
        tournament_match = cls._get_tm_player(player_id, tournament_match_id)
        cls._update_status(tournament_match, TMPlayerStatus.IN_PROGRESS.value)
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
    def _get_tm_player(cls, player_id, tournament_match_id):
        return cls.objects.get(player_id=player_id,
                               tournament_match_id=tournament_match_id)

    def _update_status(self, status):
        self.status = status
        self.save()