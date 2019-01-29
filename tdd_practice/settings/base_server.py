import os


from ib_gamification_backend.settings.base import *
from ib_gamification_backend.settings.base_pg_db import *
from ib_gamification_backend.settings.base_swagger_utils import *
from ib_gamification_backend.settings.base_aws_s3 import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
IB_RESOURCE_DB_TABLE_NAME_SPACE = 'ib-resource-%s-' % os.environ["STAGE"]
IB_TREASURE_DB_TABLE_NAME_SPACE = 'ib-treasure-%s-' % os.environ["STAGE"]
IB_TOURNAMENT_DB_TABLE_NAME_SPACE = 'ib-tournament-%s-' % os.environ["STAGE"]
IB_GAME_OBJECT_DB_TABLE_NAME_SPACE = 'ib-game-object-%s-' % os.environ["STAGE"]
IB_MATCH_DB_TABLE_NAME_SPACE = 'ib-match-%s-' % os.environ["STAGE"]
IB_CHALLENGE_DB_TABLE_NAME_SPACE = 'ib-challenge-%s-' % os.environ["STAGE"]
DYNAMO_DB_REGION = 'ap-south-1'
