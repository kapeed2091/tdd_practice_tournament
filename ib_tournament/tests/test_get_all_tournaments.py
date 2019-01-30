from django.test import TestCase
from ib_tournament.constants.general import TournamentStatus

tournaments_data = [
    {
        'id': 1,
        'name': 'Tournament 1',
        'status': TournamentStatus.CAN_JOIN.value,
        'total_rounds': 2
    },
    {
        'id': 2,
        'name': 'Tournament 2',
        'status': TournamentStatus.FULL_YET_TO_START.value,
        'total_rounds': 2
    },
    {
        'id': 3,
        'name': 'Tournament 3',
        'status': TournamentStatus.IN_PROGRESS.value,
        'total_rounds': 2
    },
    {
        'id': 4,
        'name': 'Tournament 4',
        'status': TournamentStatus.COMPLETED.value,
        'total_rounds': 2
    }
]


class TestGetAllTournaments(TestCase):

    @staticmethod
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

    @staticmethod
    def update_tournament_status(tournament_id, status):
        from ib_tournament.models import Tournament
        tournament = Tournament.objects.get(id=tournament_id)
        tournament.status = status
        tournament.save()

    def test_get_all_tournaments(self):
        from ib_tournament.models import Tournament

        next_day_datetime_str = self.get_next_day_datetime_str()
        for t_dict in tournaments_data:
            tournament_id = Tournament.create_tournament(
                total_rounds=t_dict['total_rounds'],
                start_datetime_str=next_day_datetime_str,
                name=t_dict['name'])
            self.update_tournament_status(tournament_id, t_dict['status'])
            t_dict['start_datetime'] = next_day_datetime_str

        tournaments_list = Tournament.get_all_tournaments()
        self.assertEqual(tournaments_list, tournaments_data)
