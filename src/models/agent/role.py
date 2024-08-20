from dataclasses import dataclass
from enum import Enum


class RoleUUID(Enum):
    CONTROLLER = "4ee40330-ecdd-4f2f-98a8-eb1243428373"
    DUELIST = "dbe8757e-9e92-4ed4-b39f-9dfc589691d4"
    INITIATOR = "1b47567f-8f7b-444b-aae3-b0c634622d10"
    SENTINEL = "5fc02f99-4091-4486-a531-98459a3e95e9"


@dataclass
class Role:
    uuid: RoleUUID
    name: str

    @classmethod
    def from_dict(cls, role_data: dict[str, str]) -> "Role":
        return cls(uuid=RoleUUID(role_data["uuid"]), name=role_data["displayName"])

    def to_dict(self) -> dict[str, str]:
        return {"uuid": str(self.uuid.value), "displayName": self.name}
