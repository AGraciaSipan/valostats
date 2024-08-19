import pytest

from src.models.agent.role import Role, RoleUUID


@pytest.fixture()
def invalid_role_data(uuid):
    return {"uuid": str(uuid), "displayName": "Test Role"}


def test_invalid_role_uuid(invalid_role_data):
    with pytest.raises(ValueError) as excinfo:
        Role.from_dict(invalid_role_data)
    assert str(excinfo.value) == f"'{invalid_role_data['uuid']}' is not a valid RoleUUID"


def test_role_from_dict(uuid, role_data):
    role = Role.from_dict(role_data)
    assert role.uuid == RoleUUID(role_data["uuid"])
    assert role.name == role_data["displayName"]


def test_role_to_dict(role_data):
    role = Role.from_dict(role_data)
    assert role.to_dict() == {"uuid": role_data["uuid"], "displayName": role_data["displayName"]}


def test_role_round_trip(role_data):
    role = Role.from_dict(role_data)
    role_dict = role.to_dict()
    assert role == Role.from_dict(role_dict)
