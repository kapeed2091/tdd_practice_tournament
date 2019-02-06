from django.test import TestCase


class TestUserSubmitScore(TestCase):

    def testcase_user_submit_score(self):
        from tournament.models import TournamentMatch, UserProfile
        user_id_1 = 'user_1'
        user_id_2 = 'user_2'
        match_id = 'match_1'
        tournament_id = 'tournament_1'
        score = 10

        UserProfile.objects.create(user_id=user_id_1)
        TournamentMatch.objects.create(
            t_id=tournament_id, player_one=user_id_1, player_two=user_id_2,
            match_id=match_id)

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

        TournamentMatch.objects.create(
            t_id=tournament_id, player_one=user_id_1, player_two=user_id_2,
            match_id=match_id)

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

        UserProfile.objects.create(user_id=user_id_3)

        TournamentMatch.objects.create(
            t_id=tournament_id, player_one=user_id_1, player_two=user_id_2,
            match_id=match_id)

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

        UserProfile.objects.create(user_id=user_id_1)
        UserProfile.objects.create(user_id=user_id_2)

        TournamentMatch.objects.create(
            t_id=tournament_id, player_one=user_id_1, player_two=user_id_2,
            match_id=match_id)

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