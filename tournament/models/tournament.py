from django.db import models


class Tournament(models.Model):

    @classmethod
    def create_tournament(cls, created_user_id, no_of_rounds, start_datetime):
        pass
