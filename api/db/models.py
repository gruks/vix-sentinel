"""
NewsArticle ORM Model
Defines database schema for cached news articles with deduplication support
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint, Index
from datetime import datetime
from api.db.database import Base


class NewsArticle(Base):
    """
    ORM model for news articles stored in SQLite database.
    Uses title_hash (URL + title combined) for deduplication.
    """
    __tablename__ = "news_articles"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Unique hash for deduplication (SHA256 of URL + title)
    title_hash = Column(String(64), unique=True, index=True)
    
    # Article fields
    title = Column(String(500))
    source = Column(String(100))
    url = Column(String(1000), index=True)
    published = Column(String(100))
    ticker = Column(String(10), index=True)
    
    # Sentiment score (cached from analysis)
    sentiment_score = Column(Float, nullable=True)
    
    # Fetch timestamp for cache invalidation
    fetched_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Indexes for efficient querying
    __table_args__ = (
        Index('idx_ticker_fetched', 'ticker', 'fetched_at'),
    )
