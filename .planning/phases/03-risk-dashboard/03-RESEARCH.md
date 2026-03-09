# Phase 3: Risk Calculation & Dashboard UI - Research

**Researched:** 2026-03-09
**Domain:** Financial Dashboard / Risk Visualization
**Confidence:** HIGH

## Summary

This phase implements the interactive risk dashboard combining market data (from Phase 1) and sentiment analysis (from Phase 2). The core challenge is calculating a unified risk score using volatility Z-scores and sentiment data, then visualizing it through Plotly gauges, candlestick charts, line charts, heatmaps, and a details table within a Streamlit UI.

**Primary recommendation:** Use `streamlit-autorefresh` for 15-minute auto-refresh combined with `st.cache_data(ttl=900)` for data caching. Implement risk calculation as a pure function that accepts volatility and sentiment inputs, producing normalized scores and alert levels. Use Plotly `go.Indicator` for gauges with custom color steps matching the LOW/MEDIUM/HIGH thresholds.

## User Constraints (from Phase Context)

> **Note:** No CONTEXT.md exists for this phase. This research covers the full domain based on the phase requirements.

### Prior Locked Decisions (from roadmap)
- Stack: Streamlit + yfinance + Plotly + FinBERT (LOCKED)
- Risk formula: `0.6 * vol_z + 0.4 * (1 - sentiment)` (LOCKED)
- Thresholds: LOW (<40), MEDIUM (40-75), HIGH (>75) (LOCKED)
- Streamlit for UI (LOCKED)
- Plotly for charts (LOCKED)
- st.cache_data with TTL=900s (LOCKED)

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| streamlit | 1.28+ | Web UI framework | Required by project |
| plotly | 5.x | Interactive charts | Required by project |
| yfinance | 0.2.x | Market data | Required by project |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| streamlit-autorefresh | 1.x | Auto-refresh timer | 15-minute refresh requirement |
| pandas | 2.x | Data manipulation | All data processing |
| numpy | 1.x | Numerical calculations | Z-score computation |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| streamlit-autorefresh | schedule + while loop | schedule blocks app execution; autorefresh is non-blocking |
| streamlit-autorefresh | st.fragment(run_every=) | st.fragment is experimental (Streamlit 1.28+), autorefresh is stable |
| Custom gauge | go.Indicator | Plotly's built-in gauge is well-tested and supports steps/thresholds |

**Installation:**
```bash
pip install streamlit plotly yfinance streamlit-autorefresh pandas numpy
```

## Architecture Patterns

### Recommended Project Structure
```
src/
├── risk_calculator.py    # Risk calculation logic
├── charts.py            # Plotly chart generators
└── dashboard.py         # Main Streamlit app

# app.py (root) - imports from src/
```

### Pattern 1: Risk Score Calculation
**What:** Pure function taking volatility and sentiment, returning normalized scores
**When to use:** Whenever risk needs to be computed from raw inputs
**Example:**
```python
# Source: Derived from requirements - standard statistical approach
import numpy as np

def calculate_volatility_zscore(current_vol: float, historical_vols: list) -> float:
    """Calculate Z-score normalized against historical mean."""
    if not historical_vols or len(historical_vols) < 2:
        return 0.0
    mean = np.mean(historical_vols)
    std = np.std(historical_vols)
    if std == 0:
        return 0.0
    return (current_vol - mean) / std

def calculate_risk_score(vol_zscore: float, sentiment: float) -> float:
    """Calculate combined risk score: 0.6*vol_z + 0.4*(1-sentiment)."""
    # sentiment is 0-1 (0=negative, 1=positive)
    # 1-sentiment inverts: 0(negative)=high risk, 1(positive)=low risk
    return 0.6 * vol_zscore + 0.4 * (1 - sentiment)

def get_risk_level(risk_score: float) -> tuple:
    """Determine risk level and color based on thresholds."""
    if risk_score < 40:
        return ("LOW", "GREEN", "success")
    elif risk_score <= 75:
        return ("MEDIUM", "YELLOW", "warning")
    else:
        return ("HIGH", "RED", "error")
```

### Pattern 2: Streamlit Cache with Auto-Refresh
**What:** Combine st.cache_data with streamlit-autorefresh component
**When to use:** Need periodic data refresh without blocking UI
**Example:**
```python
# Source: streamlit-autorefresh documentation + existing project patterns
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# At top of app, after st.set_page_config
count = st_autorefresh(
    interval=15 * 60 * 1000,  # 15 minutes in ms
    limit=None,  # infinite refresh
    key="dashboard_refresh"
)

@st.cache_data(ttl=900)  # 900 seconds = 15 minutes
def fetch_dashboard_data():
    """Fetch all data needed for dashboard."""
    # This will re-run only when cache expires or is cleared
    return data
```

