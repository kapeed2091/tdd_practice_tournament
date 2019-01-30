from django.test import TestCase


class TestUserCreateTournament(TestCase):
    from ib_common.date_time_utils.get_current_local_date_time \
        import get_current_local_date_time

    curr_datetime = get_current_local_date_time()
    username = "user1"

    def test_user_create_tournament(self):
        from datetime import timedelta

        no_of_rounds = 4
        start_datetime = self.curr_datetime + timedelta(days=1)
        self._populate_user()

        from tournament.models.tournament import Tournament
        tournament_details = Tournament.create_tournament(
            no_of_rounds=no_of_rounds, start_datetime=start_datetime,
            username=self.username)

        self.assertEquals(start_datetime,
                          tournament_details['start_datetime'])
        self.assertEquals(no_of_rounds, tournament_details['no_of_rounds'])

    def test_user_create_tournament_with_past_datetime(self):
        from datetime import timedelta

        no_of_rounds = 4
        start_datetime = self.curr_datetime - timedelta(days=1)
        self._populate_user()
        with self.assertRaisesMessage(Exception, "Expected future date time"):
            from tournament.models.tournament import Tournament
            Tournament.create_tournament(
                no_of_rounds=no_of_rounds, start_datetime=start_datetime,
                username=self.username)

    def test_user_create_tournament_with_non_positive_rounds(self):
        from datetime import timedelta

        no_of_rounds = 0
        start_datetime = self.curr_datetime + timedelta(days=1)
        self._populate_user()

        with self.assertRaisesMessage(Exception, "Invalid no of rounds"):
            from tournament.models.tournament import Tournament
            Tournament.create_tournament(
                no_of_rounds=no_of_rounds, start_datetime=start_datetime,
                username=self.username)

    def test_invalid_user_create_tournament(self):
        from datetime import timedelta

        no_of_rounds = 4
        start_datetime = self.curr_datetime + timedelta(days=1)

        with self.assertRaisesMessage(Exception, "Invalid username"):
            from tournament.models.tournament import Tournament
            Tournament.create_tournament(
                no_of_rounds=no_of_rounds, start_datetime=start_datetime,
                username="user")

    def _populate_user(self):
        from tournament.models.user import User
        User.objects.create(username=self.username)