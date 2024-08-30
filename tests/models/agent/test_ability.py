import pytest

from src.models.agent.ability import Ability, AbilitySlot

ALL_ABILITIES = [
    {"slot": "Ability1", "displayName": "Ability 1 Name"},
    {"slot": "Ability2", "displayName": "Ability 2 Name"},
    {"slot": "Grenade", "displayName": "Grenade Name"},
    {"slot": "Ultimate", "displayName": "Ultimate Name"},
    {"slot": "Passive", "displayName": "Passive Name"},
]


@pytest.fixture()
def invalid_ability_data():
    return {"slot": "Invalid Slot", "displayName": "Invalid Ability Name"}


@pytest.fixture(params=ALL_ABILITIES)
def ability_data(request):
    return request.param


def test_invalid_ability_slot(invalid_ability_data):
    with pytest.raises(ValueError) as excinfo:
        Ability.from_dict(invalid_ability_data)
    assert str(excinfo.value) == "'Invalid Slot' is not a valid AbilitySlot"


def test_ability_from_dict(ability_data):
    ability = Ability.from_dict(ability_data)

    expected_slot = None
    expected_name = None

    if ability_data["slot"] == "Ability1":
        expected_slot = AbilitySlot.Q_SLOT
        expected_name = "Ability 1 Name"
    elif ability_data["slot"] == "Ability2":
        expected_slot = AbilitySlot.E_SLOT
        expected_name = "Ability 2 Name"
    elif ability_data["slot"] == "Grenade":
        expected_slot = AbilitySlot.C_SLOT
        expected_name = "Grenade Name"
    elif ability_data["slot"] == "Ultimate":
        expected_slot = AbilitySlot.X_SLOT
        expected_name = "Ultimate Name"
    elif ability_data["slot"] == "Passive":
        expected_slot = AbilitySlot._SLOT
        expected_name = "Passive Name"
    else:
        pytest.fail(f"Unexpected slot value: {ability_data['slot']}")

    assert ability.slot == expected_slot
    assert ability.name == expected_name


def test_ability_to_dict(ability_data):
    ability = Ability.from_dict(ability_data)
    assert ability.to_dict() == {"slot": ability.slot.value, "displayName": ability.name}


def test_ability_round_trip(ability_data):
    ability = Ability.from_dict(ability_data)
    ability_dict = ability.to_dict()
    assert ability == Ability.from_dict(ability_dict)
