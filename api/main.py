"""
FastAPI Application - Market Risk API Backend
Exposes market risk data as REST API endpoints for React frontend
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import time
import random
import pandas as pd
import yfinance as yf
import hashlib
from typing import Dict, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from api.models import (
    RiskResponse, MarketResponse, MarketDataPoint,
    NewsResponse, NewsItem, HistoryResponse, HistoryPoint,
    RefreshResponse
)

# Import from existing modules
from src.news_fetcher import fetch_all_news
from src.sentiment.scorer import get_sentiment_scores
from src.risk_calculator import (
    calculate_volatility_zscore,
    calculate_risk_score,
    get_risk_level,
    get_all_metrics
)

# Database imports
from api.db.database import get_db, init_db, async_session_maker
from api.db.models import NewsArticle

# Create FastAPI app
app = FastAPI(
    title="Market Risk API",
    description="REST API for market risk data - serves React frontend",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory cache with TTL
CACHE_TTL = 300  # 5 minutes in seconds

# News cache TTL in database (30 minutes)
NEWS_CACHE_TTL_MINUTES = 30

cache: Dict = {
    "risk": {"data": None, "timestamp": 0},
    "market": {"data": None, "timestamp": 0},
    "news": {"data": None, "timestamp": 0},
    "history": {"data": None, "timestamp": 0}
}


def get_cached(key: str):
    """Get data from cache if fresh"""
    if cache[key]["data"] is not None:
        age = time.time() - cache[key]["timestamp"]
        if age < CACHE_TTL:
            return cache[key]["data"]
    return None


def set_cached(key: str, data):
    """Set data in cache"""
    cache[key]["data"] = data
    cache[key]["timestamp"] = time.time()


def clear_cache():
    """Clear all cache"""
    for key in cache:
        cache[key]["data"] = None
        cache[key]["timestamp"] = 0


def get_historical_volatility() -> list:
    """Generate mock historical volatility data"""
    # Generate realistic historical volatility values
    base_vol = 15.0
    return [base_vol + random.uniform(-5, 10) for _ in range(30)]


def fetch_current_volatility() -> float:
    """Fetch current volatility using yfinance directly (not Streamlit cache)"""
    try:
        # Get SPY data for volatility calculation
        spy = yf.Ticker("SPY")
        hist = spy.history(period="1mo")  # 1 month for volatility calc
        
        if hist.empty:
            return 18.0  # Default fallback
        
        # Calculate volatility (annualized standard deviation of returns)
        returns = hist['Close'].pct_change().dropna()
        if len(returns) < 2:
            return 18.0
        
        # Annualized volatility
        vol = returns.std() * (252 ** 0.5) * 100
        return round(float(vol), 2) if pd.notna(vol) else 18.0
        
    except Exception as e:
        print(f"Error fetching volatility: {e}")
        return 18.0  # Default fallback


def generate_history_data(hours: int = 24) -> list:
    """Generate mock history data for risk evolution"""
    history = []
    now = datetime.now()
    
    for i in range(hours):
        timestamp = now - timedelta(hours=hours - i - 1)
        
        # Generate somewhat realistic risk evolution
        base_risk = 45 + random.uniform(-10, 20)
        volatility = 18 + random.uniform(-5, 10)
        sentiment = 0.5 + random.uniform(-0.3, 0.3)
        
        history.append({
            "time": timestamp.isoformat(),
            "risk": round(base_risk, 2),
            "volatility": round(volatility, 2),
            "sentiment": round(sentiment, 2)
        })
    
    return history


async def get_fresh_news(tickers: List[str], db: AsyncSession) -> List[NewsArticle]:
    """
    Get news - from database cache if fresh, otherwise fetch and update.
    Uses 30-minute TTL for cache invalidation.
    """
    # Check last fetch time for any of the tickers
    result = await db.execute(
        select(func.max(NewsArticle.fetched_at)).where(
            NewsArticle.ticker.in_(tickers)
        )
    )
    last_fetch = result.scalar()
    
    should_refresh = (
        last_fetch is None or 
        (datetime.utcnow() - last_fetch).total_seconds() > NEWS_CACHE_TTL_MINUTES * 60
    )
    
    if should_refresh:
        # Fetch new articles from existing news_fetcher
        new_articles = fetch_all_news(tickers)
        
        # Get sentiment scores for the articles
        sentiment_scores = get_sentiment_scores(new_articles)
        
        # Deduplicate and store
        for article in new_articles.get('headlines', []):
            # Create hash from URL + title for deduplication
            article_hash = hashlib.sha256(
                (article.get('link', '') + article.get('title', '')).encode()
            ).hexdigest()
            
            # Check if already exists
            exists_result = await db.execute(
                select(NewsArticle).where(NewsArticle.title_hash == article_hash)
            )
            existing = exists_result.first()
            
            if not existing:
                # Get sentiment for this article's ticker
                ticker = article.get('ticker', 'overall')
                sentiment = sentiment_scores.get(ticker, sentiment_scores.get('overall', 0.5))
                
                db.add(NewsArticle(
                    title_hash=article_hash,
                    title=article.get('title', ''),
                    source=article.get('source', ''),
                    url=article.get('link', ''),
                    published=article.get('published', ''),
                    ticker=ticker if ticker else 'SPY',
                    sentiment_score=sentiment
                ))
        
        await db.commit()
    
    # Return cached articles
    result = await db.execute(
        select(NewsArticle)
        .where(NewsArticle.ticker.in_(tickers))
        .order_by(NewsArticle.fetched_at.desc())
        .limit(50)
    )
    return list(result.scalars().all())


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "service": "Market Risk API", "version": "1.0.0"}


@app.get("/api/risk", response_model=RiskResponse)
async def get_risk():
    """
    Get current market risk metrics
    Combines volatility and sentiment data
    """
    # Check cache first
    cached = get_cached("risk")
    if cached:
        return cached
    
    try:
        # Get current volatility directly from yfinance
        volatility = fetch_current_volatility()
        
        # Get historical volatility for Z-score
        historical_vols = get_historical_volatility()
        
        # Fetch news and get sentiment
        news_data = fetch_all_news(['SPY', 'VIX', 'AAPL', 'TSLA'])
        
        # Calculate sentiment score (0-1 scale)
        sentiment_scores = get_sentiment_scores(news_data)
        sentiment = sentiment_scores.get('overall', 0.5) if sentiment_scores else 0.5
        
        # Calculate risk metrics
        metrics = get_all_metrics(
            volatility=volatility / 100,  # Convert to 0-1 scale
            historical_vols=historical_vols,
            sentiment_score=sentiment
        )
        
        # Build response
        risk_response = RiskResponse(
            score=round(metrics['risk_score'], 2),
            volatility=round(volatility, 2),
            sentiment=round(sentiment, 2),
            level=metrics['level'],
            timestamp=datetime.now().isoformat()
        )
        
        # Cache result
        set_cached("risk", risk_response)
        
        return risk_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating risk: {str(e)}")


@app.get("/api/market", response_model=MarketResponse)
async def get_market_data(symbol: str = "SPY", time_range: str = "7d"):
    """
    Get market OHLC data for charts
    
    Args:
        symbol: Stock ticker symbol (default: SPY)
        time_range: Data period (1d, 5d, 7d, 1mo, 3mo)
    """
    # Check cache first
    cache_key = f"market_{symbol}_{time_range}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    
    try:
        # Fetch historical data
        from src.data_fetcher import fetch_historical_data
        
        hist_df = fetch_historical_data(symbol, time_range)
        
        if hist_df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for {symbol}")
        
        # Convert to response format
        data_points = []
        for idx, row in hist_df.iterrows():
            data_points.append(MarketDataPoint(
                time=idx.isoformat(),
                price=float(row.get('Close', 0)) if row.get('Close') is not None else 0,
                volume=int(row.get('Volume', 0)) if row.get('Volume') is not None else 0,
                open=float(row.get('Open', 0)) if row.get('Open') is not None else None,
                high=float(row.get('High', 0)) if row.get('High') is not None else None,
                low=float(row.get('Low', 0)) if row.get('Low') is not None else None,
                close=float(row.get('Close', 0)) if row.get('Close') is not None else None
            ))
        
        response = MarketResponse(
            data=data_points,
            symbol=symbol,
            time_range=time_range
        )
        
        # Cache result
        cache[cache_key] = {"data": response, "timestamp": time.time()}
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching market data: {str(e)}")


@app.get("/api/news", response_model=NewsResponse)
async def get_news(db: AsyncSession = Depends(get_db)):
    """
    Get news headlines with sentiment scores.
    Uses database caching - returns cached news if fresh (<30 min),
    otherwise fetches fresh news and updates cache.
    """
    try:
        # Get news from database (handles caching automatically)
        articles_db = await get_fresh_news(['SPY', 'VIX', 'AAPL', 'TSLA', 'MSFT'], db)
        
        # Convert to response format
        articles = []
        for item in articles_db:
            articles.append(NewsItem(
                title=item.title,
                source=item.source,
                sentiment=round(item.sentiment_score, 2) if item.sentiment_score else None,
                url=item.url,
                time=item.published
            ))
        
        return NewsResponse(
            articles=articles,
            total_count=len(articles),
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")


@app.get("/api/history", response_model=HistoryResponse)
async def get_history(period_hours: int = 24):
    """
    Get risk evolution history
    
    Args:
        period_hours: Number of hours of history to return (default: 24)
    """
    # Check cache first
    cached = get_cached("history")
    if cached and cached.period_hours == period_hours:
        return cached
    
    try:
        # Generate history data
        history_data = generate_history_data(period_hours)
        
        # Convert to response format
        points = [HistoryPoint(**item) for item in history_data]
        
        response = HistoryResponse(
            data=points,
            period_hours=period_hours
        )
        
        # Cache result
        set_cached("history", response)
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating history: {str(e)}")


@app.post("/api/refresh", response_model=RefreshResponse)
async def refresh_cache():
    """
    Force cache refresh - clears cache and returns fresh data
    """
    clear_cache()
    
    return RefreshResponse(
        status="success",
        message="Cache cleared. Next API call will fetch fresh data.",
        timestamp=datetime.now().isoformat()
    )


@app.on_event("startup")
async def startup_event():
    """Initialize database and warm cache on startup"""
    # Initialize database tables
    try:
        await init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Warning: Database initialization failed: {e}")
    
    # Pre-fetch data on startup to avoid slow first request
    try:
        # Trigger cache population (get_risk is sync, others need db)
        get_risk()
    except Exception as e:
        print(f"Warning: Risk cache warming failed: {e}")
