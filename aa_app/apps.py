from django.apps import AppConfig
from aa_app import models

class aa_appConfig(AppConfig):
    name = "aa_app"
    
    def ready(self):
        pass
            