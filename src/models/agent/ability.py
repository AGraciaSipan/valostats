from dataclasses import dataclass
from enum import Enum


class AbilitySlot(Enum):
    Q_SLOT = "Ability1"
    E_SLOT = "Ability2"
    C_SLOT = "Grenade"
    X_SLOT = "Ultimate"
    _SLOT = "Passive"


@dataclass
class Ability:
    slot: AbilitySlot
    name: str

    @classmethod
    def from_dict(cls, ability_data: dict[str, str]) -> "Ability":
        return cls(slot=AbilitySlot(ability_data["slot"]), name=ability_data["displayName"])

    def to_dict(self) -> dict[str, str]:
        return {"slot": self.slot.value, "displayName": self.name}
