import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'logs')


class Config(object):
    # Use it to encrypt or decrypt data
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'o7-6^!l1oc48=rmb=@4b8lvz67qtqbzd&=svzfh@al+o(o-+za'


    # Django security setting, if your disable debug model, you should setting that
    ALLOWED_HOSTS = ['*']

    # Development env open this, when error occur display the full process track, Production disable it
    DEBUG = True

    # DEBUG, INFO, WARNING, ERROR, CRITICAL can set. See https://docs.djangoproject.com/en/1.10/topics/logging/
    LOG_LEVEL = 'INFO'

    SESSION_COOKIE_AGE = 3600 * 24


class ProductionConfig(Config):
    DEBUG = False

    DB_HOST_1 = '192.168.12.239'
    DB_PORT_1 = 3306
    DB_USER_1 = 'root'
    DB_PASSWORD_1 = 'redhat'
    DB_NAME_1 = 'btrecharge'

    SIGIN_KEY = 'WA61NJlXwlwp3tkGd8Dj'

    REMOTE_IP_LIST = ['172.31.192.222','127.0.0.1','192.168.2.41']



config = {
    'production': ProductionConfig,
}

env = 'production'


