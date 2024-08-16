from enum import Enum
from typing import Any


class Location:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    @classmethod
    def from_dict(cls, data: dict[str, float]) -> "Location":
        x = data.get("x", 0.0)
        y = data.get("y", 0.0)
        return cls(x=x, y=y)


class Callout:
    def __init__(self, callout_data: dict[str, Any]):
        self.region_name: str = callout_data.get("regionName", "")
        self.super_region_name: str = callout_data.get("superRegionName", "")
        self.location: Location = Location.from_dict(callout_data.get("location", {}))


class Map:
    def __init__(self, map_metadata: dict[str, Any]):
        self.uuid: str = map_metadata.get("uuid", "")
        self.display_name: str = map_metadata.get("displayName", "")
        self.display_icon: str = map_metadata.get("displayIcon", "")
        self.list_view_icon: str = map_metadata.get("listViewIcon", "")
        self.splash: str = map_metadata.get("splash", "")
        self.x_multiplier: float = map_metadata.get("xMultiplier", 1.0)
        self.y_multiplier: float = map_metadata.get("yMultiplier", 1.0)
        self.x_scalar_to_add: float = map_metadata.get("xScalarToAdd", 0.0)
        self.y_scalar_to_add: float = map_metadata.get("yScalarToAdd", 0.0)

        callouts_data = map_metadata.get("callouts", [])
        if callouts_data is None:
            callouts_data = []
        self.callouts: list[Callout] = [Callout(callout) for callout in callouts_data if callouts_data is not None]


class MapUUIDs(Enum):
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
