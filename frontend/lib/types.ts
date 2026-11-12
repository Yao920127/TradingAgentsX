/**
 * TypeScript type definitions for TradingAgentsX API
 */

export interface AnalysisRequest {
  ticker: string;
  analysis_date: string;
  analysts?: string[];
  research_depth?: number;
  market_type?: "us" | "twse" | "tpex";  // 市場類型：美股、上市、上櫃/興櫃
  quick_think_llm?: string;
  deep_think_llm?: string;

  // API Configuration
  openai_api_key?: string;
  openai_base_url?: string;
  quick_think_base_url?: string;
  deep_think_base_url?: string;
  quick_think_api_key?: string;
  deep_think_api_key?: string;
  embedding_base_url?: string;
  embedding_api_key?: string;
  embedding_model?: string;  // Embedding model: 'all-mpnet-base-v2' (local), 'text-embedding-3-small' (OpenAI), etc.
  alpha_vantage_api_key?: string;
  finmind_api_key?: string;  // 台灣股市資料 API
  // News & social data sources (optional; server-side env keys are used when empty)
  finnhub_api_key?: string;
  marketaux_api_key?: string;
  newsapi_api_key?: string;
  jina_api_key?: string;
  apify_api_token?: string;
  lunarcrush_api_key?: string;
  hf_token?: string;  // Hugging Face（本地嵌入模型下載）
  language?: "en" | "zh-TW";  // Language for agent reports
}

export interface PriceData {
  Date: string;
  Open: number;
  High: number;
  Low: number;
  Close: number;
  "Adj Close"?: number; // Optional adjusted close price
  Volume: number;
}

export interface PriceStats {
  growth_rate: number;
  duration_days: number;
  start_date: string;
  end_date: string;
  start_price: number;
  end_price: number;
}

export interface AnalysisResponse {
  status: string;
  ticker: string;
  analysis_date: string;
  market_type?: "us" | "twse" | "tpex";  // 市場類型：美股、上市、上櫃/興櫃
  decision?: any;
  reports?: any;
  error?: string;
  error_type?: string;
  retry_after?: number;
  quota_limit?: number;
  price_data?: PriceData[];
  price_stats?: PriceStats;
  deep_think_llm?: string;   // Deep thinking model used for this analysis
  quick_think_llm?: string;  // Quick thinking model used for this analysis
}

export interface Decision {
  action: string;
  quantity?: number;
  reasoning?: string;
  confidence?: number;
}

export interface Reports {
  market_report?: string;
  sentiment_report?: string;
  news_report?: string;
  fundamentals_report?: string;
  investment_plan?: string;
  trader_investment_plan?: string;
  final_trade_decision?: string;
  investment_debate_state?: DebateState;
  risk_debate_state?: DebateState;
}

export interface DebateState {
  bull_history?: string;
  bear_history?: string;
  risky_history?: string;
  safe_history?: string;
  neutral_history?: string;
  judge_decision?: string;
}

export interface ConfigResponse {
  available_analysts: string[];
  available_llms: {
    [provider: string]: string[];
  };
  default_config: {
    [key: string]: any;
  };
}

export interface HealthResponse {
  status: string;
  version: string;
  timestamp: string;
}

export interface Ticker {
  symbol: string;
  name: string;
}

// Task Management Types

export interface TaskCreatedResponse {
  task_id: string;
  status: "pending";
  message: string;
}

// Agent progress (from backend tradingagents/graph/progress.py; timestamps are epoch seconds)

export interface ProgressStep {
  key: string;
  status: "pending" | "running" | "completed";
  started_at: number | null;
  completed_at: number | null;
  // Only on debate steps (research_debate / risk_debate)
  turns_done?: number;
  total_turns?: number;
}

export interface ProgressDetail {
  started_at: number;
  updated_at: number;
  percent: number;
  finished: boolean;
  current_step: string | null;
  current_agent: string | null;
  current_tools: string[];
  steps: ProgressStep[];
}

export interface TaskStatusResponse {
  task_id: string;
  status: "pending" | "running" | "completed" | "failed";
  created_at: string;
  updated_at: string;
  progress?: string;
  progress_detail?: ProgressDetail | null;
  server_time?: number;
  result?: AnalysisResponse;
  error?: string;
  completed_at?: string;
}

// Chat Types

export interface ChatMessageRequest {
  message: string;
  reports: any;
  ticker: string;
  analysis_date: string;
  history?: { role: string; content: string }[];
  model: string;
  api_key: string;
  base_url: string;
  language?: "en" | "zh-TW";
}

export interface ChatMessageResponse {
  reply: string;
}

// API Key Validation Types

export interface ValidateKeysRequest {
  openai_api_key?: string;
  anthropic_api_key?: string;
  google_api_key?: string;
  grok_api_key?: string;
  deepseek_api_key?: string;
  qwen_api_key?: string;
  custom_base_url?: string;
  custom_api_key?: string;
  alpha_vantage_api_key?: string;
  finmind_api_key?: string;
}

export type KeyValidationStatus = "valid" | "invalid" | "unknown";

export type KeyValidationReason =
  | "ok"
  | "auth_failed"
  | "timeout"
  | "network_error"
  | "rate_limited"
  | "server_error"
  | "unsupported"
  | "unknown_error";

export interface KeyValidationResult {
  field: string;
  provider: string;
  status: KeyValidationStatus;
  reason: KeyValidationReason;
  detail?: string | null;
}

export interface ValidateKeysResponse {
  results: Record<string, KeyValidationResult>;
}

// ── Live price (results page "Live" mode) ───────────────────────────────────
// All times are Unix seconds.
export interface LivePricePoint {
  time: number;
  value: number;
}

export interface LiveCandle {
  time: number;
  open: number;
  high: number;
  low: number;
  close: number;
}

export interface LiveVolumeBar {
  time: number;
  volume: number;
}

/** A trading session a bar belongs to. */
export type LiveBarSession = "pre" | "regular" | "post";
/** What the market is doing right now. */
export type LiveMarketSession = LiveBarSession | "closed";

/** A run of consecutive bars in one session (first and last bar time). */
export interface LiveSessionRange {
  session: LiveBarSession;
  start: number;
  end: number;
}

export interface LiveQuote {
  symbol: string;
  currency: string | null;
  /** Latest price. Pre/post-market price when `price_session` is "pre"/"post". */
  price: number;
  /** Close that `change` is measured against: the latest regular close in pre/post market. */
  previous_close: number | null;
  change: number | null;
  change_percent: number | null;
  market_open: boolean;
  session: LiveMarketSession;
  price_session: LiveBarSession;
  sessions: LiveSessionRange[];
  as_of: number;
  points: LivePricePoint[];
  candles: LiveCandle[];
  volumes: LiveVolumeBar[];
}

export type LiveMarketType = "us" | "twse" | "tpex";
