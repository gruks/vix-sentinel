# AI Market Risk Early Warning System

## What This Is

A real-time market risk monitoring dashboard that detects potential market crashes using news sentiment analysis combined with market volatility indicators. Mimics internal bank risk monitoring tools used by financial institutions. Targets fintech/data science roles on resume.

## Core Value

Predict market instability before it happens — provide a clear Risk Score (0-100) with actionable alerts so users can make informed trading decisions.

## Requirements

### Active

- [ ] Real-time market data fetching (S&P 500 proxy: SPY)
- [ ] News sentiment analysis using FinBERT (HuggingFace)
- [ ] Multi-source news aggregation (Google News RSS + TechCrunch RSS + Hacker News API)
- [ ] Risk score calculation algorithm
- [ ] Color-coded alerts (LOW/GREEN, MEDIUM/YELLOW, HIGH/RED)
- [ ] Interactive Streamlit dashboard with Plotly visualizations
- [ ] Live market trend charts (candlestick)
- [ ] News sentiment trend charts (line graphs)
- [ ] Risk gauge with historical evolution
- [ ] Volatility heatmap visualization
- [ ] Email alerts for HIGH risk (>75)
- [ ] Auto-refresh every 15 minutes
- [ ] Deployment to Streamlit Cloud

## Context

**Project Type:** Greenfield - building from scratch

**Timeline:** 2 days (fast prototype)

**Resume Value:** High - demonstrates:
- Full-stack Python skills
- AI/ML integration (HuggingFace FinBERT)
- Real-time data processing
- Professional dashboard design
- Cloud deployment

**Technical Environment:**
- Backend: Python 3.11
- Data: yfinance, pandas, feedparser
- AI: Transformers (FinBERT)
- Frontend: Streamlit, Plotly
- Deployment: Streamlit Cloud

## Constraints

- **Timeline:** 2 days maximum — MVP only
- **Budget:** Free tier only (no paid APIs)
- **Data Sources:** Must use free sources (RSS feeds, Hacker News API)
- **Deployment:** Streamlit Cloud (free)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use RSS + HN API instead of NewsAPI | Free, no API key needed, shows resourcefulness | — Pending |
| Use FinBERT for sentiment | Finance-specific model, better accuracy than generic | — Pending |
| Streamlit for UI | Fastest to build, professional look, easy deployment | — Pending |
| Risk formula: 0.6*volatility + 0.4*(1-sentiment) | Simple but effective, matches bank-style scoring | — Pending |

---

*Last updated: 2026-03-08 after project initialization*
