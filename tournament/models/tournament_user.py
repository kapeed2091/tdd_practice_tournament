from django.db import models


class TournamentUser(models.Model):
    user = models.ForeignKey('tournament.User')
    tournament = models.ForeignKey('tournament.Tournament')

    @classmethod
    def subscribe_user_to_tournament(cls, tournament_id, username):
        from .user import User
        from .tournament import Tournament
        from tdd_practice.constants.general import TournamentStatus

        user_id = User.get_user_id(username=username)
        tournament = Tournament. \
            get_tournament_by_id(tournament_id=tournament_id)

        cls.validate_user_already_subscribed(
            tournament_id=tournament_id, user_id=user_id)

        tournament.validate_tournament_in_can_join_status()

        cls.objects.create(user_id=user_id, tournament_id=tournament_id)

        if cls.is_max_participants_subscribed(tournament_id=tournament_id):
            tournament.update_status(
                status=TournamentStatus.FULL_YET_TO_START.value)

    @classmethod
    def validate_user_already_subscribed(cls, tournament_id, user_id):
        try:
            cls.objects.get(tournament_id=tournament_id, user_id=user_id)
            raise Exception("User already subscribed to given tournament")
        except cls.DoesNotExist:
            pass

    @classmethod
    def get_subscribed_users_count(cls, tournament_id):
        return cls.objects.filter(tournament_id=tournament_id).count()

    @classmethod
    def is_max_participants_subscribed(cls, tournament_id):
        from .tournament import Tournament

        no_of_participants = Tournament.get_no_of_participants_can_join(
            tournament_id=tournament_id)
        subscribed_users_count = cls.get_subscribed_users_count(
            tournament_id=tournament_id)

        return no_of_participants == subscribed_users_count

    @classmethod
    def get_tournament_user_ids(cls, tournament_id):
        user_ids = list(TournamentUser.objects.filter(
            tournament_id=tournament_id).values_list('user_id', flat=True))

        return user_ids

