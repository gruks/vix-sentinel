---
phase: 03-risk-dashboard
plan: 01
subsystem: risk_calculation
tags: [numpy, zscore, risk_metrics, financial_analysis]

# Dependency graph
requires:
  - phase: 01-data-pipeline
    provides: "src/data_fetcher.py with calculate_volatility function"
  - phase: 02-sentiment-analysis
    provides: "src/sentiment/scorer.py with calculate_average_sentiment"
provides:
  - "src/risk_calculator.py with risk calculation functions"
  - "Volatility Z-score normalized against historical mean"
  - "Combined risk score using LOCKED formula"
  - "Risk levels with alert colors"
affects: [03-risk-dashboard-02, dashboard_ui]

# Tech tracking
tech-stack:
  added: [numpy]
  patterns: [pure_functions, statistical_normalization, edge_case_handling]

key-files:
  created: [src/risk_calculator.py]
  modified: []

key-decisions:
  - "Used numpy for statistical calculations (mean, std)"
  - "Added epsilon check for floating-point precision in Z-score"
  - "normalize_sentiment handles both -1 to +1 and 0-1 input ranges"

patterns-established:
  - "Pure function risk calculation - testable independently from UI"
  - "Edge case handling for insufficient historical data"

# Metrics
duration: 3 min
completed: 2026-03-10
---

# Phase 3 Plan 1: Risk Calculation Summary

**Risk calculator with volatility Z-scores, LOCKED formula (0.6*vol_z + 0.4*(1-sentiment)), and threshold-based alert colors**

## Performance

- **Duration:** 3 min
- **Started:** 2026-03-10T03:19:22Z
- **Completed:** 2026-03-10T03:22:04Z
- **Tasks:** 3
- **Files modified:** 1

## Accomplishments
- Implemented volatility Z-score calculation with proper edge case handling
- Implemented LOCKED risk formula exactly as specified
- Implemented risk level thresholds with correct colors (LOW/GREEN, MEDIUM/YELLOW, HIGH/RED)
- Created comprehensive get_all_metrics function for dashboard integration

## Task Commits

Each task was committed atomically:

1. **Task 1-3: Risk calculation module** - `8574e1b` (feat)
   - Implemented all functions in single file commit

**Plan metadata:** (part of task commit)

## Files Created/Modified
- `src/risk_calculator.py` - Core risk calculation module with 5 functions

## Decisions Made
- Used numpy for statistical calculations (mean, std dev)
- Added epsilon check (1e-10) for floating-point precision when std is near-zero
- normalize_sentiment treats any value <=1.0 as -1 to +1 range input

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed floating-point precision in Z-score calculation**
- **Found during:** Task 3 (verification test)
- **Issue:** Uniform historical data ([0.15]*30) produced tiny std (~1e-17), causing massive Z-score
- **Fix:** Added epsilon check (std < 1e-10) to return 0.0 in edge case
- **Files modified:** src/risk_calculator.py
- **Verification:** get_all_metrics(0.20, [0.15]*30, 0.3) returns vol_zscore=0.0
- **Committed in:** 8574e1b (part of task commit)

**2. [Rule 1 - Bug] Fixed normalize_sentiment for 0 input**
- **Found during:** Task 2 (verification test)
- **Issue:** normalize_sentiment(0.0) returned 0.0 instead of expected 0.5
- **Fix:** Changed condition to treat any value <=1.0 and >=-1.0 as -1 to +1 range
- **Files modified:** src/risk_calculator.py
- **Verification:** Tests pass: -1.0→0.0, 0.0→0.5, 1.0→1.0
- **Committed in:** 8574e1b (part of task commit)

---

**Total deviations:** 2 auto-fixed (2 bug fixes)
**Impact on plan:** Both fixes essential for correctness. No scope creep.

## Issues Encountered
- None - all tests passed after bug fixes

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Risk calculation module ready for dashboard integration
- get_all_metrics function provides all data needed for UI display
- Ready for Phase 3 Plan 2: Dashboard UI with Plotly gauges

---
*Phase: 03-risk-dashboard*
*Completed: 2026-03-10*
