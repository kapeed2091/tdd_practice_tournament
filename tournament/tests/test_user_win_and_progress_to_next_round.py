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
        t_round_number = 1

        UserProfile.objects.create(user_id=user_id_1)
        UserProfile.objects.create(user_id=user_id_2)

        TournamentMatch.objects.create(
            t_id=tournament_id, player_one=user_id_1, player_two=user_id_2,
            match_id=match_id, t_round_number=t_round_number)

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

        TournamentMatch.decide_winner(match_id=match_id)

        tournament_match_obj = \
            TournamentMatch.objects.filter(match_id=match_id)[0]

        self.assertEquals(tournament_match_obj.winner_user_id, user_id_1)

    def testcase_winner_progresses_to_next_round(self):
        from tournament.models import KOTournament, TournamentMatch, \
            TournamentUser
        from datetime import datetime, timedelta
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time

        t_id = '1'
        tournament_name = 'tournament_1'
        number_of_rounds = 2
        start_datetime = get_current_local_date_time() + timedelta(hours=1)
        status = 'IN_PROGRESS'

        user_id_1 = 'user_1'
        user_id_2 = 'user_2'
        match_id = 'match_1'
        user_1_score = 20
        user_2_score = 10
        t_round_number = 1

        user_1_time = get_current_local_date_time()
        user_2_time = get_current_local_date_time() + timedelta(minutes=5)

        KOTournament.objects.create(
            t_id=t_id, name=tournament_name, number_of_rounds=number_of_rounds,
            start_datetime=start_datetime, status=status)

        TournamentUser.objects.create(user_id=user_id_1, t_id=t_id,
                                      current_round_number=1)
        TournamentUser.objects.create(user_id=user_id_2, t_id=t_id,
                                      current_round_number=1)

        TournamentMatch.objects.create(
            t_id=t_id, player_one=user_id_1, player_one_match_status='COMPLETED',
            player_one_score=user_1_score, player_one_submit_time=user_1_time,
            player_two=user_id_2, player_two_match_status='COMPLETED',
            player_two_score=user_2_score, player_two_submit_time=user_2_time,
            match_id=match_id, match_status='COMPLETED',
            winner_user_id=user_id_1, t_round_number=t_round_number)

        winner_old_state = TournamentUser.objects.get(
            t_id=t_id, user_id=user_id_1)
        loser_old_state = TournamentUser.objects.get(
            t_id=t_id, user_id=user_id_2)

        TournamentMatch.winner_progress_to_next_round(match_id)

        winner_new_state = TournamentUser.objects.get(
            t_id=t_id, user_id=user_id_1)
        loser_new_state = TournamentUser.objects.get(
            t_id=t_id, user_id=user_id_2)

        self.assertEquals(loser_old_state.current_round_number,
                          loser_new_state.current_round_number)
        self.assertEquals(winner_new_state.current_round_number -
                          winner_old_state.current_round_number, 1)
