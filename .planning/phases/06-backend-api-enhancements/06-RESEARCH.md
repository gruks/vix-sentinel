# Phase 6: Backend API Enhancements & News Database - Research

**Researched:** 2026-03-17
**Domain:** Backend API architecture, news caching, database integration
**Confidence:** HIGH

## Summary

Phase 6 focuses on three major improvements: (1) adding flexible time range selection in the frontend (1d, 2d, 10d, 30d), (2) removing Streamlit UI from the backend to make FastAPI purely an API, and (3) implementing a news caching system with database storage to avoid fetching news on every request.

**Primary recommendation:** Use SQLite with SQLAlchemy 2.0 for news caching (upgradeable to PostgreSQL), implement URL-based deduplication for incremental news refresh, and map frontend time ranges (1d, 2d, 10d, 30d) to yfinance-compatible date ranges using start/end parameters.

## User Constraints

Since no CONTEXT.md exists, this research addresses the full scope of Phase 6 based on the provided requirements:

1. Add time session selection in frontend (1d, 2d, 10d, 30d)
2. Remove UI from backend - make FastAPI purely an API (no Streamlit/Brotli)
3. Add news caching with database - store news, refresh only when new news arrives
4. Enhance the UI (optional)

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| SQLAlchemy | 2.0.x | ORM for database operations | Industry standard for Python ORM, database-agnostic |
| SQLite | Built-in | Local file-based database | Zero configuration, perfect for caching, easily upgradeable to PostgreSQL |
| aiosqlite | latest | Async SQLite driver | Non-blocking database operations for FastAPI |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| httpx | latest | Async HTTP client for RSS feeds | Replacing requests for async news fetching |
| python-dotenv | latest | Environment variable management | Database URL and API secrets |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| SQLite | PostgreSQL | PostgreSQL better for production/high concurrency, SQLite simpler for single-instance caching |
| SQLAlchemy | Raw SQL / DDB/ORM | SQLAlchemy provides database portability, migration support (Alembic) |
| aiosqlite | sqlite3 (sync) | Async needed for FastAPI non-blocking operations |

**Installation:**
```bash
pip install sqlalchemy aiosqlite httpx python-dotenv
```

## Architecture Patterns

### Recommended Project Structure
```
src/
├── api/
│   ├── main.py           # FastAPI app (pure API, no UI)
│   ├── models.py         # Pydantic request/response models
│   └── routers/          # API route modules
├── db/
│   ├── database.py       # SQLAlchemy engine and session setup
│   ├── models.py        # SQLAlchemy ORM models (NewsArticle)
│   └── repositories/    # Data access layer
├── services/
│   ├── news_service.py  # News fetching with caching logic
│   └── market_service.py # Market data service
└── cache.py             # In-memory cache utilities
```

### Pattern 1: News Caching with Database
**What:** Store fetched news in SQLite, only refresh when new articles detected
**When to use:** When news sources return many duplicate articles on each fetch
**Example:**
```python
# Source: Research - deduplication strategy
import hashlib
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import httpx

Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = "news_articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title_hash = Column(String(64), unique=True, index=True)  # SHA256 of URL or title
    title = Column(String(500))
    source = Column(String(100))
    url = Column(String(1000))
    published = Column(String(100))
    ticker = Column(String(10))
    sentiment = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint('title_hash', 'source', name='unique_article'),
    )

async def fetch_and_cache_news(tickers: List[str]) -> List[NewsArticle]:
    """Fetch news, deduplicate, and cache only new articles."""
    async with httpx.AsyncClient() as client:
        new_articles = []
        for ticker in tickers:
            # Fetch from RSS/HN API
            articles = await fetch_from_sources(client, ticker)
            
            for article in articles:
                # Create hash for deduplication
                article_hash = hashlib.sha256(
                    (article['url'] + article['title']).encode()
                ).hexdigest()
                
                # Check if exists in DB
                existing = session.query(NewsArticle).filter(
                    NewsArticle.title_hash == article_hash
                ).first()
                
                if not existing:
                    # Add new article
                    new_article = NewsArticle(
                        title_hash=article_hash,
                        title=article['title'],
                        source=article['source'],
                        url=article['url'],
                        published=article.get('published', ''),
                        ticker=ticker
                    )
                    session.add(new_article)
                    new_articles.append(new_article)
        
        session.commit()
        return new_articles
```

