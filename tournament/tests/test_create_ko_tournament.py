from django.test import TestCase


class TestCreateKOTournament(TestCase):

    def testcase_create_ko_tournament(self):
        import datetime
        user_id = 'user_1'
        id = '1'
        tournament_name = 'tournament_1'
        number_of_rounds = 2
        start_datetime = datetime.datetime(2019, 1, 30, 15, 00, 00)
        tournament_status = 'CAN_JOIN'

        from tournament.models import KOTournament
        tournament_details = KOTournament.create_tournament(
            user_id=user_id, id=id, name=tournament_name,
            number_of_rounds=number_of_rounds,
            start_datetime=start_datetime,
            tournament_status=tournament_status)

        self.assertEquals(id, tournament_details['id'])
        self.assertEquals(tournament_name, tournament_details['name'])
        self.assertEquals(number_of_rounds, tournament_details[
            'number_of_rounds'])
        self.assertEquals(start_datetime, tournament_details['start_datetime'])
        self.assertEquals(tournament_status, tournament_details[
            'tournament_status'])