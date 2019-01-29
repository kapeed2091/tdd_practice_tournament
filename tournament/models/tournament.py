from django.db import models


class Tournament(models.Model):
    no_of_rounds = models.IntegerField()
    start_date_time = models.DateTimeField()
    username = models.CharField(max_length=50)

    @classmethod
    def create_tournament(cls, no_of_rounds, start_date_time, username):
        tournament_obj = cls.objects.create(
            no_of_rounds=no_of_rounds,
            start_date_time=start_date_time, username=username)

        start_datetime_str = tournament_obj.start_date_time.strftime("%Y-%m-%d %H:%M:%S")

        return {"no_of_rounds": tournament_obj.no_of_rounds,
                "start_datetime": start_datetime_str}