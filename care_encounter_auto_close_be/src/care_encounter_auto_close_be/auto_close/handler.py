import logging
from datetime import datetime, timedelta

from django.db import transaction
from django.utils.dateparse import parse_datetime

from care.emr.api.viewsets.device import disassociate_device_from_encounter
from care.emr.api.viewsets.location import close_related_location_from_encounter
from care.emr.models import Encounter
from care.emr.resources.encounter.constants import COMPLETED_CHOICES, StatusChoices
from care.utils.time_util import care_now

from care_encounter_auto_close_be.auto_close.registry import (
    EncounterAutoCloseRegistry,
)

logger = logging.getLogger(__name__)


def _reference_time(encounter: Encounter) -> datetime | None:
    history = (encounter.status_history or {}).get("history") or []
    if history and history[-1].get("moved_at") and encounter.status == history[-1].get("status"):
        print(parse_datetime(history[-1]["moved_at"]))
        return parse_datetime(history[-1]["moved_at"])
    return encounter.modified_date


def _close_encounter(encounter: Encounter) -> None:
    with transaction.atomic():
        encounter.status = StatusChoices.completed.value
        history = encounter.status_history or {"history": []}
        history.setdefault("history", []).append(
            {"status": StatusChoices.completed.value, "moved_at": str(care_now())}
        )
        encounter.status_history = history
        encounter.save(update_fields=["status", "status_history", "modified_date"])
        disassociate_device_from_encounter(encounter)
        close_related_location_from_encounter(encounter)


def run_auto_close() -> dict[str, int]:
    """Close open encounters that match a registered rule and exceeded its time limit.

    Returns a per-rule count of the encounters closed.
    """
    configs = EncounterAutoCloseRegistry.get_all_configs()
    if not configs:
        return {}
    open_encounters = Encounter.objects.exclude(status__in=COMPLETED_CHOICES).filter(
        encounter_class__in=configs.keys()
    )
    now = care_now()
    summary: dict[str, int] = {}
    for encounter in open_encounters.iterator():
        rule = configs[encounter.encounter_class]
        if rule.status is not None and encounter.status != rule.status.value:
            continue
        reference = _reference_time(encounter)
        if reference is None or now - reference < timedelta(hours=rule.time_limit):
            continue
        _close_encounter(encounter)
        label = rule.encounter_class.value
        summary[label] = summary.get(label, 0) + 1

    return summary
