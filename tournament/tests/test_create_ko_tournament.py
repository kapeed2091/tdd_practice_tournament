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

        from tournament.models import KOTournament
        tournament_details = KOTournament.create_tournament(
            user_id=user_id, t_id=t_id, name=tournament_name,
            number_of_rounds=number_of_rounds,
            start_datetime=start_datetime, status=status)

        self.assertEquals(input_tournament_details, tournament_details)

    def testcase_non_positive_number_of_rounds(self):
        import datetime
        from tournament.models import KOTournament

        user_id = 'user_1'
        t_id = '1'
        tournament_name = 'tournament_1'
        number_of_rounds_case1 = 0
        number_of_rounds_case2 = -1
        start_datetime = datetime.datetime(2019, 1, 30, 15, 00, 00)
        status = 'CAN_JOIN'

        with self.assertRaises(Exception):
            KOTournament.create_tournament(
            user_id=user_id, t_id=t_id, name=tournament_name,
            number_of_rounds=number_of_rounds_case1,
            start_datetime=start_datetime, status=status)

        with self.assertRaises(Exception):
            KOTournament.create_tournament(
            user_id=user_id, t_id=t_id, name=tournament_name,
            number_of_rounds=number_of_rounds_case2,
            start_datetime=start_datetime, status=status)
