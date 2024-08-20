import os
import tempfile
from uuid import UUID

import pytest

from src.models.agent.ability import AbilitySlot
from src.models.agent.agent import Agent, AgentUUID
from src.models.agent.role import RoleUUID
from tests.models.agent.test_ability import ALL_ABILITIES
from tests.models.agent.test_role import ALL_ROLES


@pytest.fixture()
def all_ability_data():
    return ALL_ABILITIES


@pytest.fixture()
def one_role_data():
    return ALL_ROLES[0]


@pytest.fixture()
def agent_data(one_role_data, all_ability_data):
    return {
        "uuid": "601dbbe7-43ce-be57-2a40-4abd24953621",
        "displayName": "Test/Agent",
        "displayIcon": "icon.png",
        "displayIconSmall": "small_icon.png",
        "role": one_role_data,
        "abilities": all_ability_data,
    }


@pytest.fixture()
def invalid_agent_data(uuid, agent_data):
    invalid_data = agent_data.copy()
    invalid_data["uuid"] = str(uuid)

    return invalid_data


def test_agent_uuids():
    for agent in AgentUUID:
        try:
            uuid_obj = UUID(agent.value)
            assert uuid_obj.hex == agent.value.replace("-", ""), f"UUID mismatch for {agent.name}"
        except ValueError:
            pytest.fail(f"Invalid UUID format for {agent.name}: {agent.value}")


def test_invalid_agent_uuid(invalid_agent_data):
    with pytest.raises(ValueError) as excinfo:
        Agent.from_dict(invalid_agent_data)
    assert str(excinfo.value) == f"'{invalid_agent_data['uuid']}' is not a valid AgentUUID"


def test_agent_from_dict(agent_data):
    agent = Agent.from_dict(agent_data)
    assert agent.uuid == AgentUUID(agent_data["uuid"])
    assert agent.name == agent_data["displayName"].replace("/", "")
    assert agent.display_icon == agent_data["displayIcon"]
    assert agent.display_icon_small == agent_data["displayIconSmall"]
    assert agent.role.uuid == RoleUUID(agent_data["role"]["uuid"])
    assert agent.role.name == agent_data["role"]["displayName"]
    assert len(agent.abilities) == len(agent_data["abilities"])
    assert agent.abilities[0].slot == AbilitySlot(agent_data["abilities"][0]["slot"])
    assert agent.abilities[0].name == agent_data["abilities"][0]["displayName"]
    assert agent.abilities[1].slot == AbilitySlot(agent_data["abilities"][1]["slot"])
    assert agent.abilities[1].name == agent_data["abilities"][1]["displayName"]
    assert agent.abilities[2].slot == AbilitySlot(agent_data["abilities"][2]["slot"])
    assert agent.abilities[2].name == agent_data["abilities"][2]["displayName"]
    assert agent.abilities[3].slot == AbilitySlot(agent_data["abilities"][3]["slot"])
    assert agent.abilities[3].name == agent_data["abilities"][3]["displayName"]


def test_agent_to_dict(agent_data):
    agent = Agent.from_dict(agent_data)
    assert agent.to_dict() == {
        "uuid": agent.uuid.value,
        "displayName": agent.name,
        "displayIcon": agent.display_icon,
        "displayIconSmall": agent.display_icon_small,
        "role": agent.role.to_dict(),
        "abilities": [ability.to_dict() for ability in agent.abilities],
    }


def test_agent_round_trip(agent_data):
    agent = Agent.from_dict(agent_data)
    agent_dict = agent.to_dict()
    assert agent == Agent.from_dict(agent_dict)


def test_agent_json_serialization(agent_data):
    agent = Agent.from_dict(agent_data)
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name
    try:
        agent.to_json(temp_file_path)
        loaded_agent = Agent.from_json(temp_file_path)
        assert agent == loaded_agent
    finally:
        os.remove(temp_file_path)
