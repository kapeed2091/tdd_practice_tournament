from django.test import TestCase


class TestUserGetOpponentProfile(TestCase):

    def testcase_user_get_opponent_profile_for_any_round_in_tournament(self):
        from tournament.models import TournamentMatch, UserProfile
        user_id_1 = 'user_1'
        name_1 = 'John'
        age_1 = 24
        gender_1 = 'MALE'

        user_id_2 = 'user_2'
        name_2 = 'Robin'
        age_2 = 25
        gender_2 = 'FEMALE'

        user_id_3 = 'user_3'
        name_3 = 'Lee'
        age_3 = 28
        gender_3 = 'MALE'

        user_2_profile = {
            'name': name_2,
            'age': age_2,
            'gender': gender_2
        }

        user_3_profile = {
            'name': name_3,
            'age': age_3,
            'gender': gender_3
        }

        t_id = 'tournament_1'
        t_round_number_1 = 1
        t_round_number_2 = 2

        UserProfile.objects.create(
            user_id=user_id_1, name=name_1, age=age_1, gender=gender_1)
        UserProfile.objects.create(
            user_id=user_id_2, name=name_2, age=age_2, gender=gender_2)
        UserProfile.objects.create(
            user_id=user_id_3, name=name_3, age=age_3, gender=gender_3)

        TournamentMatch.objects.create(
            t_id=t_id, t_round_number=t_round_number_1, player_one=user_id_1,
            player_two=user_id_2)

        TournamentMatch.objects.create(
            t_id=t_id, t_round_number=t_round_number_2, player_one=user_id_1,
            player_two=user_id_3)

        round_1_opponent_profile = UserProfile.get_opponent_user_profile(
            tournament_id=t_id, round_number=t_round_number_1,
            user_id=user_id_1)

        round_2_opponent_profile = UserProfile.get_opponent_user_profile(
            tournament_id=t_id, round_number=t_round_number_2,
            user_id=user_id_1)

        self.assertEquals(round_1_opponent_profile, user_2_profile)
        self.assertEquals(round_2_opponent_profile, user_3_profile)
