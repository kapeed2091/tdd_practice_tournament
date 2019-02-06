from django.test import TestCase


class TestGetMatchWinner(TestCase):
    users = []

    def test_get_match_winner(self):
        from tdd_practice.constants.general import TournamentStatus
        self.users = self._populate_users()
        self._create_tournament(status=TournamentStatus.IN_PROGRESS.value)
        self._create_user_matches()

        user_id_wise_score = {}
        for index, user in enumerate(self.users):
            score = 10
            user_id_wise_score[user.id] = score + index*10

        self._submit_users_score(user_id_wise_score)

        from tournament.models import RoundMatch
        winner_id = RoundMatch.get_match_winner(match_id=self.match.id)

        expected_winner_id = self.users[1].id

        self.assertEqual(expected_winner_id, winner_id)

    def test_get_match_winner_for_tie_match(self):
        from tdd_practice.constants.general import TournamentStatus
        self.users = self._populate_users()
        self._create_tournament(status=TournamentStatus.IN_PROGRESS.value)
        self._create_user_matches()

        user_id_wise_score = {}
        for index, user in enumerate(self.users):
            score = 10
            user_id_wise_score[user.id] = score

        self._submit_users_score(user_id_wise_score)

        from tournament.models import RoundMatch
        winner_id = RoundMatch.get_match_winner(match_id=self.match.id)

        expected_winner_id = self.users[0].id

        self.assertEqual(expected_winner_id, winner_id)

    def _create_user_matches(self):
        from tournament.models import RoundMatch
        self.match = RoundMatch.objects.create(
            tournament_id=self.tournament.id, round_no=1)

        from tournament.models import Match
        for user in self.users:
            Match.objects.create(
                user_id=user.id, tournament=self.tournament,
                round_match_id=self.match.id)

    def _create_tournament(self, status):
        from ib_common.date_time_utils.get_current_local_date_time \
            import get_current_local_date_time
        from datetime import timedelta
        from tournament.models import Tournament

        curr_datetime = get_current_local_date_time()
        self.tournament = Tournament.objects.create(
            name="Knock Out",
            no_of_rounds=3,
            start_datetime=curr_datetime + timedelta(days=1),
            status=status)

    def _populate_users(self):
        from tournament.models.user import User
        no_of_participants = 2

        users = []
        for index in range(no_of_participants):
            users.append(User.objects.create(username="user"+str(index+1)))
        return users

    def _submit_users_score(self, user_id_wise_score):
        from tournament.models import Match
        from tdd_practice.constants.general import UserMatchStatus
        from ib_common.date_time_utils.get_current_local_date_time \
            import get_current_local_date_time

        for user_id, score in user_id_wise_score.items():
            curr_datetime = get_current_local_date_time()
            user_match = Match.objects.get(
                round_match_id=self.match.id, user_id=user_id)
            user_match.score = score
            user_match.status = UserMatchStatus.COMPLETED.value
            user_match.score_submission_datetime = curr_datetime
            user_match.save()
