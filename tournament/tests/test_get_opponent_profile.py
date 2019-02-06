from django.test import TestCase


class TestGetOpponentProfile(TestCase):
    users = []
    user = None
    tournament = None
    round_wise_opponent_users = {}

    def test_get_opponent_profile(self):
        from tdd_practice.constants.general import TournamentStatus
        self._populate_users()
        self.user = self.users[0]
        round_no = 2

        self._create_tournament(status=TournamentStatus.IN_PROGRESS.value)
        self._create_user_matches()

        from tournament.models import Match
        opponent_profile = Match.\
            get_opponent_user_profile(user_id=self.user.id,
                                      tournament_id=self.tournament.id,
                                      round_no=round_no)

        opponent_user = self.round_wise_opponent_users[round_no]
        exp_opponent_profile = {
            "user_id": opponent_user.id,
            "name": opponent_user.name,
            "gender": opponent_user.gender,
            "age": opponent_user.age
        }
        self.assertEqual(exp_opponent_profile, opponent_profile)

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

    def _populate_users(self):
        from tournament.models.user import User
        no_of_participants = 3

        for index in range(no_of_participants):
            self.users.append(User.objects.create(username="user"+str(index+1)))

    def _subscribe_users_to_tournament(self, users):
        from tournament.models import TournamentUser

        for user in users:
            TournamentUser.objects.create(
                tournament_id=self.tournament.id, user_id=user.id)

    def _create_user_matches(self):
        opponent_users = [x for x in self.users if x.id != self.user.id]

        self.round_wise_opponent_users[1] = opponent_users[0]
        user_ids = [self.user.id, opponent_users[0].id]
        self._create_user_round_matches(round_no=1, user_ids=user_ids)

        self.round_wise_opponent_users[2] = opponent_users[1]
        user_ids = [self.user.id, opponent_users[1].id]
        self._create_user_round_matches(round_no=2, user_ids=user_ids)

    def _create_user_round_matches(self, round_no, user_ids):
        from tournament.models import RoundMatch
        from tournament.models import Match

        match = RoundMatch.objects.create(
            tournament_id=self.tournament.id, round_no=round_no)
        for user_id in user_ids:
            Match.objects.create(
                user_id=user_id, tournament=self.tournament,
                round_match_id=match.id)

