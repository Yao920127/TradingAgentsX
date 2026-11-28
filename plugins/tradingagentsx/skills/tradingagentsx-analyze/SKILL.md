---
name: tradingagentsx-analyze
description: 以 TradingAgentsX 的 12 位 AI 分析師流程分析單一股票並產出 Markdown 報告與 PDF。輸入股票代碼＋日期（美股或台股上市／上櫃），依序完成四位分析師（技術面、社群情緒、新聞、基本面）、多空辯論、研究經理裁決、交易員提案、激進／保守／中立風險辯論與風險經理最終決策（買入／持有／賣出）。支援繁體中文與英文。Use when the user asks to analyze a stock, e.g. "分析 2330 2026-11-26", "analyze NVDA on 2026-11-26", "TradingAgentsX", multi-agent stock analysis, bull/bear debate, or a stock research PDF report.
---

# TradingAgentsX 股票分析（tradingagentsx-analyze）

由執行這個 skill 的模型本身（Claude、Gemini 等皆可）扮演 TradingAgentsX 的 12 位 agent，流程與網頁版相同：**蒐集資料 → 四位分析師 → 摘要 → 多空辯論 → 研究經理 → 交易員 → 風險辯論 → 風險經理 → PDF**。沒有模型選擇，也不需要任何 LLM 金鑰。

本 skill 的提示詞由 TradingAgentsX 原始碼產生，放在 `references/prompts/`，**不要改寫提示詞**，照著用。

> 免責：輸出僅供研究參考，不是投資建議。最終回覆與 PDF 都要保留這一點。

下文的 `SKILL_DIR` 指本檔（SKILL.md）所在的資料夾；腳本一律用 `python3 SKILL_DIR/scripts/...` 執行。

## 1. 先確認輸入

| 參數 | 規則 |
|---|---|
| ticker | 使用者給的代碼。純數字視為台股 |
| date | 分析日期 `YYYY-MM-DD`；沒給就用今天。**只能使用該日以前的資料** |
| market | `us` 美股；`twse` 上市；`tpex` 上櫃／興櫃。台股預設 `twse`，使用者說上櫃才用 `tpex` |
| lang | 使用者用繁體中文提問 → `zh-TW`；用英文 → `en`。使用者明說要哪種就照做。**所有報告、辯論、最終回覆都用同一種語言** |
| depth | 研究深度 1–5，預設 3（辯論輪數）。使用者要快就用 1 |
| analysts | 要納入的分析師，從 `market`（技術面）、`social`（社群）、`news`（新聞）、`fundamentals`（基本面）選，至少 1 位，預設全 4 位。使用者可用自然語言指定，例如「只要技術面和新聞」。**沒選的分析師不蒐集資料、不寫報告、不摘要**；但價格與技術指標（第 3 節）一律要做，走勢圖需要 |

代碼或市場無法判斷（例如同時像美股與台股）時，才問使用者一次；其餘用預設值直接開始，並在開頭一行告知所採用的參數。

工作資料夾：`WORK` = 可寫入的資料夾下的 `tradingagentsx-work/<TICKER>_<DATE>/`（Claude Code 用目前目錄；Claude app 用容器內可寫的路徑）。之後所有檔案都放這裡。

## 2. 選擇資料蒐集模式

先試腳本模式：

```bash
python3 SKILL_DIR/scripts/fetch_data.py --ticker <TICKER> --date <DATE> --market <MARKET> --workdir WORK
```

| 結束碼 | 意思 | 下一步 |
|---|---|---|
| 0 | 成功（`gaps` 列出缺口） | 腳本模式，進入第 3 節 |
| 8 | 網路被擋（Claude app 容器常見） | **網頁工具模式**：讀 `references/web-mode.md` |
| 9 | 取不到價格 | 看 stderr 原因；缺 `FINMIND_API_TOKEN` 就告知使用者設定，否則改網頁工具模式 |
| 3 | 缺相依套件 | 試 `pip install -r SKILL_DIR/requirements.txt` 一次，失敗就改網頁工具模式 |

