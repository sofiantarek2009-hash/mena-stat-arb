import backtrader as bt
import yfinance as yf
import pandas as pd

class StatArbStrategy(bt.Strategy):
    params = (('period', 20), ('dev', 2.0),)

    def __init__(self):
        # Using Bollinger Bands as a proxy for our Z-Score logic
        self.bb = bt.indicators.BollingerBands(self.data.close, 
                                               period=self.p.period, 
                                               devfactor=self.p.dev)

    def next(self):
        if not self.position:  # We are NOT in a trade
            if self.data.close[0] < self.bb.lines.bot[0]:
                self.buy() # Price is below bottom band (Z < -2)
        else:
            if self.data.close[0] > self.bb.lines.mid[0]:
                self.close() # Exit when price reverts to the mean (SMA)

def run_backtest(ticker, start, end):
    cerebro = bt.Cerebro()
    
    # 1. Add Data
    data = bt.feeds.PandasData(dataname=yf.download(ticker, start, end))
    cerebro.adddata(data)
    
    # 2. Add Strategy
    cerebro.addstrategy(StatArbStrategy)
    
    # 3. Set Initial Capital (EGP 100,000)
    cerebro.broker.setcash(100000.0)
    
    # 4. Set Commission (0.1% per trade - standard for EGX)
    cerebro.broker.setcommission(commission=0.001)

    print(f'[*] Starting Portfolio Value: {cerebro.broker.getvalue():.2f} EGP')
    cerebro.run()
    print(f'[*] Final Portfolio Value: {cerebro.broker.getvalue():.2f} EGP')
    
    # Plot the results
    cerebro.plot()

if __name__ == "__main__":
    run_backtest("COMI.CA", "2023-01-01", "2024-03-01")
