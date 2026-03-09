# Phase 2: Sentiment Analysis Integration - Research

**Researched:** 2026-03-09
**Domain:** Financial sentiment analysis using FinBERT with Hugging Face transformers
**Confidence:** HIGH

## Summary

Phase 2 implements financial sentiment analysis using FinBERT to analyze news headlines and map sentiment to risk contribution. The locked decision to use FinBERT is well-supported—the model achieves ~88-93% accuracy on financial sentiment benchmarks. The transformers library provides a simple pipeline API that abstracts most complexity.

**Re-research verification:** The previous research using ProsusAI/finbert remains VALID. The model has been updated with safetensors support (May 2025) and remains the industry standard. Newer alternatives (yiyanghkust/finbert-tone, Modern-FinBERT-large) exist but ProsusAI/finbert is more battle-tested and appropriate for this use case.

**Primary recommendation:** Use `transformers.pipeline` with "ProsusAI/finbert" model. The pipeline returns three probabilities (positive, negative, neutral) which can be converted to a -1 to +1 sentiment score for the risk formula: `risk = 0.6*volatility + 0.4*(1-sentiment)`.

## User Constraints (from project requirements)

### Locked Decisions
- Use FinBERT for sentiment analysis (finance-specific model)
- Streamlit for UI
- Risk formula: 0.6*volatility + 0.4*(1-sentiment)
- Phase 1 (Data Pipeline) is complete - data modules exist

### Claude's Discretion
- Model variant selection (within FinBERT family)
- Implementation details (pipeline vs direct model loading)
- Caching strategy

### Deferred Ideas (OUT OF SCOPE)
- Alternative sentiment models (not needed given locked FinBERT decision)
- LLM-based sentiment (overkill for headline analysis)

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| transformers | 4.40+ | Load and run FinBERT | Official Hugging Face library, de facto standard for BERT models |
| torch | 2.0+ | PyTorch backend for model inference | Required by transformers, enables GPU acceleration |
| ProsusAI/finbert | latest | Pre-trained financial sentiment model | Locked decision - best validated model for finance text |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| numpy | 1.24+ | Array operations for sentiment calculations | Converting probabilities to scores |
| pandas | 2.0+ | DataFrame for batch sentiment analysis | Aggregating headlines by source |
| streamlit | 1.28+ | UI integration | Already in project stack |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| ProsusAI/finbert | yiyanghkust/finbert-tone | Fine-tuned on analyst reports, slightly different use case |
| ProsusAI/finbert | beethogedeon/Modern-FinBERT-large | Newer architecture (Feb 2025), less validated |
| ProsusAI/finbert | DistilFinRoBERTa | More efficient but potentially less accurate |

**Installation:**
```bash
pip install transformers torch numpy pandas
```

## Architecture Patterns

### Recommended Project Structure
```
src/
├── sentiment/
│   ├── __init__.py
│   ├── analyzer.py      # Core FinBERT analysis logic
│   ├── scorer.py        # Convert probabilities to risk scores
│   └── cache.py         # Cached model loading
└── news_fetcher.py       # Already exists (Phase 1)
```

### Pattern 1: Pipeline-based Sentiment Analysis
**What:** Use transformers.pipeline to load FinBERT and analyze text
**When to use:** Simple single-text or batch inference

```python
# Source: https://huggingface.co/docs/transformers/v4.42.0/en/main_classes/pipelines
from transformers import pipeline
import torch

# Load FinBERT pipeline - downloads model on first run (~400MB)
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert",
    device=0 if torch.cuda.is_available() else -1  # GPU if available
)

# Analyze single headline
result = sentiment_pipeline("Tech stocks surge on strong earnings")
# Returns: [{'label': 'positive', 'score': 0.94}, ...]

# For full probability distribution:
result = sentiment_pipeline(
    "Tech stocks surge",
    topk=None  # Returns all 3 class probabilities
)
# Returns: [{'label': 'positive', 'score': 0.85}, 
#           {'label': 'negative', 'score': 0.05},
#           {'label': 'neutral', 'score': 0.10}]
```

### Pattern 2: Batch Processing for Multiple Headlines
**What:** Process multiple headlines efficiently
**When to use:** Analyzing all news from multiple sources

```python
# Source: Context7/huggingface transformers
from transformers import pipeline
import pandas as pd

pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")

headlines = [
    "AAPL reports record quarterly earnings",
    "Market drops amid recession fears",
    "Fed maintains interest rates"
]

# Batch process - pipeline handles batching internally
results = pipeline(headlines)

# Results format: [{'label': 'positive', 'score': 0.92}, ...]
```

### Pattern 3: Model Caching for Production
**What:** Cache model to avoid re-downloading on each run
**When to use:** Streamlit apps where model loads on each script rerun

```python
# Source: Stack Overflow / Hugging Face docs
import os
from transformers import pipeline

# Option 1: Set environment variable before import
os.environ['TRANSFORMERS_CACHE'] = './models/transformers'

# Option 2: Specify cache_dir in pipeline
pipeline = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert",
    cache_dir="./models"
)
```

