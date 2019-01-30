from django.test import TestCase
from tournament.models import Tournament


class TestGetAllTournaments(TestCase):

    def test_case_get_all_tournaments(self):
        tournaments = [
            {
                "name": "tournament_1",
                "user_id": 1,
                "total_rounds": 2,
                "start_datetime": "2019-12-12 13:00:00",
                "status": "CAN_JOIN"
            },
            {
                "name": "tournament_2",
                "user_id": 2,
                "total_rounds": 3,
                "start_datetime": "2019-12-13 13:00:00",
                "status": "FULL_YET_TO_START"
            },
            {
                "name": "tournament_3",
                "user_id": 3,
                "total_rounds": 4,
                "start_datetime": "2019-12-14 13:00:00",
                "status": "IN_PROGRESS"
            },
            {
                "name": "tournament_4",
                "user_id": 4,
                "total_rounds": 5,
                "start_datetime": "2019-12-15 13:00:00",
                "status": "COMPLETED"
            }
        ]
        date_time_format = '%Y-%m-%d %H:%M:%S'

        from ib_common.date_time_utils.convert_string_to_local_date_time \
            import convert_string_to_local_date_time
        for each in tournaments:
            date_obj = convert_string_to_local_date_time(
                each['start_datetime'], date_time_format
            )
            Tournament.objects.create(
                name=each["name"],
                user_id=each["user_id"],
                total_rounds=each["total_rounds"],
                start_datetime=date_obj,
                status=each["status"]
            )

        tournament_details = Tournament.get_all_tournament_details()

        tournaments_sorted = \
            sorted(tournaments, key=lambda k: k['start_datetime'])

        for each in tournaments_sorted:
            each['start_datetime'] = convert_string_to_local_date_time(
                each['start_datetime'], date_time_format
            )
            each.pop('user_id')

        self.assertEqual(Tournament.objects.all().count(), len(tournaments))
        for index, each in enumerate(tournaments_sorted):
            each_tournament_sorted_set = set(each)
            each_tournament_detail_set = set(tournament_details[index])
            self.assertTrue(
                each_tournament_sorted_set.issubset(each_tournament_detail_set)
            )
