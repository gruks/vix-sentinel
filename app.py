"""
VIX Sentinel - AI Market Risk Early Warning System
Main Streamlit application entry point
"""
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="VIX Sentinel",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Auto-refresh setup - triggers every 15 minutes (900 seconds = 15*60*1000 ms)
st_autorefresh(interval=15*60*1000, limit=None, key="dashboard_refresh")

# ==================== SIDEBAR CONFIGURATION ====================
st.sidebar.title("Configuration")

# Ticker multiselect
available_tickers = ["SPY", "VIX", "QQQ", "IWM", "AAPL", "TSLA", "MSFT", "NVDA", "AMD", "META"]
default_tickers = ["SPY", "VIX", "QQQ", "IWM"]
selected_tickers = st.sidebar.multiselect(
    "Select Tickers",
    available_tickers,
    default_tickers
)

# Time range selector
time_range = st.sidebar.radio(
    "Time Range",
    ["1d", "7d", "30d"],
    horizontal=True
)

# Manual refresh button
if st.sidebar.button("Refresh Now"):
    st.cache_data.clear()
    st.rerun()

# Display configuration summary
st.sidebar.markdown("---")
st.sidebar.markdown("### Configuration Summary")
if selected_tickers:
    st.sidebar.markdown(f"**Tickers:** {', '.join(selected_tickers)}")
else:
    st.sidebar.markdown("**Tickers:** None selected")
st.sidebar.markdown(f"**Time Range:** {time_range}")
st.sidebar.markdown(f"**Auto-refresh:** Every 15 minutes")

st.sidebar.markdown("---")
st.sidebar.markdown("### Data Sources")
st.sidebar.markdown("- SPY (S&P 500 ETF)")
st.sidebar.markdown("- VIX (Volatility Index)")
st.sidebar.markdown("- QQQ (Nasdaq-100)")
st.sidebar.markdown("- IWM (Russell 2000)")
st.sidebar.markdown("- Google News RSS")
st.sidebar.markdown("- TechCrunch RSS")
st.sidebar.markdown("- Hacker News API")


# ==================== DATA LOADING FUNCTIONS ====================

@st.cache_data(ttl=900, show_spinner=False)
def load_market_data(tickers, time_range):
    """Load current market data and historical data for selected tickers."""
    from src.data_fetcher import fetch_market_data, fetch_historical_data
    
    current = fetch_market_data(tickers)
    historical = {}
    for t in tickers:
        historical[t] = fetch_historical_data(t, time_range)
    return current, historical


@st.cache_data(ttl=900, show_spinner=False)
def load_news_and_sentiment(tickers):
    """Load news and calculate sentiment scores for selected tickers."""
    from src.news_fetcher import fetch_all_news
    from src.sentiment.scorer import get_sentiment_scores
    
    news = fetch_all_news(tickers)
    sentiment = get_sentiment_scores(news)
    return news, sentiment


@st.cache_data(ttl=900, show_spinner=False)
def calculate_risk_metrics(market_data, sentiment_data, tickers):
    """Calculate risk metrics for each ticker."""
    from src.risk_calculator import get_all_metrics, calculate_volatility_zscore
    
    results = {}
    for ticker in tickers:
        vol = market_data.get(ticker, {}).get('volatility', 0.15)
        # Create mock historical volatility data
        hist_vols = [vol * 0.8, vol * 0.9, vol, vol * 1.1, vol * 1.2]
        vol_z = calculate_volatility_zscore(vol, hist_vols)
        sent = sentiment_data.get(ticker, 0.5)
        metrics = get_all_metrics(vol, hist_vols, sent)
        results[ticker] = metrics
    return results


# ==================== MAIN DASHBOARD UI ====================

# Header
st.title("📈 AI Market Risk Early Warning System")
st.markdown("### Real-time market monitoring with sentiment analysis")

# Load data using cached functions
market_data, historical = load_market_data(selected_tickers, time_range)
news, sentiment = load_news_and_sentiment(selected_tickers)
risk_metrics = calculate_risk_metrics(market_data, sentiment, selected_tickers)

# Calculate aggregate values
if risk_metrics:
    avg_risk = sum(m['risk_score'] for m in risk_metrics.values()) / len(risk_metrics)
    avg_vol = sum(m['vol_zscore'] for m in risk_metrics.values()) / len(risk_metrics)
    avg_sent = sum(m['normalized_sentiment'] for m in risk_metrics.values()) / len(risk_metrics)
else:
    avg_risk = 0
    avg_vol = 0
    avg_sent = 0.5

# Render risk alert banner
from src.charts import create_risk_banner
from src.risk_calculator import get_risk_level

level, color, alert_type = get_risk_level(avg_risk)
banner = create_risk_banner(level, alert_type)

if alert_type == "success":
    st.success(f"{banner['icon']} {banner['message']}")
elif alert_type == "warning":
    st.warning(f"{banner['icon']} {banner['message']}")
else:
    st.error(f"{banner['icon']} {banner['message']}")

# Render 3 gauges row
from src.charts import create_three_gauges

gauges = create_three_gauges(avg_vol * 50, avg_sent * 100, avg_risk)
col1, col2, col3 = st.columns(3)
col1.plotly_chart(gauges[0], use_container_width=True)
col2.plotly_chart(gauges[1], use_container_width=True)
col3.plotly_chart(gauges[2], use_container_width=True)

# Render candlestick chart (7-day SPY)
st.subheader("📊 Market Trend")
if 'SPY' in historical and not historical['SPY'].empty:
    from src.charts import create_candlestick
    st.plotly_chart(create_candlestick(historical['SPY']), use_container_width=True)
else:
    st.info("No historical data available for SPY")

# Render sentiment trend line
st.subheader("📈 Sentiment Trend")
mock_dates = pd.date_range(end=pd.Timestamp.today(), periods=7, freq='D')
mock_sentiment = [0.5 + (i * 0.05) for i in range(7)]  # Mock data
from src.charts import create_sentiment_line
st.plotly_chart(
    create_sentiment_line(
        [d.strftime('%Y-%m-%d') for d in mock_dates],
        mock_sentiment
    ),
    use_container_width=True
)

# Render volatility heatmap
st.subheader("🔥 Volatility Heatmap")
vol_data = {}
for ticker in selected_tickers:
    if ticker in historical and not historical[ticker].empty:
        close_prices = historical[ticker]['Close'] if 'Close' in historical[ticker].columns else historical[ticker].iloc[:, -1]
        vol_data[ticker] = close_prices.pct_change().std()
    else:
        vol_data[ticker] = 0.0

if vol_data:
    vol_df = pd.DataFrame.from_dict(vol_data, orient='index', columns=['Volatility'])
    st.dataframe(vol_df, use_container_width=True)
else:
    st.info("No volatility data available")

# Render details table
st.subheader("📋 Per-Ticker Risk Details")
if risk_metrics:
    details_df = pd.DataFrame.from_dict(risk_metrics, orient='index')
    details_df = details_df[['vol_zscore', 'normalized_sentiment', 'risk_score', 'level', 'color']]
    st.dataframe(details_df, use_container_width=True)
else:
    st.info("No risk metrics available")

# Footer
st.markdown("---")
st.markdown("*Dashboard auto-refreshes every 15 minutes. Click 'Refresh Now' in sidebar to manually reload.*")

if __name__ == "__main__":
    st.run()
