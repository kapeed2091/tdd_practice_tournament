from django.test import TestCase


class TestUserPlayMatch(TestCase):

    def testcase_user_play_match(self):
        from tournament.models import TournamentMatch

        user_id_1 = 'user_1'
        user_id_2 = 'user_2'
        match_id = 'match_1'
        tournament_id = 'tournament_1'

        TournamentMatch.objects.create(
            t_id=tournament_id, player_one=user_id_1, player_two=user_id_2,
            match_id=match_id)

        TournamentMatch.user_play_match(user_id_1, tournament_id, match_id)

        player_one_playing_state = TournamentMatch.objects.get(
            player_one=user_id_1, t_id=tournament_id, match_id=match_id)

        self.assertEquals(
            player_one_playing_state.player_one_match_status, 'IN_PROGRESS')
        self.assertEquals(
            player_one_playing_state.player_two_match_status, 'YET_TO_START')
        self.assertEquals(player_one_playing_state.match_status, 'IN_PROGRESS')
