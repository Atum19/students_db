import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, '..', 'db.sqlite3'),
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'USER': 'django',
        'USER': 'postgres',
        'PASSWORD': 'postgres0',
        # 'PASSWORD': 'django0',
        # 'NAME': 'students_db',
        'NAME': 'django_studs_db',
        'TEST': {
            'CHARSET': 'utf8',
            # 'CHARSET': 'latin1',
            # 'COLLATION': 'utf8_general_ci',
            'use_unicode': True,
        },
        'HOST': '',
        'PORT': '',
    }
}
