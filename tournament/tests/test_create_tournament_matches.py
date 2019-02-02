from django.test import TestCase


class TestCreateTournamentMatches(TestCase):

    def testcase_create_tournament_match_for_two_users(self):
        from tournament.models import TournamentMatch
        tournament_id = 'tournament_1'
        user_id_1 = 'user_1'
        user_id_2 = 'user_2'

        old_state = list(TournamentMatch.objects.filter(
            t_id=tournament_id, player_one=user_id_1, player_two=user_id_2))
        TournamentMatch.create_match(tournament_id, user_id_1, user_id_2)
        new_state = list(TournamentMatch.objects.filter(
            t_id=tournament_id, player_one=user_id_1, player_two=user_id_2))

        diff = list(set(new_state).difference(set(old_state)))

        self.assertEquals(len(new_state) - len(old_state), 1)
        self.assertEquals(diff[0].t_id, tournament_id)
        self.assertEquals(diff[0].player_one, user_id_1)
        self.assertEquals(diff[0].player_two, user_id_2)