腳本模式需要使用者自備金鑰（環境變數），沒設只是該類資料變成缺口，不是失敗：

- 台股：`FINMIND_API_TOKEN`（必要）
- 美股新聞：`FINNHUB_API_KEY`、`MARKETAUX_API_KEY`、`NEWSAPI_API_KEY` 之一；美股基本面：`ALPHA_VANTAGE_API_KEY`（沒有會退回 yfinance）

### 資料缺口的處理（兩種模式相同）

資料不齊時，**先自己想辦法補，補不到再標示，絕不編造**：

1. 對每個缺口，用你自己的網頁搜尋／網頁讀取工具查（新聞、社群討論、財報重點、公司公告）。
2. 補到的內容寫進對應的 `data/*.md`，每筆標明**來源、日期**，並註明「由模型網路搜尋補充」。
3. 只採用日期在分析日以前的內容。查不到就保留「資料缺口」字樣，報告裡也要明講哪一塊沒有資料，並降低相應的結論力道。
4. 價格不能用搜尋摘要補：價格一定要是完整日線，走第 3 節的驗證。

## 3. 價格與技術指標

腳本模式已產生 `WORK/data/price.csv`。網頁工具模式則由你依 `references/web-mode.md` 轉寫成同格式（`Date,Open,High,Low,Close,Volume`，日期由舊到新）。接著一律執行：

```bash
python3 SKILL_DIR/scripts/indicators.py --input WORK/data/price.csv --workdir WORK --expect-rows <來源回報的筆數>
```

- 結束碼 0：產生 `WORK/price_data.json`（畫走勢圖用）、`WORK/indicators.json`，stdout 的 JSON 有最新指標與最近 30 筆。
- 結束碼 5（資料格式／內容矛盾）或 7（筆數不符）：**轉寫有誤**，回到來源逐段重抄，不要硬往下做。
- 指標與網頁版一致：close_50_sma、close_200_sma、close_10_ema、macd／macds／macdh、rsi、boll／boll_ub／boll_lb、atr、vwma、mfi。資料不足（例如沒有 200 日）的指標是 `null`，報告中要說明，不可自行估算。

## 4. 四位分析師（各寫一份報告）

**只寫 `analysts` 選到的**（預設全 4 位），沒選的不寫、不存檔。每位分析師：先讀 `references/prompts/<lang>/_common.md`（角色、情境、語言與格式規則）與該 agent 的提示詞，再**只根據下表的資料**寫報告，存成 `WORK/reports/<key>.md`。

| key | 提示詞 | 輸入資料 |
|---|---|---|
| `market` | `market_analyst.md` | `indicators.py` 的輸出（最新值＋最近 30 筆）與 `price.csv` 近期走勢 |
| `social` | `social_analyst.md` | `data/social.md` |
| `news` | `news_analyst.md` | `data/news.md` |
| `fundamentals` | `fundamentals_analyst.md` | `data/fundamentals.md` |

注意：

- 提示詞裡「使用工具取得資料」的指示，對應到的就是上面這些已備妥的資料；不要再去呼叫不存在的工具。
- 提示詞中提到「過去反思／past reflections」處，一律視為沒有。
- 報告裡的每個數字都要能在輸入資料找到；缺的資料寫「資料缺口」。
- 照提示詞末尾的格式規則與免責結尾，**不要使用 emoji**。
- 每寫完一份就存檔，不要把全文留在對話裡重複引用。

## 5. 摘要（Report Summarizer）

對上面**已寫的**報告**各自**做摘要（每份獨立壓縮，避免數字互相污染；沒選的分析師不摘要），提示詞是 `references/prompts/<lang>/_summarizer_<section>.md`：

| section | 來源報告 |
|---|---|
| `market` | `reports/market.md` |
| `sentiment` | `reports/social.md` |
| `news` | `reports/news.md` |
| `fundamentals` | `reports/fundamentals.md` |

把各段摘要依序合併存成 `WORK/analyst_summary.md`（每段前加該摘要提示詞規定的標題）。辯論與交易員階段都讀這份摘要，而不是全文。

