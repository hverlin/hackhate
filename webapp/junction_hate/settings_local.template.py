DEBUG = False

# modifier la clef secrète
SECRET_KEY = '#xinfvd=+#^del$@he^ms46$$2mrf!)+4i6icn62fx&t+4p2^a'

TWITTER_consumer_key = ''
TWITTER_consumer_secret = ''
TWITTER_access_token = ''
TWITTER_access_token_secret = ''
FACEBOOK_app_id = ""
FACEBOOK_app_secret = ""


# SqlLite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

ALLOWED_HOSTS = ["*"]

# configuration Email smtp
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'email@gmail.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_PORT = 587
