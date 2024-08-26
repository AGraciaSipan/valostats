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
    second_callout["regionName"] = "Another Test Region"
    second_callout["superRegionName"] = "Another Test Super Region"
    second_callout["location"] = {"x": -5.0, "y": 5.0}

    return {
        "uuid": "224b0a95-48b9-f703-1bd8-67aca101a61f",
        "displayName": "Test Map",
        "displayIcon": "icon.png",
        "listViewIcon": "list_icon.png",
        "splash": "splash.png",
        "xMultiplier": 2.0,
        "yMultiplier": -2.0,
        "xScalarToAdd": 1.0,
        "yScalarToAdd": -1.0,
        "callouts": [first_callout, second_callout],
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


def test_game_map_from_dict(map_metadata):
    game_map = GameMap.from_dict(map_metadata)
    assert game_map.uuid == MapUUID("224b0a95-48b9-f703-1bd8-67aca101a61f")
    assert game_map.name == "Test Map"
    assert game_map.display_icon == "icon.png"
    assert game_map.list_view_icon == "list_icon.png"
    assert game_map.splash == "splash.png"
    assert game_map.x_multiplier == 2.0
    assert game_map.y_multiplier == -2.0
    assert game_map.x_scalar_to_add == 1.0
    assert game_map.y_scalar_to_add == -1.0

    assert len(game_map.callouts) == 2

    first_callout = game_map.callouts[0]
    assert first_callout.region_name == "Test Region"
    assert first_callout.super_region_name == "Test Super Region"
    assert first_callout.location.x == 10.0
    assert first_callout.location.y == -20.0

    second_callout = game_map.callouts[1]
    assert second_callout.region_name == "Another Test Region"
    assert second_callout.super_region_name == "Another Test Super Region"
    assert second_callout.location.x == -5.0
    assert second_callout.location.y == 5.0


def test_game_map_from_dict_with_empty_values(empty_map_metadata):
    game_map = GameMap.from_dict(empty_map_metadata)
    assert game_map.uuid == MapUUID("224b0a95-48b9-f703-1bd8-67aca101a61f")
    assert game_map.name == "Test Map"
    assert game_map.display_icon == "icon.png"
    assert game_map.list_view_icon is None
    assert game_map.splash is None
    assert game_map.x_multiplier == 1.0
    assert game_map.y_multiplier == 1.0
    assert game_map.x_scalar_to_add == 0.0
    assert game_map.x_scalar_to_add == 0.0
    assert len(game_map.callouts) == 0


def test_game_map_from_dict_with_null_values(map_metadata_with_null_values):
    game_map = GameMap.from_dict(map_metadata_with_null_values)
    assert game_map.uuid == MapUUID("224b0a95-48b9-f703-1bd8-67aca101a61f")
    assert game_map.name == "Test Map"
    assert game_map.display_icon == "icon.png"
    assert game_map.list_view_icon is None
    assert game_map.splash is None
    assert game_map.x_multiplier == 1.0
    assert game_map.y_multiplier == 1.0
    assert game_map.x_scalar_to_add == 0.0
    assert game_map.x_scalar_to_add == 0.0
    assert len(game_map.callouts) == 0


@pytest.mark.parametrize("missing_key", ["uuid", "displayName", "displayIcon"])
def test_game_map_instantiation_missing_key_raises_keyerror(map_metadata, missing_key):
    map_metadata_missing_key = map_metadata.copy()
    del map_metadata_missing_key[missing_key]

    with pytest.raises(KeyError):
        GameMap.from_dict(map_metadata_missing_key)


def test_game_map_to_dict(map_metadata):
    game_map = GameMap.from_dict(map_metadata)
    assert game_map.to_dict() == map_metadata


def test_game_map_round_trip(map_metadata):
    game_map = GameMap.from_dict(map_metadata)
    map_dict = game_map.to_dict()
    assert game_map == GameMap.from_dict(map_dict)


def test_game_map_json_serialization(map_metadata):
    game_map = GameMap.from_dict(map_metadata)
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name
    try:
        game_map.to_json(temp_file_path)
        loaded_game_map = GameMap.from_json(temp_file_path)
        assert game_map == loaded_game_map
    finally:
        os.remove(temp_file_path)
