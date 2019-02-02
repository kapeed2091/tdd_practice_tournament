from django.db import models


class UserMatch(models.Model):
    user_id = models.PositiveIntegerField()
    match_id = models.PositiveIntegerField()

    @classmethod
    def create_user_match(cls, user_id, match_id):
        from .user import User
        User.validate_user_id(user_id=user_id)

        from .match import Match
        Match.validate_match_id(match_id=match_id)

        match = Match.objects.get(id=match_id)
        tournament_id = match.tournament_id

        from .user_tournament import UserTournament
        is_user_in_tournament = UserTournament.objects.filter(
            user_id=user_id,
            tournament_id=tournament_id
        ).exists()

        if not is_user_in_tournament:
            from tournaments.exceptions.custom_exceptions import \
                UserNotInTournamnet

            raise UserNotInTournamnet

        cls.objects.create(
            user_id=user_id,
            match_id=match_id
        )
