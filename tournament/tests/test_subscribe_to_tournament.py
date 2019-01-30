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

    def testcase_non_registered_user_cannot_subscribe(self):
        from tournament.models import TournamentUser
        user_id = 'user_1'
        tournament_id = 'tournament_1'

        with self.assertRaisesMessage(
                Exception, expected_message='User not registered'):
            TournamentUser.subscribe_to_tournament(user_id, tournament_id)
