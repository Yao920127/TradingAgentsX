# Graph Report - TradingAgentsX  (2026-11-03)

## Corpus Check
- 355 files · ~291,777 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 31 file(s) not represented in the graph (top: (none) 10, .ttf 10, .css 3)

## Summary
- 2664 nodes · 6134 edges · 138 communities (87 shown, 51 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 272 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- PDF 下載與公司名稱
- 設計素材腳本
- 歷史與結果頁面
- API 路由與報告
- 登入與首頁動畫
- 股票清單刷新
- 分析表單與聊天
- 發現驗證腳本
- 下載服務 PDF
- 分析結果元件
- 新聞測試
- 研究經理節點
- 使用者與報告資料
- 首頁區塊元件
- 設計抽卡腳本
- 游標特效
- 分析頁與進度
- 資安攻擊類別文件
- 覆蓋帳本驗證
- Taste 設計技能
- 股票工具與基本面
- 分析師節點
- Google OAuth
- AgentState 與 LangGraph
- 新聞供應商測試
- 設定與 CORS
- 混合任務管理器
- 版面與全域樣式
- 瀏覽器檢查器
- 資料流介面
- Redis 快取與限流
- 交易服務整合
- Google 新聞備援
- Docker Compose
- 風險經理與交易員
- 新聞聚合器
- Stockstats 指標
- 社群情緒
- 反思記憶
- ESLint 與依賴
- 混合搜尋引擎
- 資料庫連線
- CDP 瀏覽器
- 報告摘要器
- API 金鑰驗證
- 報告聊天頁
- API 依賴注入
- 聊天服務
- 覆蓋帳本測試
- shadcn 設定
- 前端依賴
- 財務情境記憶
- tsconfig
- TUI 應用
- README 英文
- Yahoo Finance 工具
- TUI 儀表板
- 排程工作流程
- 驗證與報告指南
- TUI 分析執行
- Community 60
- Community 61
- Community 62
- Community 63
- Community 64
- Community 65
- Community 66
- Community 67
- Community 68
- Community 69
- Community 70
- Community 71
- Community 72
- Community 73
- Community 74
- Community 75
- Community 76
- Community 77
- Community 78
- Community 79
- Community 80
- Community 81
- Community 82
- Community 83
- Community 84
- Community 86
- Community 87
- Community 88
- Community 89
- Community 90
- Community 91
- Community 92
- Community 93
- Community 94
- Community 95
- Community 96
- Community 97
- Community 98
- Community 99
- Community 100
- Community 101
- Community 102
- Community 103
- Community 104
- Community 105
- Community 106
- Community 108
- Community 116
- Community 117
- Community 118
- Community 119
- Community 120
- Community 121
- Community 122
- Community 123
- Community 124
- Community 125
- Community 126
- Community 127
- Community 128
- Community 129
- Community 130
- Community 131
- Community 133
- Community 134
- Community 135

## God Nodes (most connected - your core abstractions)
1. `cn()` - 86 edges
2. `useLanguage()` - 53 edges
3. `react` - 48 edges
4. `SplashCursor()` - 44 edges
5. `HistoryPage()` - 39 edges
6. `_make_api_request()` - 39 edges
7. `Button()` - 36 edges
8. `make_cached_system_message()` - 33 edges
9. `FinMindError` - 32 edges
10. `getOne()` - 31 edges

## Surprising Connections (you probably didn't know these)
- `AVGO analysis report 2026-04-01 (EN)` --conceptually_related_to--> `AI agent team: analysts, researchers, risk, trader`  [INFERRED]
  report/en/AVGO_Report_2026-04-01.pdf → README.md
- `NVDA analysis report 2026-04-01 (EN)` --conceptually_related_to--> `AI agent team: analysts, researchers, risk, trader`  [INFERRED]
  report/en/NVDA_Report_2026-04-01.pdf → README.md
- `AVGO analysis report 2026-03-21 (zh-TW)` --conceptually_related_to--> `AI agent team: analysts, researchers, risk, trader`  [INFERRED]
  report/zh_tw/AVGO_Report_2026-03-21.pdf → README.md
- `NVDA analysis report 2026-05-10 (zh-TW)` --conceptually_related_to--> `AI agent team: analysts, researchers, risk, trader`  [INFERRED]
  report/zh_tw/NVDA_Report_2026-05-10.pdf → README.md
- `chromadb + sentence-transformers memory` --semantically_similar_to--> `ChromaDB agent memory`  [INFERRED] [semantically similar]
  backend/requirements.txt → README.md

## Import Cycles
- 2-file cycle: `frontend/contexts/auth-context.tsx -> frontend/lib/user-api.ts -> frontend/contexts/auth-context.tsx`

## Hyperedges (group relationships)
- **Security audit domain hunting playbooks** — _claude_skills_security_audit_ai_and_llm, _claude_skills_security_audit_attack_classes, _claude_skills_security_audit_client_side, _claude_skills_security_audit_cloud_and_deployment, _claude_skills_security_audit_data_isolation_and_lifecycle, _claude_skills_security_audit_desktop_mobile_and_local_ipc, _claude_skills_security_audit_hunting, _claude_skills_security_audit_memory_safety_and_binary, _claude_skills_security_audit_protocols_rpc_and_messaging, _claude_skills_security_audit_reconnaissance, _claude_skills_security_audit_resource_exhaustion_and_availability, _claude_skills_security_audit_supply_chain_and_release [EXTRACTED 1.00]
- **UI style library references** — claude_skills_style_prompt_references_s01_techminimal, claude_skills_style_prompt_references_s02_minimalistmonochrome, claude_skills_style_prompt_references_s03_swiss, claude_skills_style_prompt_references_s04_brutalist, claude_skills_style_prompt_references_s05_japaneseminimal, claude_skills_style_prompt_references_s06_bauhaus [EXTRACTED 1.00]
- **style-prompt library styles S22-S30** — claude_skills_style_prompt_references_s22_luxurygold, claude_skills_style_prompt_references_s23_luxurysilver, claude_skills_style_prompt_references_s24_minimalistserif, claude_skills_style_prompt_references_s25_startupvibrant, claude_skills_style_prompt_references_s26_enterpriseblue, claude_skills_style_prompt_references_s27_fintechtrust, claude_skills_style_prompt_references_s28_claymorphism, claude_skills_style_prompt_references_s29_cyberbionoir, claude_skills_style_prompt_references_s30_auroraborealis [EXTRACTED 1.00]

## Communities (138 total, 51 thin omitted)

### Community 0 - "PDF 下載與公司名稱"
Cohesion: 0.06
Nodes (50): _finmind_stock_name(), _is_taiwan_ticker(), resolve_cover_company_name(), _convert_to_serializable(), _filter_by_date_range(), FinMindAuthenticationError, FinMindDataNotFoundError, FinMindError (+42 more)

### Community 1 - "設計素材腳本"
Cohesion: 0.07
Nodes (85): AIC_FIELDS, AIC_HEADERS, applyThumb(), ARCHIVE_LICENCE, args, argv, base(), clock() (+77 more)

### Community 2 - "歷史與結果頁面"
Cohesion: 0.07
Nodes (60): AuthCallbackContent(), AuthCallbackPage(), LoadingFallback(), ANALYSTS, detectReportLanguage(), extractDecisionFromReport(), getMarketLabels(), getReportSignature() (+52 more)

### Community 3 - "API 路由與報告"
Cohesion: 0.05
Nodes (29): chat_with_report(), download_reports(), generate_pdf_temp(), get_task_status(), get_tickers(), health_check(), run_analysis(), report_progress() (+21 more)

### Community 4 - "登入與首頁動畫"
Cohesion: 0.07
Nodes (50): GoogleIcon(), LoginButton(), LoginPrompt(), HeroTradingCanvas(), Node, NODE_COLORS, ImmersivePortalHero(), Header() (+42 more)

### Community 5 - "股票清單刷新"
Cohesion: 0.06
Nodes (26): write_rows(), fetch_json(), load_live_registry(), main(), fetch_sec_tickers(), main(), AlphaVantageAPIError, AlphaVantageRateLimitError (+18 more)

### Community 6 - "分析表單與聊天"
Cohesion: 0.08
Nodes (49): AnalysisForm(), formSchema, ChatMessage, ReportChat(), ReportChatProps, TickerCombobox(), ApiKeyHelpLink(), Props (+41 more)

### Community 7 - "發現驗證腳本"
Cohesion: 0.06
Nodes (54): canonicalKey(), append(), encode(), codePointLength(), collect(), collectDataLimitErrors(), collectFindingSemanticErrors(), collectSchemaErrors() (+46 more)

### Community 8 - "下載服務 PDF"
Cohesion: 0.06
Nodes (5): DownloadService, get_model_display_name(), get_pdf_label(), PDFGenerator, _ReportPDF

### Community 9 - "分析結果元件"
Cohesion: 0.08
Nodes (41): AnalysisResultsPage(), ANALYST_REPORT_KEYS, asContent(), getNestedValue(), DebateCard(), DebateCardProps, DebateTone, TONE_THEME (+33 more)

### Community 10 - "新聞測試"
Cohesion: 0.06
Nodes (35): _article(), _FakeResponse, _recording_paid_sources(), paid(), _Response, stub_company(), _stub_social(), test_alpha_vantage_error_payloads_raise() (+27 more)

### Community 11 - "研究經理節點"
Cohesion: 0.10
Nodes (21): create_research_manager(), research_manager_node(), create_bear_researcher(), bear_node(), create_bull_researcher(), bull_node(), create_risky_debator(), risky_node() (+13 more)

### Community 12 - "使用者與報告資料"
Cohesion: 0.08
Nodes (20): cleanup_duplicate_reports(), create_report(), delete_all_reports(), delete_report(), get_current_user_optional(), get_current_user_required(), get_report(), get_report_counts() (+12 more)

### Community 13 - "首頁區塊元件"
Cohesion: 0.14
Nodes (38): AgentCard(), FeatureCard(), HomePage(), LLMProviderCard(), SectionHeading(), TechnicalCard(), WorkflowStep(), AgentCard() (+30 more)

### Community 14 - "設計抽卡腳本"
Cohesion: 0.09
Nodes (39): adjustments(), argv, assetQueries(), ASSETS_PATH, briefStop(), briefWords(), deal(), dealHero() (+31 more)

### Community 15 - "游標特效"
Cohesion: 0.09
Nodes (39): SplashCursor(), addKeywords(), applyInputs(), calcDeltaTime(), clickSplat(), compileShader(), correctDeltaX(), correctDeltaY() (+31 more)

### Community 16 - "分析頁與進度"
Cohesion: 0.09
Nodes (34): AnalysisPage(), AnalysisFormProps, AGENT_NAME_KEYS, AnalysisProgress(), AnalysisProgressProps, fill(), formatDuration(), TradingDecisionProps (+26 more)

### Community 17 - "資安攻擊類別文件"
Cohesion: 0.05
Nodes (41): AI LLM and agent hunting, MCP trust classes, Prompt injection and memory attacks, Attack classes, Attack class selection, Client-side and browser hunting, DOM attack classes, Service-worker storage attacks (+33 more)

### Community 18 - "覆蓋帳本驗證"
Cohesion: 0.13
Nodes (39): ATTEMPT_FIELDS, ATTEMPT_STATUSES, collectUnitErrors(), createErrorList(), escapeUnsafeDiagnosticCharacters(), fs, hasOwn(), hasValidSemanticFields() (+31 more)

### Community 19 - "Taste 設計技能"
Cohesion: 0.06
Nodes (34): tasteskill v2 README, assets.mjs open image search, draw.mjs direction dealer, inspect.mjs browser inspector, lint.mjs static scan, Study of 247 curated sites, Colour, Banned colour families (+26 more)

### Community 20 - "股票工具與基本面"
Cohesion: 0.11
Nodes (14): fundamentals_analyst_node(), get_stock_data(), get_balance_sheet(), get_cashflow(), get_fundamentals(), get_income_statement(), get_global_news(), get_insider_sentiment() (+6 more)

### Community 21 - "分析師節點"
Cohesion: 0.13
Nodes (17): create_fundamentals_analyst(), create_market_analyst(), market_analyst_node(), create_news_analyst(), news_analyst_node(), create_social_media_analyst(), social_media_analyst_node(), report_text() (+9 more)

### Community 22 - "Google OAuth"
Cohesion: 0.10
Nodes (13): exchange_google_token(), get_current_user(), get_frontend_url(), get_google_client_id(), get_google_client_secret(), google_callback(), google_login(), TokenExchangeRequest (+5 more)

### Community 23 - "AgentState 與 LangGraph"
Cohesion: 0.11
Nodes (4): AgentState, ConditionalLogic, GraphSetup, SignalProcessor

### Community 24 - "新聞供應商測試"
Cohesion: 0.14
Nodes (23): test_gdelt_retries_once_after_rate_limit(), flaky(), test_get_news_raises_when_every_provider_is_empty(), get_global_news(), get_news(), marketaux(), _run_providers(), _throttled_gdelt() (+15 more)

### Community 25 - "設定與 CORS"
Cohesion: 0.08
Nodes (6): setup_cors(), global_exception_handler(), RateLimitMiddleware, root(), SecurityHeadersMiddleware, SensitiveDataFilter

### Community 27 - "版面與全域樣式"
Cohesion: 0.11
Nodes (17): inter, metadata, RootLayout(), CustomCursor(), Footer(), hexToVec3(), SoftAurora(), SoftAurora (+9 more)

### Community 28 - "瀏覽器檢查器"
Cohesion: 0.09
Nodes (17): allow, args, asJson, fails, HEIGHT, merged, outDir, report (+9 more)

### Community 29 - "資料流介面"
Cohesion: 0.12
Nodes (13): get_category_for_method(), get_data_in_range(), get_finnhub_company_insider_sentiment(), get_finnhub_company_insider_transactions(), get_finnhub_news(), get_reddit_company_news(), get_reddit_global_news(), get_simfin_balance_sheet() (+5 more)

### Community 30 - "Redis 快取與限流"
Cohesion: 0.12
Nodes (10): cache_delete(), cache_get(), cache_set(), check_rate_limit(), delete_task_from_redis(), get_redis_client(), get_task_from_redis(), is_redis_available() (+2 more)

### Community 31 - "交易服務整合"
Cohesion: 0.10
Nodes (3): _apply_env_overrides(), _restore_env(), TradingAgentsXGraph

### Community 32 - "Google 新聞備援"
Cohesion: 0.12
Nodes (11): test_google_news_fallback_adds_jina_content_to_top_three(), get_global_news_google(), get_google_company_news(), get_google_news(), getNewsData(), is_rate_limited(), make_request(), _clean() (+3 more)

### Community 33 - "Docker Compose"
Cohesion: 0.09
Nodes (24): build, container_name, environment, networks, ports, restart, volumes, context (+16 more)

### Community 34 - "風險經理與交易員"
Cohesion: 0.14
Nodes (12): create_risk_manager(), risk_manager_node(), create_trader(), trader_node(), get_fundamentals_analyst_prompt(), get_language_closing_instruction(), get_language_instruction(), get_market_analyst_prompt() (+4 more)

### Community 35 - "新聞聚合器"
Cohesion: 0.14
Nodes (11): enrich_with_content(), _build_report(), _company_query(), _yf_symbol(), date_window(), dedupe_articles(), format_articles(), _normalize_title() (+3 more)

### Community 36 - "Stockstats 指標"
Cohesion: 0.14
Nodes (9): StockstatsUtils, get_balance_sheet(), get_cashflow(), get_fundamentals(), get_income_statement(), get_insider_transactions(), get_stock_stats_indicators_window(), get_stockstats_indicator() (+1 more)

### Community 37 - "社群情緒"
Cohesion: 0.19
Nodes (17): test_ptt_date_infers_previous_year_for_later_month(), get_env_key(), apewisdom_rank(), _clean_ptt_body(), _epoch(), _get(), get_social_sentiment(), hacker_news() (+9 more)

### Community 39 - "ESLint 與依賴"
Cohesion: 0.09
Nodes (22): eslintConfig, devDependencies, babel-plugin-react-compiler@1.0.0, baseline-browser-mapping@^2.9.2, eslint@^9, eslint-config-next@16.0.3, tailwindcss@^4, @tailwindcss/postcss@^4 (+14 more)

### Community 41 - "資料庫連線"
Cohesion: 0.13
Nodes (5): Base, check_db_connection(), get_db(), init_db(), startup_event()

### Community 42 - "CDP 瀏覽器"
Cohesion: 0.16
Nodes (4): Browser, findChrome(), Page, sleep()

### Community 43 - "報告摘要器"
Cohesion: 0.12
Nodes (10): create_report_summarizer(), summarizer_node(), count_chinese_words(), ensure_min_length(), is_truncated(), _normalize_content(), post_process_agent_output(), strip_preamble() (+2 more)

### Community 44 - "API 金鑰驗證"
Cohesion: 0.18
Nodes (8): _check_alpha_vantage(), _check_anthropic(), _check_finmind(), _check_google(), _check_openai_compatible(), _result(), validate_api_keys(), test()

### Community 45 - "報告聊天頁"
Cohesion: 0.16
Nodes (17): AVAILABLE_MODELS, ChatMessage, HistoryChatContent(), HistoryChatPage(), MONO_LOGOS, MarkdownReportProps, Select(), SelectContent() (+9 more)

### Community 46 - "API 依賴注入"
Cohesion: 0.13
Nodes (5): get_current_user_optional(), get_current_user_required(), get_trading_service(), get_config(), TradingService

### Community 47 - "聊天服務"
Cohesion: 0.14
Nodes (3): chat_with_reports(), _flatten_reports(), tokenize_financial_text()

### Community 48 - "覆蓋帳本測試"
Cohesion: 0.12
Nodes (15): canonicalCoverageId(), encodeCanonicalRef(), LIMITS, archivedAttempt(), assert, fs, localCheck(), os (+7 more)

### Community 49 - "shadcn 設定"
Cohesion: 0.10
Nodes (19): aliases, components, hooks, lib, ui, utils, iconLibrary, registries (+11 more)

### Community 50 - "前端依賴"
Cohesion: 0.10
Nodes (20): dependencies, class-variance-authority@^0.7.1, clsx@^2.1.1, date-fns@^4.1.0, lucide-react@^0.554.0, next@16.0.10, next-themes@^0.4.6, @radix-ui/react-dialog@^1.1.15 (+12 more)

### Community 52 - "tsconfig"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 54 - "README 英文"
Cohesion: 0.17
Nodes (18): Core features table (EN), Jina AI Reader full-text extraction (EN), Multi-source news aggregation (Finnhub, Marketaux, NewsAPI, GDELT) (EN), TradingAgentsX README (English), Quick start and Docker deployment (EN), Security features (rate limiting, key masking, OAuth) (EN), Social sentiment sources (StockTwits, X, Reddit, PTT) (EN), Project structure tree (EN) (+10 more)

### Community 57 - "排程工作流程"
Cohesion: 0.19
Nodes (5): on, schedule, workflow_dispatch, cron, ConfigScreen

### Community 58 - "驗證與報告指南"
Cohesion: 0.18
Nodes (5): Validation and Reporting guide, FINDINGS-DETAIL.md, NEEDS-VALIDATION.md, REPORT.md, HTTP-Protocol and Authentication Hunting

### Community 59 - "TUI 分析執行"
Cohesion: 0.15
Nodes (7): build_config(), run_analysis(), save_message_decorator(), wrapper(), save_report_section_decorator(), save_tool_call_decorator(), _content_to_str()

### Community 60 - "Community 60"
Cohesion: 0.17
Nodes (10): test_body_sentence_with_action_word_is_not_treated_as_preamble(), test_label_lines_and_tables_get_separated_and_bullets_unified(), test_long_bold_sentence_is_not_turned_into_heading(), test_normalize_report_markdown_unifies_heading_styles(), _is_preamble(), _normalize_line(), normalize_report_markdown(), normalize_reports() (+2 more)

### Community 62 - "Community 62"
Cohesion: 0.13
Nodes (14): SEC_CONTACT, jobs, refresh, name, permissions, contents, runs-on, steps (+6 more)

### Community 63 - "Community 63"
Cohesion: 0.27
Nodes (8): truncate(), _flatten_metrics(), _linked_articles(), lunarcrush_topic(), _run_apify_actor(), stocktwits_messages(), _tweet_date(), x_posts()

### Community 64 - "Community 64"
Cohesion: 0.15
Nodes (5): decorate_all_methods(), get_current_date(), get_next_weekday(), save_output(), init_ticker()

### Community 65 - "Community 65"
Cohesion: 0.19
Nodes (5): embedding_models_for(), env_api_key_for_model(), env_api_key_for_provider(), infer_provider_from_model(), AnalystType

### Community 66 - "Community 66"
Cohesion: 0.24
Nodes (10): LanguageContext, LanguageContextType, useTranslation(), en, TranslationKeys, defaultLocale, Locale, localeNames (+2 more)

### Community 69 - "Community 69"
Cohesion: 0.17
Nodes (12): backend/requirements.txt Python dependencies, Market data libs (yfinance, finnhub, akshare, tushare), FastAPI, SQLAlchemy, asyncpg, redis, PyJWT backend stack, langgraph / langchain LLM stack, PDF generation libs (fpdf2, reportlab), tradingagents/dataflows data sources (yfinance, AlphaVantage, FinMind), Fast vs Deep analysis mode, LLM config: deep_think_llm and quick_think_llm (+4 more)

### Community 70 - "Community 70"
Cohesion: 0.15
Nodes (13): Artistic style category, Style S06 Bauhaus Modernism, Bauhaus Modernism Design DNA, Bauhaus Modernism landing page prompt, Style S10 Memphis, Memphis Design DNA, Memphis landing page prompt, Style S12 Doodle Sketch (+5 more)

### Community 71 - "Community 71"
Cohesion: 0.17
Nodes (13): Futuristic style category, Style S07 Glassmorphism, Glassmorphism Design DNA, Glassmorphism landing page prompt, Style S16 Cyberpunk / TRON, Cyberpunk / TRON Design DNA, Cyberpunk / TRON landing page prompt, Style S17 Retro 80s Synthwave (+5 more)

### Community 72 - "Community 72"
Cohesion: 0.15
Nodes (13): Minimalist style category, Style S01 Tech Minimal, Tech Minimal Design DNA, Tech Minimal landing page prompt, Style S02 Minimalist Monochrome, Minimalist Monochrome Design DNA, Minimalist Monochrome landing page prompt, Style S05 Japanese Minimal (+5 more)

### Community 73 - "Community 73"
Cohesion: 0.23
Nodes (12): TickerComboboxProps, displayName(), loadStocks(), loadTw(), loadUs(), MarketType, rankStocks(), searchStocks() (+4 more)

### Community 74 - "Community 74"
Cohesion: 0.15
Nodes (12): ogl@^1.0.11, @radix-ui/react-dropdown-menu@^2.1.16, @radix-ui/react-select@^2.2.6, recharts@^3.4.1, name, private, type, version (+4 more)

### Community 75 - "Community 75"
Cohesion: 0.23
Nodes (3): InvestDebateState, RiskDebateState, Propagator

### Community 76 - "Community 76"
Cohesion: 0.17
Nodes (5): log_retry_attempt(), retry(), decorator(), class_decorator(), _get_stock_stats_bulk()

### Community 77 - "Community 77"
Cohesion: 0.17
Nodes (11): args, asJson, byId, EXT, files, findings, R, roots (+3 more)

### Community 78 - "Community 78"
Cohesion: 0.40
Nodes (11): JsonStructureError, preflightJsonText(), beginContainer(), beginString(), beginValue(), closeContainer(), countValue(), currentContainer() (+3 more)

### Community 79 - "Community 79"
Cohesion: 0.20
Nodes (4): GET(), getBaseUrl(), nextConfig, next

### Community 80 - "Community 80"
Cohesion: 0.25
Nodes (8): POST(), DELETE, GET, PATCH, POST, proxyRequest(), PUT, getBackendUrl()

### Community 81 - "Community 81"
Cohesion: 0.35
Nodes (10): clearCryptoData(), decrypt(), decryptObject(), deriveKey(), encrypt(), encryptObject(), generateSalt(), getBrowserFingerprint() (+2 more)

### Community 83 - "Community 83"
Cohesion: 0.22
Nodes (10): Luxury style category, Style S13 Art Deco, Art Deco Design DNA, Art Deco landing page prompt, Style S14 Art Nouveau, Art Nouveau Design DNA, Art Nouveau landing page prompt, Style S19 Luxury Editorial (+2 more)

### Community 86 - "Community 86"
Cohesion: 0.22
Nodes (9): Style S03 Swiss Design, Swiss Design Design DNA, Swiss Design landing page prompt, Style S04 Brutalist, Brutalist Design DNA, Brutalist landing page prompt, Style S11 Neo-Brutalism, Neo-Brutalism Design DNA (+1 more)

### Community 87 - "Community 87"
Cohesion: 0.25
Nodes (6): Luxury Gold (S22) style, Luxury Gold (S22) SaaS landing page prompt, Luxury Silver (S23) style, Luxury Silver (S23) SaaS landing page prompt, Minimalist Serif (S24) style, Minimalist Serif (S24) SaaS landing page prompt

### Community 88 - "Community 88"
Cohesion: 0.22
Nodes (6): Startup Vibrant (S25) style, Startup Vibrant (S25) SaaS landing page prompt, Enterprise Blue (S26) style, Enterprise Blue (S26) SaaS landing page prompt, Fintech Trust (S27) style, Fintech Trust (S27) SaaS landing page prompt

### Community 89 - "Community 89"
Cohesion: 0.22
Nodes (8): background_color, description, display, icons, name, short_name, start_url, theme_color

### Community 91 - "Community 91"
Cohesion: 0.25
Nodes (8): chromadb + sentence-transformers memory, System architecture diagram (mermaid), ChromaDB agent memory, System architecture diagram (mermaid) (EN), ChromaDB agent memory (EN), Redis 4h result cache (EN), Redis 4h result cache, chromadb + sentence-transformers memory

### Community 92 - "Community 92"
Cohesion: 0.46
Nodes (7): apply(), clamp(), easeOut(), items, onScroll(), ScrollReveal(), tick()

### Community 93 - "Community 93"
Cohesion: 0.39
Nodes (7): isPreamble(), normalizeHeading(), normalizeReportMarkdown(), PREAMBLE, SENTENCE_ENDINGS, stripBold(), stripPreamble()

### Community 95 - "Community 95"
Cohesion: 0.33
Nodes (7): Unique style category, Style S20 Nature Organic, Nature Organic Design DNA, Nature Organic landing page prompt, Style S21 Solarpunk, Solarpunk Design DNA, Solarpunk landing page prompt

### Community 98 - "Community 98"
Cohesion: 0.33
Nodes (4): Cyber-Bio Noir (S29) style, Cyber-Bio Noir (S29) SaaS landing page prompt, Aurora Borealis (S30) style, Aurora Borealis (S30) SaaS landing page prompt

### Community 99 - "Community 99"
Cohesion: 0.47
Nodes (6): AI agent team: analysts, researchers, risk, trader, AI agent team: analysts, researchers, risk, trader (EN), AVGO analysis report 2026-04-01 (EN), NVDA analysis report 2026-04-01 (EN), AVGO analysis report 2026-03-21 (zh-TW), NVDA analysis report 2026-05-10 (zh-TW)

### Community 101 - "Community 101"
Cohesion: 0.40
Nodes (5): Agent pipeline: propagation, research, risk, trader, BYOK API key encryption (AES-GCM in browser), Key environment variables, Frontend architecture (Next.js App Router, lib/api, crypto, reports-db), TradingAgentsX project overview (12 LLM agents via LangGraph, BYOK)

### Community 103 - "Community 103"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, start

### Community 104 - "Community 104"
Cohesion: 0.40
Nodes (5): requirements.txt Python dependencies, Market data libs (yfinance, finnhub, akshare, tushare), langgraph / langchain LLM stack, TUI libs (chainlit, rich, questionary), TUI ASCII welcome banner (TradingAgentsX)

### Community 106 - "Community 106"
Cohesion: 0.50
Nodes (4): Corporate style category, Style S09 Corporate Clean, Corporate Clean Design DNA, Corporate Clean landing page prompt

## Knowledge Gaps
- **115 isolated node(s):** `tradingagents`, `lint.mjs static scan`, `Palette roles`, `Banned colour families`, `Two-line headline` (+110 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 995 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **51 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `react` connect `登入與首頁動畫` to `歷史與結果頁面`, `Community 66`, `分析表單與聊天`, `分析結果元件`, `Community 74`, `報告聊天頁`, `首頁區塊元件`, `分析頁與進度`, `前端依賴`, `版面與全域樣式`, `Community 92`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **What connects `tradingagents`, `lint.mjs static scan`, `Palette roles` to the rest of the system?**
  _115 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `PDF 下載與公司名稱` be split into smaller, more focused modules?**
  _Cohesion score 0.058497750086535134 - nodes in this community are weakly interconnected._
- **Why does `PDFGenerator` connect `下載服務 PDF` to `PDF 下載與公司名稱`, `Community 85`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Should `設計素材腳本` be split into smaller, more focused modules?**
  _Cohesion score 0.06648426812585499 - nodes in this community are weakly interconnected._
- **Why does `ConfigScreen` connect `排程工作流程` to `Community 96`, `TUI 應用`, `Community 94`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Should `歷史與結果頁面` be split into smaller, more focused modules?**
  _Cohesion score 0.06738738738738739 - nodes in this community are weakly interconnected._