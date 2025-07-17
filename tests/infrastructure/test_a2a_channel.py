import pytest
from pytest_httpx import HTTPXMock
import json

from domain.communication import Message
from infrastructure.communication.a2a_channel import A2ACommunicationChannel

BASE_URL = "http://fake-agent.com"


@pytest.mark.asyncio
async def test_a2a_communication_channel_send_success(httpx_mock: HTTPXMock):
    # Arrange
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/v1/tasks/send",
        status_code=200,
        json={"status": "ok"},
    )
    channel = A2ACommunicationChannel(base_url=BASE_URL)
    message = Message(
        sender_id="test-sender",
        receiver_id="test-receiver",
        content="Hello, world!",
    )

    # Act
    await channel.send(message)

    # Assert
    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "POST"
    assert str(request.url) == f"{BASE_URL}/v1/tasks/send"
    assert json.loads(request.content) == {
        "taskId": message.id,
        "message": {
            "role": "user",
            "parts": [{"text": "Hello, world!"}],
        },
    }


@pytest.mark.asyncio
async def test_a2a_communication_channel_send_http_error(httpx_mock: HTTPXMock):
    # Arrange
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/v1/tasks/send",
        status_code=500,
        text="Internal Server Error",
    )
    channel = A2ACommunicationChannel(base_url=BASE_URL)
    message = Message(
        sender_id="test-sender",
        receiver_id="test-receiver",
        content="This will fail",
    )

    # Act & Assert
    # We don't assert a specific exception, but we check that the error is handled
    # gracefully (i.e., a message is printed and no exception is raised).
    # A more robust implementation might raise a custom exception.
    await channel.send(message)

    # In a real app, you'd check logs or a captured output. For now, we just
    # ensure it doesn't crash.
    assert len(httpx_mock.get_requests()) == 1


@pytest.mark.asyncio
async def test_a2a_communication_channel_receive_not_implemented():
    # Arrange
    channel = A2ACommunicationChannel(base_url=BASE_URL)

    # Act
    result = await channel.receive("any-agent")

    # Assert
    assert result is None 