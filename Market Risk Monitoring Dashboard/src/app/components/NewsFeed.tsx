import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { ExternalLink, TrendingDown, TrendingUp, Minus } from 'lucide-react';
import { Badge } from './ui/badge';

interface NewsArticle {
  title: string;
  source: string;
  sentiment: number;
  url: string;
  time: string;
}

interface NewsFeedProps {
  articles: NewsArticle[];
}

export function NewsFeed({ articles }: NewsFeedProps) {
  const getSentimentBadge = (sentiment: number) => {
    if (sentiment > 0.3) {
      return {
        label: 'Positive',
        variant: 'default' as const,
        color: 'bg-green-100 text-green-800 border-green-300',
        icon: <TrendingUp className="w-3 h-3" />
      };
    }
    if (sentiment > -0.3) {
      return {
        label: 'Neutral',
        variant: 'secondary' as const,
        color: 'bg-gray-100 text-gray-800 border-gray-300',
        icon: <Minus className="w-3 h-3" />
      };
    }
    return {
      label: 'Negative',
      variant: 'destructive' as const,
      color: 'bg-red-100 text-red-800 border-red-300',
      icon: <TrendingDown className="w-3 h-3" />
    };
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Live News Feed</span>
          <Badge variant="outline" className="font-normal">
            {articles.length} Articles
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4 max-h-[500px] overflow-y-auto pr-2">
          {articles.map((article, index) => {
            const sentimentBadge = getSentimentBadge(article.sentiment);
            
            return (
              <div
                key={index}
                className="p-4 border border-gray-200 rounded-lg hover:border-gray-300 hover:shadow-md transition-all duration-200"
              >
                <div className="flex items-start justify-between gap-3 mb-2">
                  <h3 className="font-medium text-sm leading-tight flex-1">
                    {article.title}
                  </h3>
                  <a
                    href={article.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:text-blue-800 flex-shrink-0"
                  >
                    <ExternalLink className="w-4 h-4" />
                  </a>
                </div>

                <div className="flex items-center justify-between gap-4">
                  <div className="flex items-center gap-3 text-xs text-gray-500">
                    <span className="font-medium">{article.source}</span>
                    <span>•</span>
                    <span>{article.time}</span>
                  </div>

                  <div className="flex items-center gap-2">
                    <div className={`flex items-center gap-1 px-2 py-1 rounded-md border text-xs font-medium ${sentimentBadge.color}`}>
                      {sentimentBadge.icon}
                      <span>{sentimentBadge.label}</span>
                    </div>
                    <span className="text-xs font-mono text-gray-600">
                      {article.sentiment.toFixed(2)}
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
