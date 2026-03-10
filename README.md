# AI Market Risk Early Warning System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)](https://streamlit.io/)
[![Transformers](https://img.shields.io/badge/HuggingFace-FinBERT-orange)](https://huggingface.co/)
[![Plotly](https://img.shields.io/badge/Plotly-InteractiveCharts-blue)](https://plotly.com/)
[![Deployment](https://img.shields.io/badge/Deployment-StreamlitCloud-green)](https://streamlit.io/cloud)


**AI Market Risk Early Warning System** is a real-time financial monitoring platform that detects early signals of potential market instability using **market volatility indicators combined with AI-powered news sentiment analysis**.


The system aggregates financial news from multiple sources, analyzes sentiment using **FinBERT**, and combines it with volatility signals to produce a **clear Risk Score (0–100)** with automated alerts.


Inspired by internal monitoring dashboards used in modern fintech and quantitative trading environments.


---


# Table of Contents


- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Risk Scoring Algorithm](#risk-scoring-algorithm)
- [Dashboard Components](#dashboard-components)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Environment Variables](#environment-variables)
- [Data Sources](#data-sources)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)


---


# Overview


Financial markets react quickly to macroeconomic events, news sentiment, and volatility spikes.


Most traders rely on **lagging indicators**, which means risk signals often appear **after the market has already moved**.


This project attempts to detect **early warning signals** by combining:


- Market volatility indicators
- AI-based financial news sentiment
- Multi-source news aggregation
- Automated risk scoring


The system continuously analyzes these signals and produces a **unified market risk score** to help users identify potential instability before major price movements occur.


---


# Key Features


### Real-Time Market Monitoring
- Fetches live market data using **yfinance**
- Tracks **S&P 500 proxy (SPY)** and volatility indicators
- Calculates rolling volatility metrics


### AI Financial Sentiment Analysis
- Uses **FinBERT** financial NLP model
- Classifies headlines into:
  - Positive
  - Neutral
  - Negative
- Aggregates sentiment across multiple news sources


### Multi-Source News Aggregation
News is collected from:


- Google News RSS
- TechCrunch RSS
- Hacker News API


This provides signals from both **financial and technology ecosystems**.


### Intelligent Risk Scoring
Combines volatility and sentiment signals to generate a **single interpretable market risk score**.


### Interactive Dashboard
Built with **Streamlit + Plotly** for fast and interactive visualizations.


### Automated Alerts
Triggers email alerts when **risk exceeds critical thresholds**.


---


# Tech Stack


### Backend


- Python 3.11
- Pandas
- NumPy


### Data Pipeline


- yfinance
- feedparser
- Hacker News API


### AI / NLP


- HuggingFace Transformers
- FinBERT financial sentiment model


### Visualization


- Streamlit
- Plotly


### Deployment


- Streamlit Cloud


---


# System Architecture


      ┌───────────────────────────┐
      │       News Sources        │
      │ RSS Feeds + HN API       │
      └─────────────┬─────────────┘
                    │
                    ▼
         ┌───────────────────┐
         │ Sentiment Engine  │
         │ FinBERT NLP Model │
         └─────────┬─────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │ Market Data Engine  │
        │ yfinance API        │
        └─────────┬───────────┘
                  │
                  ▼
         ┌───────────────────┐
         │ Risk Calculation  │
         │ Volatility + NLP  │
         └─────────┬─────────┘
                   │
                   ▼
         ┌───────────────────┐
         │ Streamlit UI      │
         │ Dashboard         │
         └─────────┬─────────┘
                   │
                   ▼
         ┌───────────────────┐
         │ Email Alerts      │
         │ Risk > Threshold  │
         └───────────────────┘


---


# Risk Scoring Algorithm


The market risk score is computed using a weighted combination of volatility and sentiment.




risk_score = 0.6 * volatility_zscore + 0.4 * (1 - sentiment_score)




### Components


**Volatility Score**
- Rolling standard deviation of market returns
- Normalized using historical Z-score


**Sentiment Score**
- Average FinBERT sentiment across headlines
- Negative sentiment increases risk contribution


### Risk Levels


| Risk Score | Level | Meaning |
|------------|------|--------|
| 0–40 | LOW | Stable market conditions |
| 40–75 | MEDIUM | Elevated volatility or negative sentiment |
| 75–100 | HIGH | Potential market instability |


---


# Dashboard Components


The Streamlit dashboard provides multiple analytics modules:


### Market Overview
- SPY candlestick chart
- Market trend visualization


### Sentiment Analysis
- Sentiment trend graph
- Headline sentiment classification


### Risk Monitoring
- Risk score gauge
- Historical risk trend


### Volatility Analysis
- Market volatility heatmap
- Per-ticker breakdown


### Alerts Panel
- Color-coded alert banner
- Email notifications for critical risk levels


---


# Project Structure




ai-market-risk-warning
│
├── app.py
├── risk_engine.py
├── sentiment_engine.py
├── data_pipeline.py
├── alert_system.py
│
├── requirements.txt
├── README.md
├── .env.example
└── assets/




---


# Setup and Installation


Clone the repository




git clone https://github.com/yourusername/ai-market-risk-warning


cd ai-market-risk-warning




Create a virtual environment




python -m venv venv
source venv/bin/activate




Install dependencies




pip install -r requirements.txt




Run the dashboard




streamlit run app.py




---


# Environment Variables


Create a `.env` file:




EMAIL_USER=your_email
EMAIL_PASSWORD=your_password
ALERT_EMAIL=destination_email




Used for automated **risk alert notifications**.


---


# Data Sources


| Source | Purpose |
|------|------|
| yfinance | Market price and volatility data |
| Google News RSS | Financial headlines |
| TechCrunch RSS | Technology sector news |
| Hacker News API | Startup and tech discussions |


---


# Future Improvements


- Historical crash backtesting
- Multi-asset monitoring
- Portfolio-level risk scoring
- Customizable risk formula
- LLM-based financial news summarization
- Real-time streaming data integration


---


# Contributing


Contributions are welcome.


1. Fork the repository  
2. Create a feature branch  
3. Commit your changes  
4. Submit a pull request  


---


# License


MIT License


---


# Disclaimer


This project is for **educational and research purposes only**.


It does **not provide financial advice or trading recommendations**.
