# Technology Stack

**Project:** AI Market Risk Early Warning System
**Researched:** March 8, 2026
**Research Mode:** Stack dimension for market risk dashboard with sentiment analysis

## Recommended Stack

### Core Framework

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **Python** | 3.10+ | Core language | Required by Streamlit 1.55+ and transformers 5.x. Python 3.10+ is the minimum supported version for modern data science libraries. |
| **Streamlit** | 1.55.0 | Web dashboard framework | Industry standard for rapid data app prototyping. Native support for Plotly charts, auto-refresh, and Streamlit Cloud deployment. Supports Python 3.10+. |
| **pandas** | Latest | Data manipulation | Essential for time-series data from yfinance and structured news data. Industry standard for financial data wrangling. |
| **NumPy** | Latest | Numerical computing | Required dependency for pandas and financial calculations (volatility, moving averages). |

### Market Data & Data Fetching

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **yfinance** | 1.2.0 | S&P 500 market data | **De facto standard** for free market data in Python. Actively maintained (Feb 2026 release). Provides real-time-ish data, historical prices, options, and fundamentals. Use `^VIX` for VIX data. |
| **feedparser** | 6.0.x | RSS feed parsing | Mature, well-maintained library for parsing RSS/Atom feeds. Standard choice for news aggregation since 2010. Supports all common feed formats. |
| **requests** | Latest | HTTP requests | Required for Hacker News API calls and fetching RSS feed content. Lightweight and reliable. |

### AI / Sentiment Analysis

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **transformers** | 5.3.0 | Model loading/inference | The Hugging Face library. Required for FinBERT. Actively maintained with 1M+ model checkpoints. Python 3.10+ required. |
| **PyTorch** | Latest (2.4+) | ML framework | Required by transformers for model inference. CUDA support for GPU acceleration if available. |
| **FinBERT** (ProsusAI/finbert) | Latest from Hugging Face | Financial sentiment analysis | **Industry standard** for financial text sentiment. Pre-trained on Financial PhraseBank + Reuters financial corpus. Outperforms general-purpose models on financial text. Returns positive/negative/neutral with confidence scores. |

### Visualization

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **Plotly** | 6.6.0 | Interactive charts | **Best choice for Streamlit integration**. Native Streamlit support via `st.plotly_chart`. Supports candlestick, line charts, heatmaps. Active development (Mar 2026 release). |
| **kaleido** | Latest | Static image export | Required for Plotly static image generation. Needed if you want to export charts as PNG/SVG. |

### Deployment

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **Streamlit Cloud** | Cloud service | Deployment platform | Free hosting for Streamlit apps from GitHub. Zero-config deployment. Natural fit for the project. Supports environment variables for API keys. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| **hnconnector** | Latest | Hacker News API wrapper | Optional. Provides Pythonic interface to HN Firebase API. Alternative: direct HTTP requests toHN API endpoints. |
| **ta** (Technical Analysis) | Latest | Financial indicators | For calculating RSI, MACD, Bollinger Bands if you want technical indicators beyond basic volatility. |
| **python-dateutil** | Latest | Date parsing | Needed for feedparser date normalization. |
| **lxml** | Latest | XML parsing | Faster XML parsing for RSS feeds. feedparser uses it automatically if installed. |

## Alternatives Considered

| Category | Recommended | Alternative | Why Not |
|----------|-------------|-------------|---------|
| Market Data | yfinance | Alpha Vantage | Alpha Vantage requires API key and has rate limits. yfinance is free and sufficient for S&P 500/VIX. |
| Market Data | yfinance | Yahoo Finance API (official) | Yahoo discontinued official API. yfinance is the maintained unofficial wrapper. |
| Sentiment | FinBERT | VADER (NLTK) | VADER is for social media sentiment, not financial text. FinBERT is specifically trained on financial corpus. |
| Sentiment | FinBERT | GPT API | Overkill for simple sentiment classification. Higher cost, latency. FinBERT runs locally with predictable performance. |
| Visualization | Plotly | Matplotlib | Matplotlib is static. Plotly provides interactive charts essential for dashboard exploration. |
| Visualization | Plotly | Altair | Less financial chart support than Plotly. Plotly has native candlestick, treemap, etc. |
| Dashboard | Streamlit | Dash (Plotly) | Dash has steeper learning curve. Streamlit is faster to prototype. Streamlit Cloud deployment is simpler. |
| Dashboard | Streamlit | Gradio | Gradio is optimized for ML model demos. Streamlit is better for general data dashboards. |
| RSS Parsing | feedparser | fastfeedparser | fastfeedparser is faster but feedparser is more widely used and battle-tested. For prototype, simplicity wins. |
| HN Data | hnconnector | Custom requests | hnconnector adds a dependency. HN API is simple enough to call directly with requests. |

## Installation

```bash
# Core dependencies
pip install streamlit==1.55.0
pip install yfinance==1.2.0
pip install pandas
pip install numpy

# Visualization
pip install plotly==6.6.0
pip install kaleido

# AI / Sentiment
pip install transformers==5.3.0
pip install torch

# Data fetching
pip install feedparser
pip install requests

# Optional
pip install hnconnector
pip install ta
```

## Project Structure

```
vix-sentinel/
├── app.py                  # Main Streamlit application
├── requirements.txt         # All dependencies
├── .streamlit/
│   └── config.toml         # Streamlit configuration
├── src/
│   ├── data/
│   │   ├── market_data.py  # yfinance wrappers
│   │   ├── news_fetcher.py # RSS + HN aggregation
│   │   └── sentiment.py   # FinBERT integration
│   ├── analysis/
│   │   └── risk_calculator.py  # Risk scoring logic
│   └── visualization/
│       └── charts.py       # Plotly chart builders
└── data/                   # Local cache if needed
```

## Key Design Decisions

### Why FinBERT for Sentiment?
FinBERT is specifically fine-tuned on financial text (Financial PhraseBank dataset) and achieves significantly better performance than general BERT models on financial news. It returns three labels (positive, negative, neutral) with confidence scores, which maps well to risk scoring.

### Why yfinance?
- **Free**: No API key required
- **Reliable**: Actively maintained (1.2.0 released Feb 2026)
- **Comprehensive**: VIX (^VIX), S&P 500 (^GSPC), individual stocks all available
- **Pythonic**: Clean API with pandas integration

### Why Streamlit + Plotly?
- Streamlit provides the fastest path from Python script to interactive web app
- Plotly charts render natively in Streamlit with no extra code
- Both have strong Streamlit Cloud support for deployment
- This combination dominates the Python data dashboard space in 2025-2026

### Why Not a Database?
For a 2-day prototype with real-time data fetching, in-memory data structures (pandas DataFrames) are sufficient. A database adds unnecessary complexity for the fast prototype phase.

## Sources

- **yfinance**: https://pypi.org/project/yfinance/ (v1.2.0, Feb 2026)
- **Streamlit**: https://pypi.org/project/streamlit/ (v1.55.0, Mar 2026)
- **Plotly**: https://pypi.org/project/plotly/ (v6.6.0, Mar 2026)
- **transformers**: https://pypi.org/project/transformers/ (v5.3.0, Mar 2026)
- **FinBERT (ProsusAI)**: https://huggingface.co/ProsusAI/finbert
- **feedparser**: https://feedparser.readthedocs.io/
- **Hacker News API**: https://github.com/HackerNews/API
- Streamlit financial dashboard examples: Multiple GitHub repositories using Streamlit + yfinance + Plotly pattern
