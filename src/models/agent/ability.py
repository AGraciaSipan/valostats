from dataclasses import dataclass
from enum import Enum


@dataclass
class Ability:
    slot: str
    name: str

    @classmethod
    def from_dict(cls, ability_data: dict[str, str]) -> "Ability":
        return cls(slot=ability_data["slot"], name=ability_data["displayName"])

    def to_dict(self) -> dict[str, str]:
        return {"slot": self.slot, "displayName": self.name}


class AbilitySlots(Enum):
    Q_SLOT = "Ability1"
    E_SLOT = "Ability2"
    C_SLOT = "Grenade"
    X_SLOT = "Ultimate"
