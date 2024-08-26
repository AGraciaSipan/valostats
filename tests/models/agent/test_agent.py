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

    expected_abilities = [
        (AbilitySlot.Q_SLOT, "Ability 1 Name"),
        (AbilitySlot.E_SLOT, "Ability 2 Name"),
        (AbilitySlot.C_SLOT, "Grenade Name"),
        (AbilitySlot.X_SLOT, "Ultimate Name"),
        (AbilitySlot._SLOT, "Passive Name"),
    ]

    assert agent.uuid == AgentUUID("601dbbe7-43ce-be57-2a40-4abd24953621")
    assert agent.name == "TestAgent"
    assert agent.display_icon == "icon.png"
    assert agent.display_icon_small == "small_icon.png"
    assert agent.role.uuid == RoleUUID("4ee40330-ecdd-4f2f-98a8-eb1243428373")
    assert agent.role.name == "Controller"
    assert len(agent.abilities) == 5

    for ability, (expected_slot, expected_name) in zip(agent.abilities, expected_abilities):
        assert ability.slot == expected_slot
        assert ability.name == expected_name


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
