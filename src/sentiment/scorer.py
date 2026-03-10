"""
Sentiment Scorer Module
Maps sentiment analysis to risk contribution
"""
from typing import List, Dict


def calculate_average_sentiment(analyzed_headlines: List[Dict]) -> float:
    """
    Calculate average sentiment score across all analyzed headlines.
    
    Args:
        analyzed_headlines: List of headline analysis results,
            each containing 'score' field (-1 to +1)
            
    Returns:
        Average sentiment score (-1 to +1)
        Returns 0.0 if list is empty
    """
    if not analyzed_headlines:
        return 0.0
    
    # Extract all scores
    scores = [h['score'] for h in analyzed_headlines if 'score' in h]
    
    if not scores:
        return 0.0
    
    # Calculate mean
    return sum(scores) / len(scores)


def map_sentiment_to_risk(sentiment_score: float) -> float:
    """
    Map sentiment score to risk contribution.
    
    Uses the locked risk formula: 0.6*volatility + 0.4*(1-sentiment)
    This function implements only the sentiment portion.
    
    Args:
        sentiment_score: -1 (most negative) to +1 (most positive)
        
    Returns:
        Risk contribution from sentiment: 0.0 to 0.8
        - Negative sentiment (-1) -> risk = 0.4
        - Neutral sentiment (0) -> risk = 0.2
        - Positive sentiment (+1) -> risk = 0.0
    """
    # Normalize sentiment from [-1, 1] to [0, 1]
    normalized = (sentiment_score + 1) / 2
    
    # Risk contribution: 0.4 * (1 - normalized_sentiment)
    # Higher negative sentiment = higher risk
    risk = 0.4 * (1 - normalized)
    
    # Clamp to valid range
    return max(0.0, min(0.8, risk))


def calculate_combined_risk(volatility: float, sentiment_score: float) -> float:
    """
    Calculate combined risk from volatility and sentiment.
    
    Locked formula: risk = 0.6 * volatility + 0.4 * (1 - sentiment_normalized)
    
    Args:
        volatility: Market volatility score (0.0 to 1.0)
        sentiment_score: Sentiment score (-1 to +1)
        
    Returns:
        Combined risk score (0.0 to 1.0)
        Multiply by 100 for 0-100 scale
    """
    # Normalize sentiment from [-1, 1] to [0, 1]
    normalized_sentiment = (sentiment_score + 1) / 2
    
    # Combined risk formula
    risk = 0.6 * volatility + 0.4 * (1 - normalized_sentiment)
    
    # Clamp to valid range
    return max(0.0, min(1.0, risk))
