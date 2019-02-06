from django.test import TestCase


class TestUserWinAndProgressToNextRound(TestCase):

    def testcase_compare_user_score_to_decide_winner(self):
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

        TournamentMatch.user_submit_score(user_id=user_id_2, match_id=match_id,
                                          score=user_2_score)

        TournamentMatch.decide_winner(match_id=match_id)

        tournament_match_obj = \
            TournamentMatch.objects.filter(match_id=match_id)[0]

        self.assertEquals(tournament_match_obj.winner_user_id, user_id_2)

    def testcase_decide_winner_based_on_time_when_scores_are_equal(self):
        from tournament.models import TournamentMatch, UserProfile
        from datetime import timedelta
        from ib_common.date_time_utils.get_current_local_date_time \
            import get_current_local_date_time

        user_id_1 = 'user_1'
        user_id_2 = 'user_2'
        match_id = 'match_1'
        tournament_id = 'tournament_1'
        user_1_score = 20
        user_2_score = 20

        user_1_time = get_current_local_date_time()
        user_2_time = get_current_local_date_time() + timedelta(minutes=5)

        UserProfile.objects.create(user_id=user_id_1)
        UserProfile.objects.create(user_id=user_id_2)

        TournamentMatch.objects.create(
            t_id=tournament_id, player_one=user_id_1, player_two=user_id_2,
            match_id=match_id)

        TournamentMatch.user_submit_score_with_time(
            user_id=user_id_1, match_id=match_id, score=user_1_score,
            submit_time=user_1_time)
        TournamentMatch.user_submit_score_with_time(
            user_id=user_id_2, match_id=match_id, score=user_2_score,
            submit_time=user_2_time)

        TournamentMatch.decide_winner(match_id=match_id)

        tournament_match_obj = \
            TournamentMatch.objects.filter(match_id=match_id)[0]

        self.assertEquals(tournament_match_obj.winner_user_id, user_id_1)
