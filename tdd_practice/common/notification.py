class NotificationTypeDetails(object):
    INVITATION_FROM_CLUB = {
        'notification_type': 'INVITATION_FROM_CLUB',
        'title': 'Received Invitation from Club',
        'message': 'Received invitation to join in the club'}

    CAPTAIN_ACCEPT_JOIN_CLUB = {
        'notification_type': 'CAPTAIN_ACCEPT_JOIN_CLUB',
        'title': 'Join club request accepted',
        'message': 'Captain accepts request to join the club'}

    CAPTAIN_REJECT_JOIN_CLUB = {
        'notification_type': 'CAPTAIN_REJECT_JOIN_CLUB',
        'title': 'Join club request rejected',
        'message': 'Captain rejects request to join the club '}

    USER_ACCEPT_INVITATION_FROM_CLUB = {
        'notification_type': 'USER_ACCEPT_INVITATION_FROM_CLUB',
        'title': 'Join club request accepted',
        'message': 'User accepts to join the club'}

    USER_REJECT_INVITATION_FROM_CLUB = {
        'notification_type': 'USER_REJECT_INVITATION_FROM_CLUB',
        'title': 'Join club request rejected',
        'message': 'Captain rejects  request to join the club '}

    NEW_CHALLENGE_RELEASED = {
        'notification_type': 'NEW_CHALLENGE_RELEASED',
        'title': 'New challenge released',
        'message': 'New challenge released'}

    UPGRADE_USER_GAME_OBJECT = {
        'notification_type': 'GAME_OBJECT_READY_TO_UPGRADE',
        'title': 'Game Object ready to upgrade',
        'message': 'Game Object ready to upgrade'}

    INVITATION_TO_JOIN_TOURNAMENT = {
        'notification_type': 'INVITATION_TO_JOIN_TOURNAMENT',
        'title': '{invited_user_name} invited you to play {game_name} game!',
        'message': 'Join {t_name} and show your skill'
    }

    TOURNAMENT_INVITE_ACCEPTANCE_REWARD = {
        'notification_type': 'TOURNAMENT_INVITE_ACCEPTANCE_REWARD',
        'title': 'You have bagged {resource_count} {resource_name}',
        'message': '{accepted_user_name} said an YES your invitation for'
                   ' {t_name}'}

    NEW_TOURNAMENT_CREATED = {
        'notification_type': 'NEW_TOURNAMENT_CREATED',
        'title': '{t_name} has begun!',
        'message': 'Play {game_name} game and win exciting rewards!'
    }

    TOURNAMENT_COMPLETED = {
        'notification_type': 'TOURNAMENT_COMPLETED',
        'title': '{t_name} has ended!',
        'message': 'Rush to the scoreboard!'
    }

    LEADERBOARD_ROUND_COMPLETED = {
        'notification_type': 'LEADERBOARD_ROUND_COMPLETED',
        'title': '{t_name} leaderboard round has ended!',
        'message': '',
        'message_for_round_winners': 'Congrats! You are through to the next round!',
        'message_for_round_losers': 'Check the rewards you won!'
    }

    CHALLENGE_FROM_FRIEND = {
        'notification_type': 'CHALLENGE_FROM_FRIEND',
        'title': '{friend_name} is looking for a match!',
        'message': 'Compete in {game_name} game and find out who\'s the best'
    }

    FRIEND_CHALLENGE_ACCEPTED = {
        'notification_type': 'FRIEND_CHALLENGE_ACCEPTED',
        'title': '{friend_name} has accepted your challenge!',
        'message': 'Compete in {game_name} game and show who\'s the best'
    }

    COLLECT_DAILY_REWARDS = {
        'notification_type': 'COLLECT_DAILY_REWARDS',
        'title': 'Your daily rewards are here!',
        'message': 'Collect rewards and compete in tournaments!'
    }

    REMIND_DAILY_REWARDS = {
        'notification_type': 'REMIND_DAILY_REWARDS',
        'title': 'Oops! you forgot to collect your daily rewards!',
        'message': 'Collect your rewards and maintain the streak!'
    }

    # ToDo: Add gender specific messages
    REMIND_TOBE_PLAYED_USER_AFTER_OPPONENT_PLAY = {
        'notification_type': 'REMIND_MATCH_PLAY',
        'title': 'It\'s your turn now! Get in the game!',
        'message': '{opponent_name} has just played, Gear up and take on!'
    }

    MATCH_COMPLETED_ALERT_TO_FIRST_PLAYED_USER = {
        'notification_type': 'MATCH_COMPLETED',
        'title': 'Your match against {opponent_name} is finished!',
        'message': 'Find out the winner!'
    }

    # ToDo: Add schedulers accordingly
    REMIND_BEFORE_ROUND_COMPLETION = {
        'notification_type': 'REMIND_ROUND_COMPLETION',
        'title': 'Hurry up! {round_name} will end soon!',
        'message': 'Play now and get a step closer to winning exciting rewards!'
    }


