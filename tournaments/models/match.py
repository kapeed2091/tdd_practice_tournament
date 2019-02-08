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
    def create_all_matches(cls, tournament_id):
        from .tournament import Tournament
        Tournament.validate_tournament_id(
            tournament_id=tournament_id
        )

        cls._validate_if_matches_exist(tournament_id=tournament_id)

        total_rounds = Tournament.get_total_rounds_in_tournament(
            tournament_id=tournament_id
        )

        cls._create_objects_for_all_rounds(
            tournament_id=tournament_id, total_rounds=total_rounds
        )

    @classmethod
    def get_match_by_id(cls, match_id):
        obj = cls.objects.get(id=match_id)
        return obj

    @classmethod
    def get_matches_by_tournament_and_round(cls, tournament_id, round_number):
        matches = cls.objects.filter(
            tournament_id=tournament_id, round_number=round_number
        )
        return matches

    @classmethod
    def validate_and_get_match_by_id(cls, match_id):
        # ToDo FEEDBACK method name appearing as Query and Command
        try:
            obj = cls.get_match_by_id(match_id=match_id)
            return obj
        except cls.DoesNotExist:
            from ..exceptions.custom_exceptions import InvalidMatchId
            raise InvalidMatchId

    @staticmethod
    def _validate_round_number(round_number):
        if round_number < 0:
            from ..exceptions.custom_exceptions import InvalidRoundNumber
            raise InvalidRoundNumber

    @classmethod
    def _validate_if_matches_exist(cls, tournament_id):
        # Todo FEEDBACK function naming
        matches_exist = cls.objects.filter(
            tournament_id=tournament_id).exists()
        if matches_exist:
            from tournaments.exceptions.custom_exceptions import \
                TournamentMatchesAlreadyExist
            raise TournamentMatchesAlreadyExist

    @classmethod
    def _create_objects_for_all_rounds(cls, tournament_id, total_rounds):
        for round_number in range(total_rounds, 0, -1):
            match_detail = {
                "tournament_id": tournament_id,
                "round_number": round_number
            }

            matches_to_be_created = 2 ** (total_rounds - round_number)
            cls._create_multiple_objects(
                match_detail=match_detail, count=matches_to_be_created
            )

    @classmethod
    def _create_multiple_objects(cls, match_detail, count):
        tournament_id = match_detail["tournament_id"]
        round_number = match_detail["round_number"]

        objs = []
        for each in range(count):
            objs.append(
                cls(
                    tournament_id=tournament_id,
                    round_number=round_number
                )
            )
        cls.objects.bulk_create(objs)
