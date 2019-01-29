from django.db import models


class KOTournament(models.Model):
    T_ID_MAX_LENGTH = 20
    TOURNAMENT_NAME_MAX_LENGTH = 30
    TOURNAMENT_STATUS_MAX_LENGTH = 30

    t_id = models.CharField(max_length=T_ID_MAX_LENGTH)
    name = models.CharField(max_length=TOURNAMENT_NAME_MAX_LENGTH)
    number_of_rounds = models.IntegerField()
    start_datetime = models.DateTimeField()
    status = models.CharField(max_length=TOURNAMENT_STATUS_MAX_LENGTH)

    @classmethod
    def create_tournament(cls, user_id, t_id, name, number_of_rounds,
                          start_datetime, status):
        tournament = cls.create_tournament_in_db(
            t_id=t_id, name=name, number_of_rounds=number_of_rounds,
            start_datetime=start_datetime, status=status)

        return tournament.convert_to_dict()

    @classmethod
    def create_tournament_in_db(cls, t_id, name, number_of_rounds,
                                start_datetime, status):
        return cls.objects.create(
            t_id=t_id, name=name, number_of_rounds=number_of_rounds,
            start_datetime=start_datetime, status=status)

    def convert_to_dict(self):
        return {'t_id': self.t_id, 'name': self.name,
                'number_of_rounds': self.number_of_rounds,
                'start_datetime': self.start_datetime,
                'status': self.status}
