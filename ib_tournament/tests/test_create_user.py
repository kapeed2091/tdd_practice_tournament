from django.test import TestCase


class TestCreateUser(TestCase):

    def test_create_user(self):
        username = 'user1'
        from ib_tournament.models import Player
        Player.create_player(username)
        player = Player.get_player(username)
        player_details = player.get_player_dict()
        self.assertEqual(player_details['username'], username)

    def test_unique_username(self):
        username_1 = 'user1'
        username_2 = 'user1'
        from ib_tournament.models import Player
        Player.create_player(username_1)
        from django_swagger_utils.drf_server.exceptions import BadRequest
        with self.assertRaisesMessage(BadRequest, "Username already Exists"):
            Player.create_player(username_2)
