/**
 * API Service Layer for Market Risk Dashboard
 * Fetches data from FastAPI backend
 */

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// TypeScript interfaces matching FastAPI response models
export interface RiskResponse {
  score: number;
  volatility: number;
  sentiment: number;
  level: 'LOW' | 'MEDIUM' | 'HIGH';
  timestamp: string;
}

export interface MarketDataPoint {
  time: string;
  price: number;
  volume: number;
  open?: number;
  high?: number;
  low?: number;
  close?: number;
}

export interface MarketResponse {
  data: MarketDataPoint[];
  symbol: string;
  time_range: string;
}

export interface NewsItem {
  title: string;
  source: string;
  sentiment?: number;
  url?: string;
  time?: string;
}

export interface NewsResponse {
  articles: NewsItem[];
  total_count: number;
  timestamp: string;
}

export interface HistoryPoint {
  time: string;
  risk: number;
  volatility: number;
  sentiment: number;
}

export interface HistoryResponse {
  data: HistoryPoint[];
  period_hours: number;
}

// Error handling helper
async function fetchWithErrorHandling<T>(url: string): Promise<T | null> {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      console.error(`API error: ${response.status} ${response.statusText}`);
      return null;
    }
    return await response.json();
  } catch (error) {
    console.error(`Fetch error for ${url}:`, error);
    return null;
  }
}

// API functions
export async function fetchRisk(): Promise<RiskResponse | null> {
  return fetchWithErrorHandling<RiskResponse>(`${API_BASE}/api/risk`);
}

export async function fetchMarket(
  symbol: string = 'SPY',
  timeRange: string = '7d'
): Promise<MarketResponse | null> {
  return fetchWithErrorHandling<MarketResponse>(
    `${API_BASE}/api/market?symbol=${symbol}&time_range=${timeRange}`
  );
}

export async function fetchNews(): Promise<NewsResponse | null> {
  return fetchWithErrorHandling<NewsResponse>(`${API_BASE}/api/news`);
}

export async function fetchHistory(periodHours: number = 24): Promise<HistoryResponse | null> {
  return fetchWithErrorHandling<HistoryResponse>(
    `${API_BASE}/api/history?period_hours=${periodHours}`
  );
}

export async function refreshCache(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE}/api/refresh`, { method: 'POST' });
    return response.ok;
  } catch (error) {
    console.error('Cache refresh error:', error);
    return false;
  }
}
