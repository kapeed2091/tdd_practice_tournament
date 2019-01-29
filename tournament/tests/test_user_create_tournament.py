from django.test import TestCase


class TestUserCreateTournament(TestCase):
    username = "user1"

    def test_user_create_tournament(self):
        from datetime import datetime, timedelta

        no_of_rounds = 4
        start_date_time = datetime.now() + timedelta(days=1)

        from tournament.models.tournament import Tournament
        tournament_details = Tournament.create_tournament(
            no_of_rounds=no_of_rounds, start_date_time=start_date_time,
            username=self.username)

        start_date_time_str = start_date_time.strftime("%Y-%m-%d %H:%M:%S")

        self.assertEquals(start_date_time_str,
                          tournament_details['start_datetime'])
        self.assertEquals(no_of_rounds, tournament_details['no_of_rounds'])

    def test_user_create_tournament_with_past_datetime(self):
        from datetime import datetime, timedelta

        no_of_rounds = 4
        start_datetime = datetime.now() - timedelta(days=1)

        with self.assertRaisesMessage(Exception, "Expected future date time"):
            from tournament.models.tournament import Tournament
            Tournament.create_tournament(
                no_of_rounds=no_of_rounds, start_date_time=start_datetime,
                username=self.username)

    def test_user_create_tournament_with_non_positive_rounds(self):
        from datetime import datetime, timedelta

        no_of_rounds = 0
        start_datetime = datetime.now() + timedelta(days=1)

        with self.assertRaisesMessage(Exception, "Invalid no of rounds"):
            from tournament.models.tournament import Tournament
            Tournament.create_tournament(
                no_of_rounds=no_of_rounds, start_date_time=start_datetime,
                username=self.username)

    def test_invalid_user_create_tournament(self):
        from datetime import datetime, timedelta

        no_of_rounds = 4
        start_datetime = datetime.now() + timedelta(days=1)

        with self.assertRaisesMessage(Exception, "Invalid username"):
            from tournament.models.tournament import Tournament
            Tournament.create_tournament(
                no_of_rounds=no_of_rounds, start_date_time=start_datetime,
                username="user")
