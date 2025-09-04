from __future__ import annotations

import asyncio
import json
from datetime import datetime, date
from typing import Iterable

import requests
import websockets
from sqlalchemy.orm import Session

from .database import SessionLocal, init_db
from .models import OptionContract, UnderlyingPrice


class ProviderClient:
    """Simple client for a market data provider."""

    def __init__(self, websocket_url: str, rest_url: str) -> None:
        self.websocket_url = websocket_url
        self.rest_url = rest_url.rstrip("/")

    async def subscribe_ticks(self, symbols: Iterable[str], session: Session) -> None:
        """Connect to provider WebSocket and store incoming ticks."""
        async with websockets.connect(self.websocket_url) as ws:
            await ws.send(json.dumps({"type": "subscribe", "symbols": list(symbols)}))
            async for msg in ws:
                data = json.loads(msg)
                tick = UnderlyingPrice(
                    symbol=data["symbol"],
                    price=float(data["price"]),
                    timestamp=datetime.fromisoformat(data["timestamp"]),
                )
                session.add(tick)
                session.commit()

    def fetch_option_chain(self, symbol: str, session: Session) -> None:
        """Fetch option chain for *symbol* via REST and store contracts."""
        url = f"{self.rest_url}/options/{symbol}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        contracts = response.json()
        for item in contracts:
            contract = OptionContract(
                symbol=symbol,
                expiration=date.fromisoformat(item["expiration"]),
                strike=float(item["strike"]),
                option_type=item["type"],
                bid=item.get("bid"),
                ask=item.get("ask"),
            )
            session.add(contract)
        session.commit()


def main() -> None:
    """Example entrypoint for running the ingestion pipeline."""
    init_db()
    session = SessionLocal()
    client = ProviderClient(
        websocket_url="wss://example.com/marketdata",
        rest_url="https://example.com/api",
    )
    # In production, you would likely run subscribe_ticks in a background task.
    symbols = ["AAPL"]
    asyncio.run(client.subscribe_ticks(symbols, session))
    client.fetch_option_chain("AAPL", session)


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
