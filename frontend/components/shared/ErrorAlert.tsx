/**
 * Error Alert Component
 * Displays user-friendly error messages with special handling for rate limits
 */
"use client";

import { AlertCircle, Clock, TrendingUp } from "lucide-react";
import { Card } from "@/components/ui/card";

interface ErrorAlertProps {
  error: string | {
    error: string;
    error_type?: string;
    retry_after?: number;
    quota_limit?: number;
  };
}

export function ErrorAlert({ error }: ErrorAlertProps) {
  // Parse error data
  const isRateLimit = typeof error === "object" && error.error_type === "rate_limit";
  const errorMessage = typeof error === "string" ? error : error.error;
  const retryAfter = typeof error === "object" ? error.retry_after : null;
  const quotaLimit = typeof error === "object" ? error.quota_limit : null;

  // Calculate retry time display
  const getRetryTimeDisplay = (seconds: number | null) => {
    if (!seconds) return null;
    
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    
    if (minutes > 0) {
      return `${minutes} 分 ${remainingSeconds} 秒`;
    }
    return `${remainingSeconds} 秒`;
  };

  return (
    <Card className={`p-6 border-2 ${ isRateLimit ? "bg-coral/10  border-coral/50 " 
        : "bg-coral-soft/20 dark:bg-destructive/15  border-destructive/30 "
    }`}>
      <div className="flex items-start gap-4">
        <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${ isRateLimit ? "bg-coral/10 " 
            : "bg-coral-soft/20 dark:bg-destructive/15 "
        }`}>
          {isRateLimit ? (
            <Clock className="w-5 h-5 text-foreground " />
          ) : (
            <AlertCircle className="w-5 h-5 text-destructive " />
          )}
        </div>
        
        <div className="flex-1">
          <h3 className={`font-semibold text-lg mb-2 ${ isRateLimit ? "text-foreground " 
              : "text-destructive "
          }`}>
            {isRateLimit ? "API 請求額度已達上限" : "錯誤"}
          </h3>
          
          <p className={`mb-4 ${ isRateLimit ? "text-foreground " 
              : "text-destructive "
          }`}>
            {errorMessage}
          </p>

          {isRateLimit && (
            <div className="space-y-3 mt-4">
              {/* Retry Information */}
              {retryAfter && (
                <div className="flex items-start gap-2 bg-card p-3 rounded-lg">
                  <Clock className="w-4 h-4 text-foreground mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="text-sm font-medium text-foreground ">
                      建議等待時間
                    </p>
                    <p className="text-sm text-foreground ">
                      請在 <span className="font-bold text-foreground ">
                        {getRetryTimeDisplay(retryAfter)}
                      </span> 後重試
                    </p>
                  </div>
                </div>
              )}

              {/* Quota Information */}
              {quotaLimit && (
                <div className="flex items-start gap-2 bg-card p-3 rounded-lg">
                  <TrendingUp className="w-4 h-4 text-foreground mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="text-sm font-medium text-foreground ">
                      每日額度限制
                    </p>
                    <p className="text-sm text-foreground ">
                      當前計劃：每日 {quotaLimit} 次請求
                    </p>
                  </div>
                </div>
              )}

              {/* Solutions */}
              <div className="bg-secondary border border-border p-4 rounded-lg mt-4">
                <p className="text-sm font-semibold text-deep-green dark:text-pale-green mb-2">
                  💡 解決方案：
                </p>
                <ul className="text-sm text-deep-green dark:text-pale-green space-y-1.5 list-disc list-inside">
                  <li>等待額度重置（通常為每日重置）</li>
                  <li>升級至付費方案以獲得更高額度</li>
                  <li>減少分析師數量或研究深度以降低 API 呼叫次數</li>
                  <li>使用不同的 API 金鑰（如果有多個帳戶）</li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </Card>
  );
}