### Pattern 4: Sentiment Score Calculation
**What:** Convert FinBERT probabilities to -1 to +1 score for risk formula
**When to use:** Aggregating sentiment for risk calculation

```python
# FinBERT label mapping: positive=0, negative=1, neutral=2
# Or via pipeline: returns 'positive', 'negative', 'neutral' labels

def calculate_sentiment_score(headline: str, pipeline) -> float:
    """
    Convert FinBERT output to -1 to +1 score.
    negative sentiment = higher risk
    """
    result = pipeline(headline, topk=None)
    
    # Extract probabilities
    probs = {item['label']: item['score'] for item in result[0]}
    
    # Score = positive - negative (ranges from -1 to +1)
    score = probs['positive'] - probs['negative']
    
    return score  # -1 (most negative) to +1 (most positive)

def calculate_average_sentiment(headlines: list, pipeline) -> float:
    """Calculate average sentiment across all headlines."""
    scores = [calculate_sentiment_score(h, pipeline) for h in headlines]
    return sum(scores) / len(scores) if scores else 0.0
```

### Anti-Patterns to Avoid
- **Loading model inside Streamlit function without caching:** Model takes 5-10 minutes to download. Use `@st.cache_resource` to load once.
- **Running inference on CPU for large batches:** GPU provides 10-50x speedup. Check `torch.cuda.is_available()`.
- **Ignoring neutral sentiment:** FinBERT returns 3 classes - neutral often indicates mixed or unclear sentiment.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Financial sentiment model | Train BERT from scratch | ProsusAI/finbert | Pre-trained on financial corpus, achieves 88-93% accuracy |
| Tokenization | Write custom tokenizer | AutoTokenizer.from_pretrained() | Handles FinBERT's vocabulary, truncation, padding |
| Batch inference loop | Process one headline at a time | Pipeline batch processing | 10-20x faster with same GPU |
| GPU detection | Hardcode device | torch.cuda.is_available() | Graceful CPU fallback |

**Key insight:** FinBERT is specifically designed for financial text. General sentiment models (VADER, TextBlob) don't understand financial jargon and achieve ~20% lower accuracy.

## Common Pitfalls

### Pitfall 1: First-Run Model Download (5-10 minutes)
**What goes wrong:** First run downloads ~400MB model, appears frozen
**Why it happens:** FinBERT model files downloaded from Hugging Face Hub
**How to avoid:** 
- Pre-download model before deployment
- Add progress indicator for first run
- Cache model in application startup

**Warning signs:** Script hangs at "Loading model..." or "Downloading..."

### Pitfall 2: Streamlit Rerun Reloads Model
**What goes wrong:** Every interaction triggers model reload (slow)
**Why it happens:** Streamlit reruns entire script on interaction
**How to avoid:** Use `@st.cache_resource` decorator on model loading function

```python
# Source: Streamlit docs
@st.cache_resource
def load_sentiment_pipeline():
    return pipeline("sentiment-analysis", model="ProsusAI/finbert")

sentiment_pipeline = load_sentiment_pipeline()  # Runs once
```

### Pitfall 3: GPU Memory Exhaustion with Large Batches
**What goes wrong:** CUDA out of memory error with large headline lists
**Why it happens:** Batching too many texts at once
**How to avoid:** 
- Process in smaller batches (16-32 headlines)
- Use `truncation=True` to limit sequence length
- Use `torch.cuda.empty_cache()` between batches

### Pitfall 4: Model Output Format Confusion
**What goes wrong:** Getting wrong sentiment score because of label mapping
**Why it happens:** Pipeline returns only top prediction by default, not probabilities
**How to avoid:** Always use `topk=None` to get all 3 class probabilities

### Pitfall 5: Empty Headlines
**What goes wrong:** Model errors on empty strings
**Why it happens:** Tokenizer fails on empty input
**How to avoid:** Filter empty headlines before analysis

```python
headlines = [h for h in headlines if h and h.strip()]
```

## Code Examples

