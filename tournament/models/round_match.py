from django.db import models


class RoundMatch(models.Model):
    tournament = models.ForeignKey('tournament.Tournament')
    round_no = models.IntegerField()

    @classmethod
    def create_round_matches(cls, tournament_id):
        from .tournament import Tournament

        tournament = \
            Tournament.get_tournament_by_id(tournament_id=tournament_id)
        no_of_rounds = tournament.no_of_rounds

        for round_no in range(1, no_of_rounds + 1):
            no_of_matches_in_round = \
                cls._calculate_no_of_matches(no_of_rounds=no_of_rounds,
                                                   round_no=round_no)
            cls.create_matches(round_no=round_no,
                               no_of_matches_in_round=no_of_matches_in_round,
                               tournament_id=tournament_id)

    @classmethod
    def create_matches(cls, round_no, no_of_matches_in_round, tournament_id):

        for index in range(no_of_matches_in_round):
            cls.objects.create(round_no=round_no, tournament_id=tournament_id)

    @classmethod
    def get_match_winner(cls, match_id):
        from .match import Match
        user_matches = Match.objects.filter(round_match_id=match_id)

        cls._validate_match_winner(user_matches=user_matches)
        winner_id = cls._calculate_match_winner(user_matches)
        return winner_id

    @classmethod
    def progress_match_winner_to_next_round(cls, winner_details):
        curr_round_no = winner_details['curr_round_no']
        winner_id = winner_details['winner_id']
        tournament_id = winner_details['tournament_id']

        match_id = cls._pick_match_from_next_round(tournament_id=tournament_id,
                                                   curr_round_no=curr_round_no)
        match_id_wise_user_ids = {match_id: [winner_id]}

        from .match import Match
        Match.create_user_match(
            match_id_wise_user_ids=match_id_wise_user_ids,
            tournament_id=tournament_id)

    @classmethod
    def _calculate_no_of_matches(cls, no_of_rounds, round_no):
        from .tournament import Tournament

        no_of_participants = \
            Tournament.calculate_no_participants(no_of_rounds=no_of_rounds)

        no_participants_in_round = \
            cls._calculate_no_participants_in_round(
                no_of_participants=no_of_participants, round_no=round_no)
        no_of_matches_in_round = \
            cls._calculate_no_of_matches_in_round(
                no_participants_in_round=no_participants_in_round)
        return no_of_matches_in_round

    @classmethod
    def _calculate_no_participants_in_round(cls, no_of_participants, round_no):
        return no_of_participants / 2 ** round_no

    @classmethod
    def _calculate_no_of_matches_in_round(cls, no_participants_in_round):
        return no_participants_in_round / 2

    @classmethod
    def add_users_to_match(cls, tournament_id):
        from .tournament_user import TournamentUser
        from .match import Match

        user_ids = TournamentUser.get_tournament_user_ids(
            tournament_id=tournament_id)
        match_ids = cls.get_tournament_round_match_ids(
            tournament_id=tournament_id, round_no=1)

        match_id_wise_user_ids = \
            cls.match_making(match_ids=match_ids, user_ids=user_ids)

        Match.create_user_match(match_id_wise_user_ids=match_id_wise_user_ids,
                                tournament_id=tournament_id)

    @classmethod
    def get_tournament_round_match_ids(cls, tournament_id, round_no):
        match_ids = list(cls.objects.filter(
            tournament_id=tournament_id, round_no=round_no).
                         values_list('id', flat=True))
        return match_ids

    @classmethod
    def match_making(cls, match_ids, user_ids):
        match_id_wise_user_ids = {}
        for index, match_id in enumerate(match_ids):
            selected_user_ids = user_ids[index*2: index*2+2]
            match_id_wise_user_ids[match_id] = selected_user_ids
        return match_id_wise_user_ids

    @classmethod
    def _calculate_match_winner(cls, user_matches):
        user1_match = user_matches[0]
        user2_match = user_matches[1]

        user_id1 = user1_match.user_id
        user_id2 = user2_match.user_id
        user_match1_score = user1_match.score
        user_match2_score = user2_match.score

        if user_match1_score > user_match2_score:
            winner_id = user_id1
        elif user_match1_score == user_match2_score:
            winner_id = cls._calculate_match_winner_for_tie_match(user_matches)
        else:
            winner_id = user_id2
        return winner_id

    @classmethod
    def _calculate_match_winner_for_tie_match(cls, user_matches):
        user1_match = user_matches[0]
        user2_match = user_matches[1]

        user_id1 = user1_match.user_id
        user_id2 = user2_match.user_id

        if user1_match.score_submission_datetime < \
                user2_match.score_submission_datetime:
            winner_id = user_id1
        else:
            winner_id = user_id2

        return winner_id

    @classmethod
    def _pick_match_from_next_round(cls, tournament_id, curr_round_no):
        next_round_no = cls._get_next_round(curr_round_no=curr_round_no)
        match_ids = cls.get_tournament_round_match_ids(
            tournament_id=tournament_id, round_no=next_round_no)

        import random
        match_id = random.choice(match_ids)
        return match_id

    @classmethod
    def _get_next_round(cls, curr_round_no):
        return curr_round_no + 1

    @classmethod
    def _validate_match_winner(cls, user_matches):
        from .match import Match
        for user_match in user_matches:
            if Match.is_user_match_not_completed(user_match):
                raise Exception("Given match is not completed")
