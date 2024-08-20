import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from src.models.game_map.callout import Callout
from src.models.serializable import Serializable


class MapUUID(Enum):
    ABYSS = "224b0a95-48b9-f703-1bd8-67aca101a61f"
    ASCENT = "7eaecc1b-4337-bbf6-6ab9-04b8f06b3319"
    BIND = "2c9d57ec-4431-9c5e-2939-8f9ef6dd5cba"
    BREEZE = "2fb9a4fd-47b8-4e7d-a969-74b4046ebd53"
    FRACTURE = "b529448b-4d60-346e-e89e-00a4c527a405"
    HAVEN = "2bee0dc9-4ffe-519b-1cbd-7fbe763a6047"
    ICEBOX = "e2ad5c54-4114-a870-9641-8ea21279579a"
    LOTUS = "2fe4ed3a-450a-948b-6d6b-e89a78e680a9"
    PEARL = "fd267378-4d1d-484f-ff52-77821ed10dc2"
    SPLIT = "d960549e-485c-e861-8d71-aa9d1aed12a2"
    SUNSET = "92584fbe-486a-b1b2-9faa-39b0f486b498"


@dataclass
class GameMap(Serializable):
    X_MULTIPLIER = 1.0
    Y_MULTIPLIER = 1.0
    X_SCALAR_TO_ADD = 0.0
    Y_SCALAR_TO_ADD = 0.0

    uuid: MapUUID
    name: str
    display_icon: str
    list_view_icon: str | None = None
    splash: str | None = None
    x_multiplier: float = X_MULTIPLIER
    y_multiplier: float = Y_MULTIPLIER
    x_scalar_to_add: float = X_SCALAR_TO_ADD
    y_scalar_to_add: float = Y_SCALAR_TO_ADD
    callouts: list[Callout] = field(default_factory=list)

    @classmethod
    def from_dict(cls, map_metadata: dict[str, Any]) -> "GameMap":
        callouts_data = map_metadata.get("callouts", []) or []
        return cls(
            uuid=MapUUID(map_metadata["uuid"]),
            name=map_metadata["displayName"],
            display_icon=map_metadata["displayIcon"],
            list_view_icon=map_metadata.get("listViewIcon"),
            splash=map_metadata.get("splash"),
            x_multiplier=map_metadata.get("xMultiplier", cls.X_MULTIPLIER),
            y_multiplier=map_metadata.get("yMultiplier", cls.Y_MULTIPLIER),
            x_scalar_to_add=map_metadata.get("xScalarToAdd", cls.X_SCALAR_TO_ADD),
            y_scalar_to_add=map_metadata.get("yScalarToAdd", cls.Y_SCALAR_TO_ADD),
            callouts=[Callout.from_dict(callout) for callout in callouts_data],
        )

    @classmethod
    def from_json(cls, path: str) -> "GameMap":
        with open(path) as file:
            data = json.load(file)
        return cls.from_dict(data)

    def to_dict(self) -> dict[str, Any]:
        return {
            "uuid": self.uuid.value,
            "displayName": self.name,
            "displayIcon": self.display_icon,
            "listViewIcon": self.list_view_icon,
            "splash": self.splash,
            "xMultiplier": self.x_multiplier,
            "yMultiplier": self.y_multiplier,
            "xScalarToAdd": self.x_scalar_to_add,
            "yScalarToAdd": self.y_scalar_to_add,
            "callouts": [callout.to_dict() for callout in self.callouts],
        }
