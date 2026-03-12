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
- [x] 01-02-PLAN.md — Wire data pipeline to dashboard (gap closure)

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
- [x] 02-01-PLAN.md — Create sentiment module (analyzer.py, scorer.py)

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

**Plans:** 3 plans

**Plan list:**
- [x] 03-01-PLAN.md — Risk Calculator (volatility Z-score, combined risk, thresholds)
- [x] 03-02-PLAN.md — Charts Module (gauges, candlestick, trend lines, heatmap)
- [x] 03-03-PLAN.md — Dashboard Integration (sidebar, refresh, final integration)

---

## Phase 4: Alerts & Deployment

**Goal:** Complete with email alerts and Streamlit Cloud deployment
**Status:** ✓ Complete (2026-03-11)

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

**Plans:** 3 plans ✓ Complete

**Plan list:**
- [x] 04-01-PLAN.md — Email alert module and .env.example
- [x] 04-02-PLAN.md — Dashboard integration with sidebar toggle
- [x] 04-03-PLAN.md — Requirements.txt and deployment documentation

---

## Phase 5: Frontend UI/UX Integration

**Goal:** Replace Streamlit UI with React/MUI frontend for better UX and control

### Requirements (8)

| ID | Requirement |
|----|-------------|
| FE-01 | Create FastAPI backend to expose market risk data as REST API |
| FE-02 | Integrate React frontend with backend API endpoints |
| FE-03 | Implement skeleton loading states for async data |
| FE-04 | Build risk gauge component with color thresholds |
| FE-05 | Create market trend candlestick chart component |
| FE-06 | Build news sentiment display with sentiment indicators |
| FE-07 | Implement responsive layout for mobile/tablet |
| FE-08 | Add auto-refresh with loading states |

### Success Criteria

1. **API responds:** Frontend fetches and displays risk data from backend
2. **Skeletons show:** Loading states display while data fetches
3. **Risk gauge works:** Risk score 0-100 displays with color coding
4. **Charts render:** Candlestick and trend charts display market data
5. **Responsive:** Layout adapts to mobile, tablet, and desktop
6. **Auto-refresh:** Data updates every 15 minutes with visual indicator

**Plans:** 3 plans

**Plan list:**
- [x] 05-01-PLAN.md — FastAPI backend for market risk data
- [x] 05-02-PLAN.md — React frontend integration with API
- [x] 05-03-PLAN.md — UI enhancements (skeletons, charts, responsive)

---

## Coverage

| Phase | Requirements | Coverage |
|-------|--------------|----------|
| Phase 1 | DATA-01 to DATA-06 | 6/33 |
| Phase 2 | SENT-01 to SENT-04 | 4/33 |
| Phase 3 | RISK-01 to RISK-04, UI-01 to UI-07, CFG-01 to CFG-05 | 16/33 |
| Phase 4 | ALRT-01 to ALRT-03, DEPL-01 to DEPL-04 | 7/33 |
| Phase 5 | FE-01 to FE-08 | 8/33 |

**Total:** 41/41 requirements mapped ✓

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
