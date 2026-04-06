import yfinance as yf
import pandas as pd
import numpy as np
import warnings

# Suppress warnings for clean terminal output
warnings.filterwarnings('ignore')

class EmergingMarketStatArb:
    """
    Mathematical engine for calculating Mean-Reversion Standard Deviation Bands
    tailored for emerging market equities (EGX).
    """
    def __init__(self, ticker: str, window: int = 20, z_threshold: float = 2.0):
        self.ticker = ticker
        self.window = window
        self.z_threshold = z_threshold
        self.data = pd.DataFrame()

    def load_data(self, start_date: str, end_date: str):
        print(f"[*] INGESTING DATA: {self.ticker} [{start_date} -> {end_date}]")
        self.data = yf.download(self.ticker, start=start_date, end=end_date, progress=False)
        
        if self.data.empty:
            raise ValueError(f"[!] FAILED: No data found for {self.ticker}.")
            
        # Sanitize EM data gaps using modern Pandas syntax
        self.data.ffill(inplace=True)
        self.data.dropna(inplace=True)
        print(f"[*] DATA SECURE: {len(self.data)} trading days loaded.")

    def compute_vectors(self):
        print(f"[*] COMPUTING VECTORS (Window: {self.window}, Z-Limit: {self.z_threshold})...")
        
        # 1. The Mean
        self.data['SMA'] = self.data['Close'].rolling(window=self.window).mean()
        
        # 2. The Volatility
        self.data['StdDev'] = self.data['Close'].rolling(window=self.window).std()
        
        # 3. The Anomaly Detector (Z-Score)
        self.data['Z_Score'] = (self.data['Close'] - self.data['SMA']) / self.data['StdDev']
        
        # 4. Generate the Mathematical Signals
        self.data['Signal'] = 0 
        self.data.loc[self.data['Z_Score'] < -self.z_threshold, 'Signal'] = 1  # Mathematically Oversold (Buy)
        self.data.loc[self.data['Z_Score'] > self.z_threshold, 'Signal'] = -1 # Mathematically Overbought (Sell)
        
        self.data.dropna(inplace=True)

    def output_anomalies(self):
        trades = self.data[self.data['Signal'] != 0]
        
        print("\n" + "="*55)
        print(" AEGIS LABS: STATISTICAL ANOMALIES DETECTED ")
        print("="*55)
        
        if trades.empty:
            print("[-] No deviations exceeded the threshold.")
        else:
            # Show the exact moments the market broke the math
            print(trades[['Close', 'SMA', 'Z_Score', 'Signal']].tail(10))
        print("="*55 + "\n")

if __name__ == "__main__":
    # Target: VanEck Egypt Index ETF (Proxy for EGX Volatility)
    target_asset = "EGPT"
    
    # Initialize the Engine
    bot = EmergingMarketStatArb(ticker=target_asset, window=20, z_threshold=2.0)
    bot.load_data(start_date="2022-01-01", end_date="2024-01-01")
    bot.compute_vectors()
    bot.output_anomalies()
