from uuid import UUID

import pytest

from src.models.agent.role import Role, RoleUUID

ALL_ROLES = [
    {"uuid": "4ee40330-ecdd-4f2f-98a8-eb1243428373", "displayName": "Controller"},
    {"uuid": "dbe8757e-9e92-4ed4-b39f-9dfc589691d4", "displayName": "Duelist"},
    {"uuid": "1b47567f-8f7b-444b-aae3-b0c634622d10", "displayName": "Initiator"},
    {"uuid": "5fc02f99-4091-4486-a531-98459a3e95e9", "displayName": "Sentinel"},
]


@pytest.fixture()
def invalid_role_data(uuid):
    return {"uuid": str(uuid), "displayName": "Test Role"}


@pytest.fixture(params=ALL_ROLES)
def role_data(request):
    return request.param


def test_role_uuids():
    for role in RoleUUID:
        try:
            uuid_obj = UUID(role.value)
            assert uuid_obj.hex == role.value.replace("-", ""), f"UUID mismatch for {role.name}"
        except ValueError:
            pytest.fail(f"Invalid UUID format for {role.name}: {role.value}")


def test_invalid_role_uuid(invalid_role_data):
    with pytest.raises(ValueError) as excinfo:
        Role.from_dict(invalid_role_data)
    assert str(excinfo.value) == f"'{invalid_role_data['uuid']}' is not a valid RoleUUID"


def test_role_from_dict(role_data):
    role = Role.from_dict(role_data)
    assert role.uuid == RoleUUID(role_data["uuid"])
    assert role.name == role_data["displayName"]


def test_role_to_dict(role_data):
    role = Role.from_dict(role_data)
    assert role.to_dict() == {"uuid": role.uuid.value, "displayName": role.name}


def test_role_round_trip(role_data):
    role = Role.from_dict(role_data)
    role_dict = role.to_dict()
    assert role == Role.from_dict(role_dict)
