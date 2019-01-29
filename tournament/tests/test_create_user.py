from django.test import TestCase


class TestCreateUser(TestCase):

    def test_create_user(self):
        username = 'user1'
        from tournament.models import Player
        Player.create_player(username)
        player_details = Player.get_player_dict(username=username)
        self.assertEqual(player_details['username'], username)