# ToDo: Change this hardcoded values to be dynamically configurable
ENABLED_NOTIFICATIONS = [
    NotificationTypeDetails.NEW_TOURNAMENT_CREATED['notification_type'],
    NotificationTypeDetails.INVITATION_TO_JOIN_TOURNAMENT['notification_type'],
    NotificationTypeDetails.TOURNAMENT_INVITE_ACCEPTANCE_REWARD[
        'notification_type'],
    NotificationTypeDetails.CHALLENGE_FROM_FRIEND['notification_type'],
    NotificationTypeDetails.FRIEND_CHALLENGE_ACCEPTED['notification_type'],
    NotificationTypeDetails.COLLECT_DAILY_REWARDS['notification_type'],
    NotificationTypeDetails.REMIND_DAILY_REWARDS['notification_type'],
    NotificationTypeDetails.LEADERBOARD_ROUND_COMPLETED['notification_type'],
    NotificationTypeDetails.REMIND_TOBE_PLAYED_USER_AFTER_OPPONENT_PLAY[
        'notification_type'],
    NotificationTypeDetails.MATCH_COMPLETED_ALERT_TO_FIRST_PLAYED_USER[
        'notification_type'],
    NotificationTypeDetails.REMIND_BEFORE_ROUND_COMPLETION['notification_type']
]


