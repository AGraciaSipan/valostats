import os
from logging import INFO, basicConfig, getLogger

from src.models.game_map.game_map import GameMap, MapUUIDs
from valorant_client.client import ValorantClient

basicConfig(level=INFO)
logger = getLogger(__name__)


if __name__ == "__main__":
    client = ValorantClient()
    base_directory = os.path.join("src", "data")

    for map_uuid in MapUUIDs:
        map_name = map_uuid.name.lower()
        logger.info(f"Downloading data for {map_name}")
        try:
            map_data = client.get_map_by_uuid(map_uuid.value)
            game_map = GameMap.from_dict(map_data.get("data", {}))
            file_name = f"{map_name}.json"
            path = os.path.join(base_directory, "maps", file_name)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            game_map.to_json(path)
            logger.info(f"Saved map to {path}")
        except Exception as e:
            logger.exception(f"Error downloading data for {map_name}: {e}")