### Pattern 3: Plotly Gauge with Threshold Steps
**What:** Create gauge with colored zones matching risk thresholds
**When to use:** Displaying volatility, sentiment, or risk metrics
**Example:**
```python
# Source: Plotly gauge charts documentation
import plotly.graph_objects as go

def create_gauge(value: float, title: str, thresholds: list = None) -> go.Figure:
    """Create gauge chart with LOW/MEDIUM/HIGH color zones."""
    if thresholds is None:
        thresholds = [
            {'range': [0, 40], 'color': '#4CAF50'},    # GREEN - LOW
            {'range': [40, 75], 'color': '#FFC107'},    # YELLOW - MEDIUM
            {'range': [75, 100], 'color': '#F44336'}    # RED - HIGH
        ]
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': thresholds,
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    return fig
```

### Pattern 4: Candlestick Chart for Market Data
**What:** Display OHLC data as candlestick chart
**When to use:** Showing 7-day SPY market trend
**Example:**
```python
# Source: Plotly candlestick documentation
import plotly.graph_objects as go

def create_candlestick(df) -> go.Figure:
    """Create candlestick chart from OHLC data."""
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        increasing_line_color='green',
        decreasing_line_color='red'
    )])
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        title="SPY 7-Day Market Trend"
    )
    return fig
```

### Pattern 5: Volatility Heatmap
**What:** Create 2D heatmap of volatility across tickers and days
**When to use:** Visualizing volatility patterns over time
**Example:**
```python
# Source: Plotly heatmap documentation
import plotly.graph_objects as go

def create_volatility_heatmap(data: dict, tickers: list, dates: list) -> go.Figure:
    """Create heatmap from ticker volatility data."""
    # data: {ticker: [vol_day1, vol_day2, ...]}
    z_data = [data[ticker] for ticker in tickers]
    
    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        x=dates,
        y=tickers,
        colorscale='RdYlGn_r'  # Red=high, Green=low
    ))
    fig.update_layout(title="Volatility Heatmap (Tickers x Days)")
    return fig
```

### Anti-Patterns to Avoid

- **Using schedule library with while loop:** Blocks Streamlit's event loop, makes UI unresponsive. Use streamlit-autorefresh instead.
  
- **Storing large DataFrames in st.session_state:** Can cause memory issues. Use st.cache_data with TTL instead.

- **Calculating risk inside display functions:** Risk calculation should be a pure function, testable independently from UI.

- **Hardcoding chart colors:** Use constants or theme-based colors so dashboard can be restyled easily.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Auto-refresh | Custom timer with JavaScript | streamlit-autorefresh | Handles browser tab inactive states, integrates with Streamlit lifecycle |
| Data caching | Manual pickle/memcached | st.cache_data | Native integration, TTL support, clears on code changes |
| Candlestick rendering | Custom SVG/Canvas | go.Candlestick | Built-in interactivity (zoom, hover), optimized rendering |
| Gauge visualization | Custom HTML/CSS gauges | go.Indicator | Supports steps/thresholds, tooltips, multiple modes |

**Key insight:** Streamlit + Plotly ecosystem has mature, well-tested solutions for all dashboard requirements. Custom implementations would lack interactivity and require maintenance.

## Common Pitfalls

### Pitfall 1: Cache TTL Mismatch with Refresh Interval
**What goes wrong:** Data refreshes on different schedules causing stale/fresh data mismatches
**Why it happens:** st.cache_data TTL and autorefresh interval not aligned
**How to avoid:** Set both to 900 seconds (15 minutes)
**Warning signs:** Charts showing different data timestamps

### Pitfall 2: Sentiment Scale Confusion
**What goes wrong:** Risk formula produces unexpected results due to sentiment scale confusion
**Why it happens:** Sentiment can be -1 to 1, 0 to 1, or 0-100 depending on implementation
**How to avoid:** Normalize sentiment to 0-1 scale before risk calculation, document assumptions
**Warning signs:** Risk scores > 100 or < 0, or consistently extreme values

### Pitfall 3: Volatility Z-Score Without Sufficient History
**What goes wrong:** Z-score unreliable with < 30 data points
**Why it happens:** Z-score requires statistical sample to be meaningful
**How to avoid:** Require minimum 20 days historical data, use rolling window, or fall back to raw volatility
**Warning signs:** Extreme Z-scores (>3 or <-3) on new data

### Pitfall 4: YFinance Rate Limiting
**What goes wrong:** Requests fail after too many rapid calls
**Why it happens:** Yahoo API throttling on excessive requests
**How to avoid:** Use st.cache_data with TTL, batch ticker requests together
**Warning signs:** Intermittent data fetch failures, empty DataFrames

### Pitfall 5: Plotly Figure Recreation on Every Rerun
**What goes wrong:** Dashboard feels slow due to chart regeneration
**Why it happens:** Chart creation not cached, happens on every Streamlit rerun
**How to avoid:** Cache chart creation functions or use st.plotly_chart with key
**Warning signs:** Slow dashboard after interacting with sidebar controls

## Code Examples

