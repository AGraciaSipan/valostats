import pytest

from src.models.agent.ability import Ability


@pytest.fixture()
def ability_data():
    return {"slot": "Test Ability", "displayName": "Ability Name"}


def test_ability_from_dict(ability_data):
    ability = Ability.from_dict(ability_data)
    assert ability.slot == ability_data["slot"]
    assert ability.name == ability_data["displayName"]


def test_ability_to_dict(ability_data):
    ability = Ability.from_dict(ability_data)
    assert ability.to_dict() == {"slot": ability_data["slot"], "displayName": ability_data["displayName"]}


def test_ability_round_trip(ability_data):
    ability = Ability.from_dict(ability_data)
    ability_dict = ability.to_dict()
    assert ability == Ability.from_dict(ability_dict)
