#!/usr/bin/env python
import os

from django.conf import settings
from django.core.management import call_command

THIS_DIR = os.path.dirname(__file__)


def main():
    """Dynamically configure the Django settings with the
    minimum necessary to get Django running tests"""
    settings.configure(
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django_nose',
            'registration',
        ),
        TEST_RUNNER = 'django_nose.NoseTestSuiteRunner',
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                               'NAME': '/tmp/registration.db',
                               'USER': '',
                               'PASSWORD': '',
                               'HOST': '',
                               'PORT': ''}},
        NOSE_ARGS=['--with-xunit', '-s'],
        ROOT_URLCONF=None,
        TEMPLATE_DIRS = (
            os.path.join(THIS_DIR, 'templates'),
        ),
        SITE_ID=0,
    )

    call_command('test', 'registration')

if __name__ == '__main__':
    main()
