from django.test import TestCase


class TestUserPlayMatch(TestCase):

    # ToDo: Incomplete test case
    def testcase_user_play_match(self):
        from tournament.models import KOTournament, \
            TournamentUser, UserProfile
        import datetime
        from ib_common.date_time_utils.get_current_local_date_time \
            import get_current_local_date_time

        start_datetime = \
            get_current_local_date_time() + datetime.timedelta(minutes=-1)
        user_id = 'user'
        tournament_id = 'tournament_1'
        number_of_rounds = 2

        UserProfile.objects.create(user_id=user_id)
        KOTournament.objects.create(
            t_id=tournament_id, name='tournament_name_1',
            number_of_rounds=number_of_rounds,
            start_datetime=start_datetime, status='IN_PROGRESS')
