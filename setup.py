try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
        'description': 'Displays information about fixtures from the premiership.',
        'author': 'Nick Hale',
        'url': 'url',
        'author_email': 'nicholas.hale@gmail.com',
        'version': '0.1',
        'packages': ['cromwell'],
        'name': 'cromwell'
}

setup(**config)
