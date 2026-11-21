/**
 * Trading decision display component
 */
"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { AnalysisResponse } from "@/lib/types";

interface TradingDecisionProps {
  result: AnalysisResponse;
}

export function TradingDecision({ result }: TradingDecisionProps) {
  if (result.status === "error") {
    return (
      <Card className="border-destructive/30">
        <CardHeader>
          <CardTitle className="text-destructive">分析錯誤</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-destructive">{result.error}</p>
        </CardContent>
      </Card>
    );
  }

  if (!result.decision) {
    return null;
  }

  const getActionBadge = (action: string) => {
    const actionLower = action.toLowerCase();
    if (actionLower.includes("buy")) {
      return <Badge className="bg-deep-green text-white dark:bg-pale-green dark:text-deep-green">買入</Badge>;
    } else if (actionLower.includes("sell")) {
      return <Badge className="bg-destructive text-white">賣出</Badge>;
    } else {
      return <Badge className="bg-coral text-near-black">持有</Badge>;
    }
  };

  return (
    <Card className="border-2 border-border hover-lift animate-scale-up">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>交易決策</CardTitle>
          {getActionBadge(result.decision.action || "")}
        </div>
        <CardDescription>
          {result.ticker} 於 {result.analysis_date} 的分析
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <h4 className="font-semibold mb-2">行動</h4>
          <p className="text-lg">{result.decision.action}</p>
        </div>

        {result.decision.quantity && (
          <div>
            <h4 className="font-semibold mb-2">數量</h4>
            <p>{result.decision.quantity} 股</p>
          </div>
        )}

        {result.decision.confidence && (
          <div>
            <h4 className="font-semibold mb-2">信心度</h4>
            <div className="flex items-center gap-2">
              <div className="flex-1 h-2 bg-muted rounded-full overflow-hidden">
                <div
                  className="h-full bg-primary"
                  style={{ width: `${result.decision.confidence * 100}%` }}
                />
              </div>
              <span className="text-sm font-medium">
                {(result.decision.confidence * 100).toFixed(0)}%
              </span>
            </div>
          </div>
        )}

        {result.decision.reasoning && (
          <div>
            <h4 className="font-semibold mb-2">理由</h4>
            <p className="text-sm text-foreground whitespace-pre-wrap">
              {result.decision.reasoning}
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
