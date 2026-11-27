# TradingAgentsX Claude Skill

**[繁體中文](README.md) | English**　·　[Back to project home](../README_EN.md)

The full 12-agent flow (data collection → four analysts → bull/bear debate → risk debate → final decision → PDF) is packaged as a skill. Claude itself acts as the model, so no LLM API key is needed. Just give a ticker and a date, e.g. "analyze NVDA on 2026-11-26" or "analyze 2330 on 2026-11-26".

### Claude Code (plugin)

In the Claude Code prompt, paste **one line at a time**:

1. Add the marketplace:

```
/plugin marketplace add Yao920127/TradingAgentsX
```

2. Install the plugin:

```
/plugin install tradingagentsx@tradingagentsx
```

**Or from a regular terminal:**

```bash
claude plugin marketplace add Yao920127/TradingAgentsX
```

```bash
claude plugin install tradingagentsx@tradingagentsx
```

**Optional script-mode dependencies and keys**

```bash
pip install -r ~/.claude/plugins/.../skills/tradingagentsx-analyze/requirements.txt
```

Taiwan stocks need `FINMIND_API_TOKEN`; US news can use `FINNHUB_API_KEY` / `MARKETAUX_API_KEY` / `NEWSAPI_API_KEY`. Missing data is flagged as a data gap and Claude searches the web to fill it.

### Claude app

**Claude app (download and upload the zip)**: [download tradingagentsx-analyze.zip](https://github.com/Yao920127/TradingAgentsX/releases/latest/download/tradingagentsx-analyze.zip) (about 12 MB, includes the Traditional Chinese font), then upload it under Settings → Capabilities → Skills. All versions are on the [Releases](https://github.com/Yao920127/TradingAgentsX/releases) page. The Claude app sandbox cannot reach market-data hosts, so Claude collects data with its own web tools.

### How to ask

Plain language works. Ticker and date are required; everything else has a default:

```
analyze NVDA on 2026-11-26
analyze 2330 on 2026-11-26, depth 1
analyze 5274 on 2026-11-26 (OTC), depth 3
analyze NVDA on 2026-11-26, technical and news analysts only
分析 NVDA 2026-11-26，用繁體中文
```

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| Ticker | US stocks like `NVDA`; Taiwan stocks use the number, e.g. `2330` | Required |
| Date | `YYYY-MM-DD`; only data up to that date is used | Today |
| Market | US / Taiwan listed (`twse`) / Taiwan OTC (`tpex`); numeric Taiwan tickers default to listed, say so for OTC | Auto-detected |
| Language | Ask in Traditional Chinese for a Chinese report, in English for an English one | Follows your prompt |
| Research depth | 1–5, see below | 3 |
| Analysts | Any of technical, social, news and fundamentals, at least one, same as the web app's analyst team checkboxes. Unselected ones are not researched or written and the conclusion does not cover that angle. The price chart is always included | All 4 |

### What data it can use

| Data | Claude Code (script mode) | Claude app (web-tool mode) |
| ---- | ------------------------- | -------------------------- |
| US prices | Yahoo Finance | Claude reads Yahoo Finance in its built-in browser |
| Taiwan prices | FinMind (needs `FINMIND_API_TOKEN`) | FinMind public JSON |
| Technical indicators | Computed locally: 50/200-day SMA, 10-day EMA, MACD, RSI, Bollinger Bands, ATR, VWMA, MFI | Same |
| Fundamentals | US: Alpha Vantage or yfinance; Taiwan: FinMind | Earnings releases, SEC filings, FinMind |
| News | US: Finnhub / Marketaux / NewsAPI (your own keys); Taiwan: FinMind | Claude web search |
| Social | Free sources: ApeWisdom, Hacker News, PTT | Claude web search |

When a data type is unavailable, the report marks it as a "data gap". Claude first tries to fill it by searching the web and notes the source; if it still cannot, it says so and lowers the confidence of its conclusions, never inventing data. Prices must be full daily bars and pass row-count and value checks before the analysis continues.

### Research depth

Depth sets how many turns the bull/bear and risk debates run: deeper is more thorough, slower and uses more tokens. The debates always run; none is skipped.

| Depth | Bull/bear debate | Risk debate | Separate writing steps | Good for |
| ----- | ---------------- | ----------- | ---------------------- | -------- |
| 1 | 2 turns | 3 turns | about 16 | A quick look (about 8 minutes measured in Claude Code) |
| 2 | 4 turns | 6 turns | about 21 | Everyday use |
| 3 (default) | 6 turns | 9 turns | about 26 | Full debate |
| 4 | 8 turns | 12 turns | about 31 | Before an important decision |
| 5 | 10 turns | 15 turns | about 36 | Most thorough, slowest |

> Output is for research only and is not investment advice.

**Screenshots**

Claude Code (terminal) analyzing SKHY, reporting the final decision, data gaps and the PDF path when done:

![Claude Code in action](../web_screenshot/skill.png)

Claude app analyzing NVDA, with the generated PDF report previewed on the right:

![Claude app in action](../web_screenshot/skill2.png)

**Maintainers**: build the zip yourself with `python scripts/build_skill.py` (outputs `dist/tradingagentsx-analyze.zip`). After changing prompts, `pdf_generator.py`, dataflows or `skills/`, run `python scripts/build_skill.py --plugin` and commit `plugins/tradingagentsx/` (a test checks that it is in sync).
