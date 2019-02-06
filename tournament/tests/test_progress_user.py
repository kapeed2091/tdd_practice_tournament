from django.test import TestCase
from django_swagger_utils.drf_server.exceptions import BadRequest
from ib_common.date_time_utils.get_current_datetime import get_current_datetime

import datetime

from tournament.constants.general import TournamentStatus, MatchUserStatus, MatchStatus


class TestProgressUser(TestCase):

    user_id = 'User'
    user1_id = 'User1'
    user2_id = 'User2'
    match1_id = 'Match1'
    match2_id = 'Match2'
    match3_id = 'Match3'

    def setup_common(self):
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

        tournament2 = KoTournament.objects.create(
            created_user_id=self.user_id,
            name='Tournament2',
            no_of_rounds=2,
            start_datetime=now - datetime.timedelta(days=1),
            status=TournamentStatus.IN_PROGRESS.value
        )
        Match.objects.create(
            match_id=self.match3_id,
            user=user1,
            tournament=tournament2,
            score=20,
            round=2,
            status=MatchStatus.COMPLETED.value,
            user_status=MatchUserStatus.WIN.value
        )
        Match.objects.create(
            match_id=self.match3_id,
            user=user2,
            tournament=tournament,
            score=10,
            round=2,
            status=MatchStatus.COMPLETED.value,
            user_status=MatchUserStatus.LOST.value
        )

    def test_progress_winner_to_next_round(self):
        from tournament.models import Match, User

        self.setup_common()
        match2_before = Match.objects.get(match_id=self.match2_id)
        self.assertEqual(match2_before.user, None)
        Match.progress_match_winner_to_next_round(match_id=self.match1_id)

        user1 = User.objects.get(user_id=self.user1_id)
        match2_after = Match.objects.get(match_id=self.match2_id)
        self.assertEqual(match2_after.user, user1)

    def test_there_is_no_next_round_to_progress(self):
        from tournament.models import Match

        self.setup_common()
        with self.assertRaisesMessage(BadRequest, 'There are no further rounds in this tournament'):
            Match.progress_match_winner_to_next_round(match_id=self.match3_id)

    def test_get_match_to_progress(self):
        from tournament.models import Match, KoTournament

        self.setup_get_match_to_progress()

        tournament1 = KoTournament.objects.get(
            name='Tournament1'
        )
        match = Match.get_match_to_assign_v2(round=2, tournament=tournament1)
        self.assertEqual(match.user, None)
        self.assertEqual(match.round, 2)
        self.assertEqual(match.tournament, tournament1)

    def setup_get_match_to_progress(self):
        from tournament.models import Match, KoTournament

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
            for j in range(1, 5):
                Match.objects.create(
                    match_id=match_id + str(i) + str(j),
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
