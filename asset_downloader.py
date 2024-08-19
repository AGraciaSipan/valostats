import os
from logging import INFO, basicConfig, getLogger

import requests

from src.models.agent.agent import Agent, AgentUUID
from src.models.game_map.game_map import GameMap, MapUUIDs
from valorant_client.client import ValorantClient

basicConfig(level=INFO)
logger = getLogger(__name__)


class AssetDownloader:
    DEFAULT_MAP_ASSET_TYPES = ["display_icon", "list_view_icon", "splash"]
    DEFAULT_AGENT_ASSET_TYPES = ["display_icon", "display_icon_small"]

    def __init__(self, base_directory: str):
        self.base_directory = base_directory

    @staticmethod
    def _download_asset(url: str, path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            logger.info(f"Downloading asset from {url}")
            response = requests.get(url)
            response.raise_for_status()
            with open(path, "wb") as file:
                file.write(response.content)
            logger.info(f"Saved asset to {path}")
        except Exception as e:
            logger.exception(f"Error downloading asset: {e}")
            raise

    def _save_assets(self, obj: GameMap | Agent, asset_types: list[str]) -> None:
        if isinstance(obj, GameMap):
            assets = {
                "display_icon": obj.display_icon,
                "list_view_icon": obj.list_view_icon,
                "splash": obj.splash,
            }
            directory = os.path.join(self.base_directory, "maps", obj.display_name.lower())
        elif isinstance(obj, Agent):
            assets = {
                "display_icon": obj.display_icon,
                "display_icon_small": obj.display_icon_small,
            }
            directory = os.path.join(self.base_directory, "agents", obj.name.lower())
        else:
            raise TypeError("Unsupported object type for asset downloading")

        for asset_name in asset_types:
            url = assets.get(asset_name)
            if url:
                filename = f"{asset_name}.png"
                path = os.path.join(directory, filename)
                self._download_asset(url, path)
            else:
                logger.warning(f"No URL found for asset type: {asset_name} in {type(obj).__name__}")

    def save_map_assets(self, game_map: GameMap, asset_types: list[str] | None = None) -> None:
        if asset_types is None:
            asset_types = self.DEFAULT_MAP_ASSET_TYPES
        self._save_assets(game_map, asset_types)

    def save_agent_assets(self, agent: Agent, asset_types: list[str] | None = None) -> None:
        if asset_types is None:
            asset_types = self.DEFAULT_AGENT_ASSET_TYPES
        self._save_assets(agent, asset_types)


if __name__ == "__main__":
    client = ValorantClient()
    asset_manager = AssetDownloader(base_directory=os.path.join("src", "assets"))

    for map_uuid in MapUUIDs:
        map_name = map_uuid.name.lower()
        try:
            map_data = client.get_map_by_uuid(map_uuid.value)
            game_map = GameMap.from_dict(map_data.get("data", {}))
            asset_manager.save_map_assets(game_map, ["display_icon"])
        except Exception as e:
            logger.exception(f"Error downloading data for {map_name}: {e}")

    for agent_uuid in AgentUUID:
        agent_name = agent_uuid.name.lower()
        try:
            agent_data = client.get_agent_by_uuid(agent_uuid.value)
            agent = Agent.from_dict(agent_data.get("data", {}))
            asset_manager.save_agent_assets(agent, ["display_icon_small"])
        except Exception as e:
            logger.exception(f"Error downloading data for {agent_name}: {e}")
