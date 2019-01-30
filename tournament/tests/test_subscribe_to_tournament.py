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
            user_id=user_id, t_id=tournament_id))

        TournamentUser.subscribe_to_tournament(user_id, tournament_id)

        new_count = len(TournamentUser.objects.filter(
            user_id=user_id, t_id=tournament_id))

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

    def testcase_subscribe_to_tournament_after_start_datetime(self):
        from tournament.models import TournamentUser, UserProfile, KOTournament
        import datetime
        from ib_common.date_time_utils.get_current_local_date_time \
            import get_current_local_date_time

        start_datetime = \
            get_current_local_date_time() + datetime.timedelta(minutes=-10)
        user_id = 'user_1'
        tournament_id = 'tournament_1'

        UserProfile.objects.create(user_id=user_id)
        KOTournament.objects.create(
            t_id=tournament_id, name='tournament_name_1', number_of_rounds=2,
            start_datetime=start_datetime)

        with self.assertRaisesMessage(
                Exception, expected_message='Tournament has started'):
            TournamentUser.subscribe_to_tournament(user_id=user_id,
                                                   tournament_id=tournament_id)

    def testcase_subscribe_to_tournament_wrong_status(self):
        from tournament.models import TournamentUser, UserProfile, \
            KOTournament
        import datetime
        from ib_common.date_time_utils.get_current_local_date_time \
            import get_current_local_date_time

        start_datetime = \
            get_current_local_date_time() + datetime.timedelta(minutes=10)
        user_id = 'user_1'
        tournament_id = 'tournament_1'

        UserProfile.objects.create(user_id=user_id)
        KOTournament.objects.create(
            t_id=tournament_id, name='tournament_name_1',
            number_of_rounds=2,
            start_datetime=start_datetime, status='IN_PROGRESS')

        with self.assertRaisesMessage(
                Exception, expected_message='Invalid Tournament Status'):
            TournamentUser.subscribe_to_tournament(
                user_id=user_id, tournament_id=tournament_id)

    def testcase_subscribe_in_full_participants_tournament(self):
        from tournament.models import TournamentUser, UserProfile, \
            KOTournament
        import datetime
        from ib_common.date_time_utils.get_current_local_date_time \
            import get_current_local_date_time

        start_datetime = \
            get_current_local_date_time() + datetime.timedelta(minutes=10)
        number_of_rounds = 2
        user_id = 'user'
        tournament_id = 'tournament_1'

        UserProfile.objects.create(user_id=user_id)
        KOTournament.objects.create(
            t_id=tournament_id, name='tournament_name_1',
            number_of_rounds=number_of_rounds,
            start_datetime=start_datetime, status='CAN_JOIN')

        for i in range(0,pow(2,number_of_rounds)):
            user_id = 'user_' + str(i)
            UserProfile.objects.create(user_id=user_id)
            TournamentUser.subscribe_to_tournament(
                user_id=user_id, tournament_id=tournament_id)

        with self.assertRaisesMessage(
                Exception, expected_message='Tournament is full'):
            TournamentUser.subscribe_to_tournament(
                user_id=user_id, tournament_id=tournament_id)
