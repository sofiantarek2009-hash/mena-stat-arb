# mena-stat-arb
Statistical mean-reversion algorithm exploiting microstructural inefficiencies and emotional volatility in the Egyptian Exchange (EGX).
# MENA Statistical Arbitrage & Microstructural Inefficiency Engine

> **Focus:** Egyptian Exchange (EGX) | **Architecture:** Z-Score Mean-Reversion Pipeline

This repository serves as a quantitative research environment modeling the microstructural inefficiencies of Middle Eastern and North African (MENA) equity markets. 

Unlike hyper-efficient US markets, emerging markets exhibit extreme emotional volatility, lower liquidity, and information asymmetry. This engine tests the hypothesis that standard deviation expansion (Bollinger mechanics) in these specific markets creates highly predictable mean-reverting "snap-back" events.

## Mathematical Core
The pipeline utilizes a dynamic Z-Score thresholding model:
1. Calculates a rolling Simple Moving Average (SMA) baseline.
2. Derives rolling Standard Deviation ($\sigma$) bands to measure volatility.
3. Computes a real-time **Z-Score** ($Z = \frac{Price - SMA}{\sigma}$).
4. Flags statistical anomalies when $Z > 2.0$ or $Z < -2.0$.

*Architected by Sofian.*
