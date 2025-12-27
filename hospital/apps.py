import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)

class HospitalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hospital'

    def ready(self):
        # Load signal handlers.
        import hospital.signals
        logger.info("HospitalConfig.ready() executed; hospital.signals imported")
