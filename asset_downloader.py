import os
from logging import INFO, basicConfig, getLogger

import requests

from src.models.game_map import GameMap, MapUUIDs
from valorant_client.client import ValorantClient

basicConfig(level=INFO)
logger = getLogger(__name__)


class AssetDownloader:
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

    def save_map_assets(self, game_map: GameMap, asset_types: list[str] | None = None) -> None:
        if asset_types is None:
            asset_types = ["display_icon", "list_view_icon", "splash"]

        assets = {
            "display_icon": game_map.display_icon,
            "list_view_icon": game_map.list_view_icon,
            "splash": game_map.splash,
        }

        for asset_name in asset_types:
            url = assets.get(asset_name)
            if url:
                filename = f"{asset_name}.png"
                path = os.path.join(self.base_directory, "maps", game_map.display_name.lower(), filename)
                self._download_asset(url, path)
            else:
                logger.warning(f"No URL found for asset type: {asset_name}")


if __name__ == "__main__":
    client = ValorantClient()
    asset_manager = AssetDownloader(base_directory=os.path.join("src", "assets"))

    for map_uuid in MapUUIDs:
        map_data = client.get_map_by_uuid(map_uuid.value)
        game_map = GameMap.from_dict(map_data.get("data", {}))
        asset_manager.save_map_assets(game_map, ["display_icon"])
