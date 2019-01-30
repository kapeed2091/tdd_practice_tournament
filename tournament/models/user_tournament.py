from django.db import models


class UserTournament(models.Model):
    user_id = models.PositiveIntegerField()
    tournament_id = models.PositiveIntegerField()

    @classmethod
    def subscribe_to_tournament(cls, user_id, tournament_id):
        from ..models import User, Tournament

        User.validate_user_id(user_id=user_id)

        Tournament.validate_tournament_id(tournament_id=tournament_id)

        cls._validate_user_tournament_exists(
            user_id=user_id, tournament_id=tournament_id
        )

        tournament = Tournament.get_tournament_by_id(
            tournament_id=tournament_id
        )

        Tournament.validate_tournament_status(status=tournament.status)

        is_last_person = cls._is_last_person(
            tournament_id=tournament_id, total_rounds=tournament.total_rounds
        )

        cls.objects.create(
            user_id=user_id,
            tournament_id=tournament_id
        )

        if is_last_person:
            from ..constants.general import TournamentStatus
            tournament.update_status(
                status=TournamentStatus.FULL_YET_TO_START.value
            )

    @classmethod
    def _validate_user_tournament_exists(cls, user_id, tournament_id):
        user_tournament_exists = cls.objects.filter(
            user_id=user_id, tournament_id=tournament_id
        )

        if user_tournament_exists:
            from ..exceptions.exceptions import UserAlreadyRegistered
            raise UserAlreadyRegistered

    @classmethod
    def _is_last_person(cls, tournament_id, total_rounds):
        total_rounds = total_rounds
        max_num_of_participants = 2 ** total_rounds
        registered_tournament_members_count = \
            cls.objects.filter(tournament_id=tournament_id).count()

        is_last_person = \
            max_num_of_participants - 1 == registered_tournament_members_count

        return is_last_person
