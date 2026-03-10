"""
Charts Module
Provides Plotly visualization functions for the risk dashboard.

Functions:
- create_gauge: Single gauge with threshold colors
- create_three_gauges: Three gauge figures for volatility, sentiment, risk
- create_candlestick: OHLC candlestick chart
- create_sentiment_line: Sentiment trend line chart
- create_volatility_heatmap: Ticker x day volatility heatmap
- create_risk_evolution: 24h risk score evolution with thresholds
- create_risk_banner: Risk alert message for Streamlit
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List, Dict, Tuple
import pandas as pd
from datetime import datetime


# Color definitions for risk levels
COLOR_LOW = "#4CAF50"      # GREEN - Low risk
COLOR_MEDIUM = "#FFC107"   # YELLOW - Medium risk
COLOR_HIGH = "#F44336"     # RED - High risk


def create_gauge(
    value: float, 
    title: str, 
    mode: str = "gauge+number",
    max_value: float = 100
) -> go.Figure:
    """
    Create a single Plotly gauge chart with threshold color steps.
    
    Args:
        value: Current value to display on gauge
        title: Title for the gauge
        mode: Display mode ("gauge", "number", "gauge+number")
        max_value: Maximum value for gauge axis (default 100)
    
    Returns:
        Plotly Figure object
    """
    # Cap display value at max_value for readability
    display_value = min(value, max_value)
    
    # Create gauge with threshold color steps
    fig = go.Figure(go.Indicator(
        mode=mode,
        value=display_value,
        title={'text': title},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': 'darkblue'},
            'steps': [
                {'range': [0, 40], 'color': COLOR_LOW},
                {'range': [40, 75], 'color': COLOR_MEDIUM},
                {'range': [75, max_value], 'color': COLOR_HIGH}
            ],
            'threshold': {
                'line': {'color': 'black', 'width': 2},
                'thickness': 0.75,
                'value': display_value
            }
        }
    ))
    
    # Update layout for better display
    fig.update_layout(
        font={'size': 14},
        margin=dict(l=20, r=20, t=50, b=20),
        height=250,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def create_three_gauges(
    volatility: float, 
    sentiment: float, 
    risk_score: float
) -> List[go.Figure]:
    """
    Create three gauge figures for volatility, sentiment, and risk score.
    
    Args:
        volatility: Volatility Z-score (can exceed 100, will be capped for display)
        sentiment: Sentiment score (0-1 scale, will be normalized to 0-100 for display)
        risk_score: Risk score (0-100)
    
    Returns:
        List of 3 Plotly Figure objects: [volatility_gauge, sentiment_gauge, risk_gauge]
    """
    gauges = []
    
    # Volatility gauge - cap display at 100 but show real value context
    vol_display = min(volatility * 20, 100)  # Scale z-score to readable range
    vol_gauge = create_gauge(
        value=vol_display,
        title="Volatility Z-Score",
        mode="gauge+number",
        max_value=100
    )
    vol_gauge.update_layout(title={'text': f"Volatility (actual: {volatility:.2f})"})
    gauges.append(vol_gauge)
    
    # Sentiment gauge - normalize from 0-1 to 0-100
    sent_display = sentiment * 100  # 0-1 -> 0-100
    sent_gauge = create_gauge(
        value=sent_display,
        title="Market Sentiment",
        mode="gauge+number",
        max_value=100
    )
    # Reverse colors for sentiment (high sentiment = low risk = green)
    sent_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=sent_display,
        title={'text': "Market Sentiment"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': 'darkblue'},
            'steps': [
                {'range': [0, 40], 'color': COLOR_HIGH},      # Negative sentiment
                {'range': [40, 60], 'color': COLOR_MEDIUM},  # Neutral
                {'range': [60, 100], 'color': COLOR_LOW}     # Positive sentiment
            ],
            'threshold': {
                'line': {'color': 'black', 'width': 2},
                'thickness': 0.75,
                'value': sent_display
            }
        }
    ))
    sent_gauge.update_layout(
        font={'size': 14},
        margin=dict(l=20, r=20, t=50, b=20),
        height=250,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    gauges.append(sent_gauge)
    
    # Risk gauge - uses standard risk colors (low=green, medium=yellow, high=red)
    risk_gauge = create_gauge(
        value=risk_score,
        title="Risk Score",
        mode="gauge+number",
        max_value=100
    )
    gauges.append(risk_gauge)
    
    return gauges


def create_candlestick(
    df: pd.DataFrame, 
    title: str = "SPY 7-Day Market Trend"
) -> go.Figure:
    """
    Create a candlestick chart for OHLC market data.
    
    Args:
        df: DataFrame with OHLC columns (Open, High, Low, Close)
        title: Chart title
    
    Returns:
        Plotly Figure object
    """
    if df.empty:
        # Return empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(title=title, height=400)
        return fig
    
    # Ensure we have the required columns
    required_cols = ['Open', 'High', 'Low', 'Close']
    if not all(col in df.columns for col in required_cols):
        # Try to use first 4 columns if named differently
        cols = list(df.columns)[:4]
        if len(cols) >= 4:
            df = df.rename(columns={
                cols[0]: 'Open',
                cols[1]: 'High', 
                cols[2]: 'Low',
                cols[3]: 'Close'
            })
    
    # Create candlestick chart
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        increasing_line_color='green',
        decreasing_line_color='red',
        name='SPY'
    )])
    
    # Update layout
    fig.update_layout(
        title=title,
        xaxis_rangeslider_visible=False,  # Hide range slider
        height=400,
        yaxis_title='Price ($)',
        xaxis_title='Date',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(240,240,240,0.5)',
        font=dict(size=12)
    )
    
    return fig


def create_sentiment_line(
    dates: List[str], 
    sentiment_values: List[float],
    title: str = "Sentiment Trend (7-Day Avg)"
) -> go.Figure:
    """
    Create a line chart showing sentiment trend over time.
    
    Args:
        dates: List of date strings
        sentiment_values: List of sentiment scores (0-1 scale)
        title: Chart title
    
    Returns:
        Plotly Figure object
    """
    if not dates or not sentiment_values:
        fig = go.Figure()
        fig.add_annotation(
            text="No sentiment data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(title=title, height=350)
        return fig
    
    # Calculate average sentiment for color
    avg_sentiment = sum(sentiment_values) / len(sentiment_values)
    
    # Determine line color based on average sentiment
    if avg_sentiment > 0.55:
        line_color = COLOR_LOW  # Green for positive
    elif avg_sentiment < 0.45:
        line_color = COLOR_HIGH  # Red for negative
    else:
        line_color = COLOR_MEDIUM  # Yellow for neutral
    
    # Create the line chart
    fig = go.Figure()
    
    # Add main sentiment line
    fig.add_trace(go.Scatter(
        x=dates,
        y=sentiment_values,
        mode='lines+markers',
        name='Sentiment',
        line=dict(color=line_color, width=3),
        marker=dict(size=8)
    ))
    
    # Add reference line at 0.5 (neutral)
    fig.add_hline(
        y=0.5, 
        line_dash="dash", 
        line_color="gray",
        annotation_text="Neutral",
        annotation_position="bottom right"
    )
    
    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Sentiment Score',
        yaxis_range=[0, 1],
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(240,240,240,0.5)',
        font=dict(size=12),
        showlegend=False
    )
    
    # Add background color bands for sentiment zones
    fig.add_shape(type="rect",
        x0=dates[0], x1=dates[-1],
        y0=0, y1=0.4,
        fillcolor=COLOR_HIGH, opacity=0.1,
        line_width=0,
        layer="below"
    )
    fig.add_shape(type="rect",
        x0=dates[0], x1=dates[-1],
        y0=0.4, y1=0.6,
        fillcolor=COLOR_MEDIUM, opacity=0.1,
        line_width=0,
        layer="below"
    )
    fig.add_shape(type="rect",
        x0=dates[0], x1=dates[-1],
        y0=0.6, y1=1,
        fillcolor=COLOR_LOW, opacity=0.1,
        line_width=0,
        layer="below"
    )
    
    return fig


def create_volatility_heatmap(
    volatility_data: Dict[str, List[float]], 
    tickers: List[str], 
    dates: List[str],
    title: str = "Volatility Heatmap"
) -> go.Figure:
    """
    Create a heatmap showing volatility across tickers and days.
    
    Args:
        volatility_data: Dictionary mapping ticker to list of daily volatilities
        tickers: List of ticker symbols
        dates: List of date labels
    
    Returns:
        Plotly Figure object
    """
    if not tickers or not dates or not volatility_data:
        fig = go.Figure()
        fig.add_annotation(
            text="No volatility data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(title=title, height=350)
        return fig
    
    # Build z-matrix (list of lists) from volatility data
    z_data = []
    for ticker in tickers:
        if ticker in volatility_data:
            vol_list = volatility_data[ticker]
            # Ensure we have same length as dates
            if len(vol_list) < len(dates):
                vol_list = vol_list + [None] * (len(dates) - len(vol_list))
            z_data.append(vol_list[:len(dates)])
        else:
            z_data.append([None] * len(dates))
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        x=dates,
        y=tickers,
        colorscale='RdYlGn_r',  # Red=high vol, Green=low vol (reversed)
        colorbar=dict(title="Volatility"),
        showscale=True
    ))
    
    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Ticker',
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(240,240,240,0.5)',
        font=dict(size=12)
    )
    
    return fig


def _hex_to_rgba(hex_color: str, alpha: float = 0.2) -> str:
    """Convert hex color to rgba format with alpha."""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f'rgba({r},{g},{b},{alpha})'


def create_risk_evolution(
    timestamps: List[datetime], 
    risk_scores: List[float],
    title: str = "Risk Score Evolution (24h)"
) -> go.Figure:
    """
    Create a line chart showing risk score evolution over time with threshold markers.
    
    Args:
        timestamps: List of datetime objects
        risk_scores: List of risk scores (0-100)
        title: Chart title
    
    Returns:
        Plotly Figure object
    """
    if not timestamps or not risk_scores:
        fig = go.Figure()
        fig.add_annotation(
            text="No risk evolution data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(title=title, height=350)
        return fig
    
    # Create figure
    fig = go.Figure()
    
    # Add threshold lines
    fig.add_hline(
        y=40, 
        line_dash="dash", 
        line_color=COLOR_LOW,
        annotation_text="LOW Threshold",
        annotation_position="bottom right"
    )
    fig.add_hline(
        y=75, 
        line_dash="dash", 
        line_color=COLOR_HIGH,
        annotation_text="HIGH Threshold",
        annotation_position="top right"
    )
    
    # Color line segments based on risk level
    # We'll use a single line but color the area under it
    
    # Determine dominant color based on average risk
    avg_risk = sum(risk_scores) / len(risk_scores)
    
    if avg_risk < 40:
        line_color = COLOR_LOW
    elif avg_risk <= 75:
        line_color = COLOR_MEDIUM
    else:
        line_color = COLOR_HIGH
    
    # Add the risk score line
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=risk_scores,
        mode='lines',
        name='Risk Score',
        line=dict(color=line_color, width=3),
        fill='tozeroy',
        fillcolor=_hex_to_rgba(line_color, 0.2)
    ))
    
    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title='Time',
        yaxis_title='Risk Score',
        yaxis_range=[0, 100],
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(240,240,240,0.5)',
        font=dict(size=12),
        showlegend=False
    )
    
    # Add background color bands
    fig.add_shape(type="rect",
        x0=timestamps[0], x1=timestamps[-1],
        y0=0, y1=40,
        fillcolor=COLOR_LOW, opacity=0.1,
        line_width=0,
        layer="below"
    )
    fig.add_shape(type="rect",
        x0=timestamps[0], x1=timestamps[-1],
        y0=40, y1=75,
        fillcolor=COLOR_MEDIUM, opacity=0.1,
        line_width=0,
        layer="below"
    )
    fig.add_shape(type="rect",
        x0=timestamps[0], x1=timestamps[-1],
        y0=75, y1=100,
        fillcolor=COLOR_HIGH, opacity=0.1,
        line_width=0,
        layer="below"
    )
    
    return fig


def create_risk_banner(risk_level: str, alert_type: str) -> Dict[str, str]:
    """
    Create a risk banner message for Streamlit display.
    
    Args:
        risk_level: Risk level - "LOW", "MEDIUM", or "HIGH"
        alert_type: Streamlit alert type - "success", "warning", or "error"
    
    Returns:
        Dictionary with 'message' and 'icon' keys for Streamlit display
    """
    messages = {
        "LOW": {
            "message": "Market conditions appear stable. Risk levels are within normal range.",
            "icon": "✓"
        },
        "MEDIUM": {
            "message": "Elevated volatility detected. Monitor positions closely.",
            "icon": "⚠"
        },
        "HIGH": {
            "message": "WARNING: High risk conditions. Consider defensive positioning.",
            "icon": "🚨"
        }
    }
    
    # Default to LOW if not recognized
    if risk_level not in messages:
        risk_level = "LOW"
    
    # Map alert_type to Streamlit
    if alert_type not in ["success", "warning", "error"]:
        alert_type = "success"  # Default
    
    return {
        "message": messages[risk_level]["message"],
        "icon": messages[risk_level]["icon"],
        "alert_type": alert_type
    }
