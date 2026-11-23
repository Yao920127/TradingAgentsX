# Graph Report - .  (2026-11-23)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1725 nodes · 3640 edges · 95 communities (78 shown, 17 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 116 edges (avg confidence: 0.73)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `319c3d28`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- social_sentiment.py
- finmind.py
- HybridSearchEngine
- __init__.py
- _make_api_request
- prompts.py
- live_price_service.py
- YFinanceUtils
- main.py
- route_to_vendor
- interface.py
- get_config
- ._extract_current_situation
- new_listing.py
- ProgressTracker
- AgentState
- __init__.py
- report_format.py
- .create_initial_state
- debate_history.py
- _get_stock_stats_bulk
- to_traditional
- retry
- google.py
- y_finance.py
- TradingAgentsXGraph
- .__init__
- .__init__
- PDFGenerator
- HybridTaskManager
- TradingService
- ResultsView.tsx
- user.py
- LivePriceChart.tsx
- cn
- page.tsx
- types.ts
- AnalysisForm.tsx
- schemas.py
- page.tsx
- DataSourceKeyFields.tsx
- ConditionalLogic
- isCloudSyncEnabled
- ApiSettingsDialog.tsx
- utils.ts
- LwcPriceChart.tsx
- routes.py
- PriceChart.tsx
- output_filter.py
- __init__.py
- PendingTaskRecovery.tsx
- verify_access_token
- LanguageContext.tsx
- auth.py
- TickerCombobox.tsx
- useLanguage
- validate_api_keys
- DebateCard.tsx
- layout.tsx
- AgentFlowDiagram.tsx
- MarkdownReport.tsx
- PdfPreviewModal.tsx
- crypto.ts
- _summarize_section
- dependencies.py
- Settings
- AnalysisProgress.tsx
- run_analysis
- chat_with_report
- validate_keys
- __main__.py
- getBackendUrl
- Hero.tsx
- .__init__
- get_config
- health_check
- setup_cors
- route.ts
- next.config.ts
- __init__.py
- __init__.py
- __init__.py
- __init__.py
- eslint.config.mjs
- postcss.config.mjs
- css.d.ts
- DELETE
- GET
- PATCH
- POST
- PUT

## God Nodes (most connected - your core abstractions)
1. `cn()` - 86 edges
2. `useLanguage()` - 61 edges
3. `_make_api_request()` - 37 edges
4. `PDFGenerator` - 32 edges
5. `normalize_stock_id()` - 26 edges
6. `isCloudSyncEnabled()` - 25 edges
7. `HistoryPage()` - 23 edges
8. `Button()` - 22 edges
9. `format_date()` - 22 edges
10. `Article` - 20 edges

## Surprising Connections (you probably didn't know these)
- `LoadedDemo` --references--> `AnalysisResponse`  [EXTRACTED]
  frontend/app/demo/page.tsx → frontend/lib/types.ts
- `DemoPage()` --calls--> `useLanguage()`  [EXTRACTED]
  frontend/app/demo/page.tsx → frontend/contexts/LanguageContext.tsx
- `HomePage()` --calls--> `useLanguage()`  [EXTRACTED]
  frontend/app/page.tsx → frontend/contexts/LanguageContext.tsx
- `AnalystReport()` --calls--> `useLanguage()`  [EXTRACTED]
  frontend/components/analysis/AnalystReport.tsx → frontend/contexts/LanguageContext.tsx
- `DownloadReports()` --calls--> `useLanguage()`  [EXTRACTED]
  frontend/components/analysis/DownloadReports.tsx → frontend/contexts/LanguageContext.tsx

## Import Cycles
- None detected.

## Communities (95 total, 17 thin omitted)

### Community 0 - "social_sentiment.py"
Cohesion: 0.05
Nodes (94): append_linked_content(), _clean(), enrich_with_content(), extract_urls(), _is_body_line(), Jina AI Reader（r.jina.ai）：把新聞網址轉成乾淨文字，讓 LLM 讀到內文而不只是標題。  免金鑰可用（約 20 RPM）；設定 JINA, 讀取文字中引用的前 top_n 個網址，把全文摘錄附在文末。, 為前 top_n 則新聞補上全文摘錄（並行擷取），其餘原樣保留。 (+86 more)

