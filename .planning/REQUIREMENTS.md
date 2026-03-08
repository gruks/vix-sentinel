# Requirements: AI Market Risk Early Warning System

**Defined:** 2026-03-08
**Core Value:** Predict market instability before it happens with clear Risk Score (0-100) and actionable alerts

## v1 Requirements

### Data Pipeline

- [ ] **DATA-01**: Fetch real-time market data using yfinance (SPY, VIX)
- [ ] **DATA-02**: Calculate market volatility (rolling standard deviation of returns)
- [ ] **DATA-03**: Parse Google News RSS feeds for stock-related headlines
- [ ] **DATA-04**: Parse TechCrunch RSS feed for tech sector news
- [ ] **DATA-05**: Fetch top stories from Hacker News API
- [ ] **DATA-06**: Cache news data to avoid rate limiting

### Sentiment Analysis

- [ ] **SENT-01**: Load FinBERT model for financial sentiment analysis
- [ ] **SENT-02**: Analyze individual headlines for sentiment (positive/negative/neutral)
- [ ] **SENT-03**: Calculate average sentiment score across all news sources
- [ ] **SENT-04**: Map sentiment to risk contribution (negative sentiment = higher risk)

### Risk Calculation

- [ ] **RISK-01**: Calculate volatility Z-score (normalized against historical mean)
- [ ] **RISK-02**: Compute combined risk score using formula: `risk = 0.6 * vol_z + 0.4 * (1 - sentiment)`
- [ ] **RISK-03**: Apply thresholds: LOW (<40), MEDIUM (40-75), HIGH (>75)
- [ ] **RISK-04**: Determine alert level color (GREEN, YELLOW, RED)

### Dashboard UI

- [ ] **UI-01**: Display main metrics row with 3 Plotly gauges (volatility, sentiment, risk)
- [ ] **UI-02**: Show conditional risk alert banner (error/warning/success based on level)
- [ ] **UI-03**: Render market trend candlestick chart (7-day SPY data)
- [ ] **UI-04**: Render news sentiment trend line chart (7-day rolling average)
- [ ] **UI-05**: Render risk gauge evolution (hourly risk score for 24h)
- [ ] **UI-06**: Render volatility heatmap (tickers x days)
- [ ] **UI-07**: Display details table with per-ticker breakdown

### Configuration & Automation

- [ ] **CFG-01**: Sidebar with ticker selection (add/remove tickers)
- [ ] **CFG-02**: Time range selector (1d/7d/30d)
- [ ] **CFG-03**: Auto-refresh every 15 minutes using schedule library
- [ ] **CFG-04**: Manual refresh button
- [ ] **CFG-05**: Cache data using st.cache_data (TTL=900s)

### Alerts & Notifications

- [ ] **ALRT-01**: Email alert when risk score exceeds HIGH threshold (>75)
- [ ] **ALRT-02**: Configure email via environment variables
- [ ] **ALRT-03**: Toggle email alerts on/off in sidebar

### Deployment

- [ ] **DEPL-01**: Create requirements.txt with all dependencies
- [ ] **DEPL-02**: Create .env.example for configuration
- [ ] **DEPL-03**: Deploy to Streamlit Cloud from GitHub
- [ ] **DEPL-04**: Configure auto-refresh in deployed app

## v2 Requirements

- **ADV-01**: Backtesting against historical crash data (2025 AI bubble)
- **ADV-02**: Multiple timeframes for risk calculation
- **ADV-03**: Custom risk formula weights
- **ADV-04**: Export data to CSV
- **ADV-05**: User authentication for personalized alerts

## Out of Scope

| Feature | Reason |
|---------|--------|
| Real-time WebSocket updates | Too complex for 2-day prototype, polling sufficient |
| Multiple data providers | yfinance sufficient for prototype |
| Custom ML model training | FinBERT pre-trained model adequate |
| Mobile app | Web dashboard sufficient for demo |
| Paid API integrations | Free tier tools meet requirements |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| DATA-01 | Phase 1 | Pending |
| DATA-02 | Phase 1 | Pending |
| DATA-03 | Phase 1 | Pending |
| DATA-04 | Phase 1 | Pending |
| DATA-05 | Phase 1 | Pending |
| DATA-06 | Phase 1 | Pending |
| SENT-01 | Phase 2 | Pending |
| SENT-02 | Phase 2 | Pending |
| SENT-03 | Phase 2 | Pending |
| SENT-04 | Phase 2 | Pending |
| RISK-01 | Phase 3 | Pending |
| RISK-02 | Phase 3 | Pending |
| RISK-03 | Phase 3 | Pending |
| RISK-04 | Phase 3 | Pending |
| UI-01 | Phase 3 | Pending |
| UI-02 | Phase 3 | Pending |
| UI-03 | Phase 3 | Pending |
| UI-04 | Phase 3 | Pending |
| UI-05 | Phase 3 | Pending |
| UI-06 | Phase 3 | Pending |
| UI-07 | Phase 3 | Pending |
| CFG-01 | Phase 3 | Pending |
| CFG-02 | Phase 3 | Pending |
| CFG-03 | Phase 3 | Pending |
| CFG-04 | Phase 3 | Pending |
| CFG-05 | Phase 3 | Pending |
| ALRT-01 | Phase 4 | Pending |
| ALRT-02 | Phase 4 | Pending |
| ALRT-03 | Phase 4 | Pending |
| DEPL-01 | Phase 4 | Pending |
| DEPL-02 | Phase 4 | Pending |
| DEPL-03 | Phase 4 | Pending |
| DEPL-04 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 31 total
- Mapped to phases: 31
- Unmapped: 0 ✓

---

*Requirements defined: 2026-03-08*
*Last updated: 2026-03-08 after research synthesis*
