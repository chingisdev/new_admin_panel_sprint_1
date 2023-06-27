import os

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

_ENV = os.environ.get('DJANGO_ENV', 'development')

_base_settings = (
    'components/common.py',
    'components/database.py',

    # Select the right env:
    'environments/{0}.py'.format(_ENV),
)

include(*_base_settings)
