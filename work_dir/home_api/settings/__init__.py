import os

from split_settings.tools import include

include('base.py')

if 'production' == os.environ.get('ENV_SETTINGS'):
    include('production.py')
elif 'test' == os.environ.get('ENV_SETTINGS'):
    include('test.py')