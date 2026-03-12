---
phase: 03-risk-dashboard
verified: 2026-03-11T00:00:00Z
status: gaps_found
score: 14/16 must-haves verified
gaps:
  - truth: "User sees volatility heatmap (tickers x days)"
    status: failed
    reason: "create_volatility_heatmap exists in src/charts.py but NOT called in app.py. Volatility section shows DataFrame instead of Plotly heatmap."
    artifacts:
      - path: "app.py"
        issue: "Lines 172-186 render DataFrame instead of calling create_volatility_heatmap"
      - path: "src/charts.py"
        issue: "Function exists (line 326) but not imported/used in app.py"
    missing:
      - "Call create_volatility_heatmap in app.py volatility section"
      - "Pass proper ticker x day data to heatmap function"
  - truth: "User sees risk gauge evolution (hourly risk score for 24h)"
    status: failed
    reason: "create_risk_evolution exists in src/charts.py but NOT called in app.py. No risk evolution section exists in the dashboard."
    artifacts:
      - path: "app.py"
        issue: "Missing section for risk evolution chart"
      - path: "src/charts.py"
        issue: "Function exists (line 400) but not imported/used in app.py"
    missing:
      - "Add risk evolution chart section to app.py"
      - "Implement 24h risk history tracking/caching"
---

# Phase 3: Risk Calculation & Dashboard UI Verification Report

**Phase Goal:** Display interactive risk dashboard with all visualizations

**Verified:** 2026-03-11

**Status:** gaps_found

**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| #   | Truth   | Status     | Evidence       |
| --- | ------- | ---------- | -------------- |
| 1   | Volatility Z-score calculated against historical mean | ✓ VERIFIED | src/risk_calculator.py line 12-47 |
| 2   | Combined risk score computed using formula: 0.6*vol_z + 0.4*(1-sentiment) | ✓ VERIFIED | src/risk_calculator.py line 70-98 |
| 3   | Risk thresholds applied: LOW (<40), MEDIUM (40-75), HIGH (>75) | ✓ VERIFIED | src/risk_calculator.py line 101-124 |
| 4   | Alert colors determined: GREEN, YELLOW, RED | ✓ VERIFIED | src/risk_calculator.py returns in get_risk_level |
| 5   | User sees 3 Plotly gauges: volatility, sentiment, risk | ✓ VERIFIED | app.py line 142-149, calls create_three_gauges |
| 6   | User sees risk alert banner with color based on level | ✓ VERIFIED | app.py line 128-140 |
| 7   | User sees 7-day SPY candlestick chart | ✓ VERIFIED | app.py line 151-157, calls create_candlestick |
| 8   | User sees 7-day sentiment trend line chart | ✓ VERIFIED | app.py line 159-170, calls create_sentiment_line |
| 9   | User sees volatility heatmap (tickers x days) | ✗ FAILED | DataFrame rendered instead of create_volatility_heatmap |
| 10  | User sees risk gauge evolution (hourly risk score for 24h) | ✗ FAILED | create_risk_evolution exists but not called in app.py |
| 11  | Per-ticker details table displays | ✓ VERIFIED | app.py line 188-195 |
| 12  | Sidebar shows ticker multiselect with add/remove capability | ✓ VERIFIED | app.py line 24-30 |
| 13  | Sidebar shows time range selector (1d/7d/30d) | ✓ VERIFIED | app.py line 32-37 |
| 14  | Dashboard auto-refreshes every 15 minutes | ✓ VERIFIED | app.py line 17-18 |
| 15  | Manual refresh button clears cache and reloads data | ✓ VERIFIED | app.py line 40-42 |
| 16  | Data is cached with st.cache_data TTL=900s | ✓ VERIFIED | app.py lines 67, 79, 90 |

**Score:** 14/16 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
| -------- | -------- | ------ | ------- |
| `src/risk_calculator.py` | Risk calculation functions | ✓ VERIFIED | 172 lines, all functions present |
| `src/charts.py` | Chart creation functions | ✓ VERIFIED | 548 lines, all functions present |
| `app.py` | Complete dashboard | ⚠️ PARTIAL | 203 lines, missing 2 chart integrations |

### Key Link Verification

| From | To | Via | Status | Details |
| ---- | --- | --- | ------ | ------- |
| `app.py` | `src/risk_calculator.py` | imports get_all_metrics, get_risk_level | ✓ WIRED | Lines 93, 130 |
| `app.py` | `src/charts.py` | imports create_three_gauges, create_candlestick, create_sentiment_line, create_risk_banner | ⚠️ PARTIAL | 4 of 6 chart functions imported |
| `app.py` | `src/data_fetcher.py` | imports fetch_market_data, fetch_historical_data | ✓ WIRED | Line 70 |
| `app.py` | `src/sentiment` | imports get_sentiment_scores | ✓ WIRED | Line 83 |
| `src/charts.py` | `src/risk_calculator.py` | imports for color definitions | ✓ WIRED | N/A (hardcoded colors) |

### Requirements Coverage

| Requirement | Status | Blocking Issue |
| ----------- | ------ | -------------- |
| RISK-01 | ✓ SATISFIED | calculate_volatility_zscore implemented |
| RISK-02 | ✓ SATISFIED | calculate_risk_score with LOCKED formula |
| RISK-03 | ✓ SATISFIED | Threshold logic in get_risk_level |
| RISK-04 | ✓ SATISFIED | Alert colors returned |
| UI-01 | ✓ SATISFIED | 3 gauges displayed |
| UI-02 | ✓ SATISFIED | Risk banner with st.success/warning/error |
| UI-03 | ✓ SATISFIED | Candlestick chart renders |
| UI-04 | ✓ SATISFIED | Sentiment line chart renders |
| UI-05 | ✗ BLOCKED | create_risk_evolution not called |
| UI-06 | ✗ BLOCKED | create_volatility_heatmap not called |
| UI-07 | ✓ SATISFIED | Details table displays |
| CFG-01 | ✓ SATISFIED | Ticker multiselect works |
| CFG-02 | ✓ SATISFIED | Time range selector works |
| CFG-03 | ✓ SATISFIED | Auto-refresh every 15 min |
| CFG-04 | ✓ SATISFIED | Manual refresh button works |
| CFG-05 | ✓ SATISFIED | Cache with TTL=900s |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| ---- | ---- | ------- | -------- | ------ |
| - | - | None found | - | - |

### Human Verification Required

None - all gaps are code integration issues, not runtime behaviors.

### Gaps Summary

**2 gaps blocking full goal achievement:**

1. **Volatility Heatmap Not Rendered**
   - The create_volatility_heatmap function exists in src/charts.py (line 326)
   - But app.py doesn't import or call it
   - Instead shows a simple DataFrame (line 183-184)
   - Impact: UI-06 requirement not met

2. **Risk Evolution Chart Not Rendered**
   - The create_risk_evolution function exists in src/charts.py (line 400)
   - But app.py doesn't import or call it
   - No section exists for 24-hour risk history
   - Impact: UI-05 requirement not met

Both functions are fully implemented in charts.py but simply not wired into app.py.

---

_Verified: 2026-03-11_
_Verifier: Claude (gsd-verifier)_
