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

        total_rounds = tournament.total_rounds
        max_num_of_participants = 2 ** total_rounds
        registered_persons_count_for_tournament = \
            cls.objects.filter(tournament_id=tournament_id).count()

        cls.objects.create(
            user_id=user_id,
            tournament_id=tournament_id
        )

        if max_num_of_participants - 1 == registered_persons_count_for_tournament:
            from ..constants.general import TournamentStatus
            tournament.status = TournamentStatus.FULL_YET_TO_START.value
            tournament.save()

    @classmethod
    def _validate_user_tournament_exists(cls, user_id, tournament_id):
        user_tournament_exists = cls.objects.filter(
            user_id=user_id, tournament_id=tournament_id
        )

        if user_tournament_exists:
            from ..exceptions.exceptions import UserAlreadyRegistered
            raise UserAlreadyRegistered
