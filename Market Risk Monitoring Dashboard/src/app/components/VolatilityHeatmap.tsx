import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';

interface VolatilityData {
  metric: string;
  current: number;
  average: number;
  status: 'low' | 'medium' | 'high';
}

interface VolatilityHeatmapProps {
  data: VolatilityData[];
}

export function VolatilityHeatmap({ data }: VolatilityHeatmapProps) {
  const getStatusColor = (status: 'low' | 'medium' | 'high') => {
    switch (status) {
      case 'low':
        return 'bg-green-500';
      case 'medium':
        return 'bg-yellow-500';
      case 'high':
        return 'bg-red-500';
    }
  };

  const getIntensity = (current: number, average: number) => {
    const ratio = current / average;
    if (ratio < 0.8) return 0.3;
    if (ratio < 1.2) return 0.5;
    if (ratio < 1.5) return 0.7;
    return 1;
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Volatility Indicators</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {data.map((item, index) => {
            const intensity = getIntensity(item.current, item.average);
            const statusColor = getStatusColor(item.status);
            
            return (
              <div key={index} className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div 
                      className={`w-3 h-3 rounded-full ${statusColor}`}
                      style={{ opacity: intensity }}
                    />
                    <span className="font-medium">{item.metric}</span>
                  </div>
                  <div className="text-right">
                    <div className="font-bold">{item.current.toFixed(2)}%</div>
                    <div className="text-xs text-gray-500">
                      avg: {item.average.toFixed(2)}%
                    </div>
                  </div>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                  <div
                    className={`h-full ${statusColor} transition-all duration-300`}
                    style={{ 
                      width: `${Math.min((item.current / (item.average * 2)) * 100, 100)}%`,
                      opacity: intensity
                    }}
                  />
                </div>
              </div>
            );
          })}
        </div>

        {/* Legend */}
        <div className="mt-6 pt-4 border-t border-gray-200">
          <div className="flex items-center justify-center gap-6 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-green-500" />
              <span className="text-gray-600">Low</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-yellow-500" />
              <span className="text-gray-600">Medium</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500" />
              <span className="text-gray-600">High</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
