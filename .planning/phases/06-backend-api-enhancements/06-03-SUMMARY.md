---
phase: 06-backend-api-enhancements
plan: 03
subsystem: Backend API
tags: [fastapi, streamlit-removal, caching, backend-cleanup]
dependency_graph:
  requires: []
  provides:
    - "Backend works without Streamlit"
    - "Pure FastAPI backend"
  affects:
    - "api/main.py"
    - "src/news_fetcher.py"
    - "src/sentiment/scorer.py"
    - "src/sentiment/analyzer.py"
tech_stack:
  added: []
  patterns:
    - "In-memory caching at API layer"
    - "Module-level pipeline caching for FinBERT"
    - "TTL-based cache (5 min for API, handled by api/main.py)"
key_files:
  created: []
  modified:
    - "src/news_fetcher.py"
    - "src/sentiment/analyzer.py"
    - "src/sentiment/scorer.py"
decisions:
  - "Remove Streamlit from backend - API uses in-memory caching instead"
  - "Module-level caching for FinBERT pipeline - avoids re-downloading model"
metrics:
  duration: "2 min"
  completed: "2026-03-17"
  tasks: 3
  files: 3
---

# Phase 6 Plan 3: Remove Streamlit Dependencies from Backend

## Summary

Successfully removed Streamlit dependencies from the FastAPI backend modules. The backend now works purely as an API without requiring Streamlit installation.

## Objective

Remove Streamlit dependencies from backend, making FastAPI purely an API. Uses in-memory caching instead of @st.cache_data.

## Key Changes

### Files Modified

1. **src/news_fetcher.py**
   - Removed `import streamlit as st`
   - Removed `@st.cache_data(ttl=3600)` decorators from all functions
   - Added simple in-memory cache structure (for future use)
   - Caching now handled at API layer in api/main.py

2. **src/sentiment/scorer.py**
   - Removed `import streamlit as st`
   - Removed `@st.cache_data(ttl=3600)` decorator from `get_sentiment_scores`

3. **src/sentiment/analyzer.py**
   - Removed `import streamlit as st`
   - Removed `@st.cache_resource` decorator from `load_finbert_pipeline`
   - Added module-level `_finbert_pipeline` caching to avoid re-downloading model

### Verified Clean Files

- **src/data_fetcher.py** - Already had no Streamlit imports
- **src/cache.py** - Already had no Streamlit imports  
- **api/main.py** - Already had no Streamlit imports, uses in-memory dict caching

## Verification

- All core module imports work without Streamlit:
  - `from src.news_fetcher import fetch_all_news` ✓
  - `from src.sentiment.scorer import get_sentiment_scores` ✓
  - `from src.data_fetcher import fetch_market_data` ✓

- No `import streamlit` in api/ directory
- No `import streamlit` in src/ except alert.py (used by Streamlit dashboard only)

## Caching Architecture

| Layer | Technology | TTL |
|-------|------------|-----|
| API (api/main.py) | In-memory dict | 5 minutes |
| Database (news) | SQLite/aiosqlite | 30 minutes |
| Sentiment | Module-level variable | Per session |

## Remaining Streamlit Usage

- **src/alert.py** - Email alerts (Streamlit dashboard only)
- **app.py** - Main Streamlit dashboard
- These are intentionally kept as they are UI components, not API dependencies.

## Commits

- e83ecf4: fix(06-backend-api): remove Streamlit dependencies from backend modules

## Self-Check

- [x] No `import streamlit` in api/ directory
- [x] Core module imports work without Streamlit
- [x] api/main.py has no Streamlit dependencies
- [x] Caching works via in-memory dict (no @st.cache_data)
- [x] Commit created with proper format
