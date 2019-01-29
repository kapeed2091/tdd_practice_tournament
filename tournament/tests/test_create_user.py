from django.test import TestCase


class TestCreateUser(TestCase):

    def test_create_user(self):
        username = 'user1'
        from tournament.models import Player
        Player.create_player(username)
        player = Player.objects.get(username=username)
        self.assertEqual(player.username, username)
