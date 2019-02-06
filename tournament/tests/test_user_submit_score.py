from django.test import TestCase


class TestUserSubmitScore(TestCase):

    def testcase_user_submit_score(self):
        from tournament.models import TournamentMatch, UserProfile
        user_id_1 = 'user_1'
        user_id_2 = 'user_2'
        match_id = 'match_1'
        tournament_id = 'tournament_1'
        score = 10
        t_round_number = 1

        UserProfile.objects.create(user_id=user_id_1)
        TournamentMatch.objects.create(
            t_id=tournament_id, player_one=user_id_1, player_two=user_id_2,
            match_id=match_id, t_round_number=t_round_number)

        old_state = TournamentMatch.objects.get(
            player_one=user_id_1, match_id=match_id)

        TournamentMatch.user_submit_score(user_id_1, match_id, score)

        new_state = TournamentMatch.objects.get(
            player_one=user_id_1, match_id=match_id)

        self.assertEquals(
            new_state.player_one_score - old_state.player_one_score, score)

    def testcase_user_submit_score_for_valid_match(self):
        from tournament.models import TournamentMatch, UserProfile
        user_id_1 = 'user_1'
        match_id = 'match_1'
        score = 10

        UserProfile.objects.create(user_id=user_id_1)

        with self.assertRaisesMessage(Exception,
                                      expected_message='Match doesnot exist'):
            TournamentMatch.user_submit_score(
                user_id=user_id_1, match_id=match_id, score=score)

    def testcase_only_valid_user_can_submit_score(self):
        from tournament.models import TournamentMatch
        user_id_1 = 'user_1'
        user_id_2 = 'user_2'
        match_id = 'match_1'
        tournament_id = 'tournament_1'
        score = 10
        t_round_number = 1

        TournamentMatch.objects.create(
            t_id=tournament_id, player_one=user_id_1, player_two=user_id_2,
            match_id=match_id, t_round_number=t_round_number)

        with self.assertRaisesMessage(Exception,
                                      expected_message='User not registered'):
            TournamentMatch.user_submit_score(
                user_id=user_id_1, match_id=match_id, score=score)

    def testcase_user_should_belong_to_match_to_submit_score(self):
        from tournament.models import TournamentMatch, UserProfile
        user_id_1 = 'user_1'
        user_id_2 = 'user_2'
        user_id_3 = 'user_3'
        match_id = 'match_1'
        tournament_id = 'tournament_1'
        score = 10
        t_round_number = 1

        UserProfile.objects.create(user_id=user_id_3)

        TournamentMatch.objects.create(
            t_id=tournament_id, player_one=user_id_1, player_two=user_id_2,
            match_id=match_id, t_round_number=t_round_number)

        with self.assertRaisesMessage(
                Exception,
                expected_message='User doesnot belong to this match'):
            TournamentMatch.user_submit_score(
                user_id=user_id_3, match_id=match_id, score=score)

    def testcase_user_submit_score_should_update_score_of_appropraite_user(self):
        from tournament.models import TournamentMatch, UserProfile
        user_id_1 = 'user_1'
        user_id_2 = 'user_2'
        match_id = 'match_1'
        tournament_id = 'tournament_1'
        user_1_score = 10
        user_2_score = 20
        t_round_number = 1

        UserProfile.objects.create(user_id=user_id_1)
        UserProfile.objects.create(user_id=user_id_2)

        TournamentMatch.objects.create(
            t_id=tournament_id, player_one=user_id_1, player_two=user_id_2,
            match_id=match_id, t_round_number=t_round_number)

        TournamentMatch.user_submit_score(user_id=user_id_1, match_id=match_id,
                                          score=user_1_score)

        player_one_old_state = TournamentMatch.objects.get(
            player_one=user_id_1, match_id=match_id)

        player_two_old_state = TournamentMatch.objects.get(
            player_two=user_id_2, match_id=match_id)

        TournamentMatch.user_submit_score(user_id=user_id_2, match_id=match_id,
                                          score=user_2_score)

        player_one_new_state = TournamentMatch.objects.get(
            player_one=user_id_1, match_id=match_id)

        player_two_new_state = TournamentMatch.objects.get(
            player_two=user_id_2, match_id=match_id)

        self.assertEquals(
            player_one_old_state.player_one_score,
            player_one_new_state.player_one_score)

        self.assertEquals(
            player_two_new_state.player_two_score -
            player_two_old_state.player_two_score, user_2_score)

    def testcase_user_submit_score_should_be_recorded_along_with_time(self):
        from tournament.models import TournamentMatch, UserProfile
        from datetime import timedelta
        from ib_common.date_time_utils.get_current_local_date_time \
            import get_current_local_date_time

        user_id_1 = 'user_1'
        user_id_2 = 'user_2'
        match_id = 'match_1'
        tournament_id = 'tournament_1'
        user_1_score = 10
        user_2_score = 20
        t_round_number = 1

        user_1_time = get_current_local_date_time()
        user_2_time = get_current_local_date_time() + timedelta(minutes=5)

        UserProfile.objects.create(user_id=user_id_1)
        UserProfile.objects.create(user_id=user_id_2)

        TournamentMatch.objects.create(
            t_id=tournament_id, player_one=user_id_1, player_two=user_id_2,
            match_id=match_id, t_round_number=t_round_number)

        TournamentMatch.user_submit_score_with_time(
            user_id=user_id_1, match_id=match_id, score=user_1_score,
            submit_time=user_1_time)
        TournamentMatch.user_submit_score_with_time(
            user_id=user_id_2, match_id=match_id, score=user_2_score,
            submit_time=user_2_time)

        player_one_state = TournamentMatch.objects.get(
            player_one=user_id_1, match_id=match_id)

        player_two_state = TournamentMatch.objects.get(
            player_two=user_id_2, match_id=match_id)

        self.assertEquals(player_one_state.player_one_submit_time, user_1_time)
        self.assertEquals(player_two_state.player_two_submit_time, user_2_time)
