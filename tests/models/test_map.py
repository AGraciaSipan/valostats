import pytest

from src.models.map import Callout, Location, Map


@pytest.fixture()
def location_data():
    return {"x": 10.0, "y": 20.0}


@pytest.fixture()
def empty_location_data():
    return {}


@pytest.fixture()
def callout_data(location_data):
    return {"regionName": "Test Region", "superRegionName": "Test Super Region", "location": location_data}


@pytest.fixture()
def map_metadata(uuid, callout_data):
    first_callout = callout_data.copy()
    first_callout["location"] = callout_data["location"].copy()

    second_callout = callout_data.copy()
    second_callout["location"] = {"x": callout_data["location"]["x"] + 1, "y": callout_data["location"]["y"] + 1}

    return {
        "uuid": uuid,
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
def empty_map_metadata(uuid):
    return {"uuid": uuid, "displayName": "Test Map"}


def test_location_from_dict(location_data):
    location = Location.from_dict(location_data)
    assert location.x == location_data["x"]
    assert location.y == location_data["y"]


def test_location_from_empty_dict(empty_location_data):
    location = Location.from_dict(empty_location_data)
    assert location.x == 0.0
    assert location.y == 0.0


def test_callout_initialization(callout_data):
    callout = Callout(callout_data)
    assert callout.region_name == callout_data["regionName"]
    assert callout.super_region_name == callout_data["superRegionName"]
    assert callout.location.x == callout_data["location"]["x"]
    assert callout.location.y == callout_data["location"]["y"]


def test_map_initialization(map_metadata):
    map_instance = Map(map_metadata)
    assert map_instance.uuid == map_metadata["uuid"]
    assert map_instance.display_name == map_metadata["displayName"]
    assert map_instance.display_icon == map_metadata["displayIcon"]
    assert map_instance.list_view_icon == map_metadata["listViewIcon"]
    assert map_instance.splash == map_metadata["splash"]
    assert map_instance.x_multiplier == map_metadata["xMultiplier"]
    assert map_instance.y_multiplier == map_metadata["yMultiplier"]
    assert map_instance.x_scalar_to_add == map_metadata["xScalarToAdd"]
    assert map_instance.y_scalar_to_add == map_metadata["yScalarToAdd"]
    assert len(map_instance.callouts) == len(map_metadata["callouts"])
    assert map_instance.callouts[0].region_name == map_metadata["callouts"][0]["regionName"]
    assert map_instance.callouts[1].region_name == map_metadata["callouts"][1]["regionName"]


def test_map_initialization_with_default_callouts(empty_map_metadata):
    map_instance = Map(empty_map_metadata)
    assert map_instance.uuid == empty_map_metadata["uuid"]
    assert map_instance.display_name == empty_map_metadata["displayName"]
    assert len(map_instance.callouts) == 0
