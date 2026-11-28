# 網頁工具模式：由模型自己蒐集資料

用在 `fetch_data.py` 回傳結束碼 8（網路被擋，例如 Claude app 容器）或 9（取不到價格）時。容器只能離線計算與產 PDF，**資料要靠你自己的網頁搜尋／網頁讀取／內建瀏覽器工具取得**，再寫成檔案。

目標是產生與腳本模式相同的檔案（放在 `WORK/data/`）：

| 檔案 | 內容 |
|---|---|
| `price.csv` | `Date,Open,High,Low,Close,Volume`，日期 `YYYY-MM-DD` 由舊到新，約一年日線（至少 200 筆才算得出 200 日均線） |
| `fundamentals.md` | 基本面、資產負債表、現金流量表、損益表（近 4–8 季） |
| `news.md` | 個股新聞（分析日前 7 天）與全球／大盤新聞 |
| `social.md` | 社群情緒與討論（可附個股新聞） |

每個 md 檔用 `## 小標題` 分節。某節拿不到資料，寫一行：`資料缺口 / Data gap：<項目> 無法取得（<原因>）`。

## 1. 價格（最重要，也最容易抄錯）

### 台股（FinMind 公開 JSON，網頁讀取工具可用）

```
https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockPrice&data_id=<代號>&start_date=<分析日-365天>&end_date=<分析日>
```

回傳 `data[]`，欄位：`date`、`open`、`max`（最高）、`min`（最低）、`close`、`Trading_Volume`（股數）。對應成 `Open/High/Low/Close/Volume`。若回應被截斷，改分兩三段日期範圍各抓一次再合併。

### 美股

`stooq.com` 與 Yahoo 的網頁讀取常被 robots.txt 擋下，不要硬繞。優先順序：

1. **內建瀏覽器**開 `https://query1.finance.yahoo.com/v8/finance/chart/<代號>?range=1y&interval=1d`。偶爾第一次會出現 site policy 檢查失敗，重試一次即可。
2. 回傳的 `timestamp[]` 是 Unix 秒，需依 `meta.gmtoffset` 轉成交易所當地日期；`indicators.quote[0]` 內有 `open/high/low/close/volume` 陣列，值為 `null` 的日期直接略過。
3. 仍失敗：告知使用者無法取得價格資料並停止（沒有價格就不能做技術分析，**不要用搜尋摘要或記憶編造價格**）。

### 轉寫成 `price.csv` 的守則

資料是你「讀到後再寫出」的，這一步最可能出錯，所以：

1. 記下來源回報的**筆數**（`data` 陣列長度，或 `timestamp` 長度扣掉 `null`）。
2. 分批（約 50–60 列一批）用 shell 追加寫入 CSV，不要憑印象補值，不要四捨五入或調整數字。
3. 寫完先數一次列數，再把**首尾各 3 列與中間隨機 5 列**與來源逐欄比對。
4. 執行 `indicators.py --expect-rows <來源筆數>`：它會檢查筆數、日期順序與重複、最高價≥最低價、開收盤在高低價範圍內。出現結束碼 5 或 7 就回頭重抄有問題的區段。
5. 通過後才進入分析，並在最終回覆中說明價格是由模型從哪個來源轉寫的。

## 2. 基本面

### 台股（FinMind，同上網址，換 `dataset`；起始日取分析日前 2 年）

- `TaiwanStockFinancialStatements`：損益表（長格式，每列一個科目）
- `TaiwanStockBalanceSheet`：資產負債表
- `TaiwanStockCashFlowsStatement`：現金流量表
- `TaiwanStockMonthRevenue`：月營收
- `TaiwanStockPER`：本益比、股價淨值比、殖利率
- `TaiwanStockDividend`：股利

把近 4–8 季整理成表格：營收、毛利率、營業利益率、淨利、EPS、總資產／負債、現金流（營運／投資／自由現金流）、PER／PBR、殖利率。

### 美股

沒有可靠的免金鑰 JSON 來源，用網頁搜尋＋網頁讀取：公司投資人關係頁的最新財報新聞稿、SEC EDGAR 的 10-Q／10-K 摘要、可信財經網站的關鍵比率。整理同樣的項目（營收與年增、毛利率、營業利益率、淨利、EPS、自由現金流、負債、PE 等估值），**每個數字標明來源與財報期間**。找不到的項目寫資料缺口。

## 3. 新聞（`news.md`）

- 個股：搜尋分析日前 7 天的新聞（台股用中文公司名＋代號搜尋，並可加上「法說會」「外資」「財報」等關鍵字）。至少列出能找到的前 5–10 則，每則：標題、來源、日期、一句話重點。
- 全球／大盤：同期間影響該股的總經與產業新聞（利率、關稅、產業供應鏈、指數表現）。
- 只收分析日以前的內容；找不到日期的不要收。

## 4. 社群情緒（`social.md`）

搜尋近 7 天的討論熱度與語氣：美股看 Reddit、StockTwits、Hacker News；台股看 PTT Stock 板、Dcard、股市論壇。摘要寫討論量大小、多空比例的大致傾向、常見主題，**不要大段引用原文**。完全查不到就整節寫資料缺口，社群分析師報告也要如實說明資料不足。

## 5. 補缺口時的規則

- 每筆補來的資料標：來源（網站名稱或網址）、資料日期、「由模型網路搜尋補充」。
- 拿不到的就是缺口，不要用常識、記憶或推測代替。
- 不要為了湊滿欄位而把舊資料當成最新；數字的時間點要清楚。
- 金鑰（例如 Alpha Vantage）屬於使用者的私人資訊，不要要求使用者貼在對話裡。
