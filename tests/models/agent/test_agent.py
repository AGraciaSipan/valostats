import os
import tempfile
from uuid import UUID

import pytest

from src.models.agent.ability import AbilitySlot
from src.models.agent.agent import Agent
from tests.models.agent.test_ability import ALL_ABILITIES


@pytest.fixture()
def all_ability_data():
    return ALL_ABILITIES


@pytest.fixture()
def agent_data(uuid, role_data, all_ability_data):
    return {
        "uuid": str(uuid),
        "displayName": "Test/Agent",
        "displayIcon": "icon.png",
        "displayIconSmall": "small_icon.png",
        "role": role_data,
        "abilities": all_ability_data,
    }


def test_agent_from_dict(agent_data):
    agent = Agent.from_dict(agent_data)
    assert agent.uuid == UUID(agent_data["uuid"])
    assert agent.name == agent_data["displayName"].replace("/", "")
    assert agent.display_icon == agent_data["displayIcon"]
    assert agent.display_icon_small == agent_data["displayIconSmall"]
    assert agent.role.uuid == UUID(agent_data["role"]["uuid"])
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
        "uuid": str(agent.uuid),
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
