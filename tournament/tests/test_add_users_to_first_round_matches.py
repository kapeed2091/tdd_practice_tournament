from django.test import TestCase


class TestAddUserToFirstRoundMatch(TestCase):
    tournament = None

    def test_add_users_to_first_round_matches(self):
        from tdd_practice.constants.general import TournamentStatus

        self._create_tournament(status=TournamentStatus.IN_PROGRESS.value)
        users = self._populate_users()
        self._subscribe_users_to_tournament(users)
        self._create_round_matches()

        from tournament.models import RoundMatch
        RoundMatch.add_users_to_match(tournament_id=self.tournament.id)

        user_ids = [x.id for x in users]
        self.assertListEqual(user_ids, self._get_first_round_user_ids())

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
        no_of_rounds = self.tournament.no_of_rounds
        no_of_participants = 2**no_of_rounds

        users = []
        for index in range(no_of_participants):
            users.append(User.objects.create(username="user"+str(index+1)))
        return users

    def _subscribe_users_to_tournament(self, users):
        from tournament.models import TournamentUser

        for user in users:
            TournamentUser.objects.create(
                tournament_id=self.tournament.id, user_id=user.id)

    def _get_first_round_user_ids(self):
        from tournament.models import Match
        return list(Match.objects.filter(
            round_match__round_no=1,
            round_match__tournament_id=self.tournament.id).\
            values_list('user_id', flat=True))

    def get_round_matches_count(self):
        no_of_rounds = self.tournament.no_of_rounds
        total_no_of_participants = 2**no_of_rounds

        round_matches_count = {}
        for index in range(0, no_of_rounds):
            no_participants_in_round = total_no_of_participants/2**index
            round_matches_count[index+1] = no_participants_in_round/2
        return round_matches_count

    def _create_round_matches(self):
        round_matches_count = self.get_round_matches_count()

        from tournament.models import RoundMatch
        for round_no, matches_count in round_matches_count.items():
            for index in range(matches_count):
                RoundMatch.objects.create(
                    round_no=round_no, tournament_id=self.tournament.id)
