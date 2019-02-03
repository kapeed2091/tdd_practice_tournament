from django.test import TestCase


class TestUserPlayMatch(TestCase):

    def testcase_user_play_match(self):
        from tournament.models import TournamentMatch, KOTournament, \
            UserProfile, TournamentUser
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        from datetime import timedelta
        from tournament.constants import TournamentStatus

        user_id_1 = 'user_1'
        user_id_2 = 'user_2'
        match_id = 'match_1'
        tournament_id = 'tournament_1'
        tournament_name = 'city_tournament_1'
        number_of_rounds = 2
        start_datetime = get_current_local_date_time() - timedelta(minutes=10)

        UserProfile.objects.create(user_id=user_id_1)

        KOTournament.objects.create(
            t_id=tournament_id, name=tournament_name,
            number_of_rounds=number_of_rounds, start_datetime=start_datetime,
            status=TournamentStatus.IN_PROGRESS.value)

        TournamentUser.objects.create(user_id=user_id_1, t_id=tournament_id)

        TournamentMatch.objects.create(
            t_id=tournament_id, player_one=user_id_1, player_two=user_id_2,
            match_id=match_id)

        TournamentMatch.user_play_match(
            user_id=user_id_1, tournament_id=tournament_id, match_id=match_id)

        player_one_playing_state = TournamentMatch.objects.get(
            player_one=user_id_1, t_id=tournament_id, match_id=match_id)

        self.assertEquals(
            player_one_playing_state.player_one_match_status, 'IN_PROGRESS')
        self.assertEquals(
            player_one_playing_state.player_two_match_status, 'YET_TO_START')
        self.assertEquals(player_one_playing_state.match_status, 'IN_PROGRESS')

    def testcase_user_play_match_if_tournament_exists(self):
        from tournament.models import TournamentMatch

        user_id_1 = 'user_1'
        user_id_2 = 'user_2'
        match_id = 'match_1'
        tournament_id = 'tournament_1'

        TournamentMatch.objects.create(
            t_id=tournament_id, player_one=user_id_1, player_two=user_id_2,
            match_id=match_id)

        with self.assertRaisesMessage(
                Exception, expected_message='Tournament doesnot exist'):
            TournamentMatch.user_play_match(
                user_id=user_id_1, tournament_id=tournament_id,
                match_id=match_id)

    def testcase_user_play_match_after_tournament_start_datetime(self):
        from tournament.models import TournamentMatch, KOTournament
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        from datetime import timedelta

        user_id_1 = 'user_1'
        user_id_2 = 'user_2'
        match_id = 'match_1'
        tournament_id = 'tournament_1'
        tournament_name = 'city_tournament_1'
        number_of_rounds = 2
        start_datetime = get_current_local_date_time() + timedelta(minutes=10)

        KOTournament.objects.create(
            t_id=tournament_id, name=tournament_name,
            number_of_rounds=number_of_rounds, start_datetime=start_datetime)

        TournamentMatch.objects.create(
            t_id=tournament_id, player_one=user_id_1, player_two=user_id_2,
            match_id=match_id)

        with self.assertRaisesMessage(
                Exception,
                expected_message='Match cannot be played before start datetime'):
            TournamentMatch.user_play_match(
                user_id=user_id_1, tournament_id=tournament_id,
                match_id=match_id)

    def testcase_user_play_match_when_tournament_in_progress(self):
        from tournament.models import TournamentMatch, KOTournament
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        from datetime import timedelta
        from tournament.constants import TournamentStatus

        user_id_1 = 'user_1'
        user_id_2 = 'user_2'
        match_id = 'match_1'
        tournament_id = 'tournament_1'
        tournament_name = 'city_tournament_1'
        number_of_rounds = 2
        start_datetime = get_current_local_date_time() - timedelta(minutes=10)

        KOTournament.objects.create(
            t_id=tournament_id, name=tournament_name,
            number_of_rounds=number_of_rounds, start_datetime=start_datetime,
            status=TournamentStatus.FULL_YET_TO_START.value)

        TournamentMatch.objects.create(
            t_id=tournament_id, player_one=user_id_1, player_two=user_id_2,
            match_id=match_id)

        with self.assertRaisesMessage(
                Exception,
                expected_message='Tournament Status not in progress'):
            TournamentMatch.user_play_match(
                user_id=user_id_1, tournament_id=tournament_id,
                match_id=match_id)

    def testcase_user_can_play_match_if_valid_match_id(self):
        from tournament.models import TournamentMatch, KOTournament
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        from datetime import timedelta
        from tournament.constants import TournamentStatus

        user_id_1 = 'user_1'
        user_id_2 = 'user_2'
        match_id = 'match_1'
        tournament_id = 'tournament_1'
        tournament_name = 'city_tournament_1'
        number_of_rounds = 2
        start_datetime = get_current_local_date_time() - timedelta(minutes=10)

        KOTournament.objects.create(
            t_id=tournament_id, name=tournament_name,
            number_of_rounds=number_of_rounds, start_datetime=start_datetime,
            status=TournamentStatus.IN_PROGRESS.value)

        with self.assertRaisesMessage(
                Exception, expected_message='Match doesnot exist'):
            TournamentMatch.user_play_match(
                user_id=user_id_1, tournament_id=tournament_id,
                match_id=match_id)

    def testcase_user_must_exist_to_play_match(self):
        from tournament.models import TournamentMatch, KOTournament
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        from datetime import timedelta
        from tournament.constants import TournamentStatus

        user_id_1 = 'user_1'
        user_id_2 = 'user_2'
        match_id = 'match_1'
        tournament_id = 'tournament_1'
        tournament_name = 'city_tournament_1'
        number_of_rounds = 2
        start_datetime = get_current_local_date_time() - timedelta(minutes=10)

        KOTournament.objects.create(
            t_id=tournament_id, name=tournament_name,
            number_of_rounds=number_of_rounds, start_datetime=start_datetime,
            status=TournamentStatus.IN_PROGRESS.value)

        TournamentMatch.objects.create(
            t_id=tournament_id, player_one=user_id_1, player_two=user_id_2,
            match_id=match_id)

        with self.assertRaisesMessage(Exception,
                                      expected_message='User not registered'):
            TournamentMatch.user_play_match(
                user_id=user_id_1, tournament_id=tournament_id,
                match_id=match_id)

    def testcase_user_must_be_subscribed_to_tournament_to_play_match(self):
        from tournament.models import TournamentMatch, KOTournament, UserProfile
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        from datetime import timedelta
        from tournament.constants import TournamentStatus

        user_id_1 = 'user_1'
        user_id_2 = 'user_2'
        match_id = 'match_1'
        tournament_id = 'tournament_1'
        tournament_name = 'city_tournament_1'
        number_of_rounds = 2
        start_datetime = get_current_local_date_time() - timedelta(minutes=10)

        UserProfile.objects.create(user_id=user_id_1)

        KOTournament.objects.create(
            t_id=tournament_id, name=tournament_name,
            number_of_rounds=number_of_rounds, start_datetime=start_datetime,
            status=TournamentStatus.IN_PROGRESS.value)

        TournamentMatch.objects.create(
            t_id=tournament_id, player_one=user_id_1, player_two=user_id_2,
            match_id=match_id)

        with self.assertRaisesMessage(
                Exception, expected_message='User not subscribed to tournament'):
            TournamentMatch.user_play_match(
                user_id=user_id_1, tournament_id=tournament_id,
                match_id=match_id)

    def testcase_user_should_be_one_of_player_in_match(self):
        from tournament.models import TournamentMatch, KOTournament, \
            UserProfile, TournamentUser
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        from datetime import timedelta
        from tournament.constants import TournamentStatus

        user_id_1 = 'user_1'
        user_id_2 = 'user_2'
        user_id_3 = 'user_3'
        match_id = 'match_1'
        tournament_id = 'tournament_1'
        tournament_name = 'city_tournament_1'
        number_of_rounds = 2
        start_datetime = get_current_local_date_time() - timedelta(minutes=10)

        UserProfile.objects.create(user_id=user_id_3)

        KOTournament.objects.create(
            t_id=tournament_id, name=tournament_name,
            number_of_rounds=number_of_rounds, start_datetime=start_datetime,
            status=TournamentStatus.IN_PROGRESS.value)

        TournamentUser.objects.create(user_id=user_id_3, t_id=tournament_id)

        TournamentMatch.objects.create(
            t_id=tournament_id, player_one=user_id_1, player_two=user_id_2,
            match_id=match_id)

        with self.assertRaisesMessage(
                Exception,
                expected_message='User doesnot belong to this match'):
            TournamentMatch.user_play_match(
                user_id=user_id_3, tournament_id=tournament_id,
                match_id=match_id)
