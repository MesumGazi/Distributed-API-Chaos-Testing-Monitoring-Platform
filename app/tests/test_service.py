import pytest
import httpx
from unittest.mock import Mock, AsyncMock
from services.services import url_validation


@pytest.mark.asyncio
async def test_successful_request():
    mock_client = AsyncMock()
    mock_response = Mock()

    mock_response.status_code = 200
    mock_response.reason_phrase = "OK"
    mock_response.elapsed.total_seconds.return_value = 0.123
    mock_response.headers.get.return_value = None

    mock_client.get.return_value = mock_response

    result = await url_validation("https://www.dummy.com", mock_client)

    assert result["status_code"] == 200
    assert result["Status"] == "OK"
    assert result["Additional_Info"] == "Success"
    assert result["elapsed_time"] == 0.123


@pytest.mark.asyncio
async def test_timeout():
    mock_client = AsyncMock()
    mock_client.get.side_effect = httpx.TimeoutException("Timeout")

    result = await url_validation("https://slow.example.com", mock_client)

    assert result["Status"] is False
    assert "error" in result
    assert result["error"] == "request Timed out"


@pytest.mark.asyncio
async def test_request_failed():
    mock_client = AsyncMock()
    mock_response = Mock()

    mock_response.status_code = 500
    mock_response.reason_phrase = "server error"
    mock_response.headers.get.return_value = None

    mock_client.get.return_value = mock_response

    result = await url_validation("https://www.dummy.com", mock_client)

    assert result["status_code"] == 500
    assert result["Status"] == "server error"
    assert result["Additional_Info"] == "Server_Error"
