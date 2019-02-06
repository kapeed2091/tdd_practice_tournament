from django.db import models


class Match(models.Model):
    tournament_id = models.PositiveIntegerField()
    round_number = models.PositiveIntegerField()

    @classmethod
    def create_match(cls, tournament_id, round_number):
        from .tournament import Tournament
        Tournament.validate_tournament_id(tournament_id=tournament_id)

        cls._validate_round_number(round_number=round_number)

        cls.objects.create(
            tournament_id=tournament_id,
            round_number=round_number
        )

    @classmethod
    def get_match_by_id(cls, match_id):
        obj = cls.objects.get(id=match_id)
        return obj

    @staticmethod
    def _validate_round_number(round_number):
        if round_number < 0:
            from ..exceptions.custom_exceptions import InvalidRoundNumber
            raise InvalidRoundNumber

    @classmethod
    def validate_and_get_match_by_id(cls, match_id):
        try:
            obj = cls.get_match_by_id(match_id=match_id)
            return obj
        except cls.DoesNotExist:
            from ..exceptions.custom_exceptions import InvalidMatchId
            raise InvalidMatchId

    @classmethod
    def create_all_matches(cls, tournament_id):
        from .tournament import Tournament
        tournament = Tournament.objects.get(id=tournament_id)
        total_rounds = tournament.total_rounds

        for each_round in range(total_rounds, 0, -1):
            matches_to_be_created = 2 ** (total_rounds - each_round)
            for each in range(matches_to_be_created):
                cls.objects.create(
                    tournament_id=tournament_id,
                    round_number=each_round
                )
