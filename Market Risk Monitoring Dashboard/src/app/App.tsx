import React, { useState, useEffect } from 'react';
import { AlertCircle, RefreshCw, Activity } from 'lucide-react';
import { RiskGauge } from './components/RiskGauge';
import { MarketChart } from './components/MarketChart';
import { SentimentChart } from './components/SentimentChart';
import { VolatilityHeatmap } from './components/VolatilityHeatmap';
import { NewsFeed } from './components/NewsFeed';
import { RiskEvolutionChart } from './components/RiskEvolutionChart';
import { Alert, AlertDescription, AlertTitle } from './components/ui/alert';
import { Button } from './components/ui/button';
import { Badge } from './components/ui/badge';
import { Skeleton } from './components/ui/skeleton';
import { fetchRisk, fetchMarket, fetchNews, fetchHistory, RiskResponse, MarketDataPoint, NewsItem, HistoryPoint } from './services/api';

// Time range options for market data
const TIME_RANGE_OPTIONS = [
  { value: '1d', label: '1 Day' },
  { value: '2d', label: '2 Days' },
  { value: '10d', label: '10 Days' },
  { value: '30d', label: '30 Days' },
];

// Mock data generators (fallback when API is unavailable)
const generateMarketData = (): MarketDataPoint[] => {
  const data = [];
  const basePrice = 520;
  const now = new Date();
  
  for (let i = 23; i >= 0; i--) {
    const time = new Date(now.getTime() - i * 60 * 60 * 1000);
    const hours = time.getHours();
    const randomWalk = Math.random() * 10 - 5;
    const price = basePrice + randomWalk + (Math.sin(i / 4) * 3);
    
    data.push({
      time: `${hours}:00`,
      price: parseFloat(price.toFixed(2)),
      volume: Math.floor(Math.random() * 1000000) + 500000,
    });
  }
  
  return data;
};

const generateSentimentData = () => {
  const data = [];
  const now = new Date();
  
  for (let i = 11; i >= 0; i--) {
    const time = new Date(now.getTime() - i * 2 * 60 * 60 * 1000);
    const hours = time.getHours();
    
    data.push({
      time: `${hours}:00`,
      sentiment: parseFloat((Math.random() * 1.2 - 0.6).toFixed(3)),
      newsCount: Math.floor(Math.random() * 15) + 5,
    });
  }
  
  return data;
};

const generateRiskEvolutionData = (): HistoryPoint[] => {
  const data = [];
  const now = new Date();
  
  for (let i = 47; i >= 0; i--) {
    const time = new Date(now.getTime() - i * 30 * 60 * 1000);
    const hours = time.getHours();
    const minutes = time.getMinutes();
    
    // Simulate risk fluctuation
    const baseRisk = 45;
    const wave = Math.sin(i / 8) * 20;
    const noise = Math.random() * 15 - 7.5;
    const risk = Math.max(0, Math.min(100, baseRisk + wave + noise));
    
    data.push({
      time: `${hours}:${minutes.toString().padStart(2, '0')}`,
      risk: parseFloat(risk.toFixed(1)),
      volatility: 18 + Math.random() * 10,
      sentiment: 0.5 + Math.random() * 0.4 - 0.2,
    });
  }
  
  return data;
};

const generateVolatilityData = () => {
  return [
    {
      metric: 'VIX (Fear Index)',
      current: 18.45,
      average: 15.20,
      status: 'medium' as const,
    },
    {
      metric: 'Intraday Volatility',
      current: 1.87,
      average: 1.45,
      status: 'medium' as const,
    },
    {
      metric: 'Volume Spike',
      current: 2.34,
      average: 1.00,
      status: 'high' as const,
    },
    {
      metric: 'Put/Call Ratio',
      current: 1.12,
      average: 0.95,
      status: 'medium' as const,
    },
    {
      metric: 'Market Breadth',
      current: 0.42,
      average: 0.65,
      status: 'high' as const,
    },
  ];
};

const generateNewsArticles = () => {
  const sources = ['Reuters', 'Bloomberg', 'CNBC', 'WSJ', 'TechCrunch', 'Hacker News'];
  const times = ['2m ago', '15m ago', '1h ago', '2h ago', '3h ago', '4h ago'];
  
  const headlines = [
    'Federal Reserve signals potential rate cuts in Q2 2026',
    'Tech stocks rally on strong earnings reports from major companies',
    'Inflation data shows unexpected uptick in consumer prices',
    'Banking sector faces scrutiny over commercial real estate exposure',
    'AI chip manufacturer announces breakthrough in production capacity',
    'Energy markets volatile amid geopolitical tensions',
    'Consumer confidence index drops to 6-month low',
    'Major tech company announces layoffs affecting 5,000 employees',
    'Housing market shows signs of stabilization after prolonged slump',
    'Cryptocurrency markets surge on institutional adoption news',
  ];
  
  return headlines.slice(0, 8).map((title, i) => ({
    title,
    source: sources[i % sources.length],
    sentiment: parseFloat((Math.random() * 1.6 - 0.8).toFixed(3)),
    url: '#',
    time: times[i % times.length],
  }));
};

