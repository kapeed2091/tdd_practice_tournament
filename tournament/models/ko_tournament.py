from django.db import models


class KOTournament(models.Model):

    @classmethod
    def create_tournament(cls, user_id, id, name, number_of_rounds,
                          start_datetime, tournament_status):
        import datetime
        return {'id': 1, 'name': 'tournament_1', 'number_of_rounds': 2,
                'start_datetime': datetime.datetime(2019, 1, 30, 15, 00, 00),
                'tournament_status': 'CAN_JOIN'}