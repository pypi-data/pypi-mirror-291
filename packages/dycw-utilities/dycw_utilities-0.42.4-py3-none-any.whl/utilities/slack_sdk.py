from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from cachetools.func import ttl_cache
from slack_sdk.webhook import WebhookClient, WebhookResponse
from slack_sdk.webhook.async_client import AsyncWebhookClient
from typing_extensions import override

_TIMEOUT = 30


def send_slack_sync(text: str, /, *, url: str, timeout: int = _TIMEOUT) -> None:
    """Send a message to Slack, synchronously."""
    client = _get_client_sync(url, timeout=timeout)
    response = client.send(text=text)
    _check_status_code(response)


async def send_slack_async(
    text: str,
    /,
    *,
    url: str,
    timeout: int = _TIMEOUT,  # noqa: ASYNC109
) -> None:
    """Send a message via Slack."""
    client = _get_client_async(url, timeout=timeout)
    response = await client.send(text=text)
    _check_status_code(response)


def _check_status_code(response: WebhookResponse, /) -> None:
    """Check that a chunk was successfully sent."""
    if response.status_code != HTTPStatus.OK:
        raise SendSlackError(response=response)


@dataclass(kw_only=True)
class SendSlackError(Exception):
    response: WebhookResponse

    @override
    def __str__(self) -> str:
        return f"Webhook response was not OK; got {self.response.status_code}"


@ttl_cache(maxsize=1)
def _get_client_sync(url: str, /, *, timeout: int = _TIMEOUT) -> WebhookClient:
    """Get the webhook client."""
    return WebhookClient(url, timeout=timeout)


@ttl_cache(maxsize=1)
def _get_client_async(url: str, /, *, timeout: int = _TIMEOUT) -> AsyncWebhookClient:
    """Get the engine/sessionmaker for the required database."""
    return AsyncWebhookClient(url, timeout=timeout)


__all__ = ["send_slack_async", "send_slack_sync"]
