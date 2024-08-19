import pytest


@pytest.fixture()
def role_data(uuid):
    return {"uuid": str(uuid), "displayName": "Test Role"}
