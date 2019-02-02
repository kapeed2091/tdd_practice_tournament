from django.db import models


class RoundMatch(models.Model):
    tournament = models.ForeignKey('tournament.Tournament')
    round_no = models.IntegerField()

    @classmethod
    def create_round_matches(cls, tournament_id):
        from .tournament import Tournament

        tournament = \
            Tournament.get_tournament_by_id(tournament_id=tournament_id)
        no_of_rounds = tournament.no_of_rounds

        no_of_participants = \
            Tournament.calculate_no_participants(no_of_rounds=no_of_rounds)

        for round_no in range(1, no_of_rounds + 1):
            cls.create_matches(round_no=round_no,
                               no_of_participants=no_of_participants,
                               tournament_id=tournament_id)

    @classmethod
    def create_matches(cls, round_no, no_of_participants, tournament_id):
        no_participants_in_round = no_of_participants / 2 ** round_no
        no_of_matches_in_round = no_participants_in_round/2

        for index in range(no_of_matches_in_round):
            cls.objects.create(round_no=round_no, tournament_id=tournament_id)

