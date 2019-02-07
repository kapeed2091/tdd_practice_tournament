from django.test import TestCase


class TestCreateUserProfile(TestCase):

    def testcase_create_user_profile(self):
        from tournament.models import UserProfile

        user_id_1 = 'user_1'
        name_1 = 'John'
        age_1 = 24
        gender_1 = 'MALE'

        old_state = list(UserProfile.objects.filter(user_id=user_id_1))

        UserProfile.create_user_profile(
            user_id=user_id_1, name=name_1, age=age_1, gender=gender_1)

        new_state = list(UserProfile.objects.filter(user_id=user_id_1))

        diff = list(set(new_state).difference(set(old_state)))

        self.assertEquals(len(new_state) - len(old_state), 1)
        self.assertEquals(diff[0].name, name_1)
        self.assertEquals(diff[0].age, age_1)
        self.assertEquals(diff[0].gender, gender_1)
