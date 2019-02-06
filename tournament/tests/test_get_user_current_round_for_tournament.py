from django.test import TestCase


class TestGetUserCurrentRoundForTournament(TestCase):

    def testcase_get_default_current_round_for_tournament(self):
        from tournament.models import TournamentUser

        t_id = '1'
        user_id_1 = 'user_1'

        TournamentUser.objects.create(user_id=user_id_1, t_id=t_id,
                                      current_round_number=2)
        user_1_current_round = TournamentUser.get_user_current_round(
            t_id=t_id, user_id=user_id_1)

        self.assertEquals(user_1_current_round, 2)
