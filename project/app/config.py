"""
Initializes application settings based on environment variables.

project/app/config.py
"""

from logging import getLogger
from os import environ
from functools import lru_cache

from pydantic import BaseSettings, AnyUrl


log = getLogger('uvicorn')


class Settings(BaseSettings):
  environment: str = environ.get('ENVIRONMENT', 'dev')
  testing: bool = environ.get('TESTING') or 0
  database_url: AnyUrl = environ.get('DATABASE_URL')


@lru_cache()
def get_settings() -> BaseSettings:
  log.info('Loading config settings from the environment...')
  return Settings()
