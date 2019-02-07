from django.db import models
from tournament.constants.general import T_ID_MAX_LENGTH, USER_ID_MAX_LENGTH,\
    PlayerMatchStatus, MatchStatus


class TournamentMatch(models.Model):
    MATCH_ID_MAX_LENGTH = 20
    PLAYER_MATCH_STATUS_MAX_LENGTH = 20
    MATCH_STATUS_MAX_LENGTH = 20

    t_id = models.CharField(max_length=T_ID_MAX_LENGTH)
    t_round_number = models.IntegerField()

    player_one = models.CharField(max_length=USER_ID_MAX_LENGTH)
    player_one_match_status = models.CharField(
        max_length=PLAYER_MATCH_STATUS_MAX_LENGTH,
        default=PlayerMatchStatus.YET_TO_START.value)
    player_one_score = models.IntegerField(default=0)
    player_one_submit_time = models.DateTimeField(null=True)

    player_two = models.CharField(max_length=USER_ID_MAX_LENGTH)
    player_two_match_status = models.CharField(
        max_length=PLAYER_MATCH_STATUS_MAX_LENGTH,
        default=PlayerMatchStatus.YET_TO_START.value)
    player_two_score = models.IntegerField(default=0)
    player_two_submit_time = models.DateTimeField(null=True)

    match_id = models.CharField(max_length=MATCH_ID_MAX_LENGTH)
    match_status = models.CharField(max_length=MATCH_STATUS_MAX_LENGTH,
                                    default=MatchStatus.YET_TO_START.value)
    winner_user_id = models.CharField(max_length=20)

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
            player_two=request_data['player_two_user_id'],
            t_round_number=request_data['t_round_number'])

    @classmethod
    def create_match_and_assign_match_id(cls, create_match_request, match_id):
        cls.validate_match_id_to_assign(match_id=match_id)
        match_obj = cls.create_match(request_data=create_match_request)
        match_obj.assign_match_id_to_match(match_id=match_id)

    @classmethod
    def user_play_match(cls, user_id, tournament_id, match_id):
        from tournament.models import KOTournament, UserProfile, TournamentUser
        KOTournament.validate_tournament_for_play_match(
            tournament_id=tournament_id)
        cls.validate_match_id(match_id=match_id)
        UserProfile.is_registered_user(user_id=user_id)
        TournamentUser.validate_user_subscription(
            tournament_id=tournament_id, user_id=user_id)
        cls.validate_user_belong_to_match(user_id=user_id, match_id=match_id)
        cls.update_match_data_for_play_match(
            user_id=user_id, match_id=match_id, tournament_id=tournament_id)

    @classmethod
    def user_submit_score(cls, user_id, match_id, score):
        cls.validate_user_and_match(user_id=user_id, match_id=match_id)
        cls.update_score(user_id=user_id, match_id=match_id, score=score)

    @classmethod
    def user_submit_score_with_time(cls, user_id, match_id, score, submit_time):
        cls.update_player_score_and_time(
            user_id=user_id, match_id=match_id, score=score,
            submit_time=submit_time)

    @classmethod
    def decide_winner(cls, match_id):
        tournament_match_obj = cls.objects.get(match_id=match_id)
        tournament_match_obj.assign_winner()

    @classmethod
    def winner_progress_to_next_round(cls, match_id):
        from tournament.models import TournamentUser

        tournament_match_obj = cls.objects.get(match_id=match_id)
        TournamentUser.progress_user_to_next_round(
            user_id=tournament_match_obj.winner_user_id,
            t_id=tournament_match_obj.t_id)

    @classmethod
    def get_opponent_user_profile(cls, tournament_id, round_number, user_id):
        from tournament.models import UserProfile

        opponent_user_id = cls.get_opponent_user_id(
            tournament_id=tournament_id, round_number=round_number,
            user_id=user_id)
        opponent_user_profile = UserProfile.get_user_profile(
            user_id=opponent_user_id)

        return opponent_user_profile

    @classmethod
    def get_tournament_winner_profile(cls, tournament_id):
        from tournament.models import UserProfile

        winner_id = cls.get_tournament_winner_user_id(
            tournament_id=tournament_id)
        winner_profile = UserProfile.get_user_profile(user_id=winner_id)

        return winner_profile

    @classmethod
    def get_tournament_winner_user_id(cls, tournament_id):
        from tournament.models import KOTournament

        tournament = KOTournament.get_tournament(tournament_id=tournament_id)
        final_tournament_match_obj = cls.objects.get(
            t_id=tournament_id, t_round_number=tournament.number_of_rounds)

        return final_tournament_match_obj.winner_user_id

    def assign_match_id_to_match(self, match_id):
        self.match_id = match_id
        self.save()

    @classmethod
    def validate_match_id_to_assign(cls, match_id):
        if cls.does_match_exist(match_id=match_id):
            from tournament.constants.exception_messages import \
                MATCH_ID_ALREADY_ASSIGNED_TO_ANOTHER_MATCH
            raise Exception(*MATCH_ID_ALREADY_ASSIGNED_TO_ANOTHER_MATCH)

    @classmethod
    def validate_user_and_match(cls, user_id, match_id):
        from tournament.models import UserProfile
        UserProfile.is_registered_user(user_id=user_id)
        cls.validate_match_id(match_id=match_id)
        cls.validate_user_belong_to_match(user_id=user_id, match_id=match_id)

    @classmethod
    def validate_match_id(cls, match_id):
        if not cls.does_match_exist(match_id=match_id):
            from tournament.constants.exception_messages import \
                MATCH_DOES_NOT_EXIST
            raise Exception(*MATCH_DOES_NOT_EXIST)

    @classmethod
    def validate_user_belong_to_match(cls, user_id, match_id):
        if not cls.does_user_belong_to_match(user_id=user_id, match_id=match_id):
            from tournament.constants.exception_messages import \
                USER_DOES_NOT_BELONG_TO_MATCH
            raise Exception(*USER_DOES_NOT_BELONG_TO_MATCH)

    @classmethod
    def update_match_data_for_play_match(cls, user_id, match_id,
                                         tournament_id):
        if cls.is_user_player_one(user_id=user_id, match_id=match_id):
            tournament_match_obj = cls.objects.get(
                player_one=user_id, match_id=match_id,
                t_id=tournament_id)
            tournament_match_obj.update_player_one_match_status_for_play_match()
            tournament_match_obj.update_match_status_for_play_match()
        if cls.is_user_player_two(user_id=user_id, match_id=match_id):
            tournament_match_obj = cls.objects.get(
                player_two=user_id, match_id=match_id,
                t_id=tournament_id)
            tournament_match_obj.update_player_two_match_status_for_play_match()
            tournament_match_obj.update_match_status_for_play_match()

    def assign_winner(self):
        self.assign_winner_as_player_one()
        self.assign_winner_as_player_two()
        self.decide_winner_during_tie()

    @classmethod
    def update_score(cls, user_id, match_id, score):
        cls.update_player_one_score(
            user_id=user_id, match_id=match_id, score=score)
        cls.update_player_two_score(
            user_id=user_id, match_id=match_id, score=score)

    @classmethod
    def update_player_one_score(cls, user_id, match_id, score):
        if cls.is_user_player_one(user_id=user_id, match_id=match_id):
            tournament_match_obj = cls.objects.get(
                player_one=user_id, match_id=match_id)
            tournament_match_obj.change_player_one_score(score=score)

    @classmethod
    def update_player_two_score(cls, user_id, match_id, score):
        if cls.is_user_player_two(user_id=user_id, match_id=match_id):
            tournament_match_obj = cls.objects.get(
                player_two=user_id, match_id=match_id)
            tournament_match_obj.change_player_two_score(score=score)

    @classmethod
    def does_match_exist(cls, match_id):
        return cls.objects.filter(match_id=match_id).exists()

    @classmethod
    def does_user_belong_to_match(cls, user_id, match_id):
        return cls.is_user_player_one(user_id=user_id, match_id=match_id) | \
               cls.is_user_player_two(user_id=user_id, match_id=match_id)

    @classmethod
    def is_user_player_one(cls, user_id, match_id):
        return cls.objects.filter(match_id=match_id,
                                  player_one=user_id).exists()

    @classmethod
    def is_user_player_two(cls, user_id, match_id):
        return cls.objects.filter(match_id=match_id,
                                  player_two=user_id).exists()

    def update_player_one_match_status_for_play_match(self):
        self.player_one_match_status = \
            PlayerMatchStatus.IN_PROGRESS.value
        self.save()

    def update_player_two_match_status_for_play_match(self):
        self.player_two_match_status = \
            PlayerMatchStatus.IN_PROGRESS.value
        self.save()

    def update_match_status_for_play_match(self):
        self.match_status = MatchStatus.IN_PROGRESS.value
        self.save()

    def change_player_one_score(self, score):
        self.player_one_score = score
        self.save()

    def change_player_two_score(self, score):
        self.player_two_score = score
        self.save()

    def assign_winner_as_player_one(self):
        if self.is_player_one_score_higher_than_player_two():
            self.winner_user_id = self.player_one
            self.save()

    def assign_winner_as_player_two(self):
        if self.is_player_two_score_higher_than_player_one():
            self.winner_user_id = self.player_two
            self.save()

    def is_player_one_score_higher_than_player_two(self):
        if self.player_one_score > self.player_two_score:
            return True
        return False

    def is_player_two_score_higher_than_player_one(self):
        if self.player_two_score > self.player_one_score:
            return True
        return False

    def are_player_one_and_two_scores_equal(self):
        if self.player_one_score == self.player_two_score:
            return True
        return False

    @classmethod
    def update_player_score_and_time(cls, user_id, match_id, score, submit_time):
        cls.update_player_one_score_and_time(
            user_id=user_id, match_id=match_id, score=score,
            submit_time=submit_time)
        cls.update_player_two_score_and_time(
            user_id=user_id, match_id=match_id, score=score,
            submit_time=submit_time)

    @classmethod
    def update_player_one_score_and_time(cls, user_id, match_id, score,
                                         submit_time):
        if cls.is_user_player_one(user_id=user_id, match_id=match_id):
            tournament_match_obj = cls.objects.get(
                player_one=user_id, match_id=match_id)
            tournament_match_obj.change_player_one_score_and_time(
                score=score, submit_time=submit_time)

    @classmethod
    def update_player_two_score_and_time(cls, user_id, match_id, score,
                                         submit_time):
        if cls.is_user_player_two(user_id=user_id, match_id=match_id):
            tournament_match_obj = cls.objects.get(
                player_two=user_id, match_id=match_id)
            tournament_match_obj.change_player_two_score_and_time(
                score=score, submit_time=submit_time)

    def change_player_one_score_and_time(self, score, submit_time):
        self.player_one_submit_time = submit_time
        self.player_one_score = score
        self.save()

    def change_player_two_score_and_time(self, score, submit_time):
        self.player_two_submit_time = submit_time
        self.player_two_score = score
        self.save()

    def decide_winner_during_tie(self):
        if self.are_player_one_and_two_scores_equal():
            self.assign_player_one_as_winner_during_tie()
            self.assign_player_two_as_winner_during_tie()

    def assign_player_one_as_winner_during_tie(self):
        if self.did_player_one_submit_score_first():
            self.winner_user_id = self.player_one
            self.save()

    def assign_player_two_as_winner_during_tie(self):
        if self.did_player_two_submit_score_first():
            self.winner_user_id = self.player_two
            self.save()

    def did_player_one_submit_score_first(self):
        if self.player_one_submit_time < self.player_two_submit_time:
            return True
        return False

    def did_player_two_submit_score_first(self):
        if self.player_two_submit_time < self.player_one_submit_time:
            return True
        return False

    @classmethod
    def get_opponent_user_id(cls, tournament_id, round_number, user_id):
        tournament_match_obj = cls.objects.get(
            t_id=tournament_id, t_round_number=round_number)

        return tournament_match_obj.get_opponent(user_id=user_id)

    def get_opponent(self, user_id):
        if self.is_player_one(user_id=user_id):
            return self.player_two

        if self.is_player_two(user_id=user_id):
            return self.player_one

    def is_player_one(self, user_id):
        if self.player_one == user_id:
            return True
        return False

    def is_player_two(self, user_id):
        if self.player_two == user_id:
            return True
        return False
