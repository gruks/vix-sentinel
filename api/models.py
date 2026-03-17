"""
Pydantic Response Models for FastAPI
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class RiskResponse(BaseModel):
    """Risk metrics response model"""
    score: float
    volatility: float
    sentiment: float
    level: str
    timestamp: str


class MarketDataPoint(BaseModel):
    """Single market data point (OHLC)"""
    time: str
    price: float
    volume: int
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None


class MarketResponse(BaseModel):
    """Market data response model"""
    data: List[MarketDataPoint]
    symbol: str
    time_range: str


class NewsItem(BaseModel):
    """Single news article"""
    title: str
    source: str
    sentiment: Optional[float] = None
    url: Optional[str] = None
    time: Optional[str] = None


class NewsResponse(BaseModel):
    """News response model"""
    articles: List[NewsItem]
    total_count: int
    timestamp: str


class HistoryPoint(BaseModel):
    """Single history data point"""
    time: str
    risk: float
    volatility: float
    sentiment: float


class HistoryResponse(BaseModel):
    """Risk history response model"""
    data: List[HistoryPoint]
    period_hours: int


class RefreshResponse(BaseModel):
    """Cache refresh response"""
    status: str
    message: str
    timestamp: str
