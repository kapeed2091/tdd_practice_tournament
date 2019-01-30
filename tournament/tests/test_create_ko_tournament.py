from django.test import TestCase


class TestCreateKOTournament(TestCase):

    def testcase_create_ko_tournament(self):
        import datetime
        user_id = 'user_1'
        t_id = '1'
        tournament_name = 'tournament_1'
        number_of_rounds = 2
        start_datetime = datetime.datetime(2019, 1, 30, 15, 00, 00)
        status = 'CAN_JOIN'

        input_tournament_details = {
            't_id': '1',
            'name': 'tournament_1',
            'number_of_rounds': 2,
            'start_datetime': datetime.datetime(2019, 1, 30, 15, 00, 00),
            'status': 'CAN_JOIN'
        }

        from tournament.models import KOTournament, UserProfile
        UserProfile.objects.create(user_id=user_id)
        tournament_details = KOTournament.create_tournament(
            user_id=user_id, t_id=t_id, name=tournament_name,
            number_of_rounds=number_of_rounds,
            start_datetime=start_datetime, status=status)

        self.assertEquals(input_tournament_details, tournament_details)

    def testcase_non_positive_number_of_rounds(self):
        import datetime
        from tournament.models import KOTournament, UserProfile

        user_id = 'user_1'
        t_id = '1'
        tournament_name = 'tournament_1'
        number_of_rounds_case1 = 0
        number_of_rounds_case2 = -1
        start_datetime = datetime.datetime(2019, 1, 30, 15, 00, 00)
        status = 'CAN_JOIN'

        UserProfile.objects.create(user_id=user_id)
        with self.assertRaisesMessage(
                Exception,
                expected_message='Non-positive number of rounds given'):
            KOTournament.create_tournament(
            user_id=user_id, t_id=t_id, name=tournament_name,
            number_of_rounds=number_of_rounds_case1,
            start_datetime=start_datetime, status=status)

        with self.assertRaisesMessage(
                Exception,
                expected_message='Non-positive number of rounds given'):
            KOTournament.create_tournament(
            user_id=user_id, t_id=t_id, name=tournament_name,
            number_of_rounds=number_of_rounds_case2,
            start_datetime=start_datetime, status=status)

    def testcase_float_number_of_rounds(self):
        import datetime
        from tournament.models import KOTournament, UserProfile

        user_id = 'user_1'
        t_id = '1'
        tournament_name = 'tournament_1'
        number_of_rounds = 1.5
        start_datetime = datetime.datetime(2019, 1, 30, 15, 00, 00)
        status = 'CAN_JOIN'

        UserProfile.objects.create(user_id=user_id)
        with self.assertRaisesMessage(
                Exception,
                expected_message='Float type number of rounds given'):
            KOTournament.create_tournament(
                user_id=user_id, t_id=t_id, name=tournament_name,
                number_of_rounds=number_of_rounds,
                start_datetime=start_datetime, status=status)

    def testcase_start_datetime_is_greater_than_current_time(self):
        import datetime
        from tournament.models import KOTournament, UserProfile

        user_id = 'user_1'
        t_id = '1'
        tournament_name = 'tournament_1'
        number_of_rounds = 2
        start_datetime = datetime.datetime(2019, 1, 30, 01, 00, 00)
        status = 'CAN_JOIN'

        UserProfile.objects.create(user_id=user_id)
        with self.assertRaisesMessage(
                Exception,
                expected_message='Start datetime is less than current time'):
            KOTournament.create_tournament(
                user_id=user_id, t_id=t_id, name=tournament_name,
                number_of_rounds=number_of_rounds,
                start_datetime=start_datetime, status=status)

    def testcase_non_registered_users_cannot_create_tournament(self):
        import datetime
        from tournament.models import KOTournament

        user_id = 'non_user_1'
        t_id = '1'
        tournament_name = 'tournament_1'
        number_of_rounds = 2
        start_datetime = datetime.datetime(2020, 1, 30, 05, 00, 00)
        status = 'CAN_JOIN'

        with self.assertRaisesMessage(
                Exception,
                expected_message='User not registered to create tournament'):
            KOTournament.create_tournament(
                user_id=user_id, t_id=t_id, name=tournament_name,
                number_of_rounds=number_of_rounds,
                start_datetime=start_datetime, status=status)

    def testcase_create_multiple_tournaments_with_same_t_id(self):
        import datetime
        from tournament.models import KOTournament, UserProfile

        user_id = 'non_user_1'
        t_id = '1'
        tournament_name_1 = 'tournament_1'
        tournament_name_2 = 'tournament_2'
        number_of_rounds_1 = 2
        number_of_rounds_2 = 3
        start_datetime = datetime.datetime(2020, 1, 30, 05, 00, 00)
        status = 'CAN_JOIN'

        UserProfile.objects.create(user_id=user_id)

        tournament_details_1 = KOTournament.create_tournament(
            user_id=user_id, t_id=t_id, name=tournament_name_1,
            number_of_rounds=number_of_rounds_1,
            start_datetime=start_datetime, status=status)

        with self.assertRaisesMessage(
                Exception,
                expected_message='Tournaments with same t_id cannot be created'):
            KOTournament.create_tournament(
                user_id=user_id, t_id=t_id, name=tournament_name_2,
                number_of_rounds=number_of_rounds_2,
                start_datetime=start_datetime, status=status)
