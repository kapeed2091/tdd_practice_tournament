from django.test import TestCase


class TestSubscribeToTournament(TestCase):

    def testcase_user_subscribe_to_tournament(self):
        from tournament.models import TournamentUser, UserProfile, KOTournament
        import datetime
        from ib_common.date_time_utils.get_current_local_date_time \
            import get_current_local_date_time

        start_datetime = \
            get_current_local_date_time()+datetime.timedelta(minutes=10)
        user_id = 'user_1'
        tournament_id = 'tournament_1'

        UserProfile.objects.create(user_id=user_id)
        KOTournament.objects.create(
            t_id=tournament_id, name='tournament_name_1',number_of_rounds=2,
            start_datetime=start_datetime)

        old_count = len(TournamentUser.objects.filter(
            user_id=user_id, tournament_id=tournament_id))

        TournamentUser.subscribe_to_tournament(user_id, tournament_id)

        new_count = len(TournamentUser.objects.filter(
            user_id=user_id, tournament_id=tournament_id))

        self.assertEquals(new_count-old_count, 1)

    def testcase_non_registered_user_cannot_subscribe(self):
        from tournament.models import TournamentUser
        user_id = 'user_1'
        tournament_id = 'tournament_1'

        with self.assertRaisesMessage(
                Exception, expected_message='User not registered'):
            TournamentUser.subscribe_to_tournament(user_id, tournament_id)

    def testcase_tournament_should_exist_to_subscribe(self):
        from tournament.models import TournamentUser, UserProfile
        user_id = 'user_1'
        tournament_id = 'tournament_1'

        UserProfile.objects.create(user_id=user_id)
        with self.assertRaisesMessage(
                Exception, expected_message='Tournament doesnot exist'):
            TournamentUser.subscribe_to_tournament(user_id, tournament_id)
