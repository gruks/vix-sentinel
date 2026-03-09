# Roadmap: AI Market Risk Early Warning System

**Created:** 2026-03-08
**Depth:** Quick (3-5 phases)
**Total Requirements:** 33 v1

## Overview

A real-time market risk monitoring dashboard that detects potential market crashes using news sentiment analysis (FinBERT) combined with market volatility indicators (VIX, SPY). Delivers a clear Risk Score (0-100) with actionable alerts.

---

## Phase 1: Data Pipeline Foundation

**Goal:** Fetch and aggregate all market data and news sources

### Requirements (6)

| ID | Requirement |
|----|-------------|
| DATA-01 | Fetch real-time market data using yfinance (SPY, VIX) |
| DATA-02 | Calculate market volatility (rolling standard deviation of returns) |
| DATA-03 | Parse Google News RSS feeds for stock-related headlines |
| DATA-04 | Parse TechCrunch RSS feed for tech sector news |
| DATA-05 | Fetch top stories from Hacker News API |
| DATA-06 | Cache news data to avoid rate limiting |

### Success Criteria

1. **Market data loads:** User sees live SPY and VIX prices displayed in dashboard
2. **Volatility calculated:** Rolling volatility metric shows in UI
3. **News aggregated:** All three sources (Google News, TechCrunch, HN) display headlines
4. **No rate limit errors:** Caching prevents HN API rate limiting during 15-min refresh cycles

**Plans:** 2 plans

**Plan list:**
- [x] 01-01-PLAN.md — Create data pipeline modules (data_fetcher, news_fetcher, cache)
- [ ] 01-02-PLAN.md — Wire data pipeline to dashboard (gap closure)

---

## Phase 2: Sentiment Analysis Integration

**Goal:** Analyze news sentiment using FinBERT

### Requirements (4)

| ID | Requirement |
|----|-------------|
| SENT-01 | Load FinBERT model for financial sentiment analysis |
| SENT-02 | Analyze individual headlines for sentiment (positive/negative/neutral) |
| SENT-03 | Calculate average sentiment score across all news sources |
| SENT-04 | Map sentiment to risk contribution (negative sentiment = higher risk) |

### Success Criteria

1. **Model loads:** FinBERT initializes without errors on first run
2. **Headlines scored:** Each headline shows sentiment label (positive/negative/neutral)
3. **Aggregate score:** Average sentiment displays as percentage or -1 to 1 score
4. **Risk mapping works:** Negative news correctly contributes to higher risk score

**Plans:** 1 plan

**Plan list:**
- [ ] 02-01-PLAN.md — Create sentiment module (analyzer.py, scorer.py)

---

## Phase 3: Risk Calculation & Dashboard UI

**Goal:** Display interactive risk dashboard with all visualizations

### Requirements (16)

| ID | Requirement |
|----|-------------|
| RISK-01 | Calculate volatility Z-score (normalized against historical mean) |
| RISK-02 | Compute combined risk score using formula: `risk = 0.6 * vol_z + 0.4 * (1 - sentiment)` |
| RISK-03 | Apply thresholds: LOW (<40), MEDIUM (40-75), HIGH (>75) |
| RISK-04 | Determine alert level color (GREEN, YELLOW, RED) |
| UI-01 | Display main metrics row with 3 Plotly gauges (volatility, sentiment, risk) |
| UI-02 | Show conditional risk alert banner (error/warning/success based on level) |
| UI-03 | Render market trend candlestick chart (7-day SPY data) |
| UI-04 | Render news sentiment trend line chart (7-day rolling average) |
| UI-05 | Render risk gauge evolution (hourly risk score for 24h) |
| UI-06 | Render volatility heatmap (tickers x days) |
| UI-07 | Display details table with per-ticker breakdown |
| CFG-01 | Sidebar with ticker selection (add/remove tickers) |
| CFG-02 | Time range selector (1d/7d/30d) |
| CFG-03 | Auto-refresh every 15 minutes using schedule library |
| CFG-04 | Manual refresh button |
| CFG-05 | Cache data using st.cache_data (TTL=900s) |

### Success Criteria

1. **Risk score displays:** User sees Risk Score 0-100 with clear threshold coloring
2. **Three gauges work:** Volatility, Sentiment, and Risk gauges render correctly
3. **Alert banner shows:** Banner changes color based on LOW/MEDIUM/HIGH status
4. **Candlestick chart:** SPY 7-day candlestick chart renders with proper OHLC data
5. **Sentiment trend line:** 7-day rolling sentiment chart displays
6. **Risk evolution:** 24-hour risk history chart shows
7. **Volatility heatmap:** Tickers-by-days heatmap renders
8. **Ticker config works:** User can add/remove tickers in sidebar
9. **Auto-refresh works:** Page refreshes every 15 minutes automatically

---

## Phase 4: Alerts & Deployment

**Goal:** Complete with email alerts and Streamlit Cloud deployment

### Requirements (7)

| ID | Requirement |
|----|-------------|
| ALRT-01 | Email alert when risk score exceeds HIGH threshold (>75) |
| ALRT-02 | Configure email via environment variables |
| ALRT-03 | Toggle email alerts on/off in sidebar |
| DEPL-01 | Create requirements.txt with all dependencies |
| DEPL-02 | Create .env.example for configuration |
| DEPL-03 | Deploy to Streamlit Cloud from GitHub |
| DEPL-04 | Configure auto-refresh in deployed app |

### Success Criteria

1. **Email sends:** When risk exceeds 75, test email is sent successfully
2. **Toggle works:** User can enable/disable email alerts via sidebar
3. **requirements.txt exists:** All dependencies listed with versions
4. **.env.example exists:** Template shows required environment variables
5. **App deployed:** Live URL accessible on Streamlit Cloud
6. **Auto-refresh active:** Deployed app refreshes every 15 minutes

---

## Coverage

| Phase | Requirements | Coverage |
|-------|--------------|----------|
| Phase 1 | DATA-01 to DATA-06 | 6/33 |
| Phase 2 | SENT-01 to SENT-04 | 4/33 |
| Phase 3 | RISK-01 to RISK-04, UI-01 to UI-07, CFG-01 to CFG-05 | 16/33 |
| Phase 4 | ALRT-01 to ALRT-03, DEPL-01 to DEPL-04 | 7/33 |

**Total:** 33/33 requirements mapped ✓

---

## Phase Dependencies

```
Phase 1 (Data) ──────┐
                     ├──► Phase 3 (Risk & UI) ──► Phase 4 (Alerts & Deploy)
Phase 2 (Sentiment) ─┘
```

**Key dependencies:**
- Phase 1 must complete before Phases 2-3 can verify data flows
- Phase 2 must complete before Phase 3 can calculate combined risk
- Phase 3 must complete before Phase 4 deployment is meaningful
