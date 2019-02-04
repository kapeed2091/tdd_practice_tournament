from django.test import TestCase


class TestUserSubmitScore(TestCase):

    def testcase_user_submit_score(self):
        from tournament.models import TournamentMatch
        user_id_1 = 'user_1'
        user_id_2 = 'user_2'
        match_id = 'match_1'
        tournament_id = 'tournament_1'
        score = 10

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
        from tournament.models import TournamentMatch
        user_id_1 = 'user_1'
        match_id = 'match_1'
        score = 10

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
