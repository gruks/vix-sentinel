# Phase 4 Research: Alerts & Deployment

## Overview

Research findings for implementing Phase 4: Alerts & Deployment for the VIX Sentinel dashboard.

## Email Alert System

### Approach: Python smtplib

**Library:** Built-in `smtplib` + `email.mime` modules (no external dependencies needed)

**Configuration:**
- SMTP server: `smtp.gmail.com` port 587 (TLS)
- Authentication: Use Gmail App Password (not regular password)
- Environment variables via Streamlit secrets:
  - `SMTP_EMAIL`: Sender email address
  - `SMTP_PASSWORD`: App password (not regular password)
  - `ALERT_EMAIL`: Recipient email address

**Code Pattern:**
```python
import smtplib
from email.mime.text import MIMEText
import streamlit as st

def send_alert(subject, body):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = st.secrets.get('smtp_email', os.getenv('SMTP_EMAIL'))
        msg['To'] = st.secrets.get('alert_email', os.getenv('ALERT_EMAIL'))
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(
                st.secrets.get('smtp_email', os.getenv('SMTP_EMAIL')),
                st.secrets.get('smtp_password', os.getenv('SMTP_PASSWORD'))
            )
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Failed to send alert: {e}")
        return False
```

**Alert Logic:**
- Trigger when `avg_risk > 75` (HIGH threshold)
- Add cooldown to prevent spam (e.g., only send once per hour)
- Include current risk score, timestamp, and summary in email

### Alternative Options

| Option | Pros | Cons |
|--------|------|------|
| smtplib (chosen) | No external deps, free | Gmail requires app password |
| SendGrid | Reliable, templates | Requires API key |
| AWS SES | Scalable | More complex setup |

## Streamlit Cloud Deployment

### Requirements

1. **GitHub Repository:** Code must be in a GitHub repo
2. **requirements.txt:** All dependencies with versions
3. **Main file:** `app.py` in repo root or specify path
4. **Python version:** 3.9+ (Streamlit supports 3.9-3.12)

### Secrets Management

Streamlit Cloud uses `secrets.toml` pattern:

**Local development:** Create `.streamlit/secrets.toml`
```toml
[smtp]
email = "your-email@gmail.com"
password = "your-app-password"
alert_email = "recipient@example.com"
```

**Deployment:** Add secrets in Streamlit Cloud UI under "Advanced settings"

**Access in code:**
```python
import streamlit as st
import os

# Method 1: st.secrets (preferred)
email = st.secrets["smtp"]["email"]

# Method 2: Environment variable fallback
email = st.secrets.get("smtp_email", os.getenv("SMTP_EMAIL"))
```

### Auto-Refresh in Deployment

The existing `streamlit_autorefresh` library works in Streamlit Cloud:
- Already implemented in app.py
- 15-minute interval preserved
- No additional configuration needed

## Deployment Checklist

1. [ ] Create/update requirements.txt with all dependencies
2. [ ] Create .env.example template
3. [ ] Add email alert module
4. [ ] Add sidebar toggle for email alerts
5. [ ] Test locally with secrets.toml
6. [ ] Push to GitHub
7. [ ] Connect repo to Streamlit Community Cloud
8. [ ] Add secrets in Streamlit Cloud settings
9. [ ] Deploy and verify

## Dependencies to Add

For email functionality:
- No new pip packages needed (smtplib is built-in)

For requirements.txt update:
- `streamlit-autorefresh` (already in use)
- All existing dependencies with pinned versions

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Gmail blocks login | Use App Password, enable 2FA |
| Email goes to spam | Add sender to contacts, use proper headers |
| Secrets exposed | Never commit secrets.toml, use .gitignore |
| Rate limiting | Add cooldown between alerts |

## Key Decisions

1. **Email library:** Use built-in smtplib (no new dependencies)
2. **Secrets storage:** Streamlit secrets (st.secrets) with env var fallback
3. **Alert threshold:** Same as UI threshold (risk > 75)
4. **Cooldown:** 1 hour minimum between alerts to prevent spam

## References

- Streamlit Secrets: https://docs.streamlit.io/develop/concepts/connections/secrets-management
- Streamlit Cloud: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app
