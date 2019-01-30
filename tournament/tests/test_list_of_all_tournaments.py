from django.test import TestCase


class TestListAllTournaments(TestCase):

    def testcase_list_all_tournaments_when_no_tournaments(self):
        from tournament.models import KOTournament

        all_tournaments = KOTournament.get_all_tournaments()
        self.assertEquals(all_tournaments, [])
