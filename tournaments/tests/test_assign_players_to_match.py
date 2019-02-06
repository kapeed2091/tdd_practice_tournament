from .test_utils import TestUtils


class TestAssignPlayersToMatch(TestUtils):

    def test_assign_players_successful(self):
        user = self.create_user()

        users = []
        for each in range(4):
            name = "John-" + str(each + 2)
            users.append(self.create_user(name=name))

        tournament = self.create_tournament(user_id=user.id)

        self.create_tournament_matches(
            tournament_id=tournament.id, total_rounds=tournament.total_rounds
        )

        round_number = 3

        for each_user in users:
            self.create_user_tournament(
                user_id=each_user.id,
                tournament_id=tournament.id,
                round_number=round_number
            )

        from tournaments.models import UserMatch

        initial_count_of_user_matches = UserMatch.objects.all().count()
        UserMatch.assign_players(
            tournament_id=tournament.id, round_number=round_number
        )
        final_count_of_user_matches = UserMatch.objects.all().count()

        number_of_people_in_round = 2 ** (
                tournament.total_rounds - round_number + 1)

        self.assertEqual(0, initial_count_of_user_matches)
        self.assertEqual(number_of_people_in_round,
                         final_count_of_user_matches)

    def test_insufficient_members_in_round(self):
        user = self.create_user()

        users = []
        for each in range(3):
            name = "John-" + str(each + 2)
            users.append(self.create_user(name=name))

        tournament = self.create_tournament(user_id=user.id)

        self.create_tournament_matches(
            tournament_id=tournament.id, total_rounds=tournament.total_rounds
        )

        round_number = 3

        for each_user in users:
            self.create_user_tournament(
                user_id=each_user.id,
                tournament_id=tournament.id,
                round_number=round_number
            )

        from tournaments.models import UserMatch
        from tournaments.exceptions.custom_exceptions import \
            InsufficientMembersInRound
        with self.assertRaises(InsufficientMembersInRound):
            UserMatch.assign_players(
                tournament_id=tournament.id, round_number=round_number
            )

    def test_inadequate_number_of_matches(self):
        user = self.create_user()

        users = []
        for each in range(4):
            name = "John-" + str(each + 2)
            users.append(self.create_user(name=name))

        tournament = self.create_tournament(user_id=user.id)

        self.create_tournament_matches(
            tournament_id=tournament.id,
            total_rounds=tournament.total_rounds - 2
        )

        round_number = 3

        for each_user in users:
            self.create_user_tournament(
                user_id=each_user.id,
                tournament_id=tournament.id,
                round_number=round_number
            )

        from tournaments.models import UserMatch
        from tournaments.exceptions.custom_exceptions import \
            InadequateNumberOfMatches
        with self.assertRaises(InadequateNumberOfMatches):
            UserMatch.assign_players(
                tournament_id=tournament.id, round_number=round_number
            )

    def test_re_assigning_players(self):
        user = self.create_user()

        users = []
        for each in range(4):
            name = "John-" + str(each + 2)
            users.append(self.create_user(name=name))

        tournament = self.create_tournament(user_id=user.id)

        matches = self.create_tournament_matches(
            tournament_id=tournament.id, total_rounds=tournament.total_rounds
        )

        round_number = 3

        players = []
        for each_user in users:
            obj = self.create_user_tournament(
                user_id=each_user.id,
                tournament_id=tournament.id,
                round_number=round_number
            )
            players.append(obj)

        matches_ = [each for each in matches if
                    each.round_number == round_number]
        self.assign_players_to_matches(matches=matches_, players=players)

        from tournaments.models import UserMatch

        from tournaments.exceptions.custom_exceptions import \
            ReAssignmentOfPlayers
        with self.assertRaises(ReAssignmentOfPlayers):
            UserMatch.assign_players(
                tournament_id=tournament.id, round_number=round_number
            )
