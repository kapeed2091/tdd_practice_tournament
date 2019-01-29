from django.test import TestCase


class TestCreateKOTournament(TestCase):

    def testcase_create_ko_tournament(self):
        user_id = 'user_1'
        from tournament.models import KOTournament

        tournament_details = KOTournament.create_tournament(
            user_id, id, name, number_of_rounds, start_datetime,
            tournament_status)

        self.assertEquals(id, tournament_details['id'])
        self.assertEquals(name, tournament_details['name'])
        self.assertEquals(number_of_rounds, tournament_details[
            'number_of_rounds'])
        self.assertEquals(start_datetime, tournament_details['start_datetime'])
        self.assertEquals(tournament_status, tournament_details[
            'tournament_status'])