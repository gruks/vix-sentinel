"""
Email Alert Module for VIX Sentinel
Sends email notifications when risk exceeds threshold
"""
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime
import streamlit as st


# Cooldown storage - persists across reruns via session state
def _init_cooldown():
    """Initialize cooldown state if not exists."""
    if 'last_alert_time' not in st.session_state:
        st.session_state.last_alert_time = None


def check_alert_cooldown(hours=1):
    """
    Check if enough time has passed since last alert to prevent spam.
    
    Args:
        hours: Minimum hours between alerts (default: 1)
    
    Returns:
        bool: True if alert can be sent, False if cooldown is active
    """
    _init_cooldown()
    
    if st.session_state.last_alert_time is None:
        return True
    
    last_alert = st.session_state.last_alert_time
    now = datetime.now()
    
    # Calculate hours since last alert
    hours_since = (now - last_alert).total_seconds() / 3600
    
    return hours_since >= hours


def _get_smtp_config():
    """
    Get SMTP configuration from streamlit secrets or environment variables.
    
    Returns:
        dict: Configuration with email, password, and alert_email
    """
    # Try streamlit secrets first, fallback to environment variables
    smtp_email = st.secrets.get('smtp_email', os.getenv('SMTP_EMAIL'))
    smtp_password = st.secrets.get('smtp_password', os.getenv('SMTP_PASSWORD'))
    alert_email = st.secrets.get('alert_email', os.getenv('ALERT_EMAIL'))
    
    return {
        'smtp_email': smtp_email,
        'smtp_password': smtp_password,
        'alert_email': alert_email
    }


def is_valid_config():
    """
    Check if SMTP credentials are properly configured.
    
    Returns:
        bool: True if email and password are present, False otherwise
    """
    config = _get_smtp_config()
    
    # Check if required credentials are present
    smtp_email = config.get('smtp_email')
    smtp_password = config.get('smtp_password')
    
    # Validate that values are not None or empty strings
    if not smtp_email or not smtp_password:
        return False
    
    if smtp_email == 'your-email@gmail.com' or smtp_password == 'your-app-password':
        # Still using example values
        return False
    
    return True


def send_email_alert(risk_score, level, tickers, sentiment_summary):
    """
    Send an email alert when risk exceeds threshold.
    
    Args:
        risk_score (float): Current risk score (0-100)
        level (str): Risk level (LOW, MEDIUM, HIGH)
        tickers (list): List of tickers included in analysis
        sentiment_summary (str): Brief summary of sentiment analysis
    
    Returns:
        bool: True if email sent successfully, False on failure
    """
    _init_cooldown()
    
    # Check cooldown before sending
    if not check_alert_cooldown(hours=1):
        return False
    
    # Get configuration
    config = _get_smtp_config()
    smtp_email = config.get('smtp_email')
    smtp_password = config.get('smtp_password')
    alert_email = config.get('alert_email')
    
    # Validate configuration
    if not smtp_email or not smtp_password or not alert_email:
        return False
    
    # Skip if using example values
    if smtp_email == 'your-email@gmail.com' or smtp_password == 'your-app-password':
        return False
    
    try:
        # Create email message
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
        
        subject = f"VIX Sentinel Alert: {level} Risk Detected"
        
        body = f"""VIX Sentinel Market Risk Alert

Timestamp: {timestamp}
Risk Score: {risk_score:.1f}
Risk Level: {level}

Tickers Analyzed: {', '.join(tickers)}

Sentiment Summary: {sentiment_summary}

---
This is an automated alert from VIX Sentinel - AI Market Risk Early Warning System
"""
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = smtp_email
        msg['To'] = alert_email
        
        # Connect to Gmail SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.send_message(msg)
        
        # Update last alert time on success
        st.session_state.last_alert_time = datetime.now()
        
        return True
        
    except Exception as e:
        # Log error but don't crash - return False for graceful handling
        print(f"Failed to send email alert: {e}")
        return False
