from django.db import models


class Match(models.Model):
    tournament_id = models.PositiveIntegerField()
    round_number = models.PositiveIntegerField()

    @classmethod
    def create_match(cls, tournament_id, round_number):
        # todo feedback: G30 functions should do one thing
        from .tournament import Tournament

        # todo: feedback G20 function names should say what they do
        Tournament.validate_tournament_id(tournament_id=tournament_id)

        cls._validate_round_number(round_number=round_number)

        cls.objects.create(
            tournament_id=tournament_id,
            round_number=round_number
        )

    # todo: feedback misplaced responsibility and artificial coupling
    @classmethod
    def create_all_matches(cls, tournament_id):
        # todo feedback: G30 functions should do one thing
        from .tournament import Tournament
        Tournament.validate_tournament_id(
            tournament_id=tournament_id
        )

        # todo: feedback inconsistency in naming
        # todo: feedback too many arguments
        cls._validate_if_matches_exist(tournament_id=tournament_id)

        # todo feedback too many arguments (can reduce by having object)
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

    # todo: feedback standard nomenclature where possible
    @classmethod
    def get_matches_by_tournament_and_round(cls, tournament_id, round_number):
        matches = cls.objects.filter(
            tournament_id=tournament_id, round_number=round_number
        )
        return matches

    # todo: feedback standard nomenclature where possible
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
        # todo: feedback be precise round number inconsistency, max limit of it
        if round_number < 0:
            from ..exceptions.custom_exceptions import InvalidRoundNumber
            raise InvalidRoundNumber

    # todo: feedback standard nomenclature where possible
    @classmethod
    def _validate_if_matches_exist(cls, tournament_id):
        matches_exist = cls.objects.filter(
            tournament_id=tournament_id).exists()

        if matches_exist:
            from tournaments.exceptions.custom_exceptions import \
                TournamentMatchesAlreadyExist
            raise TournamentMatchesAlreadyExist

    # todo: feedback standard nomenclature where possible
    # todo: feedback function should do only one thing
    @classmethod
    def _create_objects_for_all_rounds(cls, tournament_id, total_rounds):
        # todo: feedback standard nomenclature where possible
        for round_number in range(total_rounds, 0, -1):
            match_detail = {
                "tournament_id": tournament_id,
                "round_number": round_number
            }

            # todo: feedback obscured intent
            # todo : feedback G25 magic numbers
            # todo: artificial coupling and logical dependency
            # no of matches for round calculation ???
            # todo: feedback use explanatory variables
            # todo: feedback unambiguous names
            matches_to_be_created = 2 ** (total_rounds - round_number)
            cls._create_multiple_objects(
                match_detail=match_detail, count=matches_to_be_created
            )

    # todo: feedback standard nomenclature where possible
    @classmethod
    def _create_multiple_objects(cls, match_detail, count):
        tournament_id = match_detail["tournament_id"]
        round_number = match_detail["round_number"]

        # todo: feedback missed one level of abstraction
        objs = []
        for each in range(count):
            objs.append(
                cls(
                    tournament_id=tournament_id,
                    round_number=round_number
                )
            )
        cls.objects.bulk_create(objs)