### Pattern 2: FastAPI Dependency Injection for Database
**What:** Use FastAPI's dependency injection for database sessions
**When to use:** Every API endpoint that needs database access
**Example:**
```python
# Source: SQLAlchemy 2.0 best practices
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

DATABASE_URL = "sqlite+aiosqlite:///./news_cache.db"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Usage in endpoint
@app.get("/api/news")
async def get_news(db: AsyncSession = Depends(get_db)):
    # Query from database, not live fetch
    result = await db.execute(select(NewsArticle).order_by(NewsArticle.created_at.desc()).limit(50))
    articles = result.scalars().all()
    return articles
```

### Pattern 3: Time Range Mapping for yfinance
**What:** Map frontend time ranges (1d, 2d, 10d, 30d) to yfinance-compatible parameters
**When to use:** When frontend needs time ranges that don't match yfinance's built-in periods
**Example:**
```python
# Source: yfinance documentation
from datetime import datetime, timedelta

# Mapping frontend time ranges to yfinance parameters
TIME_RANGE_MAP = {
    "1d": {"period": "1d", "interval": "5m"},    # Intraday
    "2d": {"start": lambda: (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"), 
           "end": lambda: datetime.now().strftime("%Y-%m-%d"),
           "interval": "15m"},
    "10d": {"start": lambda: (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"), 
            "end": lambda: datetime.now().strftime("%Y-%m-%d"),
            "interval": "1h"},
    "30d": {"start": lambda: (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"), 
            "end": lambda: datetime.now().strftime("%Y-%m-%d"),
            "interval": "1d"},
    "7d": {"period": "5d", "interval": "15m"},  # yfinance doesn't have 7d exactly
    "1mo": {"period": "1mo", "interval": "1d"},
    "3mo": {"period": "3mo", "interval": "1d"},
}

def fetch_with_time_range(ticker: str, time_range: str) -> pd.DataFrame:
    """Fetch data using appropriate yfinance parameters."""
    params = TIME_RANGE_MAP.get(time_range, TIME_RANGE_MAP["7d"])
    
    if "period" in params:
        return yf.download(ticker, period=params["period"], interval=params["interval"])
    else:
        start = params["start"]() if callable(params["start"]) else params["start"]
        end = params["end"]() if callable(params["end"]) else params["end"]
        return yf.download(ticker, start=start, end=end, interval=params["interval"])
```

### Anti-Patterns to Avoid
- **Using Streamlit cache in FastAPI:** `@st.cache_data` doesn't work outside Streamlit - must use SQLAlchemy or in-memory caching
- **Fetching news on every request:** Causes slow response times - use database caching with deduplication
- **Using sync database drivers in async FastAPI:** Will block the event loop - use aiosqlite or asyncpg
- **Hardcoding database URL:** Use environment variables for database connection string

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Database operations | Raw SQL queries | SQLAlchemy ORM | Prevents SQL injection, provides migration support, database portability |
| News deduplication | Custom fuzzy matching | URL/title hashing | Simple, fast, reliable for exact duplicates - sufficient for RSS feeds |
| Async database | Sync sqlite3 | aiosqlite | Non-blocking I/O essential for FastAPI performance |
| Session management | Manual session handling | FastAPI dependency injection | Ensures proper cleanup, transaction management |

**Key insight:** RSS feeds and HN API return mostly identical articles within short timeframes. URL hashing provides sufficient deduplication - complex fuzzy matching (TF-IDF, Sentence-BERT) is overkill for this use case.

