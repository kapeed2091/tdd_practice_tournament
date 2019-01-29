from ib_gamification_backend.settings.local import *


class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

DYNAMO_TEST_PORTS = []
DYNAMO_TEST_PORT = "8000"

PRINT_LOCK_LOGS = False
