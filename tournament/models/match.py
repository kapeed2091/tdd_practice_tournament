from django.db import models


class Match(models.Model):
    tournament_id = models.PositiveIntegerField()
    round_number = models.PositiveIntegerField()

    @classmethod
    def create_match(cls, tournament_id, round_number):
        from .tournament import Tournament
        Tournament.validate_tournament_id(tournament_id=tournament_id)

        if round_number < 0:
            from ..exceptions.custom_exceptions import InvalidRoundNumber
            raise InvalidRoundNumber

        cls.objects.create(
            tournament_id=tournament_id,
            round_number=round_number
        )
