from django.test import TestCase


class TestGetUserCurrentRoundForTournament(TestCase):

    def testcase_get_default_current_round_for_tournament(self):
        from tournament.models import TournamentUser

        t_id = '1'
        user_id_1 = 'user_1'

        TournamentUser.objects.create(user_id=user_id_1, t_id=t_id,
                                      current_round_number=2)
        user_1_current_round = TournamentUser.get_user_current_round(
            tournament_id=t_id, user_id=user_id_1)

        self.assertEquals(user_1_current_round, 2)

    def testcase_user_should_be_subscribed_to_tournament_to_get_current_round(
            self):
        from tournament.models import TournamentUser, KOTournament
        import datetime
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time

        user_id_1 = 'user_1'
        t_id = '1'
        tournament_name = 'tournament_1'
        number_of_rounds = 2
        start_datetime = get_current_local_date_time() + \
                         datetime.timedelta(hours=1)
        status = 'CAN_JOIN'

        KOTournament.objects.create(
            t_id=t_id, name=tournament_name, number_of_rounds=number_of_rounds,
            start_datetime=start_datetime, status=status)

        with self.assertRaisesMessage(
                Exception,
                expected_message='User not subscribed to tournament'):
            TournamentUser.get_user_current_round(tournament_id=t_id,
                                                  user_id=user_id_1)
