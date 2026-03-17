"""
Market Data Fetcher Module
Fetches real-time market data using yfinance
"""
import pandas as pd
import yfinance as yf
from typing import Dict, List, Optional
from datetime import datetime, timedelta


# Mapping frontend time ranges to yfinance parameters
# yfinance supports: 1d, 5d, 7d, 60d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, max
# For non-standard ranges (2d, 10d, 30d), use start/end with interval
TIME_RANGE_MAP = {
    "1d": {"period": "1d", "interval": "5m"},
    "2d": {"start_days": 2, "interval": "15m"},
    "5d": {"period": "5d", "interval": "15m"},
    "7d": {"period": "5d", "interval": "15m"},  # yfinance doesn't have 7d
    "10d": {"start_days": 10, "interval": "1h"},
    "30d": {"start_days": 30, "interval": "1d"},
    "1mo": {"period": "1mo", "interval": "1d"},
    "3mo": {"period": "3mo", "interval": "1d"},
    "6mo": {"period": "6mo", "interval": "1d"},
    "1y": {"period": "1y", "interval": "1d"},
}


def _get_yfinance_params(time_range: str) -> dict:
    """Convert frontend time_range to yfinance parameters"""
    params = TIME_RANGE_MAP.get(time_range, TIME_RANGE_MAP["7d"])
    
    if "period" in params:
        return {"period": params["period"], "interval": params["interval"]}
    else:
        end = datetime.now()
        start = end - timedelta(days=params["start_days"])
        return {
            "start": start.strftime("%Y-%m-%d"),
            "end": end.strftime("%Y-%m-%d"),
            "interval": params["interval"]
        }


def fetch_market_data(tickers: List[str]) -> Dict:
    """
    Fetch market data for given tickers.
    
    Args:
        tickers: List of stock ticker symbols (e.g., ['SPY', 'VIX', 'AAPL'])
    
    Returns:
        Dictionary with ticker data: {ticker: {price, change_pct, volume, history_df}}
    """
    # Always include SPY and VIX (^VIX is the CBOE Volatility Index ticker)
    ticker_map = {'SPY': 'SPY', 'VIX': '^VIX'}
    # Use display names for the result, but actual yfinance symbols for fetching
    display_tickers = list(set(['SPY', 'VIX'] + tickers))
    all_tickers = [ticker_map.get(t, t) for t in display_tickers]
    
    result = {}
    
    try:
        # Fetch data for all tickers at once
        data = yf.download(all_tickers, period="1d", progress=False)
        
        for display_name, actual_ticker in zip(display_tickers, all_tickers):
            try:
                if actual_ticker in data.columns.get_level_values(0):
                    ticker_data = data[actual_ticker]
                    
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
                        
                        result[display_name] = {
                            'price': float(latest.get('Close', 0)) if pd.notna(latest.get('Close')) else 0,
                            'change_pct': round(change_pct, 2),
                            'volume': int(latest.get('Volume', 0)) if pd.notna(latest.get('Volume')) else 0,
                            'history_df': ticker_data
                        }
                    else:
                        result[display_name] = {
                            'price': 0,
                            'change_pct': 0,
                            'volume': 0,
                            'history_df': pd.DataFrame()
                        }
                else:
                    result[display_name] = {
                        'price': 0,
                        'change_pct': 0,
                        'volume': 0,
                        'history_df': pd.DataFrame()
                    }
            except Exception as e:
                print(f"Error fetching data for {actual_ticker}: {e}")
                result[display_name] = {
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
        period: Data period (1d, 2d, 5d, 7d, 10d, 30d, 1mo, 3mo, etc.)
    
    Returns:
        DataFrame with historical price data
    """
    try:
        stock = yf.Ticker(ticker)
        params = _get_yfinance_params(period)
        hist = stock.history(**params)
        return hist
    except Exception as e:
        print(f"Error fetching historical data for {ticker}: {e}")
        return pd.DataFrame()
