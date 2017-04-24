import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, '..', 'db.sqlite3'),
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'NAME': 'students_db',
        'NAME': 'django_studs_db',
        'USER': 'django',
        'PASSWORD': 'django0',
        'HOST': '',
        'PORT': '',
    }
}
