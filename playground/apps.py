# The name for this file is misleading. It should be called
# config.py. Anyways this is the config file for this app

from django.apps import AppConfig


class PlaygroundConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'playground'
