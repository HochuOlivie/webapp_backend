import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

INSTALLED_APPS = (
    'db',
)

SECRET_KEY = 'ogew78f887fho273f1o3f(&*^&%Y(&*^G&fr46'