沒選的分析師，在之後的辯論、經理、交易員階段一律視為「**未納入分析**」：不是資料缺口，也不要自行補寫那一面的分析；各角色只就摘要裡有的內容論述，必要時可說明該面向未納入。

## 6. 多空辯論 → 研究經理 → 交易員

**投資辯論**：看漲研究員先發言，之後與看跌研究員輪流，共 `2 × depth` 次發言（depth=3 即 6 次）。

- 看漲用 `bull_researcher.md`，看跌用 `bear_researcher.md`。
- 每次發言的輸入：`analyst_summary.md`、辯論歷史、對方最近一次論點。第一位發言時辯論歷史與對方論點皆為空。
- **篇幅要求（每一次發言，包含最後幾輪）**：提示詞的字數是上限，也是目標。看漲與看跌各約 600–800 字，並照提示詞列出的每個段落各寫到標示的大約字數。每段都要引用具體數字並點名反駁對方最強的論點，後期輪次也要寫出新的證據或計算，不可只寫結論。
- 發言前綴：中文「看漲分析師：」「看跌分析師：」；英文 "Bull Analyst:" "Bear Analyst:"。
- 辯論歷史變長時，較早的發言只保留開頭摘錄，最近 2 次發言保留全文。
- 把整個辯論逐次追加存成 `WORK/debate_investment.md`。每次發言追加到檔案末尾後，再另起一行加標記 `<!-- 第 N 次 / 共 2×depth 次 -->`（N 從 1 起），讓發言數可以事後驗證；標記數必須等於 `2 × depth`，不足就繼續辯論，不可提前進入研究經理。
- 存檔：`reports/bull.md` 放看漲方**最後一次**發言（不含前綴）；`reports/bear.md` 放看跌方最後一次發言。

**研究經理**（`research_manager.md`）：輸入只有完整辯論歷史，做出投資決策 → `reports/research_manager.md`。**必須重新讀完整的 `WORK/debate_investment.md`（不可用發言時的摘錄版），並寫成與網頁版相當的完整報告**：逐一評估雙方論點與證據，不要縮成結論摘要。**有子代理工具時（Claude Code 的 Agent 工具、Claude app 若提供子代理），把這一步交給全新的子代理**，讓它在乾淨的 context 獨立完成，更接近網頁版「每個 agent 獨立呼叫」：給它的 prompt 只含提示詞檔路徑、`debate_investment.md` 路徑、輸出路徑 `reports/research_manager.md` 與語言，由它自己讀檔、寫檔。沒有子代理工具就在主對話照做，但仍須重新讀檔。

**交易員**（`trader.md`）：輸入是研究經理的決策，產出交易提案，結尾必須是「最終交易提案：**買入/持有/賣出**」（英文 "Final Trading Proposal: **Buy/Hold/Sell**"）→ `reports/trader.md`。

## 7. 風險辯論 → 風險經理（最終決策）

**風險辯論**：激進 → 保守 → 中立循環，共 `3 × depth` 次發言（depth=3 即 9 次）。

- 提示詞：`aggressive_debator.md`、`conservative_debator.md`、`neutral_debator.md`。
- 每次發言的輸入：交易員提案、`analyst_summary.md`、辯論歷史、另外兩位最近的發言。歷史較早的發言只留開頭摘錄，最近 3 次保留全文。
- **篇幅要求（每一次發言，包含最後幾輪）**：這三位的提示詞有字數硬上限（激進 400 字、保守與中立 600 字「超過即截止」），實測照上限寫出來太單薄，**本 skill 明確覆寫該上限，以本條為準**，不要因為提示詞寫「超過即截止」就縮短。目標字數：激進 700–900 字、保守與中立各 900–1,200 字。分段預算（提示詞的段落標題與格式照舊，只是字數放寬）：
  - 激進：上行論證約 300 字（報酬為何值得承擔風險、不對稱上行的算術）、反駁保守與中立約 300 字、倉位與執行條件約 200 字。
  - 保守：核心風險診斷約 250 字、下行風險論證約 500 字（2–3 個風險，各附數字與推導）、反駁激進約 200 字、倉位建議約 200 字。
  - 中立：多空核心分歧約 250 字、平衡評估約 500 字、情境分析約 250 字（列出各情境機率、目標價與加權結果）、中性倉位建議約 200 字。

  每段都要引用輸入資料中的具體數字並寫出推導，點名反駁另外兩位最強的論點；不可只寫一兩句結論或倉位數字。後期輪次立場趨近時，也要寫出新的證據、計算或情境（例如新的敏感度、觸發條件、反例），而不是重複「已收斂」。寫完自己檢查：字數明顯低於下限就補足再存檔。
