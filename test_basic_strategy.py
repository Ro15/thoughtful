import pandas as pd
from basic_strategy import BasicStrategy


def test_indicators_and_signal():
    prices = pd.Series([1,2,3,4,3,2,1,2,3,4,5,6,7,8,9,10])
    iv_history = pd.Series([0.2,0.25,0.3,0.28,0.35,0.4])
    strategy = BasicStrategy()

    rsi = strategy.compute_rsi(prices)
    macd_line, signal_line, hist = strategy.compute_macd(prices)
    iv_rank = strategy.compute_iv_rank(0.3, iv_history)

    assert len(rsi) == len(prices)
    assert len(macd_line) == len(prices)
    assert 0 <= iv_rank <= 100

    # Check that check_trade_signal returns a boolean
    result = strategy.check_trade_signal(prices, iv_history, 0.3, 10000)
    assert isinstance(result, bool)
