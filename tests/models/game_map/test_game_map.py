import os
import tempfile
from uuid import UUID

import pytest

from src.models.game_map.game_map import GameMap, MapUUID


@pytest.fixture()
def map_metadata(callout_data):
    first_callout = callout_data.copy()
    first_callout["location"] = callout_data["location"].copy()

    second_callout = callout_data.copy()
    second_callout["location"] = {"x": callout_data["location"]["x"] + 1, "y": callout_data["location"]["y"] + 1}

    return {
        "uuid": "224b0a95-48b9-f703-1bd8-67aca101a61f",
        "displayName": "Test Map",
        "displayIcon": "icon.png",
        "listViewIcon": "list_icon.png",
        "splash": "splash.png",
        "xMultiplier": 2.0,
        "yMultiplier": 2.0,
        "xScalarToAdd": 1.0,
        "yScalarToAdd": 1.0,
        "callouts": [callout_data, callout_data],
    }


@pytest.fixture()
def invalid_map_data(uuid, map_metadata):
    invalid_data = map_metadata.copy()
    invalid_data["uuid"] = str(uuid)

    return invalid_data


@pytest.fixture()
def empty_map_metadata():
    return {"uuid": "224b0a95-48b9-f703-1bd8-67aca101a61f", "displayName": "Test Map", "displayIcon": "icon.png"}


@pytest.fixture()
def map_metadata_with_null_values():
    return {
        "uuid": "224b0a95-48b9-f703-1bd8-67aca101a61f",
        "displayName": "Test Map",
        "displayIcon": "icon.png",
        "list_view_icon": None,
        "splash": None,
        "x_multiplier": None,
        "y_multiplier": None,
        "x_scalar_to_add": None,
        "y_scalar_to_add": None,
        "callouts": None,
    }


def test_map_uuids():
    for map_uuid in MapUUID:
        try:
            uuid_obj = UUID(map_uuid.value)
            assert uuid_obj.hex == map_uuid.value.replace("-", ""), f"UUID mismatch for {map_uuid.name}"
        except ValueError:
            pytest.fail(f"Invalid UUID format for {map_uuid.name}: {map_uuid.value}")


def test_invalid_map_uuid(invalid_map_data):
    with pytest.raises(ValueError) as excinfo:
        GameMap.from_dict(invalid_map_data)
    assert str(excinfo.value) == f"'{invalid_map_data['uuid']}' is not a valid MapUUID"


def test_map_from_dict_initialization(map_metadata):
    game_map = GameMap.from_dict(map_metadata)
    assert game_map.uuid == MapUUID(map_metadata["uuid"])
    assert game_map.name == map_metadata["displayName"]
    assert game_map.display_icon == map_metadata["displayIcon"]
    assert game_map.list_view_icon == map_metadata["listViewIcon"]
    assert game_map.splash == map_metadata["splash"]
    assert game_map.x_multiplier == map_metadata["xMultiplier"]
    assert game_map.y_multiplier == map_metadata["yMultiplier"]
    assert game_map.x_scalar_to_add == map_metadata["xScalarToAdd"]
    assert game_map.y_scalar_to_add == map_metadata["yScalarToAdd"]
    assert len(game_map.callouts) == len(map_metadata["callouts"])
    assert game_map.callouts[0].region_name == map_metadata["callouts"][0]["regionName"]
    assert game_map.callouts[1].region_name == map_metadata["callouts"][1]["regionName"]


def test_map_from_dict_initialization_with_empty_values(empty_map_metadata):
    game_map = GameMap.from_dict(empty_map_metadata)
    assert game_map.uuid == MapUUID(empty_map_metadata["uuid"])
    assert game_map.name == empty_map_metadata["displayName"]
    assert game_map.display_icon == "icon.png"
    assert game_map.list_view_icon is None
    assert game_map.splash is None
    assert game_map.x_multiplier == 1.0
    assert game_map.y_multiplier == 1.0
    assert game_map.x_scalar_to_add == 0.0
    assert game_map.x_scalar_to_add == 0.0
    assert len(game_map.callouts) == 0


def test_map_from_dict_initialization_with_null_values(map_metadata_with_null_values):
    game_map = GameMap.from_dict(map_metadata_with_null_values)
    assert game_map.uuid == MapUUID(map_metadata_with_null_values["uuid"])
    assert game_map.name == map_metadata_with_null_values["displayName"]
    assert game_map.display_icon == map_metadata_with_null_values["displayIcon"]
    assert game_map.list_view_icon is None
    assert game_map.splash is None
    assert game_map.x_multiplier == 1.0
    assert game_map.y_multiplier == 1.0
    assert game_map.x_scalar_to_add == 0.0
    assert game_map.x_scalar_to_add == 0.0
    assert len(game_map.callouts) == 0


@pytest.mark.parametrize("missing_key", ["uuid", "displayName", "displayIcon"])
def test_map_instantiation_missing_key_raises_keyerror(map_metadata, missing_key):
    map_metadata_missing_key = map_metadata.copy()
    del map_metadata_missing_key[missing_key]

    with pytest.raises(KeyError):
        GameMap.from_dict(map_metadata_missing_key)


def test_map_to_dict(map_metadata):
    game_map = GameMap.from_dict(map_metadata)
    assert game_map.to_dict() == map_metadata


def test_map_round_trip(map_metadata):
    game_map = GameMap.from_dict(map_metadata)
    map_dict = game_map.to_dict()
    assert game_map == GameMap.from_dict(map_dict)


def test_map_json_serialization(map_metadata):
    game_map = GameMap.from_dict(map_metadata)
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name
    try:
        game_map.to_json(temp_file_path)
        loaded_game_map = GameMap.from_json(temp_file_path)
        assert game_map == loaded_game_map
    finally:
        os.remove(temp_file_path)
