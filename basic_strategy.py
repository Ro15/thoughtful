from dataclasses import dataclass
from typing import Dict, Tuple

import pandas as pd


@dataclass
class BasicStrategy:
    """Simple trading strategy with common technical indicators.

    Attributes
    ----------
    risk_per_trade: float
        Portion of the portfolio to risk on each trade. Default is 2%.
    """

    risk_per_trade: float = 0.02

    def compute_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate the Relative Strength Index (RSI).

        Parameters
        ----------
        prices : pd.Series
            Series of asset prices.
        period : int, optional
            Lookback period for RSI, by default 14.
        """
        delta = prices.diff()
        up = delta.clip(lower=0)
        down = -delta.clip(upper=0)
        gain = up.rolling(window=period, min_periods=period).mean()
        loss = down.rolling(window=period, min_periods=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def compute_macd(
        self,
        prices: pd.Series,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9,
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Calculate the Moving Average Convergence Divergence (MACD).

        Returns
        -------
        macd_line, signal_line, histogram : Tuple[pd.Series, pd.Series, pd.Series]
            The MACD line, signal line, and histogram values.
        """
        fast_ema = prices.ewm(span=fast_period, adjust=False).mean()
        slow_ema = prices.ewm(span=slow_period, adjust=False).mean()
        macd_line = fast_ema - slow_ema
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram

    def compute_iv_rank(self, current_iv: float, iv_history: pd.Series) -> float:
        """Calculate implied volatility (IV) rank.

        IV Rank = (current IV - IV Low) / (IV High - IV Low) * 100
        """
        iv_low = iv_history.min()
        iv_high = iv_history.max()
        if iv_high == iv_low:
            return 0.0
        return (current_iv - iv_low) / (iv_high - iv_low) * 100

    def compute_position_size(self, portfolio_value: float, price: float) -> int:
        """Determine number of shares/contracts to purchase based on risk."""
        risk_amount = self.risk_per_trade * portfolio_value
        if price <= 0:
            raise ValueError("Price must be positive")
        return int(risk_amount // price)

    def check_trade_signal(
        self,
        prices: pd.Series,
        iv_history: pd.Series,
        current_iv: float,
        portfolio_value: float,
    ) -> bool:
        """Check if trade conditions are met and trigger alert.

        Conditions:
        - RSI below 30 (oversold)
        - MACD line crosses above signal line
        - IV Rank above 50
        """
        rsi_series = self.compute_rsi(prices)
        macd_line, signal_line, _ = self.compute_macd(prices)
        iv_rank = self.compute_iv_rank(current_iv, iv_history)

        rsi = rsi_series.iloc[-1]
        macd_val = macd_line.iloc[-1]
        signal_val = signal_line.iloc[-1]

        if rsi < 30 and macd_val > signal_val and iv_rank > 50:
            position = self.compute_position_size(portfolio_value, prices.iloc[-1])
            self.trigger_alert(
                {
                    "position": position,
                    "rsi": rsi,
                    "macd": macd_val,
                    "signal": signal_val,
                    "iv_rank": iv_rank,
                }
            )
            return True
        return False

    def trigger_alert(self, info: Dict[str, float]) -> None:
        """Placeholder alert mechanism. In production, hook into real alerts."""
        print("ALERT:", info)
