import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, ComposedChart } from 'recharts';

interface MarketDataPoint {
  time: string;
  price: number;
  volume: number;
}

interface MarketChartProps {
  data: MarketDataPoint[];
  currentPrice: number;
  priceChange: number;
  priceChangePercent: number;
  timeRange?: string;
}

// Format XAxis labels based on time range
const formatXAxis = (timeRange: string) => (time: string) => {
  try {
    const date = new Date(time);
    if (isNaN(date.getTime())) {
      // Handle mock data format (e.g., "14:00")
      return time;
    }
    
    if (timeRange === '1d') {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    if (timeRange === '2d') {
      return date.toLocaleDateString([], { weekday: 'short', hour: '2-digit' });
    }
    return date.toLocaleDateString([], { month: 'short', day: 'numeric' });
  } catch {
    return time;
  }
};

export function MarketChart({ data, currentPrice, priceChange, priceChangePercent, timeRange = '7d' }: MarketChartProps) {
  const isPositive = priceChange >= 0;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>SPY Market Trend</span>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <div className="text-2xl font-bold">${currentPrice.toFixed(2)}</div>
              <div className={`text-sm ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
                {isPositive ? '+' : ''}{priceChange.toFixed(2)} ({isPositive ? '+' : ''}{priceChangePercent.toFixed(2)}%)
              </div>
            </div>
          </div>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <ComposedChart data={data}>
            <defs>
              <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={isPositive ? "#22c55e" : "#ef4444"} stopOpacity={0.3}/>
                <stop offset="95%" stopColor={isPositive ? "#22c55e" : "#ef4444"} stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis 
              dataKey="time" 
              tick={{ fontSize: 12 }}
              stroke="#6b7280"
              tickFormatter={formatXAxis(timeRange)}
            />
            <YAxis 
              domain={['dataMin - 5', 'dataMax + 5']}
              tick={{ fontSize: 12 }}
              stroke="#6b7280"
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#ffffff', 
                border: '1px solid #e5e7eb',
                borderRadius: '8px'
              }}
              formatter={(value: number) => [`$${value.toFixed(2)}`, 'Price']}
            />
            <Area
              type="monotone"
              dataKey="price"
              stroke={isPositive ? "#22c55e" : "#ef4444"}
              strokeWidth={2}
              fill="url(#colorPrice)"
            />
            <Line 
              type="monotone" 
              dataKey="price" 
              stroke={isPositive ? "#22c55e" : "#ef4444"}
              strokeWidth={3}
              dot={false}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
