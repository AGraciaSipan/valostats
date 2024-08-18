import pytest


@pytest.fixture()
def role_data(uuid):
    return {"uuid": str(uuid), "displayName": "Test Role"}


@pytest.fixture()
def ability_data():
    return {"slot": "Test Ability", "displayName": "Ability Name"}
