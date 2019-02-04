from django.db import models


class TournamentMatch(models.Model):
    tournament = models.ForeignKey('ib_tournament.Tournament')
    winner = models.ForeignKey('ib_tournament.Player', default=None,
                               null=True, blank=True)
    round_no = models.IntegerField()

    @classmethod
    def create_matches(cls, tournament_id):
        from ib_tournament.models import Tournament
        tournament = Tournament.get_tournament(tournament_id)
        cls._create_tournament_matches_to_create(
            tournament_id, tournament.total_rounds)
        return

    @classmethod
    def get_tournament_match_ids_of_tournament(cls, tournament_id):
        return list(cls.objects.filter(tournament_id=tournament_id).values_list(
            'id', flat=True))

    @classmethod
    def update_winner(cls, tournament_match_id, winner_id):
        tournament_match = cls._get_tournament_match(tournament_match_id)
        cls._update_winner_id(tournament_match, winner_id)
        return

    @classmethod
    def promote_winner_to_next_round(cls, tournament_match_id, winner_id):
        from ib_tournament.models import TournamentMatch, TMPlayer
        tournament_match = TournamentMatch._get_tournament_match(
            tournament_match_id)
        tournament_id = tournament_match.tournament_id
        curr_round_no = tournament_match.round_no
        next_round_no = curr_round_no + 1
        t_match_id = cls._get_t_match_id_to_add_participant(
            tournament_id, next_round_no)
        TMPlayer.add_player_to_t_match(t_match_id, winner_id)

    @classmethod
    def _create_tournament_matches_to_create(cls, tournament_id, total_rounds):
        t_matches_to_create = cls._get_tournament_matches_to_create(
            tournament_id, total_rounds)
        cls._bulk_create(t_matches_to_create)
        return

    @classmethod
    def _get_tournament_matches_to_create(cls, tournament_id, total_rounds):
        tournament_matches_to_create = list()
        for round_no in range(1, total_rounds + 1):
            tournament_matches_to_create.extend(
                cls._get_round_tournament_matches_to_create(
                    tournament_id, round_no, total_rounds))
        return tournament_matches_to_create

    @classmethod
    def _bulk_create(cls, t_matches_to_create):
        cls.objects.bulk_create(t_matches_to_create)
        return

    @classmethod
    def _get_tournament_match(cls, tournament_match_id):
        return cls.objects.get(id=tournament_match_id)

    def _update_winner_id(self, winner_id):
        self.winner_id = winner_id
        self.save()
        return

    @classmethod
    def _get_round_tournament_matches_to_create(
            cls, tournament_id, round_no, total_rounds):
        round_matches_count = cls._get_round_matches_count(
            round_no, total_rounds)
        round_t_matches_to_create = cls._initialise_round_tournament_matches(
            tournament_id, round_no, round_matches_count)
        return round_t_matches_to_create

    @classmethod
    def _get_round_matches_count(cls, round_no, total_rounds):
        return 2 ** (total_rounds - round_no)

    @classmethod
    def _initialise_round_tournament_matches(cls, tournament_id, round_no,
                                             round_matches_count):
        round_t_matches_to_create = [
            cls(tournament_id=tournament_id, round_no=round_no)
            for count in range(round_matches_count)]
        return round_t_matches_to_create

    @classmethod
    def _get_t_match_id_to_add_participant(cls, tournament_id, round_no):
        from ib_tournament.models import TMPlayer
        from collections import defaultdict
        tournament_matches = cls.objects.filter(
            tournament_id=tournament_id, round_no=round_no)
        round_t_match_ids = list(
            tournament_matches.values_list('id', flat=True))
        tm_players = TMPlayer.get_tm_players_by_tm_ids(round_t_match_ids)

        match_id_wise_curr_players_count = defaultdict(int)
        for tm_player in tm_players:
            match_id_wise_curr_players_count[tm_player.tournament_match_id] += 1

        for t_match_id in round_t_match_ids:
            players_count = match_id_wise_curr_players_count[t_match_id]
            if players_count < 2:
                return t_match_id
