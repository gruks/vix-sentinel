# Phase 1: Data Pipeline Foundation - Context

**Gathered:** 2026-03-08
**Status:** Ready for planning

<domain>
## Phase Boundary

Fetch and aggregate all market data and news sources. This is the data layer — prepares data for sentiment analysis (Phase 2) and risk calculation (Phase 3).

**Requirements:**
- DATA-01: Fetch real-time market data using yfinance (SPY, VIX)
- DATA-02: Calculate market volatility (rolling standard deviation of returns)
- DATA-03: Parse Google News RSS feeds for stock-related headlines
- DATA-04: Parse TechCrunch RSS feed for tech sector news
- DATA-05: Fetch top stories from Hacker News API
- DATA-06: Cache news data to avoid rate limiting

</domain>

<decisions>
## Implementation Decisions

### Default Tickers
- Primary: SPY (S&P 500 ETF proxy)
- Tech stocks: AAPL, TSLA, MSFT, NVDA, GOOGL
- Additional: VIX for volatility index

### News Sources
- Google News RSS: Dynamic queries per ticker (e.g., `https://news.google.com/rss/search?q=AAPL+OR+Apple+stock`)
- TechCrunch RSS: `https://techcrunch.com/feed/`
- Hacker News API: Top 5 stories from `https://hacker-news.firebaseio.com/v0/topstories.json`

### Data Limits
- Google News: Top 5 headlines per ticker
- TechCrunch: Top 3 articles
- Hacker News: Top 5 stories

### Caching
- Cache duration: 1 hour
- Use pickle or streamlit cache
- Fallback to cached data if fetch fails

### Error Handling
- Silent fail with cached data on source error
- Log errors for debugging
- Never crash the dashboard due to data fetch failures

</decisions>

<specifics>
## Specific Ideas

From project specification:
- "Fetch stock data using yfinance"
- "Google News RSS + TechCrunch RSS + Hacker News API instead of NewsAPI"
- "Limit: 10 articles/ticker. Cache 1h in pickle"
- Rate limit respect: 1s delay between RSS requests

No deviations from spec — standard implementation approaches accepted.

</specifics>

<deferred>
## Deferred Ideas

None — Phase 1 scope is fully defined.

</deferred>

---

*Phase: 01-data-pipeline*
*Context gathered: 2026-03-08*
