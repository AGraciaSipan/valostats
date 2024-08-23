from dataclasses import dataclass, field
from typing import Any

from src.models.game_map.location import Location


@dataclass
class Callout:
    region_name: str
    super_region_name: str | None = None
    location: Location = field(default_factory=Location)

    @classmethod
    def from_dict(cls, callout_data: dict[str, Any]) -> "Callout":
        return cls(
            region_name=callout_data["regionName"],
            super_region_name=callout_data.get("superRegionName"),
            location=Location(**callout_data.get("location", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "regionName": self.region_name,
            "superRegionName": self.super_region_name,
            "location": self.location.to_dict(),
        }
