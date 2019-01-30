from django.test import TestCase


class TestSubscribeToTournament(TestCase):

    def testcase_user_subscribe_to_tournament(self):
        from tournament.models import TournamentUser
        user_id = 'user_1'
        tournament_id = 'tournament_1'

        old_count = len(TournamentUser.objects.filter(
            user_id=user_id, tournament_id=tournament_id))

        TournamentUser.subscribe_to_tournament(user_id, tournament_id)

        new_count = len(TournamentUser.objects.filter(
            user_id=user_id, tournament_id=tournament_id))

        self.assertEquals(new_count-old_count, 1)
