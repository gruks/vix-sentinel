# AI Market Risk Early Warning System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-Frontend-61dafb)](https://reactjs.org/)
[![Transformers](https://img.shields.io/badge/HuggingFace-FinBERT-orange)](https://huggingface.co/)

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

This project detects **early warning signals** by combining:

- Market volatility indicators
- AI-based financial news sentiment
- Multi-source news aggregation
- Automated risk scoring
- High-performance asynchronous backend and intelligent caching

The system continuously analyzes these signals and produces a **unified market risk score** to help users identify potential instability before major price movements occur.

---

# Key Features

### Pure API Backend & Modern Frontend
- Fully decoupled **FastAPI** backend powering a fast, responsive **React (Vite/MUI)** frontend.
- Flexible time-range selection (1d, 2d, 10d, 30d) for market trend analysis.

### Intelligent News Caching
- Asynchronous SQLite caching (`aiosqlite`) for news articles.
- Automatically stores news (30-minute TTL) to drastically reduce excessive API calls.
- De-duplicates identical articles via SHA256 URL/title hashing.

### AI Financial Sentiment Analysis
- Uses **FinBERT** financial NLP model to immediately classify the sentiment of a headline into:
  - Positive
  - Neutral
  - Negative
- Aggregates sentiment across all supported news pathways.

### Multi-Source News Aggregation
Provides signals from both **financial and technology ecosystems**:
- Google News RSS
- TechCrunch RSS
- Hacker News API

### Real-Time Fast Interactive Dashboard
- Sleek **React UI** complete with skeleton loaders and adaptive layouts for all devices.
- Comprehensive charts rendered natively using **Recharts**.

### Automated Alerts
- Triggers email notifications automatically when the computed **risk exceeds critical thresholds** (Risk > 75).

---

# Tech Stack

### Backend
- **Python 3.11**
- **FastAPI** (REST Endpoints)
- **SQLite / aiosqlite** (Async caching)
- **Pandas** & **NumPy**

### Frontend
- **React (Vite)**
- **MUI (Material UI)** & **TailwindCSS**
- **Recharts** 

### Data Pipeline
- **yfinance**
- **feedparser**
- **Hacker News API**

### AI / NLP
- **HuggingFace Transformers**
- **FinBERT** financial sentiment model

---

# System Architecture

```text
      ┌───────────────────────────┐
      │       News Sources        │
      │ RSS Feeds + HN API        │
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
         ┌───────────────────┐       ┌────────────────────┐
         │ Risk Calculation  │──────►│ SQLite News Cache  │
         │ Volatility + NLP  │       └────────────────────┘
         └─────────┬─────────┘
                   │
                   ▼
         ┌───────────────────┐
         │ FastAPI Backend   │
         │ REST Endpoints    │
         └─────────┬─────────┘
                   │
                   ▼                 ┌───────────────────┐
         ┌───────────────────┐──────►│ Email Alerts      │
         │ React Frontend    │       │ Risk > Threshold  │
         │ Dashboard UI      │       └───────────────────┘
         └───────────────────┘
```

---

# Risk Scoring Algorithm

The market risk score is computed using a weighted combination of volatility and sentiment.

```python
risk_score = 0.6 * volatility_zscore + 0.4 * (1 - sentiment_score)
```

### Components

**Volatility Score**
- Rolling standard deviation of market returns
- Normalized using historical Z-score
- Gracefully handles floating point precision edge cases

**Sentiment Score**
- Average FinBERT sentiment across headlines
- Negative sentiment increases risk contribution

### Risk Levels

| Risk Score | Level | Meaning | Color Indicator |
|------------|------|--------|----------------|
| 0–40 | LOW | Stable market conditions | Green |
| 40–75 | MEDIUM | Elevated volatility or negative sentiment | Yellow |
| 75–100 | HIGH | Potential market instability | Red |

---

# Dashboard Components

The React dashboard provides multiple analytics modules:

### Real-Time Metrics & Gauge
- Risk score presented on a clearly thresholded circular gauge.
- High-level indicators for Volatility, Sentiment, and Risk Level.

### Flexible Time Span Analytics
- Adjustable time range views spanning 1d, 2d, 10d, 30d periods dynamically populated by the FastAPI backend.

### Detailed Charts
- Market trend visualizations and candlestick-style interfaces.
- News sentiment trend charts showing temporal sentiment flow.

---

# Project Structure

```text
ai-market-risk-warning
│
├── api/                  # FastAPI Backend API
│   ├── main.py           # API Endpoints
│   ├── models.py         # Pydantic models
│   └── db/               # SQLite database directory 
│
├── Market Risk Monitoring Dashboard/ # React Frontend
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
│
├── src/                  # Core Python Modules
│   ├── data_fetcher.py
│   ├── news_fetcher.py
│   ├── risk_calculator.py
│   ├── alert.py
│   ├── cache.py
│   └── sentiment/        # FinBERT Sentiment Engine
│
├── requirements.txt      # Python dependencies
├── README.md             # Documentation
└── .env.example          # Environment variables template
```

---

# Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ai-market-risk-warning.git
cd ai-market-risk-warning
```

### 2. Setup the Backend Environment

Create and activate a virtual environment, then install Python dependencies.

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Setup the Frontend

Enter the frontend directory and install dependencies:

```bash
cd "Market Risk Monitoring Dashboard"
npm install
cd ..
```

### 4. Run the System

You'll need two separate terminal windows.

**Terminal 1 (Backend FastAPI Server):**
Ensure your virtual environment is activated.
```bash
uvicorn api.main:app --port 8000 --reload
```

**Terminal 2 (Frontend React App):**
```bash
cd "Market Risk Monitoring Dashboard"
npm run dev
```

Your system is now accessible typically via `http://localhost:5173`.

---

# Environment Variables

Create a `.env` file in the root directory corresponding precisely to the backend configuration for alerts:

```env
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
ALERT_EMAIL=destination_email@domain.com
```

*Note: For Gmail, an "App Password" is required rather than your standard account password.*

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
- Real-time WebSockets streaming data integration

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
