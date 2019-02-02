from django.test import TestCase


class TestCreateTournamentMatches(TestCase):

    def testcase_create_tournament_match_for_two_users(self):
        from tournament.models import TournamentMatch, KOTournament
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        from datetime import timedelta
        from tournament.constants import TournamentStatus

        tournament_id = 'tournament_1'
        player_one_user_id = 'user_1'
        player_two_user_id = 'user_2'
        tournament_name = 'city_tournament_1'
        number_of_rounds = 2
        start_datetime_past = \
            get_current_local_date_time() - timedelta(minutes=5)

        create_match_request = {
            'tournament_id': tournament_id,
            'player_one_user_id': player_one_user_id,
            'player_two_user_id': player_two_user_id
        }

        KOTournament.objects.create(
            t_id=tournament_id, name=tournament_name,
            number_of_rounds=number_of_rounds,
            start_datetime=start_datetime_past,
            status=TournamentStatus.FULL_YET_TO_START.value)

        old_state = list(TournamentMatch.objects.filter(
            t_id=tournament_id, player_one=player_one_user_id,
            player_two=player_two_user_id))
        TournamentMatch.create_match(request_data=create_match_request)
        new_state = list(TournamentMatch.objects.filter(
            t_id=tournament_id, player_one=player_one_user_id,
            player_two=player_two_user_id))

        diff = list(set(new_state).difference(set(old_state)))

        self.assertEquals(len(new_state) - len(old_state), 1)
        self.assertEquals(diff[0].t_id, tournament_id)
        self.assertEquals(diff[0].player_one, player_one_user_id)
        self.assertEquals(diff[0].player_two, player_two_user_id)

    def testcase_create_match_before_tournament_start_datetime(self):
        from tournament.models import TournamentMatch, KOTournament
        from datetime import timedelta
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        from tournament.constants.general import TournamentStatus

        tournament_id_1 = 'tournament_1'
        tournament_id_2 = 'tournament_2'
        tournament_name = 'city_tournament_1'
        number_of_rounds = 2
        start_datetime_past = \
            get_current_local_date_time() - timedelta(minutes=5)
        start_datetime_future = \
            get_current_local_date_time() + timedelta(minutes=5)

        player_one_user_id = 'user_1'
        player_two_user_id = 'user_2'

        create_match_request_1 = {
            'tournament_id': tournament_id_1,
            'player_one_user_id': player_one_user_id,
            'player_two_user_id': player_two_user_id
        }

        create_match_request_2 = {
            'tournament_id': tournament_id_2,
            'player_one_user_id': player_one_user_id,
            'player_two_user_id': player_two_user_id
        }

        KOTournament.objects.create(
            t_id=tournament_id_1, name=tournament_name,
            number_of_rounds=number_of_rounds,
            start_datetime=start_datetime_past,
            status=TournamentStatus.FULL_YET_TO_START.value)

        KOTournament.objects.create(
            t_id=tournament_id_2, name=tournament_name,
            number_of_rounds=number_of_rounds,
            start_datetime=start_datetime_future,
            status=TournamentStatus.FULL_YET_TO_START.value)

        old_state = list(TournamentMatch.objects.filter(
            t_id=tournament_id_1, player_one=player_one_user_id,
            player_two=player_two_user_id))
        TournamentMatch.create_match(request_data=create_match_request_1)
        new_state = list(TournamentMatch.objects.filter(
            t_id=tournament_id_1, player_one=player_one_user_id,
            player_two=player_two_user_id))

        diff = list(set(new_state).difference(set(old_state)))

        self.assertEquals(len(new_state) - len(old_state), 1)
        self.assertEquals(diff[0].t_id, tournament_id_1)

        with self.assertRaisesMessage(
                Exception,
                expected_message=
                'Tournament Match cannot be created before start datetime'):
            TournamentMatch.create_match(request_data=create_match_request_2)

    def testcase_tournament_should_exist_to_create_match(self):
        from tournament.models import TournamentMatch

        tournament_id = 'tournament_1'
        player_one_user_id = 'user_1'
        player_two_user_id = 'user_2'

        create_match_request = {
            'tournament_id': tournament_id,
            'player_one_user_id': player_one_user_id,
            'player_two_user_id': player_two_user_id
        }

        with self.assertRaisesMessage(
                Exception, expected_message='Tournament doesnot exist'):
            TournamentMatch.create_match(request_data=create_match_request)
