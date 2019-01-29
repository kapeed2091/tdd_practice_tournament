from django.db import models


class Tournament(models.Model):
    user_id = models.PositiveIntegerField()
    total_rounds = models.PositiveIntegerField()
    start_datetime = models.DateTimeField()

    @classmethod
    def create_tournament(cls, user_id, total_rounds, start_datetime):
        try:
            obj = Tournament.objects.create(
                user_id=user_id,
                total_rounds=total_rounds,
                start_datetime=start_datetime
            )
            return obj
        except cls.DoesNotExist:
            pass