class Notification(object):
    def __init__(self):
        self.notification_type = "NOTIFICATION"

    @staticmethod
    def send_notification(*args, **kwargs):
        from ib_gamification_backend.service_adapters.get_service_adapter_connection import \
            get_service_adapter_connection

        user_id = kwargs['user_id']
        notification_type = kwargs['notification_type']

        if notification_type in ENABLED_NOTIFICATIONS:
            conn = get_service_adapter_connection()
            user = conn.gas_profile.get_user_objects_from_user_id(
                user_ids=[user_id])[0]

            method_name = 'notification_for_' + notification_type.lower()
            name, title, message, extra_data, user_ids = getattr(Notification, method_name)(*args, **kwargs)
            import json
            extra_data = json.dumps(extra_data)

            conn = get_service_adapter_connection(user=None, access_token=None)
            try:
                conn.ib_notifications.notifications_service.send_notifications(
                    name=name, title=title, source="AR_VR", message=message, notification_type=notification_type,
                    cm_type='FCM', user_ids=user_ids, extra_data=extra_data)
            except Exception as e:
                pass
            return
        return

    @staticmethod
    def notification_for_invitation_from_club(*args, **kwargs):

        name = 'CLUB'
        title = NotificationTypeDetails.INVITATION_FROM_CLUB['title']
        message = NotificationTypeDetails.INVITATION_FROM_CLUB['message']
        from ib_club.models import Club
        club_details = Club.get_club_details(kwargs['club_id'])
        extra_data = club_details
        user_ids = kwargs['user_ids']
        return name, title, message, extra_data, user_ids

    @staticmethod
    def notification_for_captain_accept_join_club(*args, **kwargs):
        name = 'CLUB'
        title = NotificationTypeDetails.CAPTAIN_ACCEPT_JOIN_CLUB['title']
        message = NotificationTypeDetails.CAPTAIN_ACCEPT_JOIN_CLUB['message']
        from ib_club.models import Club
        club_details = Club.get_club_details(kwargs['club_id'])
        extra_data = club_details
        user_ids = kwargs['user_ids']
        return name, title, message, extra_data, user_ids

    @staticmethod
    def notification_for_captain_reject_join_club(*args, **kwargs):
        name = 'CLUB'
        title = NotificationTypeDetails.CAPTAIN_REJECT_JOIN_CLUB['title']
        message = NotificationTypeDetails.CAPTAIN_REJECT_JOIN_CLUB['message']
        from ib_club.models import Club
        club_details = Club.get_club_details(kwargs['club_id'])
        extra_data = club_details
        user_ids = kwargs['user_ids']
        return name, title, message, extra_data, user_ids

    @staticmethod
    def notification_for_user_accept_invitation_from_club(*args, **kwargs):
        name = 'CLUB'
        title = NotificationTypeDetails.USER_ACCEPT_INVITATION_FROM_CLUB['title']
        message = NotificationTypeDetails.USER_ACCEPT_INVITATION_FROM_CLUB['message']
        from ib_club.models import Club
        club_details = Club.get_club_details(kwargs['club_id'])
        extra_data = club_details
        user_ids = kwargs['user_ids']
        return name, title, message, extra_data, user_ids

    @staticmethod
    def notification_for_user_reject_invitation_from_club(*args, **kwargs):
        name = 'CLUB'
        title = NotificationTypeDetails.USER_REJECT_INVITATION_FROM_CLUB['title']
        message = NotificationTypeDetails.USER_REJECT_INVITATION_FROM_CLUB['message']
        from ib_club.models import Club
        club_details = Club.get_club_details(kwargs['club_id'])
        extra_data = club_details
        user_ids = kwargs['user_ids']
        return name, title, message, extra_data, user_ids

    @staticmethod
    def notification_for_new_challenge_released(*args, **kwargs):
        name = 'CHALLENGE'
        title = NotificationTypeDetails.NEW_CHALLENGE_RELEASED['title']
        message = NotificationTypeDetails.NEW_CHALLENGE_RELEASED['message']
        challenge = kwargs['challenge']
        extra_data = challenge
        user_ids = kwargs['user_ids']
        return name, title, message, extra_data, user_ids

    @staticmethod
    def notification_for_game_object_ready_to_upgrade(*args, **kwargs):
        name = 'USER_GAME_OBJECT'
        title = NotificationTypeDetails.UPGRADE_USER_GAME_OBJECT['title']
        message = NotificationTypeDetails.UPGRADE_USER_GAME_OBJECT['message']
        user_game_object_details = kwargs['user_game_object_details']
        extra_data = user_game_object_details
        user_ids = kwargs['user_ids']
        return name, title, message, extra_data, user_ids

    @staticmethod
    def notification_for_invitation_to_join_tournament(*args, **kwargs):
        name = "INVITATION_TO_JOIN_TOURNAMENT"
        title = NotificationTypeDetails.INVITATION_TO_JOIN_TOURNAMENT['title']
        title = title.format(game_name=kwargs['game_name'],
                             invited_user_name=kwargs['invited_user_name'])

        message = \
            NotificationTypeDetails.INVITATION_TO_JOIN_TOURNAMENT['message']
        message = message.format(t_name=kwargs['tournament_name'])

        tournament_details = kwargs['tournament_details']
        extra_data = tournament_details
        user_ids = kwargs['user_ids']
        return name, title, message, extra_data, user_ids

    @staticmethod
    def notification_for_tournament_invite_acceptance_reward(*args, **kwargs):
        name = "TOURNAMENT_INVITE_ACCEPTANCE_REWARD"
        title = \
            NotificationTypeDetails.TOURNAMENT_INVITE_ACCEPTANCE_REWARD['title']

        # ToDo: Works for gems, update it to use pluralize function
        resource_name = kwargs['resource_name']
        if kwargs['resource_count'] > 1:
            resource_name = resource_name + 's'

        title = title.format(resource_count=kwargs['resource_count'],
                             resource_name=resource_name)

        message = NotificationTypeDetails.TOURNAMENT_INVITE_ACCEPTANCE_REWARD[
            'message']
        message = message.format(accepted_user_name=kwargs['accepted_user_name'],
                                 t_name=kwargs['tournament_name'])

        tournament_details = kwargs['tournament_details']
        extra_data = tournament_details
        user_ids = kwargs['user_ids']
        return name, title, message, extra_data, user_ids

    @staticmethod
    def notification_for_new_tournament_created(*args, **kwargs):
        name = 'NEW_TOURNAMENT_CREATED'
        title = NotificationTypeDetails.NEW_TOURNAMENT_CREATED['title']
        message = NotificationTypeDetails.NEW_TOURNAMENT_CREATED['message']

        tournament_id = kwargs['tournament_id']
        game_id = kwargs['game_id']
        extra_data = {
            'tournament_id': tournament_id,
            'game_id': game_id,
            'game_name_enum': kwargs['game_name_enum']
        }
        user_ids = kwargs['user_ids']

        tournament_name = kwargs['tournament_name']
        game_name = kwargs['game_name']

        title = title.format(t_name=tournament_name)
        message = message.format(game_name=game_name)

        return name, title, message, extra_data, user_ids

    @staticmethod
    def notification_for_tournament_completed(*args, **kwargs):
        name = 'TOURNAMENT_COMPLETED'
        title = NotificationTypeDetails.TOURNAMENT_COMPLETED['title']
        message = NotificationTypeDetails.TOURNAMENT_COMPLETED['message']

        tournament_id = kwargs['tournament_id']
        game_id = kwargs['game_id']
        extra_data = {
            'tournament_id': tournament_id,
            'game_id': game_id,
            'game_name_enum': kwargs['game_name_enum']
        }
        user_ids = kwargs['user_ids']

        tournament_name = kwargs['tournament_name']
        title = title.format(t_name=tournament_name)

        return name, title, message, extra_data, user_ids

    @staticmethod
    def notification_for_leaderboard_round_completed(*args, **kwargs):
        name = 'MULTI_ROUND_LB_TYPE_TOURNAMENT'

        notification_for_winners = kwargs['notification_for_winners']
        tournament_name = kwargs['tournament_name']

        title = NotificationTypeDetails.LEADERBOARD_ROUND_COMPLETED['title']
        title = title.format(t_name=tournament_name)

        if notification_for_winners:
            message = NotificationTypeDetails.LEADERBOARD_ROUND_COMPLETED[
                'message_for_round_winners']
        else:
            message = NotificationTypeDetails.LEADERBOARD_ROUND_COMPLETED[
                'message_for_round_losers']

        tournament_id = kwargs['tournament_id']
        game_id = kwargs['game_id']
        extra_data = {
            'tournament_id': tournament_id,
            'game_id': game_id,
            'game_name_enum': kwargs['game_name_enum']
        }
        user_ids = kwargs['user_ids']

        return name, title, message, extra_data, user_ids

    @staticmethod
    def notification_for_challenge_from_friend(*args, **kwargs):
        name = 'CHALLENGE_FROM_FRIEND'
        title = NotificationTypeDetails.CHALLENGE_FROM_FRIEND['title']
        message = NotificationTypeDetails.CHALLENGE_FROM_FRIEND['message']

        game_id = kwargs['game_id']
        friend_name = kwargs['friend_name']
        game_name = kwargs['game_name']

        extra_data = {
            'game_id': game_id,
            'game_name_enum': kwargs['game_name_enum']
        }
        user_ids = kwargs['user_ids']

        title = title.format(friend_name=friend_name)
        message = message.format(game_name=game_name)

        return name, title, message, extra_data, user_ids

    @staticmethod
    def notification_for_friend_challenge_accepted(*args, **kwargs):
        name = 'FRIEND_CHALLENGE_ACCEPTED'
        title = NotificationTypeDetails.FRIEND_CHALLENGE_ACCEPTED['title']
        message = NotificationTypeDetails.FRIEND_CHALLENGE_ACCEPTED['message']

        game_id = kwargs['game_id']
        friend_name = kwargs['friend_name']
        game_name = kwargs['game_name']

        extra_data = {
            'game_id': game_id,
            'game_name_enum': kwargs['game_name_enum']
        }
        user_ids = kwargs['user_ids']

        title = title.format(friend_name=friend_name)
        message = message.format(game_name=game_name)

        return name, title, message, extra_data, user_ids

    @staticmethod
    def notification_for_collect_daily_rewards(*args, **kwargs):
        name = 'COLLECT_DAILY_REWARDS'
        title = NotificationTypeDetails.COLLECT_DAILY_REWARDS['title']
        message = NotificationTypeDetails.COLLECT_DAILY_REWARDS['message']

        extra_data = {}
        user_ids = kwargs['user_ids']

        return name, title, message, extra_data, user_ids

    @staticmethod
    def notification_for_remind_daily_rewards(*args, **kwargs):
        name = 'REMIND_DAILY_REWARDS'
        title = NotificationTypeDetails.REMIND_DAILY_REWARDS['title']
        message = NotificationTypeDetails.REMIND_DAILY_REWARDS['message']

        extra_data = {}
        user_ids = kwargs['user_ids']

        return name, title, message, extra_data, user_ids

    @staticmethod
    def notification_for_remind_match_play(*args, **kwargs):
        name = 'REMIND_MATCH_PLAY'
        config = \
            NotificationTypeDetails.REMIND_TOBE_PLAYED_USER_AFTER_OPPONENT_PLAY

        title = config['title']
        message = config['message']
        user_ids = kwargs['user_ids']
        extra_data = {
            'game_id': kwargs['game_id'],
            'game_name_enum': kwargs['game_name_enum'],
            'match_type': kwargs['match_type'],
            'tournament_id': kwargs.get('tournament_id', -1)
        }

        message = message.format(opponent_name=kwargs['opponent_name'])

        return name, title, message, extra_data, user_ids

    @staticmethod
    def notification_for_match_completed(*args, **kwargs):
        name = 'MATCH_COMPLETED'
        config = \
            NotificationTypeDetails.MATCH_COMPLETED_ALERT_TO_FIRST_PLAYED_USER
        title = config['title']
        message = config['message']
        user_ids = kwargs['user_ids']
        extra_data = {
            'game_id': kwargs['game_id'],
            'game_name_enum': kwargs['game_name_enum'],
            'match_type': kwargs['match_type'],
            'tournament_id': kwargs.get('tournament_id', -1)
        }

        title = title.format(opponent_name=kwargs['opponent_name'])

        return name, title, message, extra_data, user_ids

    @staticmethod
    def notification_for_remind_round_completion(*args, **kwargs):
        name = "REMIND_ROUND_COMPLETION"
        config = NotificationTypeDetails.REMIND_BEFORE_ROUND_COMPLETION

        title = config['title']
        message = config['message']
        user_ids = kwargs['user_ids']
        round_name = kwargs['round_name']
        extra_data = {
            'tournament_id': kwargs['tournament_id'],
            'game_id': kwargs['game_id'],
            'game_name_enum': kwargs['game_name_enum']
        }

        title = title.format(round_name=round_name)
        return name, title, message, extra_data, user_ids
