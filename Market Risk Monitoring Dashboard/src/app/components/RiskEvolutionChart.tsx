import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

interface RiskDataPoint {
  time: string;
  risk: number;
  volatility?: number;
  sentiment?: number;
}

interface RiskEvolutionChartProps {
  data: RiskDataPoint[];
}

export function RiskEvolutionChart({ data }: RiskEvolutionChartProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Risk Score Evolution (24h)</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={250}>
          <AreaChart data={data}>
            <defs>
              <linearGradient id="riskGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#ef4444" stopOpacity={0.8}/>
                <stop offset="50%" stopColor="#eab308" stopOpacity={0.6}/>
                <stop offset="100%" stopColor="#22c55e" stopOpacity={0.4}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis 
              dataKey="time" 
              tick={{ fontSize: 12 }}
              stroke="#6b7280"
            />
            <YAxis 
              domain={[0, 100]}
              tick={{ fontSize: 12 }}
              stroke="#6b7280"
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#ffffff', 
                border: '1px solid #e5e7eb',
                borderRadius: '8px'
              }}
              formatter={(value: number) => [value.toFixed(1), 'Risk Score']}
            />
            <ReferenceLine y={33} stroke="#22c55e" strokeDasharray="3 3" label="Low" />
            <ReferenceLine y={75} stroke="#ef4444" strokeDasharray="3 3" label="High" />
            <Area 
              type="monotone" 
              dataKey="risk" 
              stroke="#3b82f6"
              strokeWidth={2}
              fill="url(#riskGradient)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
