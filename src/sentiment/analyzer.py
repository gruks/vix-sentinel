"""
FinBERT Analyzer Module
Provides sentiment analysis using ProsusAI/finbert model
"""
from typing import List, Dict
from transformers import pipeline
import torch

# Simple in-memory cache for pipeline (TTL handled by API layer)
_finbert_pipeline = None


def load_finbert_pipeline():
    """
    Load FinBERT sentiment analysis pipeline with caching.
    
    Uses simple module-level caching to avoid re-downloading the model.
    
    Returns:
        transformers.pipeline: FinBERT sentiment pipeline
    """
    global _finbert_pipeline
    
    if _finbert_pipeline is not None:
        return _finbert_pipeline
    
    device = 0 if torch.cuda.is_available() else -1
    
    _finbert_pipeline = pipeline(
        "sentiment-analysis",
        model="ProsusAI/finbert",
        device=device,
        truncation=True,
        max_length=512
    )
    
    return _finbert_pipeline


def analyze_headline(headline: str, pipeline) -> Dict:
    """
    Analyze a single headline's sentiment.
    
    Args:
        headline: News headline text to analyze
        pipeline: Loaded FinBERT pipeline
        
    Returns:
        Dictionary with:
        - label: 'positive', 'negative', or 'neutral'
        - positive: probability score (0-1)
        - negative: probability score (0-1)
        - neutral: probability score (0-1)
        - score: composite score (-1 to +1) = positive - negative
    """
    # Handle empty headlines
    if not headline or not headline.strip():
        return {
            'label': 'neutral',
            'positive': 0.33,
            'negative': 0.33,
            'neutral': 0.34,
            'score': 0.0
        }
    
    # Get full probability distribution using topk=None
    result = pipeline(headline, topk=None)
    
    # Handle error cases
    if result is None or isinstance(result, str) or not isinstance(result, (list, tuple)):
        return {
            'label': 'neutral',
            'positive': 0.33,
            'negative': 0.33,
            'neutral': 0.34,
            'score': 0.0
        }
    
    result = result[0]
    
    # Handle case where result items are not dicts
    if not isinstance(result, dict):
        return {
            'label': 'neutral',
            'positive': 0.33,
            'negative': 0.33,
            'neutral': 0.34,
            'score': 0.0
        }
    
    # Convert list of results to dict
    try:
        probs = {item['label']: item['score'] for item in result}
    except (TypeError, KeyError):
        return {
            'label': 'neutral',
            'positive': 0.33,
            'negative': 0.33,
            'neutral': 0.34,
            'score': 0.0
        }
    
    # Calculate composite score: positive - negative (ranges -1 to +1)
    score = probs.get('positive', 0.33) - probs.get('negative', 0.33)
    
    # Determine label from highest probability
    label = max(probs, key=probs.get)
    
    return {
        'label': label,
        'positive': probs.get('positive', 0.33),
        'negative': probs.get('negative', 0.33),
        'neutral': probs.get('neutral', 0.34),
        'score': score
    }


def analyze_headlines(headlines: List[str], pipeline) -> List[Dict]:
    """
    Analyze multiple headlines' sentiment.
    
    Args:
        headlines: List of headline strings to analyze
        pipeline: Loaded FinBERT pipeline
        
    Returns:
        List of analysis results (one per headline)
    """
    # Filter empty headlines before processing
    valid_headlines = [h for h in headlines if h and h.strip()]
    
    if not valid_headlines:
        return []
    
    # Batch process via pipeline
    results = pipeline(valid_headlines, topk=None)
    
    analyzed = []
    for result in results:
        # Handle error cases where pipeline returns unexpected types
        if result is None:
            analyzed.append({
                'label': 'neutral',
                'positive': 0.33,
                'negative': 0.33,
                'neutral': 0.34,
                'score': 0.0
            })
            continue
            
        # Handle error case where pipeline returns string instead of list
        if isinstance(result, str):
            analyzed.append({
                'label': 'neutral',
                'positive': 0.33,
                'negative': 0.33,
                'neutral': 0.34,
                'score': 0.0
            })
            continue
            
        # If result is not a list, try to convert or skip
        if not isinstance(result, (list, tuple)):
            analyzed.append({
                'label': 'neutral',
                'positive': 0.33,
                'negative': 0.33,
                'neutral': 0.34,
                'score': 0.0
            })
            continue
            
        # Convert list to dict - handle case where items are not dicts
        try:
            probs = {item['label']: item['score'] for item in result}
        except (TypeError, KeyError):
            # If we can't parse the result, return neutral
            analyzed.append({
                'label': 'neutral',
                'positive': 0.33,
                'negative': 0.33,
                'neutral': 0.34,
                'score': 0.0
            })
            continue
        
        # Calculate composite score
        score = probs.get('positive', 0.33) - probs.get('negative', 0.33)
        
        # Determine label
        label = max(probs, key=probs.get)
        
        analyzed.append({
            'label': label,
            'positive': probs.get('positive', 0.33),
            'negative': probs.get('negative', 0.33),
            'neutral': probs.get('neutral', 0.34),
            'score': score
        })
    
    return analyzed


def get_sentiment_label(score: float) -> str:
    """
    Get sentiment label from score.
    
    Args:
        score: Sentiment score (-1 to +1)
        
    Returns:
        'positive', 'negative', or 'neutral'
    """
    if score > 0.1:
        return 'positive'
    elif score < -0.1:
        return 'negative'
    else:
        return 'neutral'
