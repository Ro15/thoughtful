"""Telegram alerting module.

Provides utilities to format strategy signals and send them as messages
via the Telegram Bot API.
"""

from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class StrategySignal:
    """Represents a trading strategy signal."""

    ticker: str
    strike: str
    expiry: str
    rationale: str


def format_signal(signal: StrategySignal) -> str:
    """Format a :class:`StrategySignal` for human-friendly alerts."""

    return (
        f"{signal.ticker} {signal.strike} expiring {signal.expiry}\n"
        f"Reason: {signal.rationale}"
    )


class TelegramAlerter:
    """Send messages to Telegram chats using a bot token."""

    def __init__(self, bot_token: str, chat_id: str, session: Optional[requests.Session] = None) -> None:
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.session = session or requests.Session()
        self.api_base = f"https://api.telegram.org/bot{bot_token}"

    def send_message(self, text: str) -> None:
        """Post a raw text message to the Telegram chat."""

        url = f"{self.api_base}/sendMessage"
        response = self.session.post(url, data={"chat_id": self.chat_id, "text": text}, timeout=10)
        response.raise_for_status()

    def send_signal(self, signal: StrategySignal) -> None:
        """Format and send a :class:`StrategySignal` as a Telegram message."""

        message = format_signal(signal)
        self.send_message(message)
