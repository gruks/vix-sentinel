"""
News Fetcher Module
Aggregates news from multiple sources: Google News RSS, TechCrunch RSS, Hacker News API
"""
import feedparser
import requests
import time
from typing import List, Dict
from datetime import datetime
from functools import lru_cache


# Simple in-memory cache for news (TTL handled by API layer)
_cache = {}
_cache_ttl = 3600  # 1 hour


def fetch_google_news(ticker: str, limit: int = 5) -> List[Dict]:
    """
    Fetch news from Google News RSS for a given ticker.
    
    Args:
        ticker: Stock ticker symbol
        limit: Maximum number of headlines to return
    
    Returns:
        List of news items with title, source, published date
    """
    results = []
    
    try:
        # Build RSS feed URL for Google News
        query = f"{ticker}+stock+market"
        rss_url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}"
        
        # Parse RSS feed
        feed = feedparser.parse(rss_url)
        
        # Extract entries
        for entry in feed.entries[:limit]:
            news_item = {
                'title': entry.get('title', 'No title'),
                'source': entry.get('source', {}).get('title', 'Google News'),
                'published': entry.get('published', ''),
                'link': entry.get('link', ''),
                'ticker': ticker
            }
            results.append(news_item)
            
        # Respect rate limits
        time.sleep(1)
        
    except Exception as e:
        print(f"Error fetching Google News for {ticker}: {e}")
    
    return results


def fetch_techcrunch(limit: int = 3) -> List[Dict]:
    """
    Fetch tech news from TechCrunch RSS feed.
    
    Args:
        limit: Maximum number of articles to return
    
    Returns:
        List of news items with title, source, published date
    """
    results = []
    
    try:
        rss_url = "https://techcrunch.com/feed/"
        feed = feedparser.parse(rss_url)
        
        for entry in feed.entries[:limit]:
            news_item = {
                'title': entry.get('title', 'No title'),
                'source': 'TechCrunch',
                'published': entry.get('published', ''),
                'link': entry.get('link', ''),
                'ticker': None
            }
            results.append(news_item)
        
        time.sleep(1)
        
    except Exception as e:
        print(f"Error fetching TechCrunch: {e}")
    
    return results


def fetch_hacker_news(limit: int = 5) -> List[Dict]:
    """
    Fetch top stories from Hacker News API.
    
    Args:
        limit: Maximum number of stories to return
    
    Returns:
        List of news items with title, source, published date
    """
    results = []
    
    try:
        # Get top story IDs
        topstories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(topstories_url, timeout=10)
        
        if response.status_code == 200:
            story_ids = response.json()[:limit]
            
            # Fetch each story details
            for story_id in story_ids:
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                story_response = requests.get(story_url, timeout=10)
                
                if story_response.status_code == 200:
                    story = story_response.json()
                    if story:
                        news_item = {
                            'title': story.get('title', 'No title'),
                            'source': 'Hacker News',
                            'published': '',  # HN doesn't provide publish time in API
                            'link': story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                            'ticker': None
                        }
                        results.append(news_item)
                
                time.sleep(0.2)  # Rate limit
        
    except Exception as e:
        print(f"Error fetching Hacker News: {e}")
    
    return results


def fetch_all_news(tickers: List[str] = None) -> Dict:
    """
    Aggregate news from all sources.
    
    Args:
        tickers: List of stock tickers to fetch news for
    
    Returns:
        Dictionary with headlines and sources
    """
    if tickers is None:
        tickers = []
    
    all_headlines = []
    sources = {
        'google_news': [],
        'techcrunch': [],
        'hacker_news': []
    }
    
    # Fetch Google News for each ticker
    for ticker in tickers:
        google_news = fetch_google_news(ticker)
        all_headlines.extend(google_news)
        sources['google_news'].extend(google_news)
    
    # Fetch TechCrunch
    techcrunch_news = fetch_techcrunch()
    all_headlines.extend(techcrunch_news)
    sources['techcrunch'] = techcrunch_news
    
    # Fetch Hacker News
    hn_news = fetch_hacker_news()
    all_headlines.extend(hn_news)
    sources['hacker_news'] = hn_news
    
    return {
        'headlines': all_headlines,
        'sources': sources,
        'timestamp': datetime.now().isoformat()
    }


def fetch_news_for_display(tickers: List[str] = None) -> Dict:
    """
    Convenience function to fetch news for display in the dashboard.
    
    Args:
        tickers: List of stock tickers
    
    Returns:
        Formatted news data for display
    """
    if tickers is None:
        tickers = ['SPY', 'VIX', 'AAPL', 'TSLA', 'MSFT']
    
    news_data = fetch_all_news(tickers)
    
    # Format for display
    display_data = {
        'total_articles': len(news_data['headlines']),
        'articles': news_data['headlines'],
        'by_source': {
            'Google News': len(news_data['sources']['google_news']),
            'TechCrunch': len(news_data['sources']['techcrunch']),
            'Hacker News': len(news_data['sources']['hacker_news'])
        },
        'last_updated': news_data['timestamp']
    }
    
    return display_data
