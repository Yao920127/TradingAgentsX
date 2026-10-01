# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project Overview

TradingAgentsX is a full-stack AI trading analysis platform. It orchestrates 12 specialized LLM agents (analysts, researchers, debaters, trader) via LangGraph to produce stock analysis reports. Users bring their own LLM API keys (BYOK), stored encrypted in the browser.

## Commands

### Backend (Python 3.10+)

```bash
# Activate the existing conda environment (create if missing)
conda activate tradingagents
# If the environment doesn't exist yet:
# conda create -n tradingagents python=3.13 && conda activate tradingagents

# Install dependencies
pip install -e .
pip install -r backend/requirements.txt

# Run backend (port 8000)
python -m backend
python -m backend --port 8000 --reload true

# Health check
curl http://localhost:8000/api/health
# API docs: http://localhost:8000/docs
```

### Frontend (Next.js)

```bash
# Install and run (from repo root)
bun install --cwd frontend
bun run --cwd frontend dev        # Dev server at localhost:3000
bun run --cwd frontend build      # Production build
bun run --cwd frontend lint       # ESLint

# Or from frontend/ directory
npm install && npm run dev
```

### Docker (full stack)

```bash
docker compose up                 # Both services
docker compose up backend         # Backend only
```

### TypeScript type checking

```bash
cd frontend && bunx tsc --noEmit
```

## Architecture

### Agent Pipeline (LangGraph)

Analysis flows through four sequential phases, each modeled as LangGraph nodes:

1. **Propagation** — 4 analysts run in parallel: `market_analyst` (technical), `news_analyst`, `social_media_analyst`, `fundamentals_analyst`. Results stored in `AgentState.messages`.
2. **Research** — `bull_researcher` and `bear_researcher` debate; `research_manager` synthesizes into `InvestDebateState.research_decision`.
3. **Risk** — 3 debaters (aggressive/conservative/neutral) argue; `risk_manager` produces final risk decision in `RiskDebateState`.
4. **Trader** — Synthesizes all prior state into a BUY/SELL/HOLD recommendation with confidence score.

The graph is defined in `tradingagents/graph/trading_graph.py` (main class `TradingAgentsXGraph`). Node/edge wiring is in `graph/setup.py`; routing logic in `graph/conditional_logic.py`.

Fast mode skips the debate phases (researchers + risk debaters), cutting runtime to 15–25 min. Deep mode runs all 12 agents.

### Backend Service Layer

- `backend/app/services/trading_service.py` — Main orchestrator: instantiates the LangGraph, runs analysis, manages results
- `backend/app/services/task_manager.py` — Async task queue (one analysis per task)
- `backend/app/api/routes.py` — REST API: `/api/analyze`, `/api/tasks/{id}`, `/api/download`
- `backend/app/core/config.py` — Pydantic Settings from environment variables

### Data Sources (tradingagents/dataflows/)

- `interface.py` — Unified interface over all providers
- `y_finance.py` — US stock prices, technical indicators (primary)
- `alpha_vantage*.py` — Fundamentals + technical (5 files)
- `finmind*.py` — Taiwan stock data (6 files)
- `google.py` / `googlenews_utils.py` / `reddit_utils.py` — News/sentiment

Agents call tools defined in `tradingagents/agents/utils/agent_utils.py` — LangChain `StructuredTool` wrappers over the dataflows interface.

### Frontend Architecture

- **App Router routes:** `/` home, `/analysis` run analysis, `/history` saved reports, `/auth/callback` OAuth
- **`lib/api.ts`** — Axios client; auto-attaches JWT; handles request/response transforms
- **`lib/crypto.ts`** — AES-GCM encryption for API keys stored in localStorage
- **`lib/reports-db.ts`** — Dexie.js IndexedDB for local report persistence
- **`lib/pending-task.ts`** — Recovery mechanism for interrupted analyses
- **Form validation:** React Hook Form + Zod schemas in `components/analysis/AnalysisForm.tsx`
  - Zod schema handles validation only; `useForm({ defaultValues })` handles defaults — do not use `.default()` in Zod schemas here

### LLM Configuration

The system supports OpenAI, Anthropic (Codex), Gemini, Grok, DeepSeek, and Qwen. Two LLM roles per analysis:
- `deep_think_llm` — Heavy reasoning tasks (researchers, managers, trader)
- `quick_think_llm` — Fast tasks (analysts, debaters)

Config flows from frontend form → API request body → `trading_service.py` → `TradingAgentsXGraph` init.

## Key Environment Variables

```
OPENAI_API_KEY / ANTHROPIC_API_KEY / GEMINI_API_KEY / XAI_API_KEY / DEEPSEEK_API_KEY
JWT_SECRET                  # Required; change from default in production
CORS_ORIGINS                # Comma-separated allowed origins
GOOGLE_CLIENT_ID/SECRET     # OAuth 2.0 (optional; for cloud sync)
FRONTEND_URL                # e.g., http://localhost:3000
TRADINGAGENTS_RESULTS_DIR   # Where PDF reports are written
DATABASE_URL                # PostgreSQL (optional; enables cloud sync)
REDIS_URL                   # Redis (optional; enables result caching)
```

Copy `.env.example` to `.env` to get started.

## Important Notes

- **LangGraph recursion limit** is set to 200 (configured via graph config params). Do not remove this — it prevents infinite agent loops.
- **4-analyst parallel execution:** analysts run concurrently via LangGraph fan-out; do not introduce sequential dependencies between them.
- **Redis TTL** for cached analysis results is 4 hours (extended from default 1 hour).
- **Rate limiting:** Backend enforces 30 requests/60 seconds per IP via slowapi.
- **Taiwan vs US stocks:** `market_type` parameter controls which data sources are used. FinMind is used for Taiwan (`tw`), Yahoo Finance + Alpha Vantage for US.
- The `tradingagents/` package is installed as an editable package (`pip install -e .`); import as `from tradingagents.graph import ...`.
