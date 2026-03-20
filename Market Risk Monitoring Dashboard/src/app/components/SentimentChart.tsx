import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

interface SentimentDataPoint {
  time: string;
  sentiment: number;
  newsCount: number;
}

interface SentimentChartProps {
  data: SentimentDataPoint[];
  averageSentiment: number;
}

export function SentimentChart({ data, averageSentiment }: SentimentChartProps) {
  const getSentimentLabel = (score: number) => {
    if (score > 0.3) return { label: 'POSITIVE', color: 'text-green-600' };
    if (score > -0.3) return { label: 'NEUTRAL', color: 'text-gray-600' };
    return { label: 'NEGATIVE', color: 'text-red-600' };
  };

  const sentiment = getSentimentLabel(averageSentiment);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>News Sentiment Trend</span>
          <div className="text-right">
            <div className={`text-xl font-bold ${sentiment.color}`}>
              {sentiment.label}
            </div>
            <div className="text-sm text-gray-500">
              Score: {averageSentiment.toFixed(2)}
            </div>
          </div>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis 
              dataKey="time" 
              tick={{ fontSize: 12 }}
              stroke="#6b7280"
            />
            <YAxis 
              domain={[-1, 1]}
              tick={{ fontSize: 12 }}
              stroke="#6b7280"
              ticks={[-1, -0.5, 0, 0.5, 1]}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#ffffff', 
                border: '1px solid #e5e7eb',
                borderRadius: '8px'
              }}
              formatter={(value: number, name: string) => {
                if (name === 'sentiment') return [value.toFixed(3), 'Sentiment'];
                return [value, 'Articles'];
              }}
            />
            <ReferenceLine y={0} stroke="#9ca3af" strokeDasharray="3 3" />
            <ReferenceLine y={0.3} stroke="#22c55e" strokeDasharray="2 2" opacity={0.3} />
            <ReferenceLine y={-0.3} stroke="#ef4444" strokeDasharray="2 2" opacity={0.3} />
            <Line 
              type="monotone" 
              dataKey="sentiment" 
              stroke="#3b82f6"
              strokeWidth={3}
              dot={{ fill: '#3b82f6', r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
