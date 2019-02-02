from django.test import TestCase


class TestCreateRoundMatch(TestCase):
    user = None
    match = None
    tournament = None

    def test_create_round_matches(self):
        from tdd_practice.constants.general import TournamentStatus

        self._create_tournament(status=TournamentStatus.IN_PROGRESS.value)

        RoundMatch.create_round_matches(self.tournament.id)

        round_matches_count = self.get_round_matches_count()

        for round_no, expected_matches_count in round_matches_count.items():
            matches_count = \
                self._get_round_matches_count(round_no)
            self.assertEqual(expected_matches_count, matches_count)

    def _create_tournament(self, status):
        from ib_common.date_time_utils.get_current_local_date_time \
            import get_current_local_date_time
        from tournament.models import Tournament

        curr_datetime = get_current_local_date_time()
        self.tournament = Tournament.objects.create(
            name="Knock Out",
            no_of_rounds=3,
            start_datetime=curr_datetime,
            status=status)

    def get_round_matches_count(self):
        no_of_rounds = self.tournament.no_of_rounds
        total_no_of_participants = 2**no_of_rounds

        round_matches_count = {}
        for round_no in range(1, no_of_rounds+1):
            no_participants_in_round = total_no_of_participants/2**round_no
            round_matches_count[round_no] = no_participants_in_round/2
        return round_matches_count

    def _get_round_matches_count(self, round_no):
        return RoundMatch.objects.filter(tournament_id=self.tournament.id,
                                  round_no=round_no).count()