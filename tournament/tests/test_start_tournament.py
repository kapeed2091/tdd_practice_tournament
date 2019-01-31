from django.test import TestCase

from tdd_practice.constants.general import TournamentStatus


class TestStartTournament(TestCase):
    tournament_status = TournamentStatus.CAN_JOIN.value
    tournament = None

    def test_start_tournament(self):
        from tournament.models import Tournament
        self._create_tournament()
        Tournament.start_tournament(tournament_id=self.tournament.id)

        from tournament.models import Tournament
        tournament = Tournament.objects.get(id=self.tournament.id)

        from tournament.models.tournament_match import TournamentMatch
        no_matches = \
            TournamentMatch.objects.filter(tournament_id=tournament.id).count()

        self.assertEquals(TournamentStatus.IN_PROGRESS.value,
                          tournament.status)
        self.assertEquals(self._calculate_no_matches(), no_matches)

    def _create_tournament(self):
        from tournament.models import Tournament
        from ib_common.date_time_utils.get_current_local_date_time \
            import get_current_local_date_time

        curr_datetime = get_current_local_date_time()
        self.tournament = Tournament.objects.create(
            name="Knock Out",
            no_of_rounds=3,
            start_datetime=curr_datetime,
            status=self.tournament_status)

    def _calculate_no_matches(self):
        no_of_rounds = self.tournament.no_of_rounds
        no_of_participants = 2**no_of_rounds
        no_of_matches = no_of_participants - 1
        return no_of_matches
