import datetime
import os
from dotenv import load_dotenv


load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


def as_bool(value):
    if value:
        return value.lower() in ['true', 'yes', 'on', '1']
    return False


class Config:
    # database options
    ALCHEMICAL_DATABASE_URL = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    ALCHEMICAL_ENGINE_OPTIONS = {'echo': as_bool(os.environ.get('SQL_ECHO'))}
    UPLOAD_FOLDER = './api/uploads'
    # security options
    SECRET_KEY = os.environ.get('SECRET_KEY', 'SecretKeyTestingPurposes_12bbcydsv')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'JWTTestingPurposes_4n5guyviub')
    JWT_COOKIE_SECURE = as_bool(os.environ.get('JWT_COOKIE_SECURE'))
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)
    USE_CORS = as_bool(os.environ.get('USE_CORS') or 'false')
    CORS_SUPPORTS_CREDENTIALS = True

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = 'ru-central1'

    APIFAIRY_TITLE = 'VapeHookah API'
    APIFAIRY_VERSION = '1.0'
    APIFAIRY_UI = 'swagger_ui'
