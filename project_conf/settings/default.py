import os
from os.path import dirname, abspath

BASE_DIR = dirname(dirname(dirname(abspath(__file__))))

SECRET_KEY = '!3h-1*9xzhs^#s9w52f5crh-dg9-%n43hw*a6#+1j@@chd^ejt'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'sqlite3.db'),
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'

ALLOW_REG = True