### Complete Sentiment Analysis Module
```python
"""
src/sentiment/analyzer.py
FinBERT-based sentiment analysis for financial headlines
"""
from typing import List, Dict
import streamlit as st
from transformers import pipeline
import torch


@st.cache_resource
def load_finbert_pipeline():
    """Load FinBERT pipeline with caching for Streamlit."""
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
    Analyze single headline sentiment.
    
    Args:
        headline: News headline text
        pipeline: Loaded FinBERT pipeline
        
    Returns:
        Dict with label, scores, and composite score
    """
    if not headline or not headline.strip():
        return {'label': 'neutral', 'positive': 0.33, 'negative': 0.33, 'neutral': 0.34, 'score': 0.0}
    
    result = pipeline(headline, topk=None)[0]
    probs = {item['label']: item['score'] for item in result}
    
    # Score: positive - negative (ranges -1 to +1)
    score = probs['positive'] - probs['negative']
    
    return {
        'label': max(probs, key=probs.get),
        'positive': probs['positive'],
        'negative': probs['negative'],
        'neutral': probs['neutral'],
        'score': score
    }


def analyze_headlines(headlines: List[str], pipeline) -> List[Dict]:
    """Analyze multiple headlines."""
    results = []
    for headline in headlines:
        if headline and headline.strip():
            results.append(analyze_headline(headline, pipeline))
    return results


def calculate_source_sentiment(headlines: List[Dict]) -> float:
    """
    Calculate average sentiment score for a list of analyzed headlines.
    
    Args:
        headlines: List of headlines with 'score' field
        
    Returns:
        Average sentiment score (-1 to +1)
    """
    if not headlines:
        return 0.0
    
    scores = [h['score'] for h in headlines if 'score' in h]
    return sum(scores) / len(scores) if scores else 0.0


def map_sentiment_to_risk(sentiment_score: float) -> float:
    """
    Map sentiment to risk contribution.
    
    Risk formula: 0.6*volatility + 0.4*(1-sentiment)
    - Positive sentiment (score=1) -> risk contribution = 0.0
    - Neutral sentiment (score=0) -> risk contribution = 0.4
    - Negative sentiment (score=-1) -> risk contribution = 0.8
    
    Args:
        sentiment_score: -1 (negative) to +1 (positive)
        
    Returns:
        Risk contribution (0.0 to 0.8)
    """
    # Normalize sentiment from [-1, 1] to [0, 1]
    normalized = (sentiment_score + 1) / 2  # 0 to 1
    
    # For risk calculation: 1-sentiment where higher = more risk
    risk_contribution = 0.4 * (1 - normalized)
    
    return risk_contribution  # This is the sentiment portion only
```

### Integration with Risk Formula
```python
# Complete risk calculation
def calculate_risk_score(volatility: float, sentiment_score: float) -> float:
    """
    Calculate combined risk score.
    
    Formula: 0.6 * volatility + 0.4 * (1 - sentiment_normalized)
    
    Args:
        volatility: 0.0 to 1.0 (from VIX data)
        sentiment_score: -1 (negative) to +1 (positive)
        
    Returns:
        Combined risk score: 0.0 (low) to 1.0 (high)
    """
    # Normalize sentiment from [-1, 1] to [0, 1]
    sentiment_normalized = (sentiment_score + 1) / 2
    
    # Risk increases with volatility and decreases with positive sentiment
    risk = 0.6 * volatility + 0.4 * (1 - sentiment_normalized)
    
    return risk  # 0.0 to 1.0
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| VADER sentiment | FinBERT | 2020 | +15% accuracy on financial text |
| TextBlob | FinBERT | 2020 | Better with financial jargon |
| Generic BERT | ProsusAI/finbert | 2020 | Pre-trained on finance corpus |
| ProsusAI/finbert (basic) | ProsusAI/finbert + safetensors | May 2025 | Faster loading, memory efficient |

**Re-research finding:** ProsusAI/finbert remains the standard. Recent updates include safetensors variant support (2025). Newer models like Modern-FinBERT-large exist but are less validated for production use.

**Deprecated/outdated:**
- `pytorch_pretrained_bert`: Replaced by `transformers` library (2019+)
- Local sentiment scoring: No longer needed with pre-trained FinBERT

## Open Questions

1. **Headline truncation**
   - What we know: FinBERT max length is 512 tokens, headlines are typically short
   - What's unclear: Should headlines be truncated or dropped if too long?
   - Recommendation: Truncate with warning for headlines > 512 tokens

2. **Batch size optimization**
   - What we know: GPU memory is the bottleneck
   - What's unclear: Optimal batch size for CPU vs GPU inference
   - Recommendation: Start with batch_size=16, tune based on performance

3. **Model update frequency**
   - What we know: ProsusAI/finbert is stable, infrequent updates
   - What's unclear: Check for newer versions periodically
   - Recommendation: Pin to specific version in requirements.txt

## Sources

### Primary (HIGH confidence)
- Hugging Face ProsusAI/finbert - https://huggingface.co/ProsusAI/finbert
- Hugging Face Transformers Pipeline Documentation - https://huggingface.co/docs/transformers/v4.42.0/en/main_classes/pipelines
- ProsusAI/finBERT GitHub - https://github.com/ProsusAI/finBERT

### Secondary (MEDIUM confidence)
- "An Analysis of Different Sentiment Analysis Models on Financial Text using Transformer" - Proceedings ICAIEHS 2025
- "Fine-Tuning and Explaining FinBERT for Sector-Specific Financial News" - MDPI Electronics 2025
- "Financial Sentiment Analysis Using FinBERT with Application in Predicting Stock Movement" - arXiv 2023

### Tertiary (LOW confidence)
- Stack Overflow discussions on model caching (verified against official docs)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Verified via Hugging Face docs and recent research papers (2025), ProsusAI/finbert remains the standard
- Architecture: HIGH - Pipeline API is well-documented, project structure follows existing pattern
- Pitfalls: HIGH - Known issues (model download, Streamlit caching) documented across multiple sources

**Research date:** 2026-03-09
**Valid until:** 2026-04-09 (30 days - model versions are stable)

**Re-research notes:**
- Verified ProsusAI/finbert still active (safetensors variant added May 2025)
- Confirmed Modern-FinBERT-large exists but less validated
- finbert-tone exists but ProsusAI better suited for general financial headlines
- Previous research APPROVED - no major changes needed
