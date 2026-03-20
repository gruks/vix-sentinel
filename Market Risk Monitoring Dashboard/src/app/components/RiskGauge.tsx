import React from 'react';
import { AlertTriangle, TrendingDown, TrendingUp } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';

interface RiskGaugeProps {
  riskScore: number;
  previousScore: number;
  level?: 'LOW' | 'MEDIUM' | 'HIGH';
}

export function RiskGauge({ riskScore, previousScore, level }: RiskGaugeProps) {
  const getRiskLevel = (score: number) => {
    // Use provided level or calculate from score
    if (level) {
      if (level === 'LOW') return { label: 'LOW', color: 'text-green-600', bgColor: 'bg-green-600' };
      if (level === 'MEDIUM') return { label: 'MEDIUM', color: 'text-yellow-600', bgColor: 'bg-yellow-600' };
      return { label: 'HIGH', color: 'text-red-600', bgColor: 'bg-red-600' };
    }
    // Fallback to score-based calculation
    if (score < 33) return { label: 'LOW', color: 'text-green-600', bgColor: 'bg-green-600' };
    if (score < 75) return { label: 'MEDIUM', color: 'text-yellow-600', bgColor: 'bg-yellow-600' };
    return { label: 'HIGH', color: 'text-red-600', bgColor: 'bg-red-600' };
  };

  const risk = getRiskLevel(riskScore);
  const trend = riskScore - previousScore;

  // Calculate the rotation for the needle (0-180 degrees for 0-100 score)
  const rotation = (riskScore / 100) * 180 - 90;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Market Risk Score</span>
          <div className="flex items-center gap-2">
            {trend > 0 ? (
              <TrendingUp className="w-5 h-5 text-red-500" />
            ) : (
              <TrendingDown className="w-5 h-5 text-green-500" />
            )}
            <span className="text-sm font-normal text-gray-500">
              {trend > 0 ? '+' : ''}{trend.toFixed(1)} vs 15m ago
            </span>
          </div>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col items-center">
          {/* Gauge visualization */}
          <div className="relative w-64 h-32 mb-4">
            {/* Background arc */}
            <svg viewBox="0 0 200 100" className="w-full h-full">
              {/* Green section */}
              <path
                d="M 10 90 A 90 90 0 0 1 66.7 10"
                fill="none"
                stroke="#22c55e"
                strokeWidth="20"
                opacity="0.3"
              />
              {/* Yellow section */}
              <path
                d="M 66.7 10 A 90 90 0 0 1 133.3 10"
                fill="none"
                stroke="#eab308"
                strokeWidth="20"
                opacity="0.3"
              />
              {/* Red section */}
              <path
                d="M 133.3 10 A 90 90 0 0 1 190 90"
                fill="none"
                stroke="#ef4444"
                strokeWidth="20"
                opacity="0.3"
              />
              {/* Needle */}
              <line
                x1="100"
                y1="90"
                x2="100"
                y2="20"
                stroke="#1f2937"
                strokeWidth="3"
                strokeLinecap="round"
                transform={`rotate(${rotation} 100 90)`}
              />
              {/* Center dot */}
              <circle cx="100" cy="90" r="6" fill="#1f2937" />
            </svg>
            
            {/* Scale labels */}
            <div className="absolute top-20 left-0 text-xs text-gray-500">0</div>
            <div className="absolute top-0 left-1/2 -translate-x-1/2 text-xs text-gray-500">50</div>
            <div className="absolute top-20 right-0 text-xs text-gray-500">100</div>
          </div>

          {/* Score display */}
          <div className="text-center">
            <div className={`text-6xl font-bold ${risk.color} mb-2`}>
              {riskScore.toFixed(0)}
            </div>
            <div className={`text-xl font-semibold ${risk.color} mb-4`}>
              {risk.label} RISK
            </div>
            
            {riskScore >= 75 && (
              <div className="flex items-center gap-2 px-4 py-2 bg-red-50 border border-red-200 rounded-lg">
                <AlertTriangle className="w-5 h-5 text-red-600" />
                <span className="text-sm text-red-700 font-medium">
                  Alert: High volatility detected
                </span>
              </div>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
