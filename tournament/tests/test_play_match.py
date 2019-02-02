from django.test import TestCase


class TestPlayMatch(TestCase):
    username = "user1"
    user = None
    match = None

    def test_play_match(self):
        self._populate_user()
        self._create_match()
        from tournament.models.match import Match
        Match.play_match(match_id=self.match.id, user_id=self.user.id)

        self.match = self._get_match()
        self.assertEqual(self.match.status, "IN_PROGRESS")

    def _populate_user(self):
        from tournament.models.user import User
        self.user = User.objects.create(username=self.username)

    def _create_match(self):
        from tournament.models import Match
        self.match = Match.objects.create(user_id=self.user.id)

    def _get_match(self):
        from tournament.models.match import Match
        return Match.objects.get(id=self.match.id)