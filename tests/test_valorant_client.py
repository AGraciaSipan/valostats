from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from valorant_client.client import ValorantClient


@pytest.fixture
def api_client():
    return ValorantClient()


@pytest.fixture()
def uuid():
    return uuid4()


@patch("valorant_client.client.get")
def test_success__get(mock_get, api_client):
    url = "https://testurl"
    params = {"parameter": 1}
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "success"}
    mock_get.return_value = mock_response

    response = api_client._get(url, params=params)

    mock_get.assert_called_once_with(url, params=params)
    assert response == {"status": "success"}


@patch("valorant_client.client.get")
def test_exception__get(mock_get, api_client, caplog):
    url = "https://testurl"
    mock_get.side_effect = Exception("Test error")

    with pytest.raises(Exception, match="Test error"):
        api_client._get(url)

    assert "Error during get request: Test error" in caplog.text


@patch.object(ValorantClient, "_get")
def test_get_all_maps(mock_get, api_client):
    expected_url = f"{api_client.base_url}/maps"
    api_client.get_all_maps()
    mock_get.assert_called_once_with(expected_url)


@patch.object(ValorantClient, "_get")
def test_get_map_by_uuid(mock_get, api_client, uuid):
    expected_url = f"{api_client.base_url}/maps/{uuid}"
    api_client.get_map_by_uuid(uuid)
    mock_get.assert_called_once_with(expected_url)


@patch.object(ValorantClient, "_get")
def test_get_all_agents(mock_get, api_client):
    expected_url = f"{api_client.base_url}/agents"
    expected_params = {"language": "en-US", "isPlayableCharacter": True}
    api_client.get_all_agents()
    mock_get.assert_called_once_with(expected_url, params=expected_params)


@patch.object(ValorantClient, "_get")
def test_get_agent_by_uuid(mock_get, api_client, uuid):
    expected_url = f"{api_client.base_url}/agents/{uuid}"
    expected_params = {"language": "en-US"}
    api_client.get_agent_by_uuid(uuid)
    mock_get.assert_called_once_with(expected_url, params=expected_params)


@pytest.mark.parametrize(
    "language, is_playable_character",
    [
        ("en-US", True),
        ("es-ES", False),
        ("fr-FR", True),
    ],
)
@patch.object(ValorantClient, "_get")
def test_get_all_agents_parametrized(mock_get, api_client, language, is_playable_character):
    expected_url = f"{api_client.base_url}/agents"
    expected_params = {"language": language, "isPlayableCharacter": is_playable_character}
    api_client.get_all_agents(language=language, is_playable_character=is_playable_character)
    mock_get.assert_called_once_with(expected_url, params=expected_params)


@pytest.mark.parametrize("language", ["en-US", "es-ES", "fr-FR"])
@patch.object(ValorantClient, "_get")
def test_get_agent_by_uuid_with_different_languages(mock_get, api_client, uuid, language):
    expected_url = f"{api_client.base_url}/agents/{uuid}"
    expected_params = {"language": language}
    api_client.get_agent_by_uuid(uuid, language=language)
    mock_get.assert_called_once_with(expected_url, params=expected_params)
