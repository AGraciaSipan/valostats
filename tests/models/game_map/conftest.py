import pytest


@pytest.fixture()
def location_data():
    return {"x": 10.0, "y": -20.0}


@pytest.fixture()
def callout_data(location_data):
    return {"regionName": "Test Region", "superRegionName": "Test Super Region", "location": location_data}