- 前綴：「激進分析師：」「保守分析師：」「中立分析師：」；英文 "Aggressive Analyst:" "Conservative Analyst:" "Neutral Analyst:"。
- 逐次追加存成 `WORK/debate_risk.md`。每次發言追加到檔案末尾後，再另起一行加標記 `<!-- 第 N 次 / 共 3×depth 次 -->`（N 從 1 起），讓發言數可以事後驗證；標記數必須等於 `3 × depth`，不足就繼續辯論，不可提前進入風險經理。
- **不要把最後一次發言當成這三位的報告**：最後一輪三方已收斂，發言天生只剩一句結論，放進 PDF 完全看不出重點。辯論全部完成（標記數齊全）後，**每位各寫一份「最終立場報告」**，存成 `reports/aggressive.md`、`reports/conservative.md`、`reports/neutral.md`。
  - 寫法：**有子代理工具時，三位各交給一個全新的子代理（可平行）**，prompt 只含該位的提示詞路徑、`reports/trader.md`、`analyst_summary.md`、完整的 `WORK/debate_risk.md` 路徑、輸出路徑與語言；沒有子代理工具就在主對話逐位寫，但每位都要重新讀完整的 `debate_risk.md`，不可只憑最後一輪的記憶。
  - 內容：以該位的視角，把整場辯論（不只最後一輪）整理成一份獨立、讀者不必看辯論過程就能懂的完整報告。篇幅：激進 700–900 字、保守與中立各 900–1,200 字（同樣覆寫提示詞的字數上限）。
  - 結構（標題格式照提示詞）：**開頭先給「結論與重點」**——一句話立場，加上 3 條最關鍵的理由（各附一個具體數字）；接著依序是核心論證（引用整場辯論中最有力的數字與推導）、對另外兩位最強論點的回應、讓步與立場演變（辯論中改變或放棄了什麼）、倉位與觸發條件（用表格列出進場／加碼／減碼／出場的價位與事件）。
  - 禁止：只寫「最後陳述」「承認」這類收斂句；沒有數字的泛論；重複另一位的內容。寫完自檢字數，低於下限就補足。

**風險經理**（`risk_manager.md`）：輸入是交易員提案與完整風險辯論歷史。**必須重新讀完整的 `WORK/debate_risk.md`（不可用發言時的摘錄版），並寫成與網頁版相當的完整報告**：綜合三方觀點、審查交易員提案、給出倉位與停損停利計畫，不要縮成結論摘要。**有子代理工具時，同樣交給全新的子代理執行**：prompt 只含提示詞檔路徑、`reports/trader.md` 與 `debate_risk.md` 路徑、輸出路徑 `reports/risk_manager.md` 與語言；沒有子代理工具就在主對話照做，但仍須重新讀檔。**最終買賣決策由它做出**，結尾必須是「最終交易決策：**買入/持有/賣出**」（英文 "Final Trading Decision: **Buy/Hold/Sell**"）→ `reports/risk_manager.md`。

## 8. 產生 PDF

```bash
python3 SKILL_DIR/scripts/render_pdf.py --workdir WORK --ticker <TICKER> --date <DATE> --lang <LANG> --company "<公司名稱>" --depth <DEPTH> --model "<模型名稱>"
```

