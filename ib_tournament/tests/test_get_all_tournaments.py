from django.test import TestCase
from ib_tournament.constants.general import TournamentStatus


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


def get_all_tournaments():
    next_day_datetime_str = get_next_day_datetime_str()
    tournaments_data = [
        {
            'tournament_id': 1,
            'name': 'Tournament 2',
            'status': TournamentStatus.FULL_YET_TO_START.value,
            'total_rounds': 2,
            'start_datetime': next_day_datetime_str
        },
        {
            'tournament_id': 2,
            'name': 'Tournament 1',
            'status': TournamentStatus.CAN_JOIN.value,
            'total_rounds': 2,
            'start_datetime': next_day_datetime_str
        },
        {
            'tournament_id': 3,
            'name': 'Tournament 3',
            'status': TournamentStatus.IN_PROGRESS.value,
            'total_rounds': 2,
            'start_datetime': next_day_datetime_str
        },
        {
            'tournament_id': 4,
            'name': 'Tournament 4',
            'status': TournamentStatus.COMPLETED.value,
            'total_rounds': 2,
            'start_datetime': next_day_datetime_str
        }
    ]
    return tournaments_data


def get_ordered_tournaments():
    from ib_common.date_time_utils.get_current_local_date_time import \
        get_current_local_date_time
    from datetime import timedelta
    from ib_common.date_time_utils.convert_datetime_to_local_string import \
        convert_datetime_to_local_string
    from ib_tournament.constants.general import DEFAULT_DATE_TIME_FORMAT

    ordered_tournaments_to_create = [
        {
            'tournament_id': 1,
            'name': 'Tournament 5',
            'status': TournamentStatus.IN_PROGRESS.value,
            'total_rounds': 4,
            'start_datetime': convert_datetime_to_local_string(
                get_current_local_date_time() + timedelta(days=4),
                DEFAULT_DATE_TIME_FORMAT)
        },
        {
            'tournament_id': 2,
            'name': 'Tournament 1',
            'status': TournamentStatus.FULL_YET_TO_START.value,
            'total_rounds': 2,
            'start_datetime': convert_datetime_to_local_string(
                get_current_local_date_time() + timedelta(days=1),
                DEFAULT_DATE_TIME_FORMAT)
        },
        {
            'tournament_id': 3,
            'name': 'Tournament 3',
            'status': TournamentStatus.CAN_JOIN.value,
            'total_rounds': 2,
            'start_datetime': convert_datetime_to_local_string(
                get_current_local_date_time() + timedelta(days=1),
                DEFAULT_DATE_TIME_FORMAT)
        },
        {
            'tournament_id': 4,
            'name': 'Tournament 2',
            'status': TournamentStatus.FULL_YET_TO_START.value,
            'total_rounds': 2,
            'start_datetime': convert_datetime_to_local_string(
                get_current_local_date_time() + timedelta(days=1.2),
                DEFAULT_DATE_TIME_FORMAT)
        },
        {
            'tournament_id': 5,
            'name': 'Tournament 6',
            'status': TournamentStatus.COMPLETED.value,
            'total_rounds': 4,
            'start_datetime': convert_datetime_to_local_string(
                get_current_local_date_time() + timedelta(days=0.4),
                DEFAULT_DATE_TIME_FORMAT)
        },
        {
            'tournament_id': 6,
            'name': 'Tournament 4',
            'status': TournamentStatus.IN_PROGRESS.value,
            'total_rounds': 4,
            'start_datetime': convert_datetime_to_local_string(
                get_current_local_date_time() + timedelta(days=1),
                DEFAULT_DATE_TIME_FORMAT)
        }
    ]

    ordered_tournaments_data = [
        {
            'tournament_id': 2,
            'name': 'Tournament 1',
            'status': TournamentStatus.FULL_YET_TO_START.value,
            'total_rounds': 2,
            'start_datetime': convert_datetime_to_local_string(
                get_current_local_date_time() + timedelta(days=1),
                DEFAULT_DATE_TIME_FORMAT)
        },
        {
            'tournament_id': 4,
            'name': 'Tournament 2',
            'status': TournamentStatus.FULL_YET_TO_START.value,
            'total_rounds': 2,
            'start_datetime': convert_datetime_to_local_string(
                get_current_local_date_time() + timedelta(days=1.2),
                DEFAULT_DATE_TIME_FORMAT)
        },
        {
            'tournament_id': 3,
            'name': 'Tournament 3',
            'status': TournamentStatus.CAN_JOIN.value,
            'total_rounds': 2,
            'start_datetime': convert_datetime_to_local_string(
                get_current_local_date_time() + timedelta(days=1),
                DEFAULT_DATE_TIME_FORMAT)
        },
        {
            'tournament_id': 6,
            'name': 'Tournament 4',
            'status': TournamentStatus.IN_PROGRESS.value,
            'total_rounds': 4,
            'start_datetime': convert_datetime_to_local_string(
                get_current_local_date_time() + timedelta(days=1),
                DEFAULT_DATE_TIME_FORMAT)
        },
        {
            'tournament_id': 1,
            'name': 'Tournament 5',
            'status': TournamentStatus.IN_PROGRESS.value,
            'total_rounds': 4,
            'start_datetime': convert_datetime_to_local_string(
                get_current_local_date_time() + timedelta(days=4),
                DEFAULT_DATE_TIME_FORMAT)
        },
        {
            'tournament_id': 5,
            'name': 'Tournament 6',
            'status': TournamentStatus.COMPLETED.value,
            'total_rounds': 4,
            'start_datetime': convert_datetime_to_local_string(
                get_current_local_date_time() + timedelta(days=0.4),
                DEFAULT_DATE_TIME_FORMAT)
        }
    ]
    return ordered_tournaments_to_create, ordered_tournaments_data


class TestGetAllTournaments(TestCase):

    @staticmethod
    def update_tournament_status(tournament_id, status):
        from ib_tournament.models import Tournament
        tournament = Tournament.objects.get(id=tournament_id)
        tournament.status = status
        tournament.save()

    def create_tournaments(self, tournaments_data):
        from ib_tournament.models import Tournament
        for t_dict in tournaments_data:
            tournament_id = Tournament.create_tournament(
                total_rounds=t_dict['total_rounds'],
                start_datetime_str=t_dict['start_datetime'],
                name=t_dict['name'])
            self.update_tournament_status(tournament_id, t_dict['status'])

    def test_get_all_tournaments(self):
        from ib_tournament.models import Tournament

        tournaments_data = get_all_tournaments()
        self.create_tournaments(tournaments_data)
        tournaments_list = Tournament.get_all_tournaments()
        self.assertEqual(tournaments_list, tournaments_data)

    def test_ordered_tournaments(self):
        from ib_tournament.models import Tournament

        tournaments_to_create, ordered_tournaments_data = \
            get_ordered_tournaments()
        self.create_tournaments(tournaments_to_create)
        tournaments_list = Tournament.get_all_tournaments()
        self.assertEqual(tournaments_list, ordered_tournaments_data)
