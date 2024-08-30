import pytest

from src.models.game_map.callout import Callout


def test_callout_from_dict(callout_data):
    callout = Callout.from_dict(callout_data)
    assert callout.region_name == "Test Region"
    assert callout.super_region_name == "Test Super Region"
    assert callout.location.x == 10.0
    assert callout.location.y == -20.0


def test_callout_instantiation_without_region_name_raises_keyerror(location_data):
    with pytest.raises(KeyError):
        Callout.from_dict({"superRegionName": "Test Super Region", "location": location_data})


def test_callout_to_dict(callout_data):
    callout = Callout.from_dict(callout_data)
    assert callout.to_dict() == callout_data


def test_callout_round_trip(callout_data):
    callout = Callout.from_dict(callout_data)
    callout_dict = callout.to_dict()
    assert callout == Callout.from_dict(callout_dict)
