from django.db import models
from tournament.constants.general import T_ID_MAX_LENGTH, USER_ID_MAX_LENGTH,\
    PlayerMatchStatus, MatchStatus


class TournamentMatch(models.Model):
    MATCH_ID_MAX_LENGTH = 20
    PLAYER_MATCH_STATUS_MAX_LENGTH = 20
    MATCH_STATUS_MAX_LENGTH = 20

    t_id = models.CharField(max_length=T_ID_MAX_LENGTH)
    player_one = models.CharField(max_length=USER_ID_MAX_LENGTH)
    player_one_match_status = models.CharField(
        max_length=PLAYER_MATCH_STATUS_MAX_LENGTH,
        default=PlayerMatchStatus.YET_TO_START.value)

    player_two = models.CharField(max_length=USER_ID_MAX_LENGTH)
    player_two_match_status = models.CharField(
        max_length=PLAYER_MATCH_STATUS_MAX_LENGTH,
        default=PlayerMatchStatus.YET_TO_START.value)

    match_id = models.CharField(max_length=MATCH_ID_MAX_LENGTH)
    match_status = models.CharField(max_length=MATCH_STATUS_MAX_LENGTH,
                                    default=MatchStatus.YET_TO_START.value)

    @classmethod
    def create_match(cls, request_data):
        from tournament.models import KOTournament, UserProfile, TournamentUser
        KOTournament.validate_tournament_for_create_match(
            tournament_id=request_data['tournament_id'])
        UserProfile.validate_users(user_id_1=request_data['player_one_user_id'],
                                   user_id_2=request_data['player_two_user_id'])
        TournamentUser.validate_users_subscription(
            tournament_id=request_data['tournament_id'],
            user_id_1=request_data['player_one_user_id'],
            user_id_2=request_data['player_two_user_id'])
        return cls.objects.create(
            t_id=request_data['tournament_id'],
            player_one=request_data['player_one_user_id'],
            player_two=request_data['player_two_user_id'])

    @classmethod
    def create_match_and_assign_match_id(cls, create_match_request, match_id):
        cls.validate_match_id(match_id=match_id)
        match_obj = cls.create_match(request_data=create_match_request)
        match_obj.assign_match_id_to_match(match_id=match_id)

    @classmethod
    def user_play_match(cls, user_id, tournament_id, match_id):
        from tournament.models import KOTournament, UserProfile, TournamentUser
        KOTournament.validate_tournament_for_play_match(
            tournament_id=tournament_id)
        cls.validate_match_id_for_play_match(match_id=match_id)
        UserProfile.is_registered_user(user_id=user_id)
        TournamentUser.validate_user_subscription(
            tournament_id=tournament_id, user_id=user_id)
        cls.validate_user_belong_to_match(user_id=user_id, match_id=match_id)
        cls.update_user_match_status_for_play_match(
            user_id=user_id, match_id=match_id, tournament_id=tournament_id)


    @classmethod
    def validate_match_id(cls, match_id):
        if cls.does_match_exist(match_id=match_id):
            from tournament.constants.exception_messages import \
                MATCH_ID_ALREADY_ASSIGNED_TO_ANOTHER_MATCH
            raise Exception(*MATCH_ID_ALREADY_ASSIGNED_TO_ANOTHER_MATCH)

    @classmethod
    def validate_match_id_for_play_match(cls, match_id):
        if not cls.does_match_exist(match_id=match_id):
            from tournament.constants.exception_messages import \
                MATCH_DOES_NOT_EXIST
            raise Exception(*MATCH_DOES_NOT_EXIST)

    @classmethod
    def does_match_exist(cls, match_id):
        return cls.objects.filter(match_id=match_id).exists()

    def assign_match_id_to_match(self, match_id):
        self.match_id = match_id
        self.save()

    @classmethod
    def update_status_for_user_play_match(cls, tournament_obj):
        tournament_obj.player_one_match_status = \
            PlayerMatchStatus.IN_PROGRESS.value
        tournament_obj.match_status = MatchStatus.IN_PROGRESS.value
        tournament_obj.save()

    @classmethod
    def validate_user_belong_to_match(cls, user_id, match_id):
        if not cls.does_user_belong_to_match(user_id=user_id, match_id=match_id):
            from tournament.constants.exception_messages import \
                USER_DOES_NOT_BELONG_TO_MATCH
            raise Exception(*USER_DOES_NOT_BELONG_TO_MATCH)

    @classmethod
    def does_user_belong_to_match(cls, user_id, match_id):
        return cls.objects.filter(
            match_id=match_id, player_one=user_id).exists() |\
               cls.objects.filter(
            match_id=match_id, player_two=user_id).exists()

    @classmethod
    def is_player_one(cls, user_id, match_id):
        return cls.objects.filter(match_id=match_id,
                                  player_one=user_id).exists()

    @classmethod
    def is_player_two(cls, user_id, match_id):
        return cls.objects.filter(match_id=match_id,
                                  player_two=user_id).exists()

    @classmethod
    def is_user_player_one_or_two(cls, user_id, match_id):
        if cls.is_player_one(user_id=user_id, match_id=match_id):
            return 'player_one'
        if cls.is_player_two(user_id=user_id, match_id=match_id):
            return 'player_two'

    @classmethod
    def update_user_match_status_for_play_match(cls,user_id, match_id, tournament_id):
        if cls.is_user_player_one_or_two(user_id=user_id, match_id=match_id) == 'player_one':
            tm_obj = cls.objects.get(
                player_one=user_id, match_id=match_id,
                t_id=tournament_id)
            tm_obj.player_one_match_status = \
                PlayerMatchStatus.IN_PROGRESS.value
            tm_obj.match_status = MatchStatus.IN_PROGRESS.value
            tm_obj.save()
        if cls.is_user_player_one_or_two(user_id=user_id, match_id=match_id) == 'player_two':
            tm_obj = cls.objects.get(
                player_two=user_id, match_id=match_id,
                t_id=tournament_id)
            tm_obj.player_two_match_status = \
                PlayerMatchStatus.IN_PROGRESS.value
            tm_obj.match_status = MatchStatus.IN_PROGRESS.value
            tm_obj.save()
