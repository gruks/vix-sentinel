"""
Risk Calculator Module
Provides risk calculation functions combining volatility Z-scores with sentiment data.

LOCKED FORMULA: risk = 0.6 * vol_z + 0.4 * (1 - sentiment)
THRESHOLDS: LOW (<40), MEDIUM (40-75), HIGH (>75)
"""
import numpy as np
from typing import List, Tuple, Dict, Optional


def calculate_volatility_zscore(current_vol: float, historical_vols: List[float]) -> float:
    """
    Calculate volatility Z-score normalized against historical mean.
    
    The Z-score indicates how many standard deviations the current volatility
    is from the historical average. A positive Z-score means current
    volatility is higher than historical average.
    
    Args:
        current_vol: Current volatility value (e.g., 0.20 for 20%)
        historical_vols: List of historical volatility values
        
    Returns:
        Z-score as float. Returns 0.0 if:
        - historical_vols has fewer than 2 values
        - standard deviation is 0 (no variation in historical data)
    """
    # Edge case: insufficient historical data
    if not historical_vols or len(historical_vols) < 2:
        return 0.0
    
    # Convert to numpy array for calculations
    hist_array = np.array(historical_vols)
    
    # Calculate mean and standard deviation
    mean = np.mean(hist_array)
    std = np.std(hist_array, ddof=1)  # Sample standard deviation
    
    # Edge case: no variation in historical data (std is ~0 due to floating point)
    if std < 1e-10:
        return 0.0
    
    # Calculate Z-score
    zscore = (current_vol - mean) / std
    
    return float(zscore)


def normalize_sentiment(sentiment_value: float) -> float:
    """
    Normalize sentiment score to 0-1 scale.
    
    Args:
        sentiment_value: Sentiment in -1 to +1 range or 0-1 range
        
    Returns:
        Normalized sentiment in 0-1 scale
    """
    # If in -1 to +1 range (or 0 which is ambiguous - assume -1 to +1), normalize to 0-1
    # -1 -> 0, 0 -> 0.5, +1 -> 1
    if sentiment_value <= 1.0 and sentiment_value >= -1.0:
        normalized = (sentiment_value + 1) / 2
        return max(0.0, min(1.0, normalized))
    
    # If already in 0-1 range (or greater than 1), return as-is
    return max(0.0, min(1.0, sentiment_value))


def calculate_risk_score(vol_zscore: float, sentiment_score: float) -> float:
    """
    Calculate combined risk score using LOCKED formula.
    
    LOCKED FORMULA: risk = 0.6 * vol_z + 0.4 * (1 - sentiment)
    
    The formula combines:
    - Volatility Z-score (0.6 weight): higher volatility = higher risk
    - Sentiment (0.4 weight): negative sentiment = higher risk
    
    Args:
        vol_zscore: Volatility Z-score (can be negative or positive)
        sentiment_score: Sentiment in 0-1 scale (0=negative, 1=positive)
        
    Returns:
        Risk score in 0-100 scale
    """
    # Normalize sentiment to 0-1 scale
    normalized_sentiment = normalize_sentiment(sentiment_score)
    
    # Apply LOCKED formula: 0.6 * vol_z + 0.4 * (1 - sentiment)
    # Note: sentiment is inverted so negative sentiment = higher risk
    risk_contribution = 0.6 * vol_zscore + 0.4 * (1 - normalized_sentiment)
    
    # Scale to 0-100
    risk_score = risk_contribution * 100
    
    # Clamp to valid range (can be negative if vol_zscore is very negative)
    return max(0.0, min(100.0, risk_score))


def get_risk_level(risk_score: float) -> Tuple[str, str, str]:
    """
    Determine risk level and alert colors based on LOCKED thresholds.
    
    LOCKED THRESHOLDS:
    - < 40: LOW, GREEN, success
    - 40-75: MEDIUM, YELLOW, warning  
    - > 75: HIGH, RED, error
    
    Args:
        risk_score: Risk score in 0-100 scale
        
    Returns:
        Tuple of (level, color, alert_type):
        - level: "LOW", "MEDIUM", or "HIGH"
        - color: "GREEN", "YELLOW", or "RED"  
        - alert_type: "success", "warning", or "error" (for Streamlit)
    """
    if risk_score < 40:
        return ("LOW", "GREEN", "success")
    elif risk_score <= 75:
        return ("MEDIUM", "YELLOW", "warning")
    else:
        return ("HIGH", "RED", "error")


def get_all_metrics(
    volatility: float,
    historical_vols: List[float],
    sentiment_score: float
) -> Dict:
    """
    Calculate all risk metrics in a single call.
    
    Combines Z-score calculation, sentiment normalization, risk scoring,
    and level determination into one comprehensive dict for dashboard display.
    
    Args:
        volatility: Current volatility value
        historical_vols: List of historical volatility values
        sentiment_score: Sentiment score (can be -1 to +1 or 0-1)
        
    Returns:
        Dictionary with all calculated metrics:
        - vol_zscore: Volatility Z-score
        - normalized_sentiment: Sentiment normalized to 0-1
        - risk_score: Combined risk score (0-100)
        - level: Risk level ("LOW", "MEDIUM", "HIGH")
        - color: Alert color ("GREEN", "YELLOW", "RED")
        - alert_type: Streamlit alert type ("success", "warning", "error")
    """
    # Calculate volatility Z-score
    vol_zscore = calculate_volatility_zscore(volatility, historical_vols)
    
    # Normalize sentiment
    normalized_sentiment = normalize_sentiment(sentiment_score)
    
    # Calculate risk score
    risk_score = calculate_risk_score(vol_zscore, normalized_sentiment)
    
    # Determine risk level
    level, color, alert_type = get_risk_level(risk_score)
    
    return {
        'vol_zscore': vol_zscore,
        'normalized_sentiment': normalized_sentiment,
        'risk_score': risk_score,
        'level': level,
        'color': color,
        'alert_type': alert_type
    }
