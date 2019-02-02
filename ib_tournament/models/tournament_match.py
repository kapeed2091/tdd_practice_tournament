from django.db import models


class TournamentMatch(models.Model):
    tournament = models.ForeignKey('ib_tournament.Tournament')
    winner = models.ForeignKey('ib_tournament.Player', default=None,
                               null=True, blank=True)

    @classmethod
    def create_matches(cls, tournament_id):
        from ib_tournament.models import Tournament
        matches_count = Tournament.get_no_of_matches(tournament_id)
        cls._create_tournament_matches_to_create(tournament_id, matches_count)
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
    def _create_tournament_matches_to_create(cls, tournament_id, matches_count):
        t_matches_to_create = cls._get_tournament_matches_to_create(
            tournament_id, matches_count)
        cls._bulk_create(t_matches_to_create)
        return

    @classmethod
    def _bulk_create(cls, t_matches_to_create):
        cls.objects.bulk_create(t_matches_to_create)
        return

    @classmethod
    def _get_tournament_matches_to_create(cls, tournament_id, matches_count):
        return [cls(tournament_id=tournament_id)
                for count in range(matches_count)]

    @classmethod
    def _get_tournament_match(cls, tournament_match_id):
        return cls.objects.get(id=tournament_match_id)

    def _update_winner_id(self, winner_id):
        self.winner_id = winner_id
        self.save()
        return
