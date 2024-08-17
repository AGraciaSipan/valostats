from dataclasses import dataclass


@dataclass
class Location:
    DEFAULT_X = 0.0
    DEFAULT_Y = 0.0

    x: float = DEFAULT_X
    y: float = DEFAULT_Y

    @classmethod
    def from_dict(cls, location_data: dict[str, float]) -> "Location":
        return cls(x=location_data.get("x", cls.DEFAULT_X), y=location_data.get("y", cls.DEFAULT_Y))

    def to_dict(self) -> dict[str, float]:
        return {"x": self.x, "y": self.y}