## Common Pitfalls

### Pitfall 1: Streamlit Dependencies in FastAPI
**What goes wrong:** Backend fails to start, missing module errors
**Why it happens:** `app.py` imports Streamlit (`import streamlit as st`), but FastAPI backend shouldn't have Streamlit installed/run
**How to avoid:** Remove `app.py` as the entry point, keep only `api/main.py`. Remove Streamlit from requirements.txt or keep it as optional
**Warning signs:** Import errors for `streamlit`, `streamlit_autorefresh`, `brotli` when running uvicorn

### Pitfall 2: Incompatible Time Range Parameters
**What goes wrong:** yfinance throws "Period 'X' is invalid" error
**Why it happens:** Frontend requests 2d or 10d, but yfinance only accepts 1d, 5d, 1mo, 3mo, 6mo, 1y, etc.
**How to avoid:** Use start/end date parameters instead of period for non-standard ranges
**Warning signs:** Error message: "Period '10d' is invalid, must be one of ['1d', '5d', '1mo'...]"

### Pitfall 3: Duplicate News Articles
**What goes wrong:** Same articles returned repeatedly, database grows with duplicates
**Why it happens:** Not implementing deduplication before storing in database
**How to avoid:** Use URL or title hashing to check for existing articles before inserting
**Warning signs:** Same news titles appearing in API response, database file growing rapidly

### Pitfall 4: Session Not Closed
**What goes wrong:** Database connections exhausted, application hangs
**Why it happens:** Not using async context manager or try/finally for database sessions
**How to avoid:** Always use `async with async_session_maker() as session:` pattern
**Warning signs:** "QueuePool limit exceeded" errors, high memory usage

### Pitfall 5: CORS Issues After Removing Streamlit
**What goes wrong:** Frontend can't reach API, CORS errors in browser
**Why it happens:** FastAPI CORS middleware only allows specific origins
**How to adjust:** Update CORS allow_origins to include frontend development server (localhost:5173 for Vite)
**Warning signs:** "Access to fetch has been blocked by CORS policy"

## Code Examples

### Database Setup for News Caching
```python
# Source: SQLAlchemy 2.0 documentation
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = "news_articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title_hash = Column(String(64), unique=True, index=True)
    title = Column(String(500))
    source = Column(String(100))
    url = Column(String(1000), unique=True, index=True)
    published = Column(String(100))
    ticker = Column(String(10), index=True)
    sentiment_score = Column(Float, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow, index=True)

# Create engine and tables
engine = create_async_engine("sqlite+aiosqlite:///./news_cache.db")
async_session = async_sessionmaker(engine, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

### Incremental News Refresh Logic
```python
# Source: Research - incremental refresh pattern
async def get_fresh_news(tickers: List[str], db: AsyncSession) -> List[Dict]:
    """Get news - from cache if fresh, otherwise fetch and update."""
    CACHE_MAX_AGE_MINUTES = 30
    
    # Check last fetch time
    from sqlalchemy import select, func
    result = await db.execute(
        select(func.max(NewsArticle.fetched_at)).where(
            NewsArticle.ticker.in_(tickers)
        )
    )
    last_fetch = result.scalar()
    
    should_refresh = (
        last_fetch is None or 
        (datetime.utcnow() - last_fetch).total_seconds() > CACHE_MAX_AGE_MINUTES * 60
    )
    
    if should_refresh:
        # Fetch new articles from sources
        new_articles = await fetch_from_rss_hn(tickers)
        
        # Deduplicate and store
        for article in new_articles:
            article_hash = hashlib.sha256(article['url'].encode()).hexdigest()
            
            exists = await db.execute(
                select(NewsArticle).where(NewsArticle.title_hash == article_hash)
            )
            if not exists.first():
                db.add(NewsArticle(
                    title_hash=article_hash,
                    title=article['title'],
                    source=article['source'],
                    url=article['url'],
                    published=article.get('published', ''),
                    ticker=article.get('ticker')
                ))
        
        await db.commit()
    
    # Return cached articles
    result = await db.execute(
        select(NewsArticle)
        .where(NewsArticle.ticker.in_(tickers))
        .order_by(NewsArticle.fetched_at.desc())
        .limit(50)
    )
    return result.scalars().all()
