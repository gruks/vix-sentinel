"""
Market Data Fetcher Module
Fetches real-time market data using yfinance
"""
import pandas as pd
import yfinance as yf
import streamlit as st
from typing import Dict, List, Optional


@st.cache_data(ttl=900)  # Cache for 15 minutes
def fetch_market_data(tickers: List[str]) -> Dict:
    """
    Fetch market data for given tickers.
    
    Args:
        tickers: List of stock ticker symbols (e.g., ['SPY', 'VIX', 'AAPL'])
    
    Returns:
        Dictionary with ticker data: {ticker: {price, change_pct, volume, history_df}}
    """
    # Always include SPY and VIX
    all_tickers = list(set(['SPY', 'VIX'] + tickers))
    
    result = {}
    
    try:
        # Fetch data for all tickers at once
        data = yf.download(all_tickers, period="1d", progress=False)
        
        for ticker in all_tickers:
            try:
                if ticker in data.columns.get_level_values(0):
                    ticker_data = data[ticker]
                    
                    # Get the latest price
                    if len(ticker_data) > 0:
                        latest = ticker_data.iloc[-1]
                        
                        # Calculate change percentage
                        prev_close = latest.get('Close')
                        if pd.notna(prev_close) and prev_close > 0:
                            current_close = latest.get('Open', prev_close)
                            if pd.notna(current_close):
                                change_pct = ((current_close - prev_close) / prev_close) * 100
                            else:
                                change_pct = 0
                        else:
                            change_pct = 0
                        
                        result[ticker] = {
                            'price': float(latest.get('Close', 0)) if pd.notna(latest.get('Close')) else 0,
                            'change_pct': round(change_pct, 2),
                            'volume': int(latest.get('Volume', 0)) if pd.notna(latest.get('Volume')) else 0,
                            'history_df': ticker_data
                        }
                    else:
                        result[ticker] = {
                            'price': 0,
                            'change_pct': 0,
                            'volume': 0,
                            'history_df': pd.DataFrame()
                        }
                else:
                    result[ticker] = {
                        'price': 0,
                        'change_pct': 0,
                        'volume': 0,
                        'history_df': pd.DataFrame()
                    }
            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")
                result[ticker] = {
                    'price': 0,
                    'change_pct': 0,
                    'volume': 0,
                    'history_df': pd.DataFrame()
                }
    except Exception as e:
        print(f"Error fetching market data: {e}")
        # Return empty result on failure
        for ticker in all_tickers:
            result[ticker] = {
                'price': 0,
                'change_pct': 0,
                'volume': 0,
                'history_df': pd.DataFrame()
            }
    
    return result


def calculate_volatility(prices: pd.DataFrame, period: int = 20) -> Optional[float]:
    """
    Calculate rolling volatility (standard deviation of returns).
    
    Args:
        prices: DataFrame with price data
        period: Rolling window period (default 20 days)
    
    Returns:
        Annualized volatility as percentage, or None on failure
    """
    if prices is None or prices.empty:
        return None
    
    try:
        # Get closing prices
        if 'Close' in prices.columns:
            close_prices = prices['Close']
        elif len(prices.columns) > 0:
            close_prices = prices.iloc[:, 0]  # Use first column
        else:
            return None
        
        # Calculate daily returns
        returns = close_prices.pct_change().dropna()
        
        if len(returns) < 2:
            return None
        
        # Calculate rolling standard deviation
        rolling_std = returns.rolling(window=min(period, len(returns))).std()
        
        if rolling_std.empty or pd.isna(rolling_std.iloc[-1]):
            return None
        
        # Annualize the volatility (252 trading days)
        annualized_vol = rolling_std.iloc[-1] * (252 ** 0.5) * 100
        
        return round(annualized_vol, 2)
    except Exception as e:
        print(f"Error calculating volatility: {e}")
        return None


def fetch_historical_data(ticker: str, period: str = "7d") -> pd.DataFrame:
    """
    Fetch historical data for a ticker.
    
    Args:
        ticker: Stock ticker symbol
        period: Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 5y, max)
    
    Returns:
        DataFrame with historical price data
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        return hist
    except Exception as e:
        print(f"Error fetching historical data for {ticker}: {e}")
        return pd.DataFrame()
