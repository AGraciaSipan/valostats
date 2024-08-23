import pytest

from src.models.game_map.location import Location


@pytest.fixture()
def empty_location_data():
    return {}


def test_location_from_dict(location_data):
    location = Location(**location_data)
    assert location.x == location_data["x"]
    assert location.y == location_data["y"]


def test_location_from_empty_dict(empty_location_data):
    location = Location(**empty_location_data)
    assert location.x == 0.0
    assert location.y == 0.0


def test_location_to_dict(location_data):
    location = Location(**location_data)
    assert location.to_dict() == location_data


def test_location_round_trip(location_data):
    location = Location(**location_data)
    location_dict = location.to_dict()
    assert location == Location(**location_dict)
