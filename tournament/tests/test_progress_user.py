from django.test import TestCase
from django_swagger_utils.drf_server.exceptions import BadRequest, NotFound
from ib_common.date_time_utils.get_current_datetime import get_current_datetime

import datetime

from tournament.constants.general import TournamentStatus, MatchUserStatus, MatchStatus


class TestProgressUser(TestCase):

    user_id = 'User'
    user1_id = 'User1'
    user2_id = 'User2'
    match1_id = 'Match1'
    match2_id = 'Match2'
    tournament_name = 'Tournament'

    def test_progress_winner_to_next_round(self):
        from tournament.models import Match, User

        self.setup_progress_winner_to_next_round()
        match2_before = Match.objects.get(match_id=self.match2_id)
        self.assertEqual(match2_before.user, None)
        Match.progress_match_winner_to_next_round(match_id=self.match1_id)

        user1 = User.objects.get(user_id=self.user1_id)
        match2_after = Match.objects.get(match_id=self.match2_id)
        self.assertEqual(match2_after.user, user1)

    def setup_progress_winner_to_next_round(self):
        from tournament.models import User, KoTournament, Match

        now = get_current_datetime()
        user1 = User.objects.create(
            user_id=self.user1_id
        )
        user2 = User.objects.create(
            user_id=self.user2_id
        )
        tournament = KoTournament.objects.create(
            created_user_id=self.user_id,
            name='Tournament',
            no_of_rounds=2,
            start_datetime=now - datetime.timedelta(days=1),
            status=TournamentStatus.IN_PROGRESS.value
        )
        Match.objects.create(
            match_id=self.match1_id,
            user=user1,
            tournament=tournament,
            score=20,
            round=1,
            status=MatchStatus.COMPLETED.value,
            user_status=MatchUserStatus.WIN.value
        )
        Match.objects.create(
            match_id=self.match1_id,
            user=user2,
            tournament=tournament,
            score=10,
            round=1,
            status=MatchStatus.COMPLETED.value,
            user_status=MatchUserStatus.LOST.value
        )
        Match.objects.create(
            match_id=self.match2_id,
            tournament=tournament,
            round=2,
            status=MatchStatus.YET_TO_START.value,
        )

    def test_there_is_no_next_round_to_progress(self):
        from tournament.models import Match

        self.setup_there_is_no_next_round_to_progress()
        with self.assertRaisesMessage(BadRequest, 'There are no further rounds in this tournament'):
            Match.progress_match_winner_to_next_round(match_id=self.match1_id)

    def setup_there_is_no_next_round_to_progress(self):
        from tournament.models import User, KoTournament, Match

        now = get_current_datetime()
        user1 = User.objects.create(
            user_id=self.user1_id
        )
        user2 = User.objects.create(
            user_id=self.user2_id
        )

        tournament = KoTournament.objects.create(
            created_user_id=self.user_id,
            name='Tournament',
            no_of_rounds=2,
            start_datetime=now - datetime.timedelta(days=1),
            status=TournamentStatus.IN_PROGRESS.value
        )

        match_id = 'Match'
        Match.objects.create(
            match_id=self.match1_id,
            user=user1,
            tournament=tournament,
            score=20,
            round=2,
            status=MatchStatus.COMPLETED.value,
            user_status=MatchUserStatus.WIN.value
        )
        Match.objects.create(
            match_id=self.match1_id,
            user=user2,
            tournament=tournament,
            score=10,
            round=2,
            status=MatchStatus.COMPLETED.value,
            user_status=MatchUserStatus.LOST.value
        )

    def test_get_match_to_progress(self):
        from tournament.models import Match, KoTournament

        self.setup_get_match_to_progress()

        tournament1 = KoTournament.objects.get(
            name='Tournament1'
        )
        match = Match.get_match_to_assign(match_round=2, tournament=tournament1)
        self.assertEqual(match.user, None)
        self.assertEqual(match.round, 2)
        self.assertEqual(match.tournament, tournament1)

    def setup_get_match_to_progress(self):
        from tournament.models import User, Match, KoTournament

        user = User.objects.create(
            user_id='User'
        )

        now = get_current_datetime()
        tournament_name = 'Tournament'
        for i in range(1, 3):
            tournament = KoTournament.objects.create(
                created_user_id=self.user_id,
                name=tournament_name + str(i),
                no_of_rounds=3,
                start_datetime=now - datetime.timedelta(days=1),
                status=TournamentStatus.IN_PROGRESS.value
            )

            match_id = 'Match'
            for j in range(1, 4):
                Match.objects.create(
                    match_id=match_id + str(i) + str(j),
                    tournament=tournament,
                    round=2,
                    status=MatchStatus.YET_TO_START.value,
                    user_status=MatchUserStatus.NOT_DECIDED_YET.value
                )
            for j in range(4, 5):
                Match.objects.create(
                    match_id=match_id + str(i) + str(j),
                    user=user,
                    tournament=tournament,
                    round=2,
                    status=MatchStatus.YET_TO_START.value,
                    user_status=MatchUserStatus.NOT_DECIDED_YET.value
                )
            for j in range(1, 3):
                Match.objects.create(
                    match_id=match_id + str(i) + str(j),
                    tournament=tournament,
                    round=3,
                    status=MatchStatus.YET_TO_START.value,
                    user_status=MatchUserStatus.NOT_DECIDED_YET.value
                )

    def test_get_match_to_progress_there_are_no_vacant_matches(self):
        from tournament.models import Match, KoTournament

        self.setup_get_match_to_progress_there_are_no_vacant_matches()

        tournament1 = KoTournament.objects.get(
            name=self.tournament_name
        )

        with self.assertRaisesMessage(NotFound, 'There are no vacant matches'):
            Match.get_match_to_assign(match_round=3, tournament=tournament1)

    def setup_get_match_to_progress_there_are_no_vacant_matches(self):
        from tournament.models import User, Match, KoTournament

        user1 = User.objects.create(
            user_id=self.user1_id
        )
        user2 = User.objects.create(
            user_id=self.user2_id
        )

        now = get_current_datetime()
        tournament = KoTournament.objects.create(
            created_user_id=self.user_id,
            name=self.tournament_name,
            no_of_rounds=3,
            start_datetime=now - datetime.timedelta(days=1),
            status=TournamentStatus.IN_PROGRESS.value
        )

        match_id = 'Match'
        Match.objects.create(
            match_id=match_id,
            user=user1,
            tournament=tournament,
            round=3,
            status=MatchStatus.YET_TO_START.value,
            user_status=MatchUserStatus.NOT_DECIDED_YET.value
        )
        Match.objects.create(
            match_id=match_id,
            user=user2,
            tournament=tournament,
            round=3,
            status=MatchStatus.YET_TO_START.value,
            user_status=MatchUserStatus.NOT_DECIDED_YET.value
        )
