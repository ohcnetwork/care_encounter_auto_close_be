from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

PLUGIN_NAME = "care_encounter_auto_close_be"


class CareEncounterAutoClosePluginConfig(AppConfig):
    name = PLUGIN_NAME
    verbose_name = _("Care encounter auto close plugin")

    def ready(self):
        import care_encounter_auto_close_be.auto_close.encounter  # noqa F401
        import care_encounter_auto_close_be.tasks  # noqa F401