### Community 1 - "finmind.py"
Cohesion: 0.06
Nodes (90): _convert_to_serializable(), _filter_by_date_range(), FinMindAuthenticationError, FinMindDataNotFoundError, FinMindError, FinMindRateLimitError, format_date(), format_output() (+82 more)

### Community 2 - "HybridSearchEngine"
Cohesion: 0.05
Nodes (30): extract_tickers(), HybridSearchEngine, Any, 混合搜索引擎 (Hybrid Search Engine)  結合兩種互補的搜索策略： - BM25 關鍵字搜索 (Keyword Search)：精確匹配股票, 取得文字的嵌入向量（自動截斷至 4000 字元）。, 從目前語料庫重建 BM25Okapi 索引。, 將文件加入混合搜索索引。          Args:             documents : 文件字串列表             metadatas, BM25 關鍵字搜索，含股票代號精確匹配加分。         回傳 [(文件索引, 分數), ...] 依分數降序排列。 (+22 more)

### Community 3 - "__init__.py"
Cohesion: 0.08
Nodes (27): create_fundamentals_analyst(), 建立一個基本面分析師節點。      Args:         llm: 用於分析的語言模型。         language: 報告語言 ('en' 或, create_market_analyst(), 建立一個市場分析師節點。      Args:         llm: 用於分析的語言模型。         language: 報告語言 ('en' 或 ', create_news_analyst(), 建立一個新聞分析師節點。      Args:         llm: 用於分析的語言模型。         language: 報告語言 ('en' 或 ', create_social_media_analyst(), 建立一個社群媒體分析師節點。      Args:         llm: 用於分析的語言模型。         language: 報告語言 ('en' 或 (+19 more)

### Community 4 - "_make_api_request"
Cohesion: 0.09
Nodes (38): AlphaVantageAPIError, AlphaVantageRateLimitError, _filter_csv_by_date_range(), format_datetime_for_api(), get_api_key(), _make_api_request(), Exception, 過濾 CSV 數據，只包含指定日期範圍內的資料列。      Args:         csv_data: 來自 Alpha Vantage API 的 CS (+30 more)

### Community 5 - "prompts.py"
Cohesion: 0.08
Nodes (43): get_agent_role_instruction(), get_aggressive_debator_prompt(), get_analyst_principles(), get_bear_researcher_prompt(), get_bull_researcher_prompt(), get_conservative_debator_prompt(), get_context_message(), get_debate_principles() (+35 more)

### Community 6 - "live_price_service.py"
Cohesion: 0.09
Nodes (32): live_price(), Live price routes: today's intraday quote for the results page "Live" mode., Latest price plus today's 1-minute prices and volumes (Yahoo, may be delayed)., _bar_sessions(), build_live_quote(), _current_session(), fetch_live_quote(), get_live_quote() (+24 more)

### Community 7 - "YFinanceUtils"
Cohesion: 0.08
Nodes (22): decorate_all_methods(), get_current_date(), get_next_weekday(), DataFrame, SavePathType, 將 DataFrame 儲存到 CSV 檔案。      Args:         data (pl.DataFrame): 要儲存的 DataFrame。, 以 YYYY-MM-DD 格式獲取當前日期。      Returns:         str: 當前日期字串。, 一個裝飾器，用於將另一個裝飾器應用於一個類別的所有方法。      Args:         decorator: 要應用的裝飾器。      Returns (+14 more)

### Community 8 - "main.py"
Cohesion: 0.09
Nodes (20): global_exception_handler(), RateLimitMiddleware, FastAPI application entry point for TradingAgentsX Backend, Filter to mask API keys in log messages, Root endpoint - redirect to API documentation, Global exception handler - returns appropriate status codes and masks sensitive, Add security headers to all responses, Simple in-memory rate limiting middleware (+12 more)

### Community 9 - "route_to_vendor"
Cohesion: 0.09
Nodes (25): get_stock_data(), 檢索給定股票代碼的股價數據 (OHLCV)。     使用設定的核心股票 API 供應商。     Args:         symbol (str): 公司, get_balance_sheet(), get_cashflow(), get_fundamentals(), get_income_statement(), 檢索給定股票代碼的綜合基本面數據。     使用設定的基本面數據供應商。     Args:         ticker (str): 公司的股票代碼, 檢索給定股票代碼的資產負債表數據。     使用設定的基本面數據供應商。     Args:         ticker (str): 公司的股票代碼 (+17 more)

### Community 10 - "interface.py"
Cohesion: 0.14
Nodes (21): get_data_in_range(), get_finnhub_company_insider_sentiment(), get_finnhub_company_insider_transactions(), get_finnhub_news(), get_reddit_company_news(), get_reddit_global_news(), get_simfin_balance_sheet(), get_simfin_cashflow() (+13 more)

### Community 11 - "get_config"
Cohesion: 0.12
Nodes (19): get_config(), initialize_config(), set_config(), get_vendor(), 獲取數據類別或特定工具方法的已設定供應商。     工具級別的設定優先於類別級別。, get_fundamentals_openai(), 使用 OpenAI 模型搜索公司的基本面數據。      Args:         ticker (str): 股票代碼。         curr_date, load_price_csv_cached() (+11 more)

### Community 12 - "._extract_current_situation"
Cohesion: 0.17
Nodes (8): Any, 反思看漲研究員的分析並更新其記憶。          Args:             current_state: 當前的圖狀態。, 反思看跌研究員的分析並更新其記憶。          Args:             current_state: 當前的圖狀態。, 反思交易員的決策並更新其記憶。          Args:             current_state: 當前的圖狀態。             re, 反思投資裁判的決策並更新其記憶。          Args:             current_state: 當前的圖狀態。             r, 反思風險管理者的決策並更新其記憶。          Args:             current_state: 當前的圖狀態。, 從狀態中提取當前的市場情況。         這會整合來自不同分析師的報告，為反思提供全面的市場背景。          Args:             c, 為一個組件生成反思。         這個通用函式會呼叫 LLM 來評估特定組件（例如，看漲研究員）的報告或決策。          Args:

### Community 13 - "new_listing.py"
Cohesion: 0.17
Nodes (19): build_new_listing_report(), download_daily(), fetch_intraday_bars(), _fetch_recent_daily(), format_intraday_csv(), IntradayBars, pick_intraday_interval(), DataFrame (+11 more)

### Community 14 - "ProgressTracker"
Cohesion: 0.26
Nodes (4): ProgressTracker, Any, ProgressCallback, 根據所選分析師與辯論回合數建立步驟計畫，並依節點事件更新狀態。      進度百分比以「代理回合」計算：每位分析師、每次辯論發言、     摘要員、研究經理、交

### Community 15 - "AgentState"
Cohesion: 0.14
Nodes (8): AgentState, 判斷風險分析是否應該繼續。         如果討論回合數達到上限，則由風險裁判做出最終決定。         否則，在激進、保守和中立分析師之間輪流進行。, 判斷市場分析是否應該繼續。         如果最後一條訊息包含工具呼叫，則表示代理需要使用工具，         流程應該轉到市場工具節點。否則，分析完成。, 判斷社群媒體分析是否應該繼續。         邏輯與 `should_continue_market` 類似。          Args:, 判斷新聞分析是否應該繼續。         邏輯與 `should_continue_market` 類似。          Args:, 判斷基本面分析是否應該繼續。         邏輯與 `should_continue_market` 類似。          Args:, 判斷投資辯論是否應該繼續。         如果辯論回合數達到上限，則由研究經理做出最終決定。         否則，在看漲和看跌研究員之間輪流進行。, MessagesState

### Community 17 - "report_format.py"
Cohesion: 0.24
Nodes (11): _is_preamble(), _normalize_line(), normalize_report_markdown(), normalize_reports(), Any, 報告 Markdown 版面校正：讓所有報告的標題層級一致。  即使提示詞規定了格式，LLM 仍會混用「## 一、標題」、「**一、標題**」、純文字「一、標題, 遞迴校正 dict / list 中的所有報告文字，回傳新物件（不修改原物件）。, 回傳校正後的標題行；不是標題則回傳 None。 (+3 more)

### Community 18 - ".create_initial_state"
Cohesion: 0.28
Nodes (6): InvestDebateState, RiskDebateState, Any, 獲取圖呼叫的參數。         這些參數控制著圖的執行方式，例如串流模式和遞迴限制。          Returns:             Dict[, 為代理圖建立初始狀態。         這個狀態字典包含了執行開始時所需的所有資訊。          Args:             company_na, TypedDict

### Community 19 - "debate_history.py"
Cohesion: 0.36
Nodes (7): _cap(), compact_debate_history(), _digest(), latest_round(), 只取某位辯論者最後一輪的發言，並去掉輪次標題（相容舊報告的累加格式）。, 壓縮辯論歷史供辯論者閱讀。      Args:         history: 完整辯論歷史（每次發言以發言者標籤開頭）。         recent_t, _split_turns()

### Community 20 - "_get_stock_stats_bulk"
Cohesion: 0.24
Nodes (10): indicator_min_bars(), 回傳指標至少需要幾根 K 棒；未知指標回傳 1（不額外遮蔽）。, _get_stock_stats_bulk(), get_stock_stats_indicators_window(), get_stockstats_indicator(), _intraday_indicator_report(), 獲取給定股票在一個時間窗口內的技術指標。      Args:         symbol (str): 公司的股票代碼。         indicator, 優化的股票統計指標批量計算。     一次性獲取數據並計算所有可用日期的指標。     返回將日期字串映射到指標值的字典。 (+2 more)

### Community 21 - "to_traditional"
Cohesion: 0.36
Nodes (7): _converter(), localize_for(), Any, 簡體 → 繁體（台灣用語）轉換。  即使提示詞要求繁體中文，LLM（尤其讀到簡體來源資料時）仍可能混入簡體字， 例如「财务分析」「资料中心」。簡體字也會造成 P, 遞迴轉換字串、dict、list 中的所有文字，回傳新物件（不修改原物件）。, 只有繁體中文報告才轉換；英文報告原樣回傳。, to_traditional()

### Community 22 - "retry"
Cohesion: 0.33
Nodes (6): log_retry_attempt(), Exception, 重試工具模組，提供統一的重試機制和錯誤處理, 重試裝飾器，支援指數退避          Args:         max_attempts: 最大重試次數（包含首次嘗試）         backoff, 記錄重試嘗試的標準回調函數          Args:         attempt: 當前嘗試次數         exception: 遇到的例外, retry()

### Community 23 - "google.py"
Cohesion: 0.22
Nodes (11): get_global_news_google(), get_google_company_news(), get_google_news(), 使用 Google News 檢索新聞文章。      Args:         query (str): 用於搜索的查詢。         curr_dat, 全球宏觀 / 市場新聞（透過 Google News，免 API 金鑰）。      get_global_news 供應商鏈原本只有 openai（需 Ope, get_news 介面（代碼、起訖日期）的轉接：改以回溯天數呼叫 get_google_news。, getNewsData(), is_rate_limited() (+3 more)

### Community 24 - "y_finance.py"
Cohesion: 0.15
Nodes (14): is_new_listing(), 日 K 根數不足（但至少有 1 根）即視為新上市。, get_balance_sheet(), get_cashflow(), get_fundamentals(), get_income_statement(), get_insider_transactions(), get_YFin_data_online() (+6 more)

### Community 25 - "TradingAgentsXGraph"
Cohesion: 0.18
Nodes (8): ProgressCallback, ToolNode, 使用抽象方法為不同的資料來源建立工具節點。, 在特定日期為某家公司執行交易代理圖。          Args:             company_name (str): 公司名稱或股票代碼。, 根據回報反思決策並更新記憶。         這個方法會觸發對每個相關代理的決策進行反思的過程。, 處理信號以提取核心決策。         將原始的 LLM 輸出轉換為標準化的交易信號（例如，BUY, SELL, HOLD）。, 協調交易代理框架的主要類別。     這個類別整合了所有組件，包括 LLM、記憶體、工具和圖的邏輯，     以執行一個完整的金融分析和交易決策流程。, TradingAgentsXGraph

### Community 26 - ".__init__"
Cohesion: 0.50
Nodes (3): ChatOpenAI, ToolNode, 使用必要的組件進行初始化。          Args:             quick_thinking_llm (ChatOpenAI): 用於快速任務

### Community 29 - "PDFGenerator"
Cohesion: 0.05
Nodes (40): DownloadService, _finmind_stock_name(), _is_taiwan_ticker(), Download Service for Analyst Reports Generates combined PDF reports with all ana, Create a single combined PDF containing all analyst reports                  Fea, 以 FinMind TaiwanStockInfo 取得台股中文簡稱（如 2379 → 瑞昱），失敗回傳空字串（不快取失敗）。, 解析封面公司全名：一律優先英文名（yfinance），台股查不到時退回 FinMind 中文名，再不行回傳 ticker。, Service for handling analyst report downloads (+32 more)

### Community 30 - "HybridTaskManager"
Cohesion: 0.06
Nodes (41): cache_delete(), cache_get(), cache_set(), check_rate_limit(), delete_task_from_redis(), get_redis_client(), get_task_from_redis(), is_redis_available() (+33 more)

### Community 31 - "TradingService"
Cohesion: 0.08
Nodes (25): PriceService, Any, DataFrame, Price data service for loading and processing stock price data, Check if cache file is still valid based on modification time                  A, Fetch data from yfinance and cache it                  Args:             ticker:, Service for loading and processing price data from data_cache, 台股代碼（4-6 位數字）轉成 Yahoo Finance 格式（.TW / .TWO），其他原樣回傳。 (+17 more)

### Community 32 - "ResultsView.tsx"
Cohesion: 0.09
Nodes (29): AnalysisResultsPage(), ReportSection(), DebateCard(), DebateTone, FullReport(), FullReportProps, FullReportSection, ANALYST_REPORT_KEYS (+21 more)

### Community 33 - "user.py"
Cohesion: 0.12
Nodes (33): cleanup_duplicate_reports(), create_report(), delete_all_reports(), delete_report(), get_current_user_optional(), get_current_user_required(), get_report(), get_report_counts() (+25 more)

### Community 34 - "LivePriceChart.tsx"
Cohesion: 0.11
Nodes (30): LivePriceChart(), LivePriceChartProps, LiveStats(), LiveStatsProps, marketStatusLabel(), PriceSectionLabels, referenceCloseLabel(), SESSION_COLORS (+22 more)

### Community 35 - "cn"
Cohesion: 0.09
Nodes (23): LoadingSpinnerProps, Badge(), badgeVariants, CardAction(), CardFooter(), Checkbox(), DropdownMenuCheckboxItem(), DropdownMenuLabel() (+15 more)

### Community 36 - "page.tsx"
Cohesion: 0.11
Nodes (18): HomePage(), AnalystReport(), AnalystReportProps, TradingDecisionProps, InteractiveCard(), ScrollReveal(), ErrorAlert(), ErrorAlertProps (+10 more)

### Community 37 - "types.ts"
Cohesion: 0.12
Nodes (24): AnalysisFormProps, INITIAL_STATE, KeyedState, LivePriceState, nextPollDelay(), useLivePrice(), api, apiClient (+16 more)

### Community 38 - "AnalysisForm.tsx"
Cohesion: 0.14
Nodes (22): AVAILABLE_MODELS, ChatMessage, HistoryChatContent(), MONO_LOGOS, AnalysisForm(), formSchema, ChatMessage, ReportChat() (+14 more)

### Community 39 - "schemas.py"
Cohesion: 0.10
Nodes (28): AnalysisResponse, AnalystReport, ErrorResponse, KeyValidationResult, LiveCandle, LivePricePoint, LiveQuoteResponse, LiveSessionRange (+20 more)

### Community 40 - "page.tsx"
Cohesion: 0.13
Nodes (22): ANALYSTS, detectReportLanguage(), extractDecisionFromReport(), getMarketLabels(), getReportSignature(), HistoryPage(), parseUTCDate(), IMPORTANT: Delete from BOTH cloud AND local to prevent re-sync issues (+14 more)

### Community 41 - "DataSourceKeyFields.tsx"
Cohesion: 0.12
Nodes (21): ApiKeyHelpLink(), Props, DATA_SOURCE_FIELDS, DataSourceField, DataSourceKeyFields(), Props, SettingsText, FormControl() (+13 more)

### Community 42 - "ConditionalLogic"
Cohesion: 0.14
Nodes (15): ConditionalLogic, 使用設定參數進行初始化。          Args:             max_debate_rounds (int): 投資辯論的最大回合數。, 處理用於確定圖流程的條件邏輯。     這個類別定義了在圖中不同節點之間轉換的規則，     例如，決定下一個應該執行的代理或是否繼續一個循環。, Propagator, 處理狀態在圖中的初始化和傳播。     這個類別負責建立圖執行的初始狀態，並提供圖呼叫所需的參數。, 使用設定參數進行初始化。          Args:             max_recur_limit (int): 圖的最大遞迴深度限制，以防止無限循, 處理對決策的反思並更新記憶。     這個類別的目的是評估過去的交易決策，從中學習，並將學到的知識儲存起來以供未來使用。, Reflector (+7 more)

### Community 43 - "isCloudSyncEnabled"
Cohesion: 0.19
Nodes (21): SyncInitializer(), getAuthHeaders(), getAuthToken(), getReportKey(), markForRetry(), retryMap, retryPendingSyncs(), RetryRecord (+13 more)

### Community 44 - "ApiSettingsDialog.tsx"
Cohesion: 0.16
Nodes (22): ApiSettingsDialog(), formSchema, FormValues, keyValidationMessage(), AuthContext, AuthContextType, AuthProvider(), User (+14 more)

### Community 45 - "utils.ts"
Cohesion: 0.15
Nodes (15): DEMO_URLS, DemoPage(), LoadedDemo, AnalystInfo, DownloadReports(), DownloadReportsProps, Button(), buttonVariants (+7 more)

### Community 46 - "LwcPriceChart.tsx"
Cohesion: 0.16
Nodes (19): compactVolume(), formatTime(), LegendState, LwcPriceChart(), LwcPriceChartInner(), LwcPriceChartProps, PALETTE, ReferenceLine (+11 more)

### Community 47 - "routes.py"
Cohesion: 0.12
Nodes (20): cleanup_task(), delete_pdf_temp(), download_reports(), generate_pdf_temp(), get_task_status(), get_tickers(), API route definitions for TradingAgentsX Backend, Get the status of an analysis task.          Args:         task_id: Task identif (+12 more)

### Community 48 - "PriceChart.tsx"
Cohesion: 0.21
Nodes (17): PriceChart(), PriceChartProps, PriceMode, availableRanges(), closeOf(), formatDay(), monthsBefore(), parseDay() (+9 more)

### Community 49 - "output_filter.py"
Cohesion: 0.15
Nodes (19): count_chinese_words(), ensure_min_length(), fix_common_llm_errors(), is_truncated(), _normalize_content(), post_process_agent_output(), Normalize LLM response content to a plain string.      Some providers (e.g. Gemi, Strip word count annotations that models insert into section headings.     Examp (+11 more)

### Community 50 - "__init__.py"
Cohesion: 0.16
Nodes (16): Base, check_db_connection(), get_db(), init_db(), Database configuration and connection management, Check if database connection is working, Base class for all database models, Dependency for getting database sessions (+8 more)

### Community 51 - "PendingTaskRecovery.tsx"
Cohesion: 0.22
Nodes (12): AnalysisPage(), AuthCallbackContent(), PendingTaskRecovery(), useAnalysisContext(), useAuth(), useAnalysis(), clearPendingTask(), getPendingTask() (+4 more)

### Community 52 - "verify_access_token"
Cohesion: 0.13
Nodes (16): SSE stream for real-time cross-device sync.     The JWT must come in the Authori, user_events(), create_access_token(), decrypt_settings(), encrypt_settings(), _get_fernet_key(), get_user_id_from_token(), Any (+8 more)

### Community 53 - "LanguageContext.tsx"
Cohesion: 0.20
Nodes (13): getServerSnapshot(), getStoredLocale(), LanguageContext, LanguageContextType, LanguageProvider(), subscribeToStorage(), useTranslation(), en (+5 more)

### Community 54 - "auth.py"
Cohesion: 0.21
Nodes (15): exchange_google_token(), get_current_user(), get_frontend_url(), get_google_client_id(), get_google_client_secret(), google_callback(), google_login(), AsyncSession (+7 more)

### Community 55 - "TickerCombobox.tsx"
Cohesion: 0.25
Nodes (14): TickerCombobox(), TickerComboboxProps, displayName(), loadStocks(), loadTw(), loadUs(), lookupStockName(), MarketType (+6 more)

### Community 56 - "useLanguage"
Cohesion: 0.28
Nodes (11): LoginButton(), LoginPrompt(), Header(), LanguageSwitcher(), LanguageSwitcherProps, ThemeToggle(), DropdownMenu(), DropdownMenuContent() (+3 more)

### Community 57 - "validate_api_keys"
Cohesion: 0.26
Nodes (13): _check_alpha_vantage(), _check_anthropic(), _check_finmind(), _check_google(), _check_openai_compatible(), Live connectivity/auth checks for user-supplied API keys.  Used by the Settings, Google's SDK (google-genai) raises ClientError for a bad key, but     unlike Ope, Alpha Vantage returns HTTP 200 even for an invalid key — the error     shows up (+5 more)

### Community 58 - "DebateCard.tsx"
Cohesion: 0.19
Nodes (10): DebateCardProps, TONE_THEME, Dialog(), DialogContent(), DialogDescription(), DialogFooter(), DialogHeader(), DialogOverlay() (+2 more)

### Community 59 - "layout.tsx"
Cohesion: 0.19
Nodes (8): inter, metadata, spaceGrotesk, Footer(), ThemeProvider(), AnalysisContext, AnalysisContextType, AnalysisProvider()

### Community 60 - "AgentFlowDiagram.tsx"
Cohesion: 0.25
Nodes (8): AgentCard(), AgentFlowDiagram(), CARD_TONES, CardTone, DataSourceCard(), ManagerCard(), toneStyles(), TraderCard()

### Community 61 - "MarkdownReport.tsx"
Cohesion: 0.33
Nodes (9): MarkdownReport(), MarkdownReportProps, isPreamble(), normalizeHeading(), normalizeReportMarkdown(), PREAMBLE, SENTENCE_ENDINGS, stripBold() (+1 more)

### Community 62 - "PdfPreviewModal.tsx"
Cohesion: 0.31
Nodes (8): PdfPreviewModal(), PdfPreviewModalProps, usePdfPreview(), buildPdfRequestBody(), detectLanguage(), getPath(), PDF_SECTIONS, toText()

### Community 63 - "crypto.ts"
Cohesion: 0.35
Nodes (10): clearCryptoData(), decrypt(), decryptObject(), deriveKey(), encrypt(), encryptObject(), generateSalt(), getBrowserFingerprint() (+2 more)

### Community 64 - "_summarize_section"
Cohesion: 0.22
Nodes (9): create_report_summarizer(), _lang(), Report Summarizer — 將 4 份分析師報告「分別」壓縮後，合併成單一結構化摘要。  用途：在 Bull/Bear 研究員和風險辯論員收到報告之, 摘要單一份報告；沒有報告時不呼叫 LLM，失敗或空輸出時退回原文。, 建立 Report Summarizer 節點。      Args:         llm: quick_thinking_llm（使用者設定的輕量模型）, _summarize_section(), make_cached_system_message(), 建立 SystemMessage，若使用 Claude 則自動加上 cache_control 啟用 Prompt Caching。      - Claude (+1 more)

### Community 65 - "dependencies.py"
Cohesion: 0.25
Nodes (8): get_current_user_optional(), get_current_user_required(), get_trading_service(), Any, Shared dependencies for API routes, Dependency to get trading service instance, Get current user from JWT token (optional - returns None if not authenticated), Get current user from JWT token (required - raises 401 if not authenticated)

### Community 66 - "Settings"
Cohesion: 0.25
Nodes (6): Config, Configuration management for TradingAgentsX Backend API, Application settings loaded from environment variables, Get CORS origins from environment or use defaults, Settings, BaseSettings

### Community 67 - "AnalysisProgress.tsx"
Cohesion: 0.36
Nodes (7): AGENT_NAME_KEYS, AnalysisProgress(), AnalysisProgressProps, fill(), formatDuration(), ProgressDetail, ProgressStep

### Community 68 - "run_analysis"
Cohesion: 0.29
Nodes (6): Start an async trading analysis task.          This endpoint creates an async ta, run_analysis(), AnalysisRequest, Request model for trading analysis, Response when a task is created, TaskCreatedResponse

### Community 69 - "chat_with_report"
Cohesion: 0.33
Nodes (6): chat_with_report(), Chat with the analysis report using the user's LLM.          Sends the analysis, ChatRequest, ChatResponse, Request model for chatting about analysis reports, Response model for chat

### Community 70 - "validate_keys"
Cohesion: 0.33
Nodes (6): Test connectivity/auth for each non-empty API key the user submitted     in the, validate_keys(), One optional field per key the settings dialog can submit.     Only non-empty fi, Keyed by field name; only fields that were actually tested appear., ValidateKeysRequest, ValidateKeysResponse

### Community 71 - "__main__.py"
Cohesion: 0.40
Nodes (5): main(), parse_args(), Backend module entry point Run with: python -m backend Options:   --reload / --r, Parse command line arguments, Start the FastAPI server

### Community 72 - "getBackendUrl"
Cohesion: 0.60
Nodes (3): POST(), proxyRequest(), getBackendUrl()

### Community 73 - "Hero.tsx"
Cohesion: 0.40
Nodes (4): Hero(), HeroTradingCanvas(), Node, NODE_COLORS

### Community 74 - ".__init__"
Cohesion: 0.40
Nodes (3): ChatOpenAI, 使用一個 LLM 初始化反思器。          Args:             quick_thinking_llm (ChatOpenAI): 用於生, 獲取用於反思的系統提示。         這個提示指導 LLM 如何分析交易決策、提出改進建議並總結經驗教訓。

### Community 75 - "get_config"
Cohesion: 0.50
Nodes (4): get_config(), Get available configuration options, ConfigResponse, Response model for configuration options

### Community 76 - "health_check"
Cohesion: 0.50
Nodes (4): health_check(), Health check endpoint, HealthResponse, Response model for health check

## Knowledge Gaps
- **88 isolated node(s):** `DEMO_URLS`, `ChatMessage`, `ANALYSTS`, `inter`, `spaceGrotesk` (+83 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `_summarize_section()` connect `_summarize_section` to `output_filter.py`, `prompts.py`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `get_section_summarizer_prompt()` connect `prompts.py` to `_summarize_section`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Why does `useLanguage()` connect `useLanguage` to `ResultsView.tsx`, `LivePriceChart.tsx`, `AnalysisProgress.tsx`, `page.tsx`, `AnalysisForm.tsx`, `page.tsx`, `Hero.tsx`, `DataSourceKeyFields.tsx`, `ApiSettingsDialog.tsx`, `utils.ts`, `PriceChart.tsx`, `PendingTaskRecovery.tsx`, `LanguageContext.tsx`, `TickerCombobox.tsx`, `DebateCard.tsx`, `AgentFlowDiagram.tsx`, `PdfPreviewModal.tsx`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `PDFGenerator` (e.g. with `DownloadService` and `.__init__()`) actually correct?**
  _`PDFGenerator` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `DEMO_URLS`, `ChatMessage`, `ANALYSTS` to the rest of the system?**
  _88 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `social_sentiment.py` be split into smaller, more focused modules?**
  _Cohesion score 0.051970302684180465 - nodes in this community are weakly interconnected._
- **Should `finmind.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06013745704467354 - nodes in this community are weakly interconnected._