from django.db import models


class KOTournament(models.Model):
    t_id = models.CharField(max_length=20)
    name = models.CharField(max_length=30)
    number_of_rounds = models.IntegerField()
    start_datetime = models.DateTimeField()
    tournament_status = models.CharField(max_length=30)

    @classmethod
    def create_tournament(cls, user_id, id, name, number_of_rounds,
                          start_datetime, tournament_status):
        tournament = cls.objects.create(
            t_id=id, name=name, number_of_rounds=number_of_rounds,
            start_datetime=start_datetime, tournament_status=tournament_status)

        return {'id': tournament.t_id, 'name': tournament.name,
                'number_of_rounds': tournament.number_of_rounds,
                'start_datetime': tournament.start_datetime,
                'tournament_status': tournament.tournament_status}
