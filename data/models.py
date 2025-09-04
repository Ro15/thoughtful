from __future__ import annotations

from datetime import datetime, date
from typing import Optional

from sqlalchemy import Column, Date, DateTime, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UnderlyingPrice(Base):
    __tablename__ = "underlying_prices"

    id: int = Column(Integer, primary_key=True)
    symbol: str = Column(String, index=True, nullable=False)
    price: float = Column(Float, nullable=False)
    timestamp: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)


class OptionContract(Base):
    __tablename__ = "option_contracts"

    id: int = Column(Integer, primary_key=True)
    symbol: str = Column(String, index=True, nullable=False)
    expiration: date = Column(Date, nullable=False)
    strike: float = Column(Float, nullable=False)
    option_type: str = Column(String(4), nullable=False)  # 'call' or 'put'
    bid: Optional[float] = Column(Float)
    ask: Optional[float] = Column(Float)
    timestamp: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
