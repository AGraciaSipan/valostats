import json
from abc import ABC, abstractmethod


class Serializable(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        pass

    def to_json(self, path: str) -> None:
        with open(path, "w") as file:
            json.dump(self.to_dict(), file, indent=2)
