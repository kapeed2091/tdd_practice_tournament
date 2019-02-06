from django.db import models


class User(models.Model):
    NAME_MAX_LENGTH = 20
    GENDER_MAX_LENGTH = 20

    name = models.CharField(max_length=20)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=GENDER_MAX_LENGTH)

    @classmethod
    def get_winner_profile(cls, tournament_id):
        from .user_tournament import UserTournament
        user_tournament = UserTournament.get_winner(
            tournament_id=tournament_id
        )
        user_id = user_tournament.user_id

        user_obj = cls.get_user_by_id(user_id=user_id)
        user_details = user_obj.convert_to_dict()

        return user_details

    @classmethod
    def get_user_by_id(cls, user_id):
        user = cls.objects.get(id=user_id)

        return user

    def convert_to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "gender": self.gender
        }

    @classmethod
    def validate_user_id(cls, user_id):
        user_exists = User.objects.filter(id=user_id).exists()
        if not user_exists:
            from ..exceptions.custom_exceptions import InvalidUserId
            raise InvalidUserId
