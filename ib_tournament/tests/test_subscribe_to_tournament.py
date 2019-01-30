from django.test import TestCase


def get_next_day_datetime_str():
    from ib_common.date_time_utils.get_current_local_date_time import \
        get_current_local_date_time
    from ib_common.date_time_utils.convert_datetime_to_local_string import \
        convert_datetime_to_local_string
    from ib_tournament.constants.general import DEFAULT_DATE_TIME_FORMAT
    from datetime import timedelta

    next_day_datetime = get_current_local_date_time() + timedelta(days=1)
    return convert_datetime_to_local_string(
        next_day_datetime, DEFAULT_DATE_TIME_FORMAT)


class TestSubscribeToTournament(TestCase):
    username = 'user1'

    def test_subscribe_to_tournament(self):
        from ib_tournament.models import Tournament, Player, TournamentPlayer

        Player.create_player(self.username)
        player = Player.get_player(self.username)
        player_id = player.id
        tournament_id = Tournament.create_tournament(
            total_rounds=2, start_datetime_str=get_next_day_datetime_str(),
            name='Tournament 1')
        Tournament.subscribe_to_tournament(
            tournament_id=tournament_id, player_id=player_id)
        tournament_player = TournamentPlayer.get_tournament_player(
            tournament_id=tournament_id, player_id=player_id)
        tournament_player_dict = tournament_player.get_tournament_player_dict()
        self.assertEqual(tournament_player_dict['tournament_id'], tournament_id)
        self.assertEqual(tournament_player_dict['player_id'], player_id)
