"""
FinBERT Analyzer Module
Provides sentiment analysis using ProsusAI/finbert model
"""
from typing import List, Dict
import streamlit as st
from transformers import pipeline
import torch


@st.cache_resource
def load_finbert_pipeline():
    """
    Load FinBERT sentiment analysis pipeline with caching.
    
    Uses @st.cache_resource to avoid re-downloading the model
    on each Streamlit rerun.
    
    Returns:
        transformers.pipeline: FinBERT sentiment pipeline
    """
    device = 0 if torch.cuda.is_available() else -1
    
    return pipeline(
        "sentiment-analysis",
        model="ProsusAI/finbert",
        device=device,
        truncation=True,
        max_length=512
    )


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
    result = pipeline(headline, topk=None)[0]
    
    # Convert list of results to dict
    probs = {item['label']: item['score'] for item in result}
    
    # Calculate composite score: positive - negative (ranges -1 to +1)
    score = probs['positive'] - probs['negative']
    
    # Determine label from highest probability
    label = max(probs, key=probs.get)
    
    return {
        'label': label,
        'positive': probs['positive'],
        'negative': probs['negative'],
        'neutral': probs['neutral'],
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
        # Convert list to dict
        probs = {item['label']: item['score'] for item in result}
        
        # Calculate composite score
        score = probs['positive'] - probs['negative']
        
        # Determine label
        label = max(probs, key=probs.get)
        
        analyzed.append({
            'label': label,
            'positive': probs['positive'],
            'negative': probs['negative'],
            'neutral': probs['neutral'],
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
