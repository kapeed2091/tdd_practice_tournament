from django.db import models


class Tournament(models.Model):
    CUSTOMER_ID_LENGTH = 20

    created_user_id = models.CharField(max_length=CUSTOMER_ID_LENGTH)
    no_of_rounds = models.PositiveIntegerField()
    start_datetime = models.DateTimeField()

    @classmethod
    def create_tournament(cls, created_user_id, no_of_rounds, start_datetime):
        tournament = cls.objects.create(
            created_user_id=created_user_id,
            no_of_rounds=no_of_rounds,
            start_datetime=start_datetime
        )
        return tournament.convert_to_dict()

    def convert_to_dict(self):
        return {
            "created_user_id": self.created_user_id,
            "no_of_rounds": self.no_of_rounds,
            "start_datetime": self.start_datetime
        }
