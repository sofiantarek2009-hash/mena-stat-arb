import backtrader as bt
import yfinance as yf
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

class StatArbStrategy(bt.Strategy):
    params = (('period', 20), ('dev', 2.0),)

    def __init__(self):
        # The mathematical core: Bollinger Bands for Z-Score proxy
        self.bb = bt.indicators.BollingerBands(self.data.close, 
                                               period=self.p.period, 
                                               devfactor=self.p.dev)

    def next(self):
        if not self.position:  # No active trades
            if self.data.close[0] < self.bb.lines.bot[0]:
                self.buy() # Asset is mathematically oversold (Z < -2)
        else:
            if self.data.close[0] > self.bb.lines.mid[0]:
                self.close() # Reversion to the mean achieved; take profit

def run_backtest(ticker, start, end):
    print(f"[*] INITIALIZING BACKTEST ENGINE: Target Asset [{ticker}]")
    cerebro = bt.Cerebro()
    
    # 1. Ingest Clean Data
    data = bt.feeds.PandasData(dataname=yf.download(ticker, start, end, progress=False))
    cerebro.adddata(data)
    
    # 2. Load the Math
    cerebro.addstrategy(StatArbStrategy)
    
    # 3. Institutional Parameters (USD)
    starting_capital = 10000.0
    cerebro.broker.setcash(starting_capital)
    cerebro.broker.setcommission(commission=0.001) # 0.1% simulated friction/slippage

    print(f'[*] Starting Capital: ${cerebro.broker.getvalue():.2f} USD')
    cerebro.run()
    
    final_capital = cerebro.broker.getvalue()
    roi = ((final_capital - starting_capital) / starting_capital) * 100
    
    print(f'[*] Final Capital: ${final_capital:.2f} USD')
    print(f'[*] Net ROI: {roi:.2f}% (After Friction)')
    
    # Render the proof
    cerebro.plot()

if __name__ == "__main__":
    # Target: VanEck Egypt Index ETF (NYSE)
    run_backtest("EGPT", "2022-01-01", "2024-01-01")
