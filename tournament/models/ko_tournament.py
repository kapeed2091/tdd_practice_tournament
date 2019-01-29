from django.db import models


class KOTournament(models.Model):
    pass

    @classmethod
    def create_tournament(cls, user_id, id, name, number_of_rounds,
                          start_datetime, tournament_status):
        pass