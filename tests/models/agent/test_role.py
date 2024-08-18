from uuid import UUID

from src.models.agent.role import Role


def test_role_from_dict(uuid, role_data):
    role = Role.from_dict(role_data)
    assert role.uuid == UUID(role_data["uuid"])
    assert role.name == role_data["displayName"]


def test_role_to_dict(role_data):
    role = Role.from_dict(role_data)
    assert role.to_dict() == {"uuid": str(role.uuid), "displayName": role_data["displayName"]}


def test_role_round_trip(role_data):
    role = Role.from_dict(role_data)
    role_dict = role.to_dict()
    assert role == Role.from_dict(role_dict)
