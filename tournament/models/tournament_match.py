from django.db import models


class TournamentMatch(models.Model):
    tournament = models.ForeignKey('tournament.Tournament')
    round_no = models.IntegerField()
    match_id = models.CharField(max_length=50)

    @classmethod
    def create_tournament_matches(cls, tournament_id):
        from .tournament import Tournament

        tournament = \
            Tournament.get_tournament_by_id(tournament_id=tournament_id)
        cls.create_matches(tournament)

    @classmethod
    def create_matches(cls, tournament):
        from .tournament import Tournament

        no_of_participants = \
            Tournament.calculate_no_participants(tournament.no_of_rounds)

        for round_no in range(1, tournament.no_of_rounds+1):
            cls.create_round_matches(round_no, no_of_participants, tournament.id)

    @classmethod
    def create_round_matches(cls, round_no, no_of_participants, tournament_id):
        import uuid
        no_of_matches_in_round = no_of_participants / 2 ** round_no

        for index in range(no_of_matches_in_round):
            match_id = str(uuid.uuid4())
            cls.objects.create(round_no=round_no, tournament_id=tournament_id,
                               match_id=match_id)