`--company` 一定要填**公司正式全稱**（含 Corporation／Inc.／Co., Ltd. 等），封面才會顯示完整名稱，例如 `NVIDIA Corporation`、`Apple Inc.`、`台灣積體電路製造股份有限公司`；不可只填簡稱（如 `NVIDIA`、`台積電`）。全稱從基本面資料的公司名稱（如 yfinance 的 `longName`）取得；查不到才憑可靠知識補全。

`--model` 一定要填**你自己（正在執行這個 skill 的模型）的名稱**，例如 `Claude Opus 4.8`、`Gemini 3 Pro`，會顯示在 PDF 封面的「分析模型」欄；不要沿用預設值 `Claude`，否則用別的模型分析時封面會寫錯。不確定確切版本時寫你知道的模型名稱即可，不可編造。

`--depth` 一定要帶：腳本會檢查 `debate_investment.md` 與 `debate_risk.md` 的發言標記是否恰為 `2×depth`、`3×depth` 個（編號 1 到總數各一個），不符就不產生 PDF。

| 結束碼 | 處理 |
|---|---|
| 0 | 成功，stdout JSON 的 `pdf` 是檔案路徑；`missing_reports` 裡**使用者沒選的分析師屬預期**，不必提；其餘（預期要有卻缺少的）要告知使用者 |
| 2 | `reports/` 沒有報告，檢查是否漏存檔 |
| 4 | 找不到中文字型（`assets/NotoSerifTC-Regular.ttf`）；改用 `--lang en`，並告知原因 |
| 5 | `price_data.json` 格式錯，回第 3 節重做 |
| 7 | 辯論發言次數與 depth 不符（stderr 會說明哪個檔、缺哪幾次）；回第 6／7 節繼續辯論補足、補上標記，再重跑，**不可改標記或降低 depth 來過關** |

把 PDF 放到使用者拿得到的位置（Claude app 若有輸出資料夾就放那裡；Claude Code 則在工作資料夾並告知路徑）。

## 9. 最終回覆

用使用者的語言，簡短回報：

1. 最終決策（風險經理的買入／持有／賣出）與 2–4 點關鍵理由。
2. 交易員的提案與風險經理決策不一致時，說明差異。
3. 資料缺口與哪些內容是模型搜尋補充的。
   資料來源要寫**真實的來源名稱與網址**（例如 FinMind、Yahoo Finance、公司法說會新聞稿、新聞媒體網址），不要列 `data/*.md`、`reports/` 這類內部檔案路徑；查不到網址就只寫來源名稱。
4. PDF 路徑、使用參數（代碼、日期、市場、語言、depth、實際納入的分析師）。只選了部分分析師時，要明講結論未涵蓋沒選的面向。
5. 一句免責聲明。

不要把十二份報告全文貼回對話，除非使用者要求。

## 工作量與節奏

撰寫次數約為 `6 + 2×N + 5×depth`（N 是納入的分析師數）。全 4 位、depth=3 約 29 次（4 份報告、4 份摘要、6 次投資辯論、研究經理、交易員、9 次風險辯論、3 份最終立場報告、風險經理）；只選 1 位則少 6 次。開始前用一句話告知使用者大概的規模與所選 depth；使用者想快可改 depth=1。過程中每完成一個階段簡短報告進度即可。Claude Code 可把互不相依的四位分析師交給子代理平行處理，但辯論與裁決必須依序進行。

## 檔案一覽

```
SKILL_DIR/
  scripts/fetch_data.py     腳本模式資料蒐集
  scripts/indicators.py     資料驗證與技術指標（離線）
  scripts/render_pdf.py     報告合併成 PDF
  references/web-mode.md    網頁工具模式的資料蒐集食譜
  references/prompts/<zh-TW|en>/   12 位 agent 提示詞、_common.md、_summarizer_*.md
  vendor/  assets/  requirements.txt
WORK/
  data/ price.csv fundamentals.md news.md social.md
  price_data.json indicators.json analyst_summary.md debate_*.md
  reports/ market social news fundamentals bull bear research_manager trader aggressive conservative neutral risk_manager (.md)
```
