from django.test import TestCase


class TestCreateTournamentMatches(TestCase):

    def testcase_create_tournament_match_for_two_users(self):
        from tournament.models import TournamentMatch
        tournament_id = 'tournament_1'
        player_one_user_id = 'user_1'
        player_two_user_id = 'user_2'

        create_match_request = {
            'tournament_id': tournament_id,
            'player_one_user_id': player_one_user_id,
            'player_two_user_id': player_two_user_id
        }

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