```

### Frontend Time Range Selector
```tsx
// Source: React + TypeScript pattern
interface TimeRangeOption {
  value: string;
  label: string;
  apiParam: string;
}

const TIME_RANGE_OPTIONS: TimeRangeOption[] = [
  { value: '1d', label: '1 Day', apiParam: '1d' },
  { value: '2d', label: '2 Days', apiParam: '2d' },
  { value: '10d', label: '10 Days', apiParam: '10d' },
  { value: '30d', label: '30 Days', apiParam: '30d' },
];

// In component:
const [timeRange, setTimeRange] = useState('7d');

// When fetching market data:
const market = await fetchMarket('SPY', timeRange);
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Streamlit UI in backend | Pure FastAPI API | Phase 6 | Frontend/Backend clearly separated, backend serves only data |
| In-memory cache (dict) | SQLite database caching | Phase 6 | Persistent cache survives restarts, deduplication prevents duplicates |
| Live news fetch every request | Incremental refresh with DB | Phase 6 | Fast response times, only fetches when cache stale |
| Hardcoded time ranges | Flexible range mapping | Phase 6 | Frontend can request 2d, 10d, etc. |

**Deprecated/outdated:**
- `@st.cache_data` decorator: Only works in Streamlit, replaced with SQLAlchemy caching
- `requests` library for RSS fetching: Should use `httpx` for async operations in FastAPI
- Single-period yfinance fetch: Must use start/end dates for non-standard periods

## Open Questions

1. **Database Upgrade Path**
   - What we know: SQLite works for single-instance caching
   - What's unclear: When to upgrade to PostgreSQL? What are the triggers?
   - Recommendation: Keep SQLite for now, design models to be compatible with PostgreSQL (use SQLAlchemy, avoid SQLite-specific features)

2. **News Refresh Frequency**
   - What we know: RSS feeds update at varying intervals (minutes to hours)
   - What's unclear: What is the optimal cache TTL? 15 minutes? 30 minutes? 1 hour?
   - Recommendation: Start with 30 minutes, allow manual refresh via API endpoint

3. **Sentiment Caching**
   - What we know: FinBERT takes time to run, should not run on every request
   - What's unclear: Should sentiment be cached in DB or recalculated periodically?
   - Recommendation: Store sentiment with news articles in DB, recalculate when article first added

4. **Streamlit App Disposition**
   - What we know: Currently have both app.py (Streamlit) and api/main.py (FastAPI)
   - What's unclear: Should app.py be deleted entirely or kept as a separate demo?
   - Recommendation: Remove from production backend, can keep as reference in separate folder if needed

## Sources

### Primary (HIGH confidence)
- SQLAlchemy 2.0 documentation - ORM patterns, async support
- yfinance official documentation - period/interval parameters, date range handling
- FastAPI official documentation - dependency injection, async sessions
- Python aiosqlite documentation - async SQLite operations

### Secondary (MEDIUM confidence)
- WebSearch: News deduplication strategies - URL hashing sufficient for RSS
- WebSearch: SQLAlchemy async session management patterns
- WebSearch: yfinance time period invalid error solutions

### Tertiary (LOW confidence)
- WebSearch: News caching best practices (general patterns, needs validation)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - SQLAlchemy + SQLite is well-documented, standard choice
- Architecture: HIGH - Patterns verified with official documentation
- Pitfalls: HIGH - Common issues well-documented, solutions straightforward
- Time range mapping: MEDIUM - yfinance parameter mapping requires testing

**Research date:** 2026-03-17
**Valid until:** 30 days (database patterns stable, yfinance API may change)