### Example: Full Dashboard Data Loading Pattern
```python
# Source: Streamlit caching + existing project code
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd

# Auto-refresh setup (15 minutes)
st_autorefresh(
    interval=15 * 60 * 1000,
    limit=None,
    key="data_refresh"
)

@st.cache_data(ttl=900, show_spinner=False)
def load_market_data(tickers: list) -> dict:
    """Load market data with 15-minute cache."""
    from src.data_fetcher import fetch_market_data
    return fetch_market_data(tickers)

@st.cache_data(ttl=900, show_spinner=False)
def load_sentiment_data(tickers: list) -> dict:
    """Load sentiment data with 15-minute cache."""
    from src.sentiment import get_sentiment_scores
    return get_sentiment_scores(tickers)
```

### Example: Risk Level Banner
```python
# Source: Streamlit status elements
def render_risk_banner(risk_level: str, alert_type: str):
    """Render conditional alert banner based on risk level."""
    messages = {
        "LOW": "Market conditions appear stable. Risk levels are within normal range.",
        "MEDIUM": "Elevated volatility detected. Monitor positions closely.",
        "HIGH": "WARNING: High risk conditions. Consider defensive positioning."
    }
    
    st.alert(
        message=messages[risk_level],
        icon=alert_type  # "error", "warning", "success"
    )
```

### Example: Three-Column Gauge Layout
```python
# Source: Streamlit columns + Plotly
import streamlit as st
import plotly.graph_objects as go

col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(create_gauge(volatility, "Volatility"), use_container_width=True)

with col2:
    st.plotly_chart(create_gauge(sentiment * 100, "Sentiment"), use_container_width=True)

with col3:
    st.plotly_chart(create_gauge(risk_score, "Risk Score"), use_container_width=True)
```

### Example: Sidebar Ticker Selection
```python
# Source: Streamlit sidebar components
st.sidebar.title("Configuration")

# Ticker management
default_tickers = ["SPY", "VIX", "QQQ", "IWM"]
selected_tickers = st.sidebar.multiselect(
    "Select Tickers",
    options=["SPY", "VIX", "QQQ", "IWM", "AAPL", "TSLA", "MSFT", "NVDA", "AMD", "META"],
    default=default_tickers
)

# Time range selector
time_range = st.sidebar.radio(
    "Time Range",
    options=["1d", "7d", "30d"],
    horizontal=True
)

# Manual refresh
if st.sidebar.button("Refresh Now"):
    st.cache_data.clear()
    st.rerun()
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| st.experimental_rerun | st.rerun() | Streamlit 1.28+ | Cleaner API, no experimental prefix |
| @st.cache | @st.cache_data / @st.cache_resource | Streamlit 1.23+ | Better separation, TTL support |
| schedule library loop | streamlit-autorefresh | 2023 | Non-blocking refresh |
| st.empty() for updates | st.fragment with run_every | Streamlit 1.28+ | Partial page refresh (experimental) |

**Deprecated/outdated:**
- `st.experimental_rerun()` - Use `st.rerun()` (Streamlit 1.28+)
- `@st.cache` - Use `@st.cache_data` or `@st.cache_resource`
- `st.deprecated` - Various APIs deprecated in favor of new names

## Open Questions

1. **Sentiment Data Structure**
   - What we know: Phase 2 will provide sentiment scores, format to be determined
   - What's unclear: Exact sentiment scale (0-1, -1 to 1, 0-100?)
   - Recommendation: Document sentiment contract in Phase 2, implement normalization in Phase 3

2. **Historical Volatility Storage**
   - What we know: Need historical volatility for Z-score calculation
   - What's unclear: Where is historical data stored? How many days needed?
   - Recommendation: Store in `.cache/` directory, calculate rolling from available data

3. **Risk Score History**
   - What we know: Requirement shows "hourly risk score for 24h" visualization
   - What's unclear: Where does hourly historical risk data come from?
   - Recommendation: Store risk calculations in session state or `.cache/` for display

## Sources

### Primary (HIGH confidence)
- Plotly gauge charts documentation - https://plotly.com/python/gauge-charts/
- Plotly candlestick charts documentation - https://plotly.com/python/candlestick-charts/
- Streamlit st.cache_data - https://docs.streamlit.io/develop/api-reference/caching-and-state/st.cache_data
- streamlit-autorefresh component - https://github.com/kmcgrady/streamlit-autorefresh

### Secondary (MEDIUM confidence)
- Streamlit community discussion on auto-refresh patterns
- Existing project code (src/data_fetcher.py, src/news_fetcher.py)

### Tertiary (LOW confidence)
- Various tutorials on Streamlit + Plotly dashboards

## Metadata

**Confidence breakdown:**
- Standard Stack: HIGH - Streamlit/Plotly/yfinance are required by project, versions from existing codebase
- Architecture: HIGH - Patterns derived from official documentation and project requirements
- Pitfalls: HIGH - Common Streamlit/financial dashboard issues, verified by community discussions

**Research date:** 2026-03-09
**Valid until:** 30 days (stable stack) - Streamlit/Plotly APIs change infrequently
