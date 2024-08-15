from logging import INFO, basicConfig, getLogger
from typing import Any
from uuid import UUID

from requests import get

basicConfig(level=INFO)
logger = getLogger(__name__)


class ValorantClient:
    def __init__(self):
        self.base_url = "https://valorant-api.com/v1"

    @staticmethod
    def _get(url: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        try:
            response = get(url, params=params)
            response.raise_for_status()
        except Exception as e:
            logger.exception(f"Error during get request: {e}")
            raise

        return response.json()

    def get_all_maps(self) -> dict[str, Any]:
        url = f"{self.base_url}/maps"
        return self._get(url)

    def get_map_by_uuid(self, map_uuid: UUID) -> dict[str, Any]:
        url = f"{self.base_url}/maps/{map_uuid}"
        return self._get(url)

    def get_all_agents(self, language: str = "en-US", is_playable_character: bool = True) -> dict[str, Any]:
        url = f"{self.base_url}/agents"
        params = {"language": language, "isPlayableCharacter": is_playable_character}
        return self._get(url, params=params)

    def get_agent_by_uuid(self, agent_uuid: UUID, language: str = "en-US") -> dict[str, Any]:
        url = f"{self.base_url}/agents/{agent_uuid}"
        params = {"language": language}
        return self._get(url, params=params)


if __name__ == "__main__":
    client = ValorantClient()
    all_maps = client.get_all_maps()
    # print(all_maps)

    haven_map = client.get_map_by_uuid(UUID("2bee0dc9-4ffe-519b-1cbd-7fbe763a6047"))
    # print(haven_map)

    all_agents = client.get_all_agents()
    # print(all_agents)

    gekko_agent = client.get_agent_by_uuid(UUID("e370fa57-4757-3604-3648-499e1f642d3f"))
    # print(gekko_agent)