export default function App() {
  const [lastUpdate, setLastUpdate] = useState(new Date());
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [apiError, setApiError] = useState<string | null>(null);
  const [timeRange, setTimeRange] = useState('7d');

  // API data state
  const [riskData, setRiskData] = useState<RiskResponse | null>(null);
  const [marketData, setMarketData] = useState<MarketDataPoint[]>(generateMarketData());
  const [newsArticles, setNewsArticles] = useState<NewsItem[]>([]);
  const [riskEvolutionData, setRiskEvolutionData] = useState<HistoryPoint[]>(generateRiskEvolutionData());
  const [sentimentData, setSentimentData] = useState<{time: string; sentiment: number; newsCount: number}[]>(generateSentimentData());

  // Fetch data from API
  const fetchAllData = async () => {
    setIsRefreshing(true);
    setApiError(null);
    
    try {
      // Fetch risk data
      const risk = await fetchRisk();
      if (risk) {
        setRiskData(risk);
      }
      
      // Fetch market data
      const market = await fetchMarket('SPY', timeRange);
      if (market && market.data) {
        setMarketData(market.data);
      }
      
      // Fetch news
      const news = await fetchNews();
      if (news && news.articles) {
        setNewsArticles(news.articles);
      }
      
      // Fetch history
      const history = await fetchHistory();
      if (history && history.data) {
        setRiskEvolutionData(history.data);
        // Extract sentiment from history for the sentiment chart
        const sentimentFromHistory = history.data.slice(-12).map((point, i) => ({
          time: new Date(point.time).getHours().toString() + ':00',
          sentiment: point.sentiment,
          newsCount: 10,
        }));
        setSentimentData(sentimentFromHistory);
      }
      
      setLastUpdate(new Date());
    } catch (error) {
      console.error('Error fetching data:', error);
      setApiError('Failed to fetch data from API');
    } finally {
      setLoading(false);
      setIsRefreshing(false);
    }
  };

  // Initial data fetch
  useEffect(() => {
    fetchAllData();
  }, []);

  // Auto-refresh every 15 minutes
  useEffect(() => {
    if (!autoRefresh) return;
    
    const interval = setInterval(() => {
      fetchAllData();
    }, 15 * 60 * 1000); // 15 minutes

    return () => clearInterval(interval);
  }, [autoRefresh]);

  // Calculate current metrics from API data or fallback to mock
  const currentPrice = marketData.length > 0 ? marketData[marketData.length - 1].price : 520;
  const previousPrice = marketData.length > 1 ? marketData[marketData.length - 2].price : 518;
  const priceChange = currentPrice - previousPrice;
  const priceChangePercent = previousPrice > 0 ? (priceChange / previousPrice) * 100 : 0;

  const averageSentiment = sentimentData.length > 0 
    ? sentimentData.reduce((sum, d) => sum + d.sentiment, 0) / sentimentData.length 
    : 0;
  
  // Use API risk score if available, otherwise calculate
  const currentRisk = riskData?.score ?? (
    riskEvolutionData.length > 0 ? riskEvolutionData[riskEvolutionData.length - 1].risk : 45
  );
  const previousRisk = riskEvolutionData.length > 1 ? riskEvolutionData[riskEvolutionData.length - 2].risk : 40;

  // Risk level from API or calculate
  const riskLevel = riskData?.level ?? (currentRisk >= 75 ? 'HIGH' : currentRisk >= 40 ? 'MEDIUM' : 'LOW');
  
  // Handle refresh button
  const handleRefresh = () => {
    fetchAllData();
  };

  const isHighRisk = currentRisk >= 75;

  // Loading state with skeletons
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white border-b border-gray-200 sticky top-0 z-10 shadow-sm">
          <div className="max-w-[1800px] mx-auto px-6 py-4">
            <div className="flex items-center gap-3">
              <Activity className="w-8 h-8 text-blue-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  AI Market Risk Early Warning System
                </h1>
                <Skeleton className="h-4 w-64 mt-1" />
              </div>
            </div>
          </div>
        </header>
        <main className="max-w-[1800px] mx-auto px-6 py-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="space-y-6">
              <Skeleton className="h-64 w-full" />
              <Skeleton className="h-48 w-full" />
            </div>
            <div className="lg:col-span-2 space-y-6">
              <Skeleton className="h-64 w-full" />
              <Skeleton className="h-48 w-full" />
            </div>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10 shadow-sm">
        <div className="max-w-[1800px] mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Activity className="w-8 h-8 text-blue-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  AI Market Risk Early Warning System
                </h1>
                <p className="text-sm text-gray-500">
                  Real-time market monitoring & sentiment analysis
                </p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              {/* Time Range Selector */}
              <select
                value={timeRange}
                onChange={(e) => {
                  setTimeRange(e.target.value);
                  fetchAllData();
                }}
                className="border border-gray-300 rounded px-3 py-1.5 text-sm bg-white text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {TIME_RANGE_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>

              <div className="text-right text-sm">
                <div className="text-gray-500">Last update</div>
                <div className="font-medium">{lastUpdate.toLocaleTimeString()}</div>
                {apiError && <div className="text-red-500 text-xs">{apiError}</div>}
              </div>
              
              <Button
                onClick={handleRefresh}
                variant="outline"
                size="sm"
                disabled={isRefreshing}
              >
                <RefreshCw className={`w-4 h-4 mr-2 ${isRefreshing ? 'animate-spin' : ''}`} />
                Refresh
              </Button>

              <Badge variant={autoRefresh ? 'default' : 'secondary'}>
                Auto-refresh: {autoRefresh ? 'ON' : 'OFF'}
              </Badge>
            </div>
          </div>
        </div>
      </header>

      {/* Alert Banner */}
      {isHighRisk && (
        <div className="bg-red-50 border-b border-red-200">
          <div className="max-w-[1800px] mx-auto px-6 py-3">
            <Alert variant="destructive" className="border-0 bg-transparent">
              <AlertCircle className="h-5 w-5" />
              <AlertTitle>High Risk Alert</AlertTitle>
              <AlertDescription>
                Market risk score has exceeded 75. Elevated volatility and negative sentiment detected.
                Consider reviewing your portfolio exposure.
              </AlertDescription>
            </Alert>
          </div>
        </div>
      )}

      {/* Main Dashboard */}
      <main className="max-w-[1800px] mx-auto px-6 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Risk Gauge & Evolution */}
          <div className="space-y-6">
            <RiskGauge 
              riskScore={currentRisk} 
              previousScore={previousRisk} 
              level={riskLevel as 'LOW' | 'MEDIUM' | 'HIGH'}
            />
            <RiskEvolutionChart data={riskEvolutionData} />
          </div>

          {/* Middle Column - Charts */}
          <div className="lg:col-span-2 space-y-6">
            <MarketChart
              data={marketData}
              currentPrice={currentPrice}
              priceChange={priceChange}
              priceChangePercent={priceChangePercent}
              timeRange={timeRange}
            />
            <SentimentChart
              data={sentimentData}
              averageSentiment={averageSentiment}
            />
          </div>
        </div>

        {/* Bottom Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
          <VolatilityHeatmap 
            data={riskData ? [
              { metric: 'VIX (Fear Index)', current: riskData.volatility, average: 15.20, status: riskData.volatility > 20 ? 'high' as const : 'medium' as const },
              { metric: 'Intraday Volatility', current: riskData.volatility / 10, average: 1.45, status: 'medium' as const },
              { metric: 'Volume Spike', current: 2.34, average: 1.00, status: 'high' as const },
              { metric: 'Put/Call Ratio', current: 1.12, average: 0.95, status: 'medium' as const },
              { metric: 'Market Breadth', current: 0.42, average: 0.65, status: 'high' as const },
            ] : []} 
          />
          <NewsFeed 
            articles={newsArticles.length > 0 ? newsArticles : [
              { title: 'Loading...', source: 'API', sentiment: 0, url: '#', time: '' }
            ]} 
          />
        </div>

        {/* Footer Info */}
        <div className="mt-8 p-6 bg-white border border-gray-200 rounded-lg">
          <h3 className="font-semibold mb-3">Risk Calculation Methodology</h3>
          <p className="text-sm text-gray-600 mb-2">
            <strong>Formula:</strong> Risk Score = 0.6 × Volatility Index + 0.4 × (1 - Sentiment Score)
          </p>
          <p className="text-sm text-gray-600 mb-2">
            <strong>Data Sources:</strong> {apiError ? 'Mock data (API unavailable)' : 'Live API - SPY market data, multi-source news aggregation'}
          </p>
          <p className="text-sm text-gray-600">
            <strong>Sentiment Analysis:</strong> {apiError ? 'Simulated' : 'FinBERT model'} scores ranging from -1 (very negative) to +1 (very positive)
          </p>
        </div>
      </main>
    </div>
  );
}
