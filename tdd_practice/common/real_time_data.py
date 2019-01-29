from django.conf import settings


class RealTimeData(object):
    USER_REWARDS = {
        'badge_name': 'USER_REWARDS',
        'event_type': 'REAL_TIME'
    }
    USER_GO_UPGRADE_DETAILS = {
        'badge_name': 'USER_GO_UPGRADE_DETAILS',
        "event_type": "BADGE"
    }
    LEVEL_UNLOCKED = {
        'badge_name': 'LEVEL_UNLOCKED',
        'event_type': 'REAL_TIME'
    }
    TOURNAMENT_UPDATE = {
        'badge_name': 'TOURNAMENT_UPDATE',
        'event_type': 'REAL_TIME'
    }
    TOURNAMENT_INVITE = {
        'badge_name': 'TOURNAMENT_INVITE',
        'event_type': 'REAL_TIME'
    }
    OPEN_TREASURE = {
        'badge_name': 'OPEN_TREASURE',
        'event_type': 'REAL_TIME'
    }
    UNLOCK_TREASURE = {
        'badge_name': 'UNLOCK_TREASURE',
        'event_type': 'REAL_TIME'
    }
    SLOT_TREASURE_UNLOCKED = {
        'badge_name': 'SLOT_TREASURE_UNLOCKED',
        'event_type': 'REAL_TIME'
    }

    def __init__(self):
        self.payload_list = []
        pass

    def publish(self,  *args, **kwargs):
        content_type = kwargs.get('content_type')
        if not content_type:
            content_type = kwargs.get('badge_name')

        add_to_queue = kwargs.get('add_to_queue', False)

        user_ids = kwargs.get('user_ids', [])
        if not user_ids:
            user_id = kwargs.get('user_id')
            if not user_id:
                return
            user_ids = [user_id]
        user_ids = [str(x) for x in user_ids]

        method_name = "publish_real_time_data_for_"+content_type.lower()
        event_type, content = getattr(
            RealTimeData, method_name)(*args, **kwargs)

        import json
        payload = {
                "user_ids": user_ids,
                "payload": json.dumps({
                    "event_type": event_type,
                    "content": content
                })
            }

        if not settings.ENABLE_REAL_TIME:
            return

        if add_to_queue:
            self.payload_list.append(payload)
        else:
            try:
                from zappa_async_tasks import publish_payload_to_users
                publish_payload_to_users([payload])
            except Exception as e:
                print 'publish_payload_to_user: Exception --->', e
            return

    def flush(self):
        if self.payload_list:
            try:
                from zappa_async_tasks import publish_payload_to_users
                publish_payload_to_users(self.payload_list)
                self.payload_list = []
            except Exception as e:
                print 'publish_payload_to_user: Exception --->', e
            return

    @staticmethod
    def publish_real_time_data_for_level_unlocked(*args, **kwargs):
        event_type = RealTimeData.LEVEL_UNLOCKED['event_type']
        content = {
            'name': RealTimeData.LEVEL_UNLOCKED['badge_name'],
            'data': {
                'level_id': kwargs['level_id'],
                'level_no': kwargs['level_no'],
                'level_type': kwargs['level_type'],
                'name': kwargs['name'],
                'display_name': kwargs['display_name']
            }
        }
        return event_type, content

    @staticmethod
    def publish_real_time_data_for_user_rewards(*args, **kwargs):
        event_type = RealTimeData.USER_REWARDS['event_type']
        content = {
            'name': RealTimeData.USER_REWARDS['badge_name'],
            'data': {
                "user_rewards": kwargs['data']
            }
        }
        return event_type, content

    @staticmethod
    def publish_real_time_data_for_user_go_upgrade_details(*args, **kwargs):
        event_type = RealTimeData.USER_GO_UPGRADE_DETAILS['event_type']
        user_go_name = kwargs['user_go_name']
        upgrade_count = kwargs['upgrade_count']
        content = {
            "badges": [{
                "name": user_go_name,
                "value": upgrade_count
            }]
        }
        return event_type, content

    @staticmethod
    def publish_real_time_data_for_tournament_update(*args, **kwargs):
        event_type = RealTimeData.TOURNAMENT_UPDATE['event_type']
        data = kwargs.get('data', None)
        content = {
            'name': RealTimeData.TOURNAMENT_UPDATE['badge_name'],
            'data': data
        }
        return event_type, content

    @staticmethod
    def publish_real_time_data_for_tournament_invite(*args, **kwargs):
        event_type = RealTimeData.TOURNAMENT_INVITE['event_type']
        data = kwargs.get('data', None)
        content = {
            'name': RealTimeData.TOURNAMENT_INVITE['badge_name'],
            'data': data
        }
        return event_type, content

    @staticmethod
    def publish_real_time_data_for_open_treasure(*args, **kwargs):
        event_type = RealTimeData.OPEN_TREASURE['event_type']
        data = kwargs.get('data', None)
        content = {
            'name': RealTimeData.OPEN_TREASURE['badge_name'],
            'data': data
        }
        return event_type, content

    @staticmethod
    def publish_real_time_data_for_unlock_treasure(*args, **kwargs):
        event_type = RealTimeData.UNLOCK_TREASURE['event_type']
        data = kwargs.get('data', None)
        content = {
            'name': RealTimeData.UNLOCK_TREASURE['badge_name'],
            'data': data
        }
        return event_type, content

    @staticmethod
    def publish_real_time_data_for_slot_treasure_unlocked(*args, **kwargs):
        event_type = RealTimeData.SLOT_TREASURE_UNLOCKED['event_type']
        data = kwargs.get('data', None)
        content = {
            'name': RealTimeData.SLOT_TREASURE_UNLOCKED['badge_name'],
            'data': data
        }
        return event_type, content
