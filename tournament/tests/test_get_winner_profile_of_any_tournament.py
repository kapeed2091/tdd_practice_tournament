from django.test import TestCase


class TestGetWinnerProfileOfAnyTournament(TestCase):

    def testcase_get_winner_profile_of_any_tournament(self):
        from tournament.models import TournamentMatch, KOTournament, UserProfile
        from datetime import timedelta
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time

        user_id_1 = 'user_1'
        name_1 = 'John'
        age_1 = 24
        gender_1 = 'MALE'

        user_id_2 = 'user_2'
        name_2 = 'Robin'
        age_2 = 25
        gender_2 = 'FEMALE'

        user_1_profile = {
            'name': name_1,
            'age': age_1,
            'gender': gender_1
        }

        user_2_profile = {
            'name': name_2,
            'age': age_2,
            'gender': gender_2
        }

        t_id = 'tournament_1'
        tournament_name = 'tournament_1'
        number_of_rounds = 3
        start_datetime = get_current_local_date_time() + timedelta(hours=-1)
        status = 'COMPLETED'

        t_round_number = 3
        match_id = 'match_1'
        user_1_score = 20
        user_2_score = 10
        user_1_time = get_current_local_date_time() + timedelta(minutes=-10)
        user_2_time = get_current_local_date_time() + timedelta(minutes=-20)


        UserProfile.objects.create(
            user_id=user_id_1, name=name_1, age=age_1, gender=gender_1)
        UserProfile.objects.create(
            user_id=user_id_2, name=name_2, age=age_2, gender=gender_2)

        KOTournament.objects.create(
            t_id=t_id, name=tournament_name, number_of_rounds=number_of_rounds,
            start_datetime=start_datetime, status=status)

        TournamentMatch.objects.create(
            t_id=t_id, player_one=user_id_1, player_one_match_status='COMPLETED',
            player_one_score=user_1_score, player_one_submit_time=user_1_time,
            player_two=user_id_2, player_two_match_status='COMPLETED',
            player_two_score=user_2_score, player_two_submit_time=user_2_time,
            match_id=match_id, match_status='COMPLETED',
            winner_user_id=user_id_1, t_round_number=t_round_number)

        tournament_winner_profile = \
            TournamentMatch.get_tournament_winner_profile(tournament_id=t_id)

        self.assertEquals(tournament_winner_profile, user_1_profile)
