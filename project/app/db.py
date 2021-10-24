"""
Tortois config for Aerich database migration

project/app/db.py
"""
from os import environ


TORTOISE_ORM = {
  'connections': {'default': environ.get('DATABASE_URL')},
  'apps': {
    'models': {
      'models': ['app.models.tortoise', 'aerich.models'],
      'default_connection': 'default',
    }
  }
}
