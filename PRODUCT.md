# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Two audiences, served roughly equally:

- **Individual retail investors** (US and Taiwan stock markets) doing self-directed research before a buy/sell/hold decision.
- **Quant/developer-minded users** experimenting with and inspecting the multi-agent LLM pipeline itself, more interested in the agent architecture and debate process than in a single verdict.

## Product Purpose

TradingAgentsX orchestrates 13 specialized LLM agents (analysts, researchers, debaters, trader) via LangGraph to produce a multi-perspective stock analysis report for a given ticker. Success for a session is a rich, legible multi-perspective report — the bull/bear research debate and the aggressive/conservative/neutral risk debate are the primary value; the final BUY/SELL/HOLD recommendation is a summary label on top of that reasoning, not the main point.

## Positioning

A multi-agent debate architecture (not a single-model opinion): specialized agents independently analyze technicals, news, social sentiment, and fundamentals, then argue the case from opposing research and risk postures before a decision synthesis. Combined with a strict BYOK (bring-your-own-API-key) model — keys are encrypted client-side (AES-GCM) and never held in plaintext by the service — this is the core differentiator versus hosted-key competitors: users get the multi-agent debate transparency and keep custody of their own LLM credentials.

Credited as an extension/improvement of [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents).

## Operating Context

- User picks a market (US or Taiwan), enters a ticker, selects analyst team / LLM providers (deep-think and quick-think roles) and embeddings model, then runs an analysis.
- Fast mode (analysts only, skips debate phases, ~15–25 min) vs. deep mode (all 13 agents, full debate).
- Pipeline runs through four phases: parallel analyst propagation (market/news/social/fundamentals, summarized by a report-summarizer agent) → bull/bear research debate synthesized by a research manager → aggressive/conservative/neutral risk debate synthesized by a risk manager → trader synthesis into a final BUY/SELL/HOLD call with confidence.
- Results are downloadable as PDF reports; users can revisit history of past analyses; an AI Q&A feature lets users ask follow-up questions about a generated report.
- Supports a TUI (terminal) mode in addition to the web app, for the same underlying pipeline.
- Google OAuth login is optional locally, recommended in production, enabling cloud sync of API settings and report history across devices; without login, data stays local-only (and is cleared on leaving the page in production, never in local dev).

## Capabilities and Constraints

- LLM providers supported: OpenAI, Anthropic (Claude), Gemini, Grok, DeepSeek, Qwen — user supplies their own API key per provider (BYOK).
- Market data: Yahoo Finance + Alpha Vantage for US stocks; FinMind for Taiwan stocks; Google News/Reddit for sentiment and news.
- Rate limiting (30 req/60s per IP), security headers, API key masking in logs, CORS restrictions.
- LangGraph recursion limit fixed at 200 to guard against infinite agent loops — not to be removed.
- The 4 analyst agents must run in parallel (LangGraph fan-out); no sequential dependency between them is introduced.
- Redis result cache TTL is 4 hours.
- Supports light/dark theme and Traditional Chinese + English localization.

## Brand Commitments

- Product name: **TradingAgentsX**.
- 13 specialized agents total: 4 analysts (market/news/social/fundamentals) + 1 report-summarizer + 2 researchers (bull/bear) + 1 research manager + 3 risk debaters (aggressive/conservative/neutral) + 1 risk manager + 1 trader.
- Built on LangGraph for agent orchestration.
- BYOK model is a binding, user-facing privacy/security commitment, not an implementation detail: user API keys are encrypted client-side and the product should never be redesigned toward a hosted-key model without an explicit decision to drop this commitment.
- Attribution to TauricResearch/TradingAgents as the project this extends.

## Evidence on Hand

- Existing logo/icon assets at `frontend/public/icon-v8.png` and `frontend/app/icon*.png`.
- README.md / README_EN.md contain the canonical (Traditional Chinese / English) feature descriptions, architecture diagram, and agent roster — treat as authoritative product copy, not to be silently rewritten.
- No testimonials, case studies, or customer evidence exist; future work must not fabricate any.

## Product Principles

1. The multi-agent debate is the product's substance — UI should make the bull/bear and risk debates legible and inspectable, not bury them behind the final verdict.
2. BYOK and client-side key encryption are non-negotiable trust commitments; never suggest or imply server-side custody of user API keys.
3. Serve both audiences without forcing a choice: retail-investor clarity (a confident, well-reasoned call) and architecture transparency (seeing each agent's contribution) can and should coexist in the same report view.
4. Preserve market-specific correctness (US vs. Taiwan data sourcing) as a first-class constraint, not an edge case.
5. Respect the existing bilingual (Traditional Chinese / English) and light/dark-theme commitments already shipped.

## Accessibility & Inclusion

Responsive design is an existing commitment (desktop and mobile browsers); no further accessibility standard has been explicitly established yet.
