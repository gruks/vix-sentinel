# Research Summary: AI Market Risk Early Warning System

**Domain:** Financial technology / Market risk monitoring dashboard
**Researched:** March 8, 2026
**Overall confidence:** HIGH

## Executive Summary

This research identifies the standard stack for building a market risk dashboard with sentiment analysis in 2025-2026. The recommended stack leverages Streamlit for rapid dashboard development, yfinance for free market data (S&P 500, VIX), Plotly for interactive visualizations, and FinBERT (via Hugging Face transformers) for financial sentiment analysis. This combination is well-established in the Python data science ecosystem, with all libraries actively maintained and compatible.

The key finding is that the Streamlit + yfinance + Plotly + FinBERT pattern is the de facto standard for rapid financial dashboard prototyping. All components are free (or have generous free tiers), work locally, and deploy easily to Streamlit Cloud. The 2-day prototype timeline is achievable with this stack.

## Key Findings

**Stack:** Streamlit 1.55.0 + yfinance 1.2.0 + Plotly 6.6.0 + FinBERT (transformers 5.3.0)

**Architecture:** Single-page Streamlit app with three data pipelines:
1. Market data pipeline (yfinance → pandas DataFrame)
2. News aggregation pipeline (RSS feeds + Hacker News API → unified news list)
3. Sentiment pipeline (FinBERT → sentiment scores → risk calculation)

**Critical pitfall:** FinBERT model download on first run can take 5-10 minutes. Need to cache or pre-download model for prototype演示.

## Implications for Roadmap

Based on research, the recommended phase structure for a 2-day prototype:

1. **Phase 1: Data Pipeline Foundation** - Set up yfinance for VIX/S&P 500 data, RSS feed parsing, and basic Streamlit layout
   - Addresses: FEATURES.md (real-time volatility display, news list)
   - Avoids: PITFALLS.md (starting with complex ML before data pipeline works)

2. **Phase 2: Sentiment Integration** - Add FinBERT for news sentiment analysis
   - Addresses: FEATURES.md (sentiment analysis feature)
   - Avoids: PITFALLS.md (model download delay blocking development)

3. **Phase 3: Risk Calculation & Visualization** - Build risk score algorithm and Plotly charts
   - Addresses: FEATURES.md (risk score, alerts, visualizations)
   - Avoids: PITFALLS.md (premature optimization of risk algorithm)

4. **Phase 4: Deployment** - Deploy to Streamlit Cloud
   - Addresses: FEATURES.md (deployment requirement)
   - Avoids: PITFALLS.md (deployment as afterthought)

**Phase ordering rationale:**
- Data pipeline must work before visualization makes sense
- Sentiment model needs separate module to avoid blocking UI development
- Risk algorithm can be simple (weighted average) for prototype, refined later

**Research flags for phases:**
- Phase 2 (Sentiment): Needs deeper research on FinBERT inference speed and batching for real-time updates
- Phase 3 (Risk Calculation): May need research on standard risk metrics beyond simple sentiment averaging
- Phases 1, 4: Standard patterns, unlikely to need additional research

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All versions verified from PyPI (March 2026). Library choices confirmed by multiple GitHub examples. |
| Features | HIGH | Based on project context provided and market analysis patterns. |
| Architecture | HIGH | Single-page Streamlit app is standard pattern for this use case. |
| Pitfalls | MEDIUM | Identified model download as key risk. Other pitfalls inferred from typical dashboard development patterns. |

## Gaps to Address

- **Risk algorithm specifics**: Research didn't cover exact risk score calculation formula. Recommend simple weighted average for prototype.
- **Hacker News API rate limits**: Didn't verify HN API rate limits. May need caching if aggressive polling.
- **Real-time update frequency**: Streamlit auto-refresh has tradeoffs. Need to determine optimal refresh rate.

## Sources

- PyPI package versions verified March 2026
- Hugging Face FinBERT model page: https://huggingface.co/ProsusAI/finbert
- Multiple GitHub repositories using Streamlit + yfinance + Plotly pattern
- Hacker News API documentation: https://github.com/HackerNews/API
