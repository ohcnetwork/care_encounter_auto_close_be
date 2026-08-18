
from care.emr.resources.encounter.constants import ClassChoices, StatusChoices

class EncounterAutoClose:
    """
    This class is responsible for automatically closing encounters based on certain rules.
    It checks the status and class of encounters and closes them if they meet the criteria defined in the configuration.
    """

    def __init__(
        self,
        display_name: str,
        encounter_class: ClassChoices,
        time_limit:int = 24 ,
        status: StatusChoices | None = None,
    ):
        self.key = encounter_class.value
        self.status = status
        self.display_name = display_name
        self.encounter_class = encounter_class
        self.time_limit = time_limit



class EncounterAutoCloseRegistry:
    _registry: dict[str, EncounterAutoClose] = {}

    @classmethod
    def register(
        cls,
        encounter_class: ClassChoices,
        time_limit:int = 24,
        status: StatusChoices | None = None,
        display_name: str | None = None,
        )-> None:
        if not isinstance(encounter_class, ClassChoices):
            msg=f"encounter_class must be an instance of ClassChoices, got {encounter_class}"
            raise TypeError(msg)
        key = encounter_class.value
        if key in cls._registry:
            msg=f"EncounterAutoClose with key '{key}' is already registered."
            raise ValueError(msg)
        if status is not None and not isinstance(status, StatusChoices):
            msg=f"status must be an instance of StatusChoices, got {status}"
            raise TypeError(msg)

        config=EncounterAutoClose(
            display_name=display_name,
            status=status,
            encounter_class=encounter_class,
            time_limit=time_limit,
        )
        cls._registry[key]=config

    @classmethod
    def get(cls,key:str)->EncounterAutoClose:
        if key not in cls._registry:
            msg=f"EncounterAutoClose with key '{key}' is not registered."
            raise KeyError(msg)
        return cls._registry[key]

    @classmethod
    def get_all_keys(cls)->list[str]:
        return list(cls._registry.keys())

    @classmethod
    def get_all_configs(cls)->dict[str,EncounterAutoClose]:
        return cls._registry.copy()

    @classmethod
    def clear_registry(cls)->None:
        cls._registry.clear()


