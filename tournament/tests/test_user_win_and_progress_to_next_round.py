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
