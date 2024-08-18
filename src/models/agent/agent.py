import json
from dataclasses import dataclass
from enum import Enum
from typing import Any
from uuid import UUID

from src.models.agent.ability import Ability
from src.models.agent.role import Role
from src.models.serializable import Serializable


@dataclass
class Agent(Serializable):
    uuid: UUID
    name: str
    display_icon: str
    display_icon_small: str
    role: Role
    abilities: list[Ability]

    @classmethod
    def from_dict(cls, agent_data: dict[str, Any]) -> "Agent":
        return cls(
            uuid=UUID(agent_data["uuid"]),
            name=agent_data["displayName"].replace("/", ""),
            display_icon=agent_data["displayIcon"],
            display_icon_small=agent_data["displayIconSmall"],
            role=Role.from_dict(agent_data["role"]),
            abilities=[Ability.from_dict(ability) for ability in agent_data["abilities"]],
        )

    @classmethod
    def from_json(cls, path: str) -> "Agent":
        with open(path) as file:
            data = json.load(file)
        return cls.from_dict(data)

    def to_dict(self) -> dict[str, Any]:
        return {
            "uuid": str(self.uuid),
            "displayName": self.name,
            "displayIcon": self.display_icon,
            "displayIconSmall": self.display_icon_small,
            "role": self.role.to_dict(),
            "abilities": [ability.to_dict() for ability in self.abilities],
        }


class AgentUUIDs(Enum):
    ASTRA = UUID("41fb69c1-4189-7b37-f117-bcaf1e96f1bf")
    BREACH = UUID("5f8d3a7f-467b-97f3-062c-13acf203c006")
    BRIMSTONE = UUID("9f0d8ba9-4140-b941-57d3-a7ad57c6b417")
    CHAMBER = UUID("22697a3d-45bf-8dd7-4fec-84a9e28c69d7")
    CLOVE = UUID("1dbf2edd-4729-0984-3115-daa5eed44993")
    CYPHER = UUID("117ed9e3-49f3-6512-3ccf-0cada7e3823b")
    DEADLOCK = UUID("cc8b64c8-4b25-4ff9-6e7f-37b4da43d235")
    FADE = UUID("dade69b4-4f5a-8528-247b-219e5a1facd6")
    GEKKO = UUID("e370fa57-4757-3604-3648-499e1f642d3f")
    HARBOR = UUID("95b78ed7-4637-86d9-7e41-71ba8c293152")
    ISO = UUID("0e38b510-41a8-5780-5e8f-568b2a4f2d6c")
    JETT = UUID("add6443a-41bd-e414-f6ad-e58d267f4e95")
    KAYO = UUID("601dbbe7-43ce-be57-2a40-4abd24953621")
    KILLJOY = UUID("1e58de9c-4950-5125-93e9-a0aee9f98746")
    NEON = UUID("bb2a4828-46eb-8cd1-e765-15848195d751")
    OMEN = UUID("8e253930-4c05-31dd-1b6c-968525494517")
    PHOENIX = UUID("eb93336a-449b-9c1b-0a54-a891f7921d69")
    RAZE = UUID("f94c3b30-42be-e959-889c-5aa313dba261")
    REYNA = UUID("a3bfb853-43b2-7238-a4f1-ad90e9e46bcc")
    SAGE = UUID("569fdd95-4d10-43ab-ca70-79becc718b46")
    SKYE = UUID("6f2a04ca-43e0-be17-7f36-b3908627744d")
    SOVA = UUID("320b2a48-4d9b-a075-30f1-1f93a9b638fa")
    VIPER = UUID("707eab51-4836-f488-046a-cda6bf494859")
    YORU = UUID("7f94d92c-4234-0a36-9646-3a87eb8b5c89")
