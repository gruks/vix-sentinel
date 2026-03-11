# Deployment Guide: VIX Sentinel to Streamlit Cloud

## Prerequisites
- GitHub repository with all code pushed
- Gmail account with 2FA enabled (for email alerts)

## Step 1: Prepare Secrets
1. Enable 2FA on your Gmail account
2. Generate an App Password:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Copy the 16-character app password

## Step 2: Deploy to Streamlit Cloud
1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select your repository, branch, and main file path (app.py)
5. Click "Deploy"

## Step 3: Configure Secrets (After Deployment)
1. In your deployed app page, click "Edit secrets" (gear icon)
2. Add the following:
   ```toml
   [smtp]
   email = "your-email@gmail.com"
   password = "your-app-password"
   alert_email = "recipient@example.com"
   ```
3. Click "Save"

## Step 4: Verify Deployment
- App should load with auto-refresh every 15 minutes
- Check sidebar shows "Enable email alerts" checkbox
- Enable alerts and verify configuration status

## Troubleshooting
- If emails fail: Check app password is correct (16 characters)
- If app won't load: Check requirements.txt has all dependencies
- Auto-refresh: Works automatically in cloud deployment
