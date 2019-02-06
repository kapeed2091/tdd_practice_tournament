from django.db import models


class TournamentUser(models.Model):
    user = models.ForeignKey('tournament.User')
    tournament = models.ForeignKey('tournament.Tournament')

    @classmethod
    def subscribe_user_to_tournament(cls, tournament_id, username):
        from .user import User
        from .tournament import Tournament

        cls.validate_user_already_subscribed(
            tournament_id=tournament_id, username=username)
        Tournament.validate_tournament_id(tournament_id=tournament_id)
        Tournament.\
            validate_tournament_in_can_join_status(tournament_id=tournament_id)

        user_id = User.get_user_id(username=username)

        cls.objects.create(user_id=user_id, tournament_id=tournament_id)

        if cls.is_max_participants_subscribed(tournament_id=tournament_id):
            from tdd_practice.constants.general import TournamentStatus
            Tournament.update_tournament_status(
                tournament_id=tournament_id,
                status=TournamentStatus.FULL_YET_TO_START.value)

    @classmethod
    def validate_user_already_subscribed(cls, tournament_id, username):
        try:
            cls.objects.get(tournament_id=tournament_id, user__username=username)
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

