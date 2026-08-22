import logging

from celery import current_app, shared_task
from celery.schedules import crontab

from care_encounter_auto_close_be.auto_close.handler import run_auto_close
from care_encounter_auto_close_be.settings import plugin_settings

logger = logging.getLogger(__name__)


@shared_task
def auto_close_encounters():
    """Close eligible open encounters based on the configured rules."""
    if not plugin_settings.CARE_ENCOUNTER_AUTO_CLOSE_ENABLED:
        logger.info("Auto close encounters task is disabled.")
        return {}
    logger.info("Starting auto close encounters task.")
    run_auto_close()

current_app.conf.beat_schedule["auto_close_encounters"] = {
    "task": "care_encounter_auto_close_be.tasks.auto_close_encounters",
    "schedule": crontab(minute="0", hour="0"),
}
