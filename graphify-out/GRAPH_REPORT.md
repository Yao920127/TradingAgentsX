# Graph Report - .  (2026-11-17)

## Corpus Check
- Large corpus: 339 files · ~2,829,557 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder.

## Summary
- 2292 nodes · 4927 edges · 138 communities (117 shown, 21 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 180 edges (avg confidence: 0.72)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- PDF Download & Name Lookup
- Taste Skill Assets Script
- Download Service
- Analysis Progress UI
- AI Security Hunting Guide
- Alpha Vantage Data
- Inspect Script
- Project Docs & Architecture
- Draw Script
- Price Service
- Analysis Form & Report
- Live Price Tests
- News & Social Tests
- Agent State & Routing
- Live Price API
- History Chat Page
- API Schemas
- Home Page UI
- User & Report API
- News Provider Tests
- Dataflow Utils
- Debate History Tests
- Core Stock Tools
- REST Routes & PDF
- Key Validation Service
- Login & Header
- Hybrid Task Manager
- Results Helpers
- API Key Help & Fields
- API Settings & Crypto
- Analyst Nodes
- Config & CORS
- Sync Initializer
- Retry Utils
- Dataflow Interface
- Redis Client
- Analysis & Auth Pages
- Results Page
- Research & Risk Managers
- Auth Dependencies
- Misc: test_ptt_date_infers_previous_ye
- Misc: Any
- Misc: design-taste-frontend README
- Misc: Article
- Misc: auth.py
- Misc: bull_researcher.py
- Misc: database.py
- Misc: DownloadReports.tsx
- Misc: FinancialSituationMemory
- Misc: S01 Tech Minimal
- Misc: DebateCard.tsx
- Misc: LanguageContext.tsx
- Misc: test_body_sentence_with_action_w
- Misc: TickerCombobox.tsx
- Misc: SystemMessage
- Misc: Analysis History page (English)
- Misc: test_report_summarizer.py
- Misc: config.py
- Misc: progress.py
- Misc: FullReport.tsx
- Misc: HybridSearchEngine
- Misc: set_config()
- Misc: truncate()
- Misc: MessageBuffer
- Misc: DashboardScreen
- Misc: Changed
- Misc: Enum
- Misc: layout.tsx
- Misc: Lock
- Misc: health_check()
- Misc: lint.mjs
- Misc: main.py
- Misc: analysis.py
- Misc: 首頁截圖 (繁中)：TradingAgentsX 首頁 Hero
- Misc: chat_with_report()
- Misc: report_summarizer.py
- Misc: social_media_analyst.py
- Misc: HybridFinancialMemory
- Misc: App
- Misc: AVGO Fundamentals Report Screens
- Misc: jina_reader.py
- Misc: config.py
- Misc: Multi-provider LLM support (BYOK
- Misc: AnalysisForm()
- Misc: hybrid_search.py
- Misc: auth-context.tsx
- Misc: ._reciprocal_rank_fusion()
- Misc: Words (copy)
- Misc: __main__.py
- Misc: backend/requirements.txt Python 
- Misc: clean_cache.sh
- Misc: route.ts
- Misc: Next.js App Router Icon Set (ico
- Misc: requirements.txt Python dependen
- Misc: AnalysisRequest
- Misc: Test connectivity/auth for each 
- Misc: Application settings loaded from
- Misc: VerdictBanner.tsx
- Misc: LoadingSpinner.tsx
- Misc: .__init__()
- Misc: Colour
- Misc: Critique of the render
- Misc: Imagery
- Misc: Layout
- Misc: Motion
- Misc: The study
- Misc: Type
- Misc: S13 Art Deco
- Misc: Cactus Classical Serif font (OFL
- Misc: route.ts
- Misc: SoftAurora.jsx
- Misc: next.config.ts
- Misc: NVDA PDF Report Preview (zh-TW)
- Misc: __init__.py
- Misc: __init__.py
- Misc: __init__.py
- Misc: __init__.py
- Misc: __init__.py
- Misc: eslint.config.mjs
- Misc: postcss.config.mjs
- Misc: css.d.ts
- Misc: .__init__()
- Misc: .__init__()
- Misc: DELETE
- Misc: GET
- Misc: PATCH
- Misc: POST
- Misc: PUT
- Misc: Google Search Console site verif
- Misc: tradingagents

## God Nodes (most connected - your core abstractions)
1. `cn()` - 86 edges
2. `useLanguage()` - 55 edges
3. `_make_api_request()` - 39 edges
4. `PDFGenerator` - 33 edges
5. `getOne()` - 32 edges
6. `normalize_stock_id()` - 28 edges
7. `isCloudSyncEnabled()` - 25 edges
8. `NewsProviderError` - 25 edges
9. `TradingAgentsXGraph` - 25 edges
10. `route_to_vendor()` - 24 edges

## Surprising Connections (you probably didn't know these)
- `AVGO analysis report (EN, 2026-04-01)` --conceptually_related_to--> `LangGraph multi-agent pipeline (analysis, research debate, risk debate, trader)`  [INFERRED]
  report/en/AVGO_Report_2026-04-01.pdf → README_EN.md
- `NVDA analysis report (EN, 2026-04-01)` --conceptually_related_to--> `LangGraph multi-agent pipeline (analysis, research debate, risk debate, trader)`  [INFERRED]
  report/en/NVDA_Report_2026-04-01.pdf → README_EN.md
- `CLAUDE.md (repo guidance for Claude Code)` --semantically_similar_to--> `README_EN.md (English project README)`  [INFERRED] [semantically similar]
  CLAUDE.md → README_EN.md
- `README.md (Traditional Chinese project README)` --semantically_similar_to--> `README_EN.md (English project README)`  [INFERRED] [semantically similar]
  README.md → README_EN.md
- `extractDecisionFromResult()` --indirect_call--> `text()`  [INFERRED]
  frontend/lib/report-utils.ts → .claude/skills/design-taste-frontend/scripts/assets.mjs

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Six-phase full audit pipeline** — _claude_skills_security_audit_reconnaissance, _claude_skills_security_audit_hunting, _claude_skills_security_audit_validation_and_reporting, _claude_skills_security_audit_skill_full_audit_workflow [EXTRACTED 1.00]
- **Domain companion hunting guides selected from ATTACK-CLASSES** — _claude_skills_security_audit_ai_and_llm, _claude_skills_security_audit_client_side, _claude_skills_security_audit_cloud_and_deployment, _claude_skills_security_audit_data_isolation_and_lifecycle, _claude_skills_security_audit_desktop_mobile_and_local_ipc, _claude_skills_security_audit_memory_safety_and_binary, _claude_skills_security_audit_protocols_rpc_and_messaging, _claude_skills_security_audit_resource_exhaustion_and_availability, _claude_skills_security_audit_supply_chain_and_release, _claude_skills_security_audit_web_protocol_and_auth [EXTRACTED 1.00]
- **Candidate to verified-record to report verification chain** — _claude_skills_security_audit_hunting_structured_result, _claude_skills_security_audit_validation_and_reporting_candidate_verifier, _claude_skills_security_audit_validation_and_reporting_findings_json, _claude_skills_security_audit_validation_and_reporting_final_verification, _claude_skills_security_audit_validation_and_reporting_report_files [EXTRACTED 1.00]
- **Hard offset shadow, thick border styles** — claude_skills_style_prompt_references_s04_brutalist, claude_skills_style_prompt_references_s10_memphis, claude_skills_style_prompt_references_s11_neobrutalism [INFERRED 0.85]
- **Zero-radius grid-driven styles** — claude_skills_style_prompt_references_s02_minimalistmonochrome, claude_skills_style_prompt_references_s03_swiss, claude_skills_style_prompt_references_s04_brutalist, claude_skills_style_prompt_references_s06_bauhaus [INFERRED 0.75]
- **Neon futuristic styles** — claude_skills_style_prompt_references_s16_cyberpunk, claude_skills_style_prompt_references_s17_synthwave, claude_skills_style_prompt_references_s29_cyberbionoir [INFERRED 0.85]
- **Luxury styles** — claude_skills_style_prompt_references_s19_luxuryeditorial, claude_skills_style_prompt_references_s22_luxurygold, claude_skills_style_prompt_references_s23_luxurysilver, claude_skills_style_prompt_references_s24_minimalistserif [INFERRED 0.85]
- **Corporate styles** — claude_skills_style_prompt_references_s25_startupvibrant, claude_skills_style_prompt_references_s26_enterpriseblue, claude_skills_style_prompt_references_s27_fintechtrust [INFERRED 0.85]
- **LangGraph agent pipeline phases** — concept_analyst_team, concept_report_summarizer, concept_research_debate, concept_risk_debate [EXTRACTED 1.00]
- **Stock ticker list refresh flow** — github_workflows_refresh_stock_lists_yml, scripts_refresh_stocks_tw, scripts_refresh_stocks_us, frontend_public_data_stocks_json [EXTRACTED 1.00]
- **BYOK 設定到分析流程** — web_screenshot_concept_byok_encryption, web_screenshot_concept_data_api_keys, web_screenshot_concept_llm_provider_keys, web_screenshot_concept_analysis_form [INFERRED 0.85]
- **Report detail page sections** — web_screenshot_5_final_decision_banner, web_screenshot_5_price_trend_chart, web_screenshot_5_1_debate_cards_zh, web_screenshot_5_2_full_report_tabs [INFERRED 0.85]
- **Report viewing: detail, PDF preview, Q&A chat** — web_screenshot_5_en, web_screenshot_6_pdf_preview_modal, web_screenshot_7_report_chat_feature [INFERRED 0.75]
- **LLM provider logos used in UI** — frontend_public_logos_llm_provider_logos, frontend_public_logos_deepseek_color, frontend_public_logos_gemini_color, frontend_public_logos_grok, frontend_public_logos_openai, frontend_public_logos_qwen_color, frontend_public_logos_huggingface_color [INFERRED 0.85]
- **App icon variants derived from brand logo** — frontend_public_logo, frontend_app_icon_set, frontend_public_icon_v8_set, frontend_public_apple_touch_icon [INFERRED 0.85]

## Communities (138 total, 21 thin omitted)

### Community 0 - "PDF Download & Name Lookup"
Cohesion: 0.06
Nodes (92): _finmind_stock_name(), _is_taiwan_ticker(), Download Service for Analyst Reports Generates combined PDF reports with all ana, 以 FinMind TaiwanStockInfo 取得台股中文簡稱（如 2379 → 瑞昱），失敗回傳空字串（不快取失敗）。, 解析封面公司全名：一律優先英文名（yfinance），台股查不到時退回 FinMind 中文名，再不行回傳 ticker。, resolve_cover_company_name(), datetime, Series (+84 more)

### Community 1 - "Taste Skill Assets Script"
Cohesion: 0.07
Nodes (85): AIC_FIELDS, AIC_HEADERS, applyThumb(), ARCHIVE_LICENCE, args, argv, base(), clock() (+77 more)

### Community 2 - "Download Service"
Cohesion: 0.06
Nodes (34): DownloadService, Create a single combined PDF containing all analyst reports                  Fea, Service for handling analyst report downloads, Initialize download service, get_model_display_name(), get_pdf_label(), PDFGenerator, Full-bleed navy section divider (+26 more)

### Community 3 - "Analysis Progress UI"
Cohesion: 0.06
Nodes (56): AGENT_NAME_KEYS, AnalysisProgress(), AnalysisProgressProps, fill(), formatDuration(), LivePriceChart(), LivePriceChartProps, LiveStats() (+48 more)

### Community 4 - "AI Security Hunting Guide"
Cohesion: 0.05
Nodes (67): AI, LLM, and Agent Hunting, Action-confirmation and approval binding, Excessive agency and confused-deputy authority, MCP and sub-agent trust classes, Persistent memory poisoning and indirect injection, Prompt injection alone is not a finding, Attack Classes, Access control attack class (+59 more)

### Community 5 - "Alpha Vantage Data"
Cohesion: 0.08
Nodes (43): AlphaVantageAPIError, AlphaVantageRateLimitError, _filter_csv_by_date_range(), format_datetime_for_api(), get_api_key(), _make_api_request(), Exception, 過濾 CSV 數據，只包含指定日期範圍內的資料列。      Args:         csv_data: 來自 Alpha Vantage API 的 CS (+35 more)

### Community 6 - "Inspect Script"
Cohesion: 0.07
Nodes (21): allow, args, asJson, fails, HEIGHT, merged, name(), outDir (+13 more)

### Community 7 - "Project Docs & Architecture"
Cohesion: 0.07
Nodes (39): CLAUDE.md (repo guidance for Claude Code), Analyst team (market, news, social, fundamentals), BYOK mode (AES-GCM encrypted browser-stored API keys), ChromaDB memory system, FastAPI backend service, FinMind Taiwan stock data, Floorplan interactive codebase map (Railway), Jina AI Reader full-text extraction (+31 more)

### Community 8 - "Draw Script"
Cohesion: 0.10
Nodes (39): adjustments(), argv, assetQueries(), ASSETS_PATH, briefStop(), briefWords(), deal(), dealHero() (+31 more)

### Community 9 - "Price Service"
Cohesion: 0.08
Nodes (25): get_trading_service(), Dependency to get trading service instance, PriceService, Any, DataFrame, Path, Price data service for loading and processing stock price data, Service for loading and processing price data from data_cache (+17 more)

### Community 10 - "Analysis Form & Report"
Cohesion: 0.10
Nodes (28): AnalysisFormProps, formSchema, AnalystReport(), AnalystReportProps, ReportSection(), calculateHeikinAshi(), HeikinAshiCandlestickShapeProps, HeikinAshiData (+20 more)

### Community 11 - "Live Price Tests"
Cohesion: 0.11
Nodes (22): _build(), _FakeTicker, _intraday_frame(), _ny_epoch(), _patch_yf(), DataFrame, 即時股價服務與 /api/price/live 接口的單元測試（不打外部 API）。, test_build_live_quote_marks_market_closed_when_last_bar_is_stale() (+14 more)

### Community 12 - "News & Social Tests"
Cohesion: 0.08
Nodes (31): _article(), _FakeResponse, 新聞聚合、社群情緒、Alpha Vantage 錯誤處理與簡轉繁的單元測試（不打外部 API）。, _recording_paid_sources(), _Response, _stub_social(), test_alpha_vantage_error_payloads_raise(), test_alpha_vantage_news_feed_gets_jina_content() (+23 more)

### Community 13 - "Agent State & Routing"
Cohesion: 0.12
Nodes (20): MessagesState, AgentState, InvestDebateState, RiskDebateState, ConditionalLogic, 判斷風險分析是否應該繼續。         如果討論回合數達到上限，則由風險裁判做出最終決定。         否則，在激進、保守和中立分析師之間輪流進行。, 判斷市場分析是否應該繼續。         如果最後一條訊息包含工具呼叫，則表示代理需要使用工具，         流程應該轉到市場工具節點。否則，分析完成。, 判斷社群媒體分析是否應該繼續。         邏輯與 `should_continue_market` 類似。          Args: (+12 more)

### Community 14 - "Live Price API"
Cohesion: 0.10
Nodes (31): live_price(), Live price routes: today's intraday quote for the results page "Live" mode., Latest price plus today's 1-minute prices and volumes (Yahoo, may be delayed)., _bar_sessions(), build_live_quote(), _current_session(), fetch_live_quote(), get_live_quote() (+23 more)

### Community 15 - "History Chat Page"
Cohesion: 0.10
Nodes (28): AVAILABLE_MODELS, ChatMessage, HistoryChatContent(), MONO_LOGOS, Badge(), badgeVariants, CardAction(), CardFooter() (+20 more)

### Community 16 - "API Schemas"
Cohesion: 0.08
Nodes (32): AnalysisRequest, AnalysisResponse, AnalystReport, ChatResponse, ErrorResponse, KeyValidationResult, LiveCandle, LivePricePoint (+24 more)

### Community 17 - "Home Page UI"
Cohesion: 0.08
Nodes (16): frame(), HomePage(), AgentFlowDiagram(), FullReport(), HeroTradingCanvas(), Node, NODE_COLORS, ImmersivePortalHero() (+8 more)

### Community 18 - "User & Report API"
Cohesion: 0.12
Nodes (32): cleanup_duplicate_reports(), create_report(), delete_all_reports(), delete_report(), get_current_user_optional(), get_current_user_required(), get_report(), get_report_counts() (+24 more)

### Community 19 - "News Provider Tests"
Cohesion: 0.10
Nodes (30): ProviderCall, test_gdelt_retries_once_after_rate_limit(), test_get_news_raises_when_every_provider_is_empty(), test_global_news_drops_articles_after_analysis_date(), test_search_name_strips_corporate_suffix(), _build_report(), _company_query(), get_global_news() (+22 more)

### Community 20 - "Dataflow Utils"
Cohesion: 0.08
Nodes (22): decorate_all_methods(), get_current_date(), get_next_weekday(), DataFrame, SavePathType, 將 DataFrame 儲存到 CSV 檔案。      Args:         data (pl.DataFrame): 要儲存的 DataFrame。, 以 YYYY-MM-DD 格式獲取當前日期。      Returns:         str: 當前日期字串。, 一個裝飾器，用於將另一個裝飾器應用於一個類別的所有方法。      Args:         decorator: 要應用的裝飾器。      Returns (+14 more)

### Community 21 - "Debate History Tests"
Cohesion: 0.11
Nodes (25): FakeLLM, FakeMemory, 辯論歷史工具與辯論者節點的單元測試（不打外部 API）。, 每次呼叫回傳帶序號的內容，並記錄收到的 human message。, test_bull_and_bear_keep_only_their_final_round(), test_compact_falls_back_to_tail_when_turns_cannot_be_split(), test_compact_keeps_recent_turns_in_full_and_digests_earlier_ones(), test_compact_returns_short_history_unchanged() (+17 more)

### Community 22 - "Core Stock Tools"
Cohesion: 0.09
Nodes (27): test_empty_vendor_result_falls_back_to_next_vendor(), test_multi_vendor_stops_before_fallback_vendors(), get_stock_data(), 檢索給定股票代碼的股價數據 (OHLCV)。     使用設定的核心股票 API 供應商。     Args:         symbol (str): 公司, get_balance_sheet(), get_cashflow(), get_fundamentals(), get_income_statement() (+19 more)

### Community 23 - "REST Routes & PDF"
Cohesion: 0.10
Nodes (26): cleanup_task(), delete_pdf_temp(), download_reports(), generate_pdf_temp(), get_config(), get_task_status(), get_tickers(), API route definitions for TradingAgentsX Backend (+18 more)

### Community 24 - "Key Validation Service"
Cohesion: 0.11
Nodes (25): _check_alpha_vantage(), _check_anthropic(), _check_finmind(), _check_google(), _check_openai_compatible(), Live connectivity/auth checks for user-supplied API keys.  Used by the Settings, Google's SDK (google-genai) raises ClientError for a bad key, but     unlike Ope, Alpha Vantage returns HTTP 200 even for an invalid key — the error     shows up (+17 more)

### Community 25 - "Login & Header"
Cohesion: 0.14
Nodes (18): LoginButton(), LoginPrompt(), Header(), LanguageSwitcher(), LanguageSwitcherProps, ThemeToggle(), DropdownMenu(), DropdownMenuCheckboxItem() (+10 more)

### Community 26 - "Hybrid Task Manager"
Cohesion: 0.13
Nodes (15): HybridTaskManager, Any, Get task from in-memory first, then Redis, Create a new task with initial data                  Args:             initial_d, Update task status and optional progress message                  Args:, Update task progress message                  Args:             task_id: Task ID, Update structured agent progress (steps, current agent, timings)          Args:, Set task result and mark as completed.                  Note: Completed tasks wi (+7 more)

### Community 27 - "Results Helpers"
Cohesion: 0.14
Nodes (21): ANALYSTS, detectReportLanguage(), extractDecisionFromReport(), getMarketLabels(), getReportSignature(), HistoryPage(), parseUTCDate(), IMPORTANT: Delete from BOTH cloud AND local to prevent re-sync issues (+13 more)

### Community 28 - "API Key Help & Fields"
Cohesion: 0.12
Nodes (21): ApiKeyHelpLink(), Props, DATA_SOURCE_FIELDS, DataSourceField, DataSourceKeyFields(), Props, SettingsText, FormControl() (+13 more)

### Community 29 - "API Settings & Crypto"
Cohesion: 0.17
Nodes (24): ApiSettingsDialog(), keyValidationMessage(), clearCryptoData(), decrypt(), decryptObject(), deriveKey(), encrypt(), encryptObject() (+16 more)

### Community 30 - "Analyst Nodes"
Cohesion: 0.15
Nodes (23): create_market_analyst(), 建立一個市場分析師節點。      Args:         llm: 用於分析的語言模型。         language: 報告語言 ('en' 或 ', create_news_analyst(), 建立一個新聞分析師節點。      Args:         llm: 用於分析的語言模型。         language: 報告語言 ('en' 或 ', get_agent_role_instruction(), get_analyst_principles(), get_context_message(), get_fundamentals_analyst_prompt() (+15 more)

### Community 31 - "Config & CORS"
Cohesion: 0.10
Nodes (18): Config, Configuration management for TradingAgentsX Backend API, Configure CORS middleware for the FastAPI application, setup_cors(), global_exception_handler(), Exception, RateLimitMiddleware, FastAPI application entry point for TradingAgentsX Backend (+10 more)

### Community 32 - "Sync Initializer"
Cohesion: 0.19
Nodes (21): SyncInitializer(), getAuthHeaders(), getAuthToken(), getReportKey(), markForRetry(), retryMap, retryPendingSyncs(), RetryRecord (+13 more)

### Community 33 - "Retry Utils"
Cohesion: 0.12
Nodes (22): log_retry_attempt(), Exception, 重試工具模組，提供統一的重試機制和錯誤處理, 重試裝飾器，支援指數退避          Args:         max_attempts: 最大重試次數（包含首次嘗試）         backoff, 記錄重試嘗試的標準回調函數          Args:         attempt: 當前嘗試次數         exception: 遇到的例外, retry(), get_balance_sheet(), get_cashflow() (+14 more)

### Community 34 - "Dataflow Interface"
Cohesion: 0.14
Nodes (21): get_data_in_range(), get_finnhub_company_insider_sentiment(), get_finnhub_company_insider_transactions(), get_finnhub_news(), get_reddit_company_news(), get_reddit_global_news(), get_simfin_balance_sheet(), get_simfin_cashflow() (+13 more)

### Community 35 - "Redis Client"
Cohesion: 0.14
Nodes (21): cache_delete(), cache_get(), cache_set(), check_rate_limit(), delete_task_from_redis(), get_redis_client(), get_task_from_redis(), Any (+13 more)

### Community 36 - "Analysis & Auth Pages"
Cohesion: 0.17
Nodes (15): AnalysisPage(), AuthCallbackContent(), PendingTaskRecovery(), AnalysisContext, AnalysisContextType, AnalysisProvider(), useAnalysisContext(), useAuth() (+7 more)

### Community 37 - "Results Page"
Cohesion: 0.14
Nodes (19): AnalysisResultsPage(), ANALYST_REPORT_KEYS, asContent(), getNestedValue(), DebateCard(), DebateTone, DEBATE_ROUND_PREFIXES, decision() (+11 more)

### Community 38 - "Research & Risk Managers"
Cohesion: 0.14
Nodes (19): create_research_manager(), 建立一個研究管理員（裁判）節點。      Args:         llm: 用於生成決策和計畫的語言模型。         memory: 儲存過去情況和, create_risk_manager(), 建立一個風險管理員（裁判）節點。      Args:         llm: 用於生成決策的語言模型。         memory: 儲存過去情況和反思的, create_trader(), 建立一個交易員節點。      Args:         llm: 用於生成決策的語言模型。         memory: 儲存過去情況和反思的記憶體物件。, get_bear_researcher_prompt(), get_debate_principles() (+11 more)

### Community 39 - "Auth Dependencies"
Cohesion: 0.11
Nodes (20): get_current_user_optional(), get_current_user_required(), Any, Shared dependencies for API routes, Get current user from JWT token (optional - returns None if not authenticated), Get current user from JWT token (required - raises 401 if not authenticated), SSE stream for real-time cross-device sync.     The JWT must come in the Authori, user_events() (+12 more)

### Community 40 - "Misc: test_ptt_date_infers_previous_ye"
Cohesion: 0.21
Nodes (21): test_ptt_date_infers_previous_year_for_later_month(), get_env_key(), apewisdom_rank(), _clean_ptt_body(), _epoch(), _get(), get_social_sentiment(), hacker_news() (+13 more)

### Community 41 - "Misc: Any"
Cohesion: 0.14
Nodes (13): Any, ChatOpenAI, 反思看漲研究員的分析並更新其記憶。          Args:             current_state: 當前的圖狀態。, 反思看跌研究員的分析並更新其記憶。          Args:             current_state: 當前的圖狀態。, 反思交易員的決策並更新其記憶。          Args:             current_state: 當前的圖狀態。             re, 使用一個 LLM 初始化反思器。          Args:             quick_thinking_llm (ChatOpenAI): 用於生, 反思投資裁判的決策並更新其記憶。          Args:             current_state: 當前的圖狀態。             r, 反思風險管理者的決策並更新其記憶。          Args:             current_state: 當前的圖狀態。 (+5 more)

### Community 42 - "Misc: design-taste-frontend README"
Cohesion: 0.14
Nodes (21): design-taste-frontend README, tasteskill v2 (design-taste-frontend), Anti-slop house style, draw.mjs direction dealer (3 of 20 directions), Style S16: Cyberpunk, Style S17: Synthwave, Style S18: Y2K, Style S19: Luxury Editorial (+13 more)

### Community 43 - "Misc: Article"
Cohesion: 0.24
Nodes (19): Article, NewsProviderError, Exception, 供應商回傳錯誤或無法使用（缺金鑰、權限不足、配額用盡）。, require_env_key(), _finnhub_articles(), finnhub_company_news(), finnhub_general_news() (+11 more)

### Community 44 - "Misc: auth.py"
Cohesion: 0.17
Nodes (19): exchange_google_token(), get_current_user(), get_frontend_url(), get_google_client_id(), get_google_client_secret(), google_callback(), google_login(), AsyncSession (+11 more)

### Community 45 - "Misc: bull_researcher.py"
Cohesion: 0.14
Nodes (18): create_bull_researcher(), 建立一個看漲研究員節點。      Args:         llm: 用於生成回應的語言模型。         memory: 儲存過去情況和反思的記憶體物, create_risky_debator(), 建立一個激進的風險辯論員節點。      Args:         llm: 用於生成回應的語言模型。         language: 報告語言 ('en, fix_common_llm_errors(), post_process_agent_output(), Strip word count annotations that models insert into section headings.     Examp, Fix common LLM character selection errors and strip preamble text.      Args: (+10 more)

### Community 46 - "Misc: database.py"
Cohesion: 0.16
Nodes (16): Base, check_db_connection(), get_db(), init_db(), Database configuration and connection management, Check if database connection is working, Base class for all database models, Dependency for getting database sessions (+8 more)

### Community 47 - "Misc: DownloadReports.tsx"
Cohesion: 0.19
Nodes (12): AnalystInfo, DownloadReports(), DownloadReportsProps, Button(), buttonVariants, Calendar(), CalendarDayButton(), DatePicker() (+4 more)

### Community 48 - "Misc: FinancialSituationMemory"
Cohesion: 0.15
Nodes (10): FinancialSituationMemory, Get embedding for a text using the configured provider., Get embedding using the local backend (sentence-transformers 或 ONNX)., Get embedding using OpenAI API., Add financial situations and their corresponding advice. Parameter is a list of, Initialize the memory with configurable embedding provider.                  Con, Find matching recommendations using embeddings, Initialize local embedding without any API key.          優先用 sentence-transforme (+2 more)

### Community 49 - "Misc: S01 Tech Minimal"
Cohesion: 0.15
Nodes (17): S01 Tech Minimal, S02 Minimalist Monochrome, S03 Swiss Design, S04 Brutalist, S05 Japanese Minimal, S06 Bauhaus Modernism, S07 Glassmorphism, S08 Dark Mode Elegance (+9 more)

### Community 50 - "Misc: DebateCard.tsx"
Cohesion: 0.19
Nodes (12): DebateCardProps, TONE_THEME, formSchema, FormValues, Dialog(), DialogContent(), DialogDescription(), DialogFooter() (+4 more)

### Community 51 - "Misc: LanguageContext.tsx"
Cohesion: 0.20
Nodes (13): getServerSnapshot(), getStoredLocale(), LanguageContext, LanguageContextType, LanguageProvider(), subscribeToStorage(), useTranslation(), en (+5 more)

### Community 52 - "Misc: test_body_sentence_with_action_w"
Cohesion: 0.15
Nodes (16): test_body_sentence_with_action_word_is_not_treated_as_preamble(), test_label_lines_and_tables_get_separated_and_bullets_unified(), test_long_bold_sentence_is_not_turned_into_heading(), test_normalize_report_markdown_unifies_heading_styles(), test_report_preamble_and_rules_are_removed(), _is_preamble(), _normalize_line(), normalize_report_markdown() (+8 more)

### Community 53 - "Misc: TickerCombobox.tsx"
Cohesion: 0.25
Nodes (14): TickerCombobox(), TickerComboboxProps, displayName(), loadStocks(), loadTw(), loadUs(), lookupStockName(), MarketType (+6 more)

### Community 54 - "Misc: SystemMessage"
Cohesion: 0.23
Nodes (11): SystemMessage, create_fundamentals_analyst(), 建立一個基本面分析師節點。      Args:         llm: 用於分析的語言模型。         language: 報告語言 ('en' 或, create_safe_debator(), 建立一個保守的風險辯論員節點。      Args:         llm: 用於生成回應的語言模型。         language: 報告語言 ('en, create_msg_delete(), make_cached_system_message(), 建立 SystemMessage，若使用 Claude 則自動加上 cache_control 啟用 Prompt Caching。      - Claude (+3 more)

### Community 55 - "Misc: Analysis History page (English)"
Cohesion: 0.14
Nodes (16): Analysis History page (English), 分析歷史頁面 (繁中), Deep/quick LLM model labels on cards, Market tabs: US / TWSE / TPEX, Saved report card (view, PDF, report Q&A, delete), Bull Researcher and Bear Researcher, 多空辯論與風險辯論卡片, Bull vs Bear and Risk debate cards (AVGO, English) (+8 more)

### Community 56 - "Misc: test_report_summarizer.py"
Cohesion: 0.27
Nodes (12): FakeLLM, Report Summarizer 的單元測試：四份報告分別摘要後再合併（不打外部 API）。, 記錄每次呼叫的 human message，並回傳可辨識的摘要。, test_each_report_is_summarized_in_its_own_call(), test_empty_llm_output_falls_back_to_original_report(), test_english_headings(), test_failed_section_falls_back_to_original_report_only_for_that_section(), test_missing_report_skips_llm_and_marks_unavailable() (+4 more)

### Community 57 - "Misc: config.py"
Cohesion: 0.21
Nodes (12): get_config(), initialize_config(), get_vendor(), 獲取數據類別或特定工具方法的已設定供應商。     工具級別的設定優先於類別級別。, append_linked_content(), 讀取文字中引用的前 top_n 個網址，把全文摘錄附在文末。, get_fundamentals_openai(), get_global_news_openai() (+4 more)

### Community 58 - "Misc: progress.py"
Cohesion: 0.26
Nodes (4): ProgressTracker, Any, ProgressCallback, 根據所選分析師與辯論回合數建立步驟計畫，並依節點事件更新狀態。      進度百分比以「代理回合」計算：每位分析師、每次辯論發言、     摘要員、研究經理、交

### Community 59 - "Misc: FullReport.tsx"
Cohesion: 0.24
Nodes (11): FullReportProps, FullReportSection, MarkdownReport(), MarkdownReportProps, isPreamble(), normalizeHeading(), normalizeReportMarkdown(), PREAMBLE (+3 more)

### Community 60 - "Misc: HybridSearchEngine"
Cohesion: 0.21
Nodes (6): HybridSearchEngine, 取得文字的嵌入向量（自動截斷至 4000 字元）。, 從目前語料庫重建 BM25Okapi 索引。, 將文件加入混合搜索索引。          Args:             documents : 文件字串列表             metadatas, 向量語意搜索（ChromaDB）。         回傳 [(文件ID, 相似度分數), ...] 依分數降序排列。, 混合搜索引擎：結合 BM25 關鍵字搜索與向量語意搜索。      工作流程：     1. add_documents() — 同時建立 BM25 倒排索引和

### Community 61 - "Misc: set_config()"
Cohesion: 0.14
Nodes (10): set_config(), ChatOpenAI, 使用一個 LLM 進行初始化以進行處理。          Args:             quick_thinking_llm (ChatOpenAI):, 處理完整的交易信號以提取核心決策。          Args:             full_signal (str): 完整的交易信號文本。, 處理交易信號以提取可執行的決策。     這個類別的目的是將來自代理的自然語言格式的完整交易信號，     轉換為標準化的、機器可讀的決策（例如 "BUY",, SignalProcessor, Any, ToolNode (+2 more)

### Community 62 - "Misc: truncate()"
Cohesion: 0.27
Nodes (13): truncate(), _flatten_metrics(), _linked_articles(), lunarcrush_topic(), Any, SourceResult, 需要金鑰的社群來源（皆為選用，未設定金鑰就略過）：  - StockTwits  經 Apify 的 fetch_cat/stocktwits-scraper, 取出數值與短字串欄位，以及一層的 dict（例如各平台情緒），交給 LLM 解讀。 (+5 more)

### Community 63 - "Misc: MessageBuffer"
Cohesion: 0.16
Nodes (4): MessageBuffer, 合併工具呼叫與一般訊息，依時間排序後回傳最近 N 筆。, 回傳 (工具呼叫數, LLM 呼叫數, 已生成報告數)。, 用於儲存和管理應用程式訊息、工具呼叫和報告狀態的緩衝區。

### Community 64 - "Misc: DashboardScreen"
Cohesion: 0.24
Nodes (3): DashboardScreen, ComposeResult, Screen

### Community 65 - "Misc: Changed"
Cohesion: 0.23
Nodes (4): Changed, ConfigScreen, Screen, 驗證並收集所有選項，回傳 selections 字典；失敗時回傳 None。

### Community 66 - "Misc: Enum"
Cohesion: 0.21
Nodes (11): Enum, str, embedding_models_for(), env_api_key_for_model(), env_api_key_for_provider(), infer_provider_from_model(), 根據嵌入供應商的 URL 回傳對應的模型清單。, 根據供應商名稱從環境變數讀取對應的 API Key（找不到回傳 None）。 (+3 more)

### Community 67 - "Misc: layout.tsx"
Cohesion: 0.21
Nodes (7): inter, metadata, CustomCursor(), Footer(), SoftAurora, SoftAuroraBackground(), ThemeProvider()

### Community 68 - "Misc: Lock"
Cohesion: 0.17
Nodes (12): Lock, load_price_csv_cached(), _lock_for(), NoPriceDataError, DataFrame, Exception, 下載結果為空：代碼不存在、已下市，或該期間沒有任何價格資料。, 每個快取檔案一把鎖，避免平行工具呼叫同時讀寫同一個 CSV。 (+4 more)

### Community 69 - "Misc: health_check()"
Cohesion: 0.17
Nodes (9): health_check(), Health check endpoint, HealthResponse, Response model for health check, is_redis_available(), Check if Redis is available and connected., Delete a task                  Args:             task_id: Task ID, Initialize hybrid task storage (+1 more)

### Community 70 - "Misc: lint.mjs"
Cohesion: 0.20
Nodes (11): args, asJson, byId, EXT, files, findings, R, roots (+3 more)

### Community 71 - "Misc: main.py"
Cohesion: 0.20
Nodes (6): ProgressCallback, 在特定日期為某家公司執行交易代理圖。          Args:             company_name (str): 公司名稱或股票代碼。, 根據回報反思決策並更新記憶。         這個方法會觸發對每個相關代理的決策進行反思的過程。, 處理信號以提取核心決策。         將原始的 LLM 輸出轉換為標準化的交易信號（例如，BUY, SELL, HOLD）。, 協調交易代理框架的主要類別。     這個類別整合了所有組件，包括 LLM、記憶體、工具和圖的邏輯，     以執行一個完整的金融分析和交易決策流程。, TradingAgentsXGraph

### Community 72 - "Misc: analysis.py"
Cohesion: 0.24
Nodes (8): build_config(), 依使用者選擇組出 TradingAgentsXGraph 的設定字典。回傳 (config, notes)。, 執行完整的分析流程。      參數:         selections (dict): 使用者於設定畫面收集到的所有選項。         buffer, run_analysis(), _content_to_str(), 將訊息內容（可能是 Anthropic 的區塊列表）轉換為純字串。, _decision_badge(), 依 BUY / SELL / HOLD 產生帶色的最終決策標記。

### Community 73 - "Misc: 首頁截圖 (繁中)：TradingAgentsX 首頁 Hero"
Cohesion: 0.17
Nodes (12): 首頁截圖 (繁中)：TradingAgentsX 首頁 Hero, Home page screenshot (EN): TradingAgentsX Hero, API 配置對話框截圖 (繁中), API Configuration dialog screenshot (EN), 交易分析頁截圖 (繁中), Trading Analysis page screenshot (EN), Analysis form: analyst team, market type, ticker autocomplete, date, depth, quick/deep/embedding models, BYOK API keys encrypted in browser (AES-256-GCM) (+4 more)

### Community 74 - "Misc: chat_with_report()"
Cohesion: 0.22
Nodes (10): chat_with_report(), Chat with the analysis report using the user's LLM.          Sends the analysis, ChatRequest, Request model for chatting about analysis reports, chat_with_reports(), _flatten_reports(), Any, Chat service for answering questions about analysis reports Uses the user's LLM (+2 more)

### Community 75 - "Misc: report_summarizer.py"
Cohesion: 0.24
Nodes (10): _lang(), Report Summarizer — 將 4 份分析師報告「分別」壓縮後，合併成單一結構化摘要。  用途：在 Bull/Bear 研究員和風險辯論員收到報告之, 摘要單一份報告；沒有報告時不呼叫 LLM，失敗或空輸出時退回原文。, _summarize_section(), _normalize_content(), Normalize LLM response content to a plain string.      Some providers (e.g. Gemi, get_section_summarizer_prompt(), get_section_summary_title() (+2 more)

### Community 76 - "Misc: social_media_analyst.py"
Cohesion: 0.25
Nodes (9): create_social_media_analyst(), 建立一個社群媒體分析師節點。      Args:         llm: 用於分析的語言模型。         language: 報告語言 ('en' 或, count_chinese_words(), ensure_min_length(), is_truncated(), 確保報告達到字數要求範圍 (500-1000)，如果不符合則返回False觸發重試      Args:         content: The report, 取出 LLM 回應的報告文字；若因長度上限被截斷，記錄警告並在文末加註。, Count Chinese characters in text (excluding markdown and tables)          Args: (+1 more)

### Community 77 - "Misc: HybridFinancialMemory"
Cohesion: 0.25
Nodes (5): HybridFinancialMemory, Any, 混合搜索金融記憶體 (Hybrid Financial Memory)      在 FinancialSituationMemory 的向量搜索基礎上，, 新增金融情境與建議，同時建立 BM25 索引和向量索引。         Parameter: list of (situation, recommendati, 混合搜索：BM25 + 向量搜索，透過 RRF 融合後回傳最相關的過去情境。          Args:             current_situat

### Community 78 - "Misc: App"
Cohesion: 0.24
Nodes (6): App, main(), _prewarm_multiprocessing(), 在 Textual 接管終端機之前，先啟動 multiprocessing 的 resource_tracker。      背景說明：         分析過, TradingAgentsX 的 Textual 應用程式。, TradingAgentsXApp

### Community 79 - "Misc: AVGO Fundamentals Report Screens"
Cohesion: 0.22
Nodes (10): AVGO Fundamentals Report Screenshot (EN), Broadcom (AVGO) Fundamental Analysis Report, Full Report Tabs (Fundamentals, Technical, News, Social Sentiment, Trader Verdict), AVGO Detailed Analysis Results Screenshot (EN), HOLD Final Call Card, AVGO Price Trend Chart (line/candlestick, +75.52%), NVDA Report Q&A Chat Screenshot (zh-TW), AVGO Ask About Report Chat Screenshot (EN) (+2 more)

### Community 80 - "Misc: jina_reader.py"
Cohesion: 0.33
Nodes (8): _clean(), enrich_with_content(), _is_body_line(), Jina AI Reader（r.jina.ai）：把新聞網址轉成乾淨文字，讓 LLM 讀到內文而不只是標題。  免金鑰可用（約 20 RPM）；設定 JINA, 為前 top_n 則新聞補上全文摘錄（並行擷取），其餘原樣保留。, 並行讀取多個網址，失敗的位置回傳空字串（順序與輸入相同）。, read_article(), read_urls()

### Community 81 - "Misc: config.py"
Cohesion: 0.36
Nodes (4): Field, ComposeResult, Section, Vertical

### Community 82 - "Misc: Multi-provider LLM support (BYOK"
Cohesion: 0.25
Nodes (8): Multi-provider LLM support (BYOK), DeepSeek logo, Gemini logo, Grok logo, HuggingFace logo, LLM Provider Logo Set (Claude, DeepSeek, Gemini, Grok, HuggingFace, OpenAI, Qwen), OpenAI logo, Qwen logo

### Community 83 - "Misc: AnalysisForm()"
Cohesion: 0.39
Nodes (6): AnalysisForm(), ChatMessage, ReportChat(), ReportChatProps, getApiKeyForModel(), getBaseUrlForModel()

### Community 84 - "Misc: hybrid_search.py"
Cohesion: 0.32
Nodes (5): extract_tickers(), 混合搜索引擎 (Hybrid Search Engine)  結合兩種互補的搜索策略： - BM25 關鍵字搜索 (Keyword Search)：精確匹配股票, BM25 關鍵字搜索，含股票代號精確匹配加分。         回傳 [(文件索引, 分數), ...] 依分數降序排列。, 將財務文字分詞，保留股票代號和財務術語的原始大小寫。     其他詞彙統一轉為小寫以提升 BM25 召回率。, tokenize_financial_text()

### Community 85 - "Misc: auth-context.tsx"
Cohesion: 0.38
Nodes (6): AuthContext, AuthContextType, AuthProvider(), User, clearAllReports(), clearApiSettings()

### Community 86 - "Misc: ._reciprocal_rank_fusion()"
Cohesion: 0.29
Nodes (4): Any, 倒數排名融合 (RRF)：合併 BM25 與向量搜索的排名。          RRF 分數 = Σ weight_i / (k + rank_i), 混合搜索：BM25 關鍵字 + 向量語意，透過 RRF 融合排名。          Args:             query     : 查詢字串（可包, 搜索並回傳格式化字串，供 LLM Agent 直接使用。         每條結果顯示 BM25 分數、向量分數、混合分數及文件摘要。

### Community 87 - "Misc: Words (copy)"
Cohesion: 0.33
Nodes (6): Words (copy), Copy tells, Two-line headline, Tells registry, Dated waves of generated tells, Structural tells

### Community 88 - "Misc: __main__.py"
Cohesion: 0.40
Nodes (5): main(), parse_args(), Backend module entry point Run with: python -m backend Options:   --reload / --r, Parse command line arguments, Start the FastAPI server

### Community 89 - "Misc: backend/requirements.txt Python "
Cohesion: 0.33
Nodes (6): backend/requirements.txt Python dependencies, chromadb + sentence-transformers memory, Market data libs (yfinance, finnhub, akshare, tushare), FastAPI, SQLAlchemy, asyncpg, redis, PyJWT backend stack, langgraph / langchain LLM stack, PDF generation libs (fpdf2, reportlab)

### Community 90 - "Misc: clean_cache.sh"
Cohesion: 0.67
Nodes (5): remove_by_name(), remove_path(), section(), clean_cache.sh script, usage()

### Community 91 - "Misc: route.ts"
Cohesion: 0.60
Nodes (3): POST(), proxyRequest(), getBackendUrl()

### Community 92 - "Misc: Next.js App Router Icon Set (ico"
Cohesion: 0.40
Nodes (6): Next.js App Router Icon Set (icon, favicon, icon-192/512, apple-icon, apple-touch-icon), Public apple-touch-icon.png, Public v8 Cache-busted Icon Set (favicon, icon-192/512, apple-icon, apple-touch-icon), TradingAgentsX Brand Logo (bull-horned circuit brain with candlestick chart arrow, 'AI Trading Platform'), TradingAgentsX Logo (dark variant), Tauric Research logo (8x8 green dot-matrix pattern SVG)

### Community 93 - "Misc: requirements.txt Python dependen"
Cohesion: 0.33
Nodes (6): requirements.txt Python dependencies, chromadb + sentence-transformers memory, Market data libs (yfinance, finnhub, akshare, tushare), langgraph / langchain LLM stack, TUI libs (chainlit, rich, questionary), TUI ASCII welcome banner (TradingAgentsX)

### Community 94 - "Misc: AnalysisRequest"
Cohesion: 0.40
Nodes (5): AnalysisRequest, Start an async trading analysis task.          This endpoint creates an async ta, run_analysis(), Response when a task is created, TaskCreatedResponse

### Community 95 - "Misc: Test connectivity/auth for each "
Cohesion: 0.40
Nodes (5): Test connectivity/auth for each non-empty API key the user submitted     in the, validate_keys(), Keyed by field name; only fields that were actually tested appear., ValidateKeysResponse, ValidateKeysRequest

### Community 96 - "Misc: Application settings loaded from"
Cohesion: 0.40
Nodes (4): Application settings loaded from environment variables, Get CORS origins from environment or use defaults, Settings, BaseSettings

### Community 97 - "Misc: VerdictBanner.tsx"
Cohesion: 0.50
Nodes (4): SIGNAL_THEME, VerdictBanner(), VerdictBannerProps, DecisionSignal

### Community 99 - "Misc: .__init__()"
Cohesion: 0.50
Nodes (3): ChatOpenAI, ToolNode, 使用必要的組件進行初始化。          Args:             quick_thinking_llm (ChatOpenAI): 用於快速任務

### Community 100 - "Misc: Colour"
Cohesion: 0.67
Nodes (3): Colour, Banned colour families, Palette roles

### Community 101 - "Misc: Critique of the render"
Cohesion: 0.67
Nodes (3): Critique of the render, Fix first, then stop, Score rubric

### Community 102 - "Misc: Imagery"
Cohesion: 0.67
Nodes (3): Imagery, Drawing the subject, Open-collection pictures

### Community 103 - "Misc: Layout"
Cohesion: 0.67
Nodes (3): Layout, Layout failure modes, Margins and grid

### Community 104 - "Misc: Motion"
Cohesion: 0.67
Nodes (3): Motion, Motion budget, Reduced motion

### Community 105 - "Misc: The study"
Cohesion: 0.67
Nodes (3): The study, Scores and method, Top 25 sites

### Community 106 - "Misc: Type"
Cohesion: 0.67
Nodes (3): Type, Loading fonts, Type scale

### Community 107 - "Misc: S13 Art Deco"
Cohesion: 1.00
Nodes (3): S13 Art Deco, S14 Art Nouveau, Luxury style category

### Community 108 - "Misc: Cactus Classical Serif font (OFL"
Cohesion: 0.67
Nodes (3): Cactus Classical Serif font (OFL 1.1), Noto Serif TC font (OFL 1.1), Noto Serif TC variable font README

### Community 112 - "Misc: NVDA PDF Report Preview (zh-TW)"
Cohesion: 1.00
Nodes (3): NVDA PDF Report Preview (zh-TW), AVGO PDF Report Preview (EN), PDF Report Preview Modal with Download

## Knowledge Gaps
- **214 isolated node(s):** `SELF`, `SOURCES`, `SOURCE_ALIAS`, `VIDEO_TYPES`, `SAFE` (+209 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Reflector` connect `Misc: Any` to `Misc: set_config()`, `Agent State & Routing`, `Misc: main.py`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Why does `cn()` connect `History Chat Page` to `Misc: VerdictBanner.tsx`, `Misc: LoadingSpinner.tsx`, `Analysis Progress UI`, `Results Page`, `Analysis Form & Report`, `Misc: DownloadReports.tsx`, `Home Page UI`, `Misc: DebateCard.tsx`, `Misc: AnalysisForm()`, `Misc: TickerCombobox.tsx`, `Login & Header`, `Misc: FullReport.tsx`, `API Key Help & Fields`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Why does `chat_with_reports()` connect `Misc: chat_with_report()` to `REST Routes & PDF`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **What connects `SELF`, `SOURCES`, `SOURCE_ALIAS` to the rest of the system?**
  _214 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `PDF Download & Name Lookup` be split into smaller, more focused modules?**
  _Cohesion score 0.058383838383838385 - nodes in this community are weakly interconnected._
- **Should `Taste Skill Assets Script` be split into smaller, more focused modules?**
  _Cohesion score 0.06730506155950752 - nodes in this community are weakly interconnected._
- **Should `Download Service` be split into smaller, more focused modules?**
  _Cohesion score 0.060528559249786874 - nodes in this community are weakly interconnected._