"""
Sentiment Analysis Module
Provides FinBERT-based sentiment analysis for financial headlines
"""
from src.sentiment.analyzer import (
    load_finbert_pipeline,
    analyze_headline,
    analyze_headlines
)
from src.sentiment.scorer import (
    calculate_average_sentiment,
    map_sentiment_to_risk,
    calculate_combined_risk
)

__all__ = [
    'load_finbert_pipeline',
    'analyze_headline',
    'analyze_headlines',
    'calculate_average_sentiment',
    'map_sentiment_to_risk',
    'calculate_combined_risk'
]
