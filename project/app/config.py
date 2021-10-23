"""
Initializes application settings based on environment variables.

project/app/config.py
"""

from logging import getLogger
from os import getenv
from functools import lru_cache

from pydantic import BaseSettings


log = getLogger('uvicorn')


class Settings(BaseSettings):
  environment: str = getenv('ENVIRONMENT', 'dev')
  testing: bool = getenv('TESTING') or 0


@lru_cache()
def get_settings() -> BaseSettings:
  log.info('Loading config settings from the environment...')
  return Settings()
