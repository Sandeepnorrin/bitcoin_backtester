# Trading Strategies Reference

| Strategy Name | Market Type | Time Frames | Indicators Required | Risk-Reward Ratio (RRR) | Entry Rules (When & How) | Exit Rules (When & How) | Indicator Alignment for Entry/Exit |
|---------------|------------|------------|---------------------|-------------------------|--------------------------|-------------------------|------------------------------------|
| 10 EMA Jackpot Strategy | Trending | 5m, 15m (Intraday); Daily (Swing) | 10 EMA | 1:2 to 1:3 (can reach 1:6) | When: Trigger candle (Green for Short, Red for Long) doesn't touch 10 EMA. How: Enter when the next candle breaks the trigger candle's low (Short) or high (Long). | When: Price closes on opposite side of 10 EMA. How: Set SL at trigger candle's high/low or 10 EMA. | Entry: Price must be physically separated (not touching) the 10 EMA. Exit: Close candle cross-over. |
| 10 & 20 EMA Bumper | Trending | 15m (Index); Daily (Stocks) | 10 EMA, 20 EMA, Marubozu Candle | 1:2 to 1:3 | When: 10 EMA crosses over/under 20 EMA. How: Confirm with a Bullish or Bearish Marubozu candle. | How: Set SL at the Marubozu candle's low/high or the previous candle. | Entry: 10 EMA health must be better than 20 EMA (cross-over). |
| 5 EMA Reversal | Trending (Reversal) | 15m (Shorts); 5m (Longs) | 5 EMA, 20 EMA (for trailing) | 1:3 to 1:4 | When: Candle high/low is completely outside the 5 EMA. How: Enter when the next candle breaks the trigger candle's extreme. | When: Price closes on the opposite side of 20 EMA. How: SL at trigger candle's high/low. | Entry: Absolute non-touch of 5 EMA. Exit: 20 EMA under-cut/over-cut. |
| Triple Confirmation | Trending | Intraday / Swing | 50 EMA, Supertrend (20,3), VWAP | High RRR (Trend Following) | When: Supertrend flips color and price is above/below 50 EMA. How: Price must also be near VWAP. | When: Supertrend signal reverses. How: SL at previous candle's low/high. | Entry: Supertrend, EMA, and VWAP must align in the same direction. |
| 50 EMA Reclaim | Trending | Daily | 50 EMA | 1:2 Minimum | When: Price crosses 50 EMA. How: Wait for 2 red candles (Long) or 2 green candles (Short) that don't touch 50 EMA. Enter when their high/low breaks. | How: SL at the 50 EMA or the range low/high of the 2-candle setup. | Entry: Price must reclaim 50 EMA, followed by a non-touching re-test range. |
| Inside Candle | Trending (Follow/Rev) | 15m-30m; 4h or Daily | Price Action (Mother & Child) | 1:2 to 1:3 (can reach 1:7+) | When: Small Child candle forms inside a large Mother candle. How: Enter when the Mother candle's high or low is broken. | How: SL at the Mother candle's opposite extreme (High for Short, Low for Long). | Entry: Consolidation (Inside Candle) followed by expansion break. |
| 12 PM Crypto | Trending (Intraday) | 30m | Price Action | 1:2 to 1:3 | When: Between 12:00 PM and 12:30 PM (IST). How: Mark the high/low of this candle. Enter long on high break and short on low break. | When: Profit target met or 2:00 PM adjustment. How: SL at the opposite side of the 12:00 PM candle. | Entry: Time-based price action break. Exit: Trail SL to cost if profitable by 2:00 PM. |
| Slow Stochastic | Trending (Swing) | Daily | Slow Stochastic (90/10), 20 or 50 EMA | 1:3 to 1:4 | When: Stochastic crosses above 10 (Long) or below 90 (Short). How: Price must be on the correct side of the EMA. | How: SL at previous candle's high/low. Exit: At major support/resistance or Stochastic reversal. | Entry: Stochastic reversal from extremes (10 or 90) with EMA trend confirmation. |

## Notes

- SL = Stop Loss
- EMA = Exponential Moving Average
- VWAP = Volume Weighted Average Price
- RRR = Risk-Reward Ratio
- Marubozu = Strong-bodied candle with little/no wicks
- These strategies are trend-following in nature and work best when combined with proper risk management and position sizing.