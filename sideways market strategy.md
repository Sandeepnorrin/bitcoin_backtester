# Additional Trading Strategies Reference

| Strategy Name | Market Type | Time Frames | Indicators Required | Risk-Reward Ratio (RRR) | Entry Rules (When & How) | Exit Rules (When & How) | Indicator Alignment for Entry/Exit |
|---------------|------------|------------|---------------------|-------------------------|--------------------------|-------------------------|------------------------------------|
| Triple Straddle | Sideways | Monthly | Option Straddles, Greeks | 60% of Premium Target | When: Start of the month (1st) or immediately after the previous expiry. How: Sell an ATM Call and ATM Put to create a wide trading range (e.g., ±18% from spot). | When: 60% premium decay achieved or price breaches the defined range. How: Adjust by adding up to 3 additional straddles if the range breaks. | Entry: Market-neutral setup with expectation of low volatility. Exit: Theta decay reaches the 60% premium target. |
| Funding Fee Strategy | Sideways / Range | Hourly / Daily | Supertrend, Funding Rates | ~18% to 50% Monthly ROI | When: Supertrend is negative (bearish trend). How: Short Futures and simultaneously Buy a Call Option as a hedge when the funding rate is positive. | When: Supertrend flips positive. How: Close all positions to avoid paying funding fees and preserve gains. | Entry: Negative trend (Supertrend) aligned with positive funding income opportunity. Exit: Trend reversal indicated by Supertrend turning positive. |

## Notes

- ATM = At-The-Money
- Greeks = Option risk measures (Delta, Gamma, Theta, Vega, Rho)
- Theta Decay = Reduction in option premium as time passes
- Funding Rate = Periodic payment exchanged between long and short futures traders in perpetual contracts
- Supertrend = Trend-following indicator based on ATR (Average True Range)
- The Triple Straddle strategy benefits from low volatility and time decay.
- The Funding Fee strategy aims to earn funding payments while maintaining directional hedge protection.