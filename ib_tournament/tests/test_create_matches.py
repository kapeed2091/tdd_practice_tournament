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


class TestCreateMatches(TestCase):

    @staticmethod
    def create_tournament(tournament_details):
        from ib_tournament.models import Tournament
        from ib_common.date_time_utils.convert_string_to_local_date_time \
            import convert_string_to_local_date_time
        from ib_tournament.constants.general import DEFAULT_DATE_TIME_FORMAT

        start_datetime = convert_string_to_local_date_time(
            tournament_details['start_datetime'], DEFAULT_DATE_TIME_FORMAT)
        tournament = Tournament.objects.create(
            total_rounds=tournament_details['total_rounds'],
            start_datetime=start_datetime, name=tournament_details['name'])
        return tournament.id

    def test_create_matches(self):
        from ib_tournament.models import TournamentMatch

        tournament_details = {
            'total_rounds': 2,
            'start_datetime': get_next_day_datetime_str(),
            'name': 'Tournament 1'
        }
        tournament_id = self.create_tournament(tournament_details)

        pre_tournament_matches_count = TournamentMatch.objects.count()
        TournamentMatch.create_matches(tournament_id)
        post_tournament_matches_count = TournamentMatch.objects.count()
        self.assertEqual(
            post_tournament_matches_count - pre_tournament_matches_count, 3)

    def test_create_round_wise_matches(self):
        from ib_tournament.models import TournamentMatch

        tournament_details = {
            'total_rounds': 2,
            'start_datetime': get_next_day_datetime_str(),
            'name': 'Tournament 1'
        }
        tournament_id = self.create_tournament(tournament_details)

        pre_round_1_matches = TournamentMatch.objects.filter(
            round_no=1).count()
        pre_round_2_matches = TournamentMatch.objects.filter(
            round_no=2).count()
        TournamentMatch.create_matches(tournament_id)
        post_round_1_matches = TournamentMatch.objects.filter(
            round_no=1).count()
        post_round_2_matches = TournamentMatch.objects.filter(
            round_no=2).count()
        self.assertEqual(post_round_1_matches - pre_round_1_matches, 2)
        self.assertEqual(post_round_2_matches - pre_round_2_matches, 1)
