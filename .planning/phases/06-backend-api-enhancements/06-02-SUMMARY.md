---
phase: 06-backend-api-enhancements
plan: 02
subsystem: api
tags: [database, caching, news, sqlite]
dependency_graph:
  requires:
    - src/news_fetcher.py (news source)
    - src/sentiment/scorer.py (sentiment analysis)
  provides:
    - api/db/database.py (async database layer)
    - api/db/models.py (NewsArticle ORM)
    - api/main.py (updated news endpoint with caching)
  affects:
    - /api/news endpoint behavior
    - Database file: news_cache.db
tech_stack:
  added:
    - sqlalchemy>=2.0.0
    - aiosqlite>=0.19.0
  patterns:
    - SQLAlchemy async engine with aiosqlite
    - Database-backed caching with TTL
    - URL+title hashing for deduplication
key_files:
  created:
    - api/db/database.py (async engine, session, get_db dependency)
    - api/db/models.py (NewsArticle ORM model)
  modified:
    - api/main.py (added news caching logic, imports)
    - requirements.txt (added sqlalchemy, aiosqlite)
decisions:
  - Use SQLite with aiosqlite for async database operations
  - Use 30-minute cache TTL for news articles
  - Use SHA256 hash of URL+title for deduplication
  - Cache sentiment scores with articles in database
---

# Phase 6 Plan 2: News Caching with SQLite Summary

Implemented news caching with SQLite database to avoid fetching news on every request. News is now cached in the database and only refreshed when the cache is stale (>30 minutes). Duplicate articles are prevented via URL+title hashing.

## Tasks Completed

| Task | Description | Commit |
|------|-------------|--------|
| 1 | Create database layer with SQLAlchemy | 383ca9e |
| 2 | Create NewsArticle ORM model | 3639cf5 |
| 3 | Update API with news caching logic | ec6e5b1 |

## Key Features

- **SQLite Database**: Uses aiosqlite for async operations with FastAPI
- **30-minute TTL**: News only refreshes when cache is stale
- **Deduplication**: SHA256 hash of URL+title prevents duplicate articles
- **Sentiment Caching**: Sentiment scores are stored with articles
- **Database Initialization**: Tables created on API startup

## Verification

After starting the API server with `uvicorn api.main:app --reload`:
1. First call to `/api/news` will fetch fresh news and store in database
2. Subsequent calls within 30 minutes return cached articles
3. `news_cache.db` file is created in the project directory

## Files Modified

- `api/db/database.py` - New async database layer
- `api/db/models.py` - New NewsArticle ORM model  
- `api/main.py` - Updated news endpoint with caching
- `requirements.txt` - Added sqlalchemy, aiosqlite

## Self-Check

- [x] database.py exists with async engine setup
- [x] get_db dependency exported
- [x] init_db function exists
- [x] NewsArticle model defined with all columns
- [x] Indexes for efficient querying
- [x] get_fresh_news function handles caching
- [x] /api/news endpoint uses database
- [x] Database initialized on startup

## Deviation Documentation

No deviations from plan. Implementation followed the specification exactly.

## Duration

Tasks completed in single execution wave.
