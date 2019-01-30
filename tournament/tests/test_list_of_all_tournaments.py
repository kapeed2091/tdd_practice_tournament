from django.test import TestCase


class TestListAllTournaments(TestCase):

    def testcase_list_all_tournaments_when_no_tournaments(self):
        from tournament.models import KOTournament

        all_tournaments = KOTournament.get_all_tournaments()
        self.assertEquals(all_tournaments, [])

    def testcase_list_all_tournaments(self):
        from tournament.models import KOTournament, UserProfile
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        import datetime
        user_id = 'user_1'
        t_id_1 = '1'
        t_id_2 = '2'
        tournament_name_1 = 'tournament_1'
        tournament_name_2 = 'tournament_2'
        number_of_rounds = 2
        start_datetime_1 = get_current_local_date_time()+\
                           datetime.timedelta(hours=1)
        start_datetime_2 = get_current_local_date_time()+\
                           datetime.timedelta(days=365)
        status = 'CAN_JOIN'

        expected_all_tournaments = list()

        expected_output_1 = {
            't_id': '1',
            'name': 'tournament_1',
            'number_of_rounds': 2,
            'start_datetime': start_datetime_1,
            'status': 'CAN_JOIN'}

        expected_output_2 = {
            't_id': '2',
            'name': 'tournament_2',
            'number_of_rounds': 2,
            'start_datetime': start_datetime_2,
            'status': 'CAN_JOIN'
        }
        expected_all_tournaments.append(expected_output_1)
        expected_all_tournaments.append(expected_output_2)

        UserProfile.objects.create(user_id=user_id)
        KOTournament.assign_t_id_to_tournament(
            t_id=t_id_1, name=tournament_name_1,
            number_of_rounds=number_of_rounds,
            start_datetime=start_datetime_1, status=status)

        KOTournament.assign_t_id_to_tournament(
            t_id=t_id_2, name=tournament_name_2,
            number_of_rounds=number_of_rounds,
            start_datetime=start_datetime_2, status=status)

        actual_all_tournaments = KOTournament.get_all_tournaments()

        import deepdiff
        diff = deepdiff.DeepDiff(expected_all_tournaments,
                                 actual_all_tournaments)
        self.assertEquals(diff, {})
