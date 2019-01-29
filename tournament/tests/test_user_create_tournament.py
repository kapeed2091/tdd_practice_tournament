from django.test import TestCase


class TestUserCreateTournament(TestCase):
    username = "user1"

    def test_user_create_tournament(self):
        from datetime import datetime

        no_of_rounds = 4
        start_date_time = datetime.now()

        from tournament.models.tournament import Tournament
        tournament_details = Tournament.create_tournament(
            no_of_rounds=no_of_rounds, start_date_time=start_date_time)

        start_date_time_str = start_date_time.strftime("%Y-%m-%d")

        self.assertEquals(start_date_time_str,
                          tournament_details['start_datetime'])
        self.assertEquals(no_of_rounds, tournament_details['no_of_rounds'])
