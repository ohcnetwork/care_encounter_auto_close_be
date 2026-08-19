
from care_encounter_auto_close_be.auto_close.registry import EncounterAutoCloseRegistry
from care.emr.resources.encounter.constants import StatusChoices, ClassChoices

EncounterAutoCloseRegistry.register(
    display_name="Ambulatory",
    encounter_class=ClassChoices.amb,
    time_limit=0,
)

EncounterAutoCloseRegistry.register(
    display_name="Inpatient",
    encounter_class=ClassChoices.imp,
    status=StatusChoices.discharged,
    time_limit=24,
)
EncounterAutoCloseRegistry.register(
    display_name="Observation",
    encounter_class=ClassChoices.obsenc,
    status=StatusChoices.discharged,
    time_limit=24,
)



