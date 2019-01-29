from django.db import models


class Tournament(models.Model):

    @classmethod
    def create_tournament(cls, user_id, total_rounds, start_datetime):
        pass
