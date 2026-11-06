#!/usr/bin/env bash
# ========================================
# TradingAgentsX：清除快取與暫存檔
#
#   ./clean_cache.sh            清建置產物、工具快取、日誌、系統暫存檔
#   ./clean_cache.sh --app      另外清應用快取（股價資料快取、本機 Redis 的 cache:* 與 ratelimit:*）
#   ./clean_cache.sh --deep     另外刪除 node_modules 與 *.egg-info（之後需重新安裝）
#   ./clean_cache.sh --all      等於 --app --deep
#   ./clean_cache.sh -n         只列出會刪什麼，不實際刪除
#
# 不會碰：原始碼、.env、lock 檔（bun.lock / uv.lock）、分析結果與 PDF（results/、report/）、
#         floorplan/、conda 環境、Redis 裡進行中的分析任務（task:*）
# ========================================

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

DRY_RUN=0
CLEAN_APP=0
CLEAN_DEEP=0

usage() {
  sed -n '3,13p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
}

for arg in "$@"; do
  case "$arg" in
    -n | --dry-run) DRY_RUN=1 ;;
    --app) CLEAN_APP=1 ;;
    --deep) CLEAN_DEEP=1 ;;
    --all) CLEAN_APP=1 CLEAN_DEEP=1 ;;
    -h | --help) usage ;;
    *)
      echo "未知參數：${arg}（用 -h 看說明）" >&2
      exit 1
      ;;
  esac
done

REMOVED=0

# 刪除單一路徑（檔案或目錄），dry-run 時只印出
remove_path() {
  local path="$1"
  [ -e "$path" ] || return 0
  local size
  size="$(du -sh "$path" 2>/dev/null | cut -f1)"
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "  [預覽] $path ($size)"
  else
    rm -rf -- "$path"
    echo "  ✓ $path ($size)"
  fi
  REMOVED=$((REMOVED + 1))
}

# 依名稱在專案中搜尋並刪除；跳過 node_modules、.venv、.git，避免刪到依賴套件內的同名目錄
remove_by_name() {
  local type="$1" name="$2" path
  while IFS= read -r path; do
    remove_path "$path"
  done < <(
    find . \( -name node_modules -o -name .venv -o -name .git \) -prune -o \
      -type "$type" -name "$name" -print 2>/dev/null
  )
}

section() {
  echo ""
  echo "$1"
}

[ "$DRY_RUN" -eq 1 ] && echo "🔍 預覽模式：只列出、不刪除"
echo "🧹 清理 TradingAgentsX 快取與暫存檔（${ROOT}）"

section "⚛️  前端（Next.js / TypeScript）"
remove_path frontend/.next
remove_path frontend/out
remove_path frontend/node_modules/.cache
remove_by_name f "*.tsbuildinfo"

section "🐍 後端與 AI 引擎（Python）"
remove_by_name d __pycache__
remove_by_name f "*.py[co]"
remove_by_name d .pytest_cache
remove_by_name d .mypy_cache
remove_by_name d .ruff_cache
remove_path .coverage
remove_path htmlcov
remove_path coverage.xml

section "📝 日誌與系統暫存檔"
remove_by_name f "*.log"
remove_by_name f ".DS_Store"
remove_by_name f "Thumbs.db"
remove_by_name f "*.sw[op]"

if [ "$CLEAN_DEEP" -eq 1 ]; then
  section "📦 依賴套件（--deep）"
  remove_path node_modules
  remove_path frontend/node_modules
  remove_by_name d "*.egg-info"
fi

# 應用快取：分析時下載的股價資料（24 小時內會重用），以及 Redis 的結果快取與請求次數計數
if [ "$CLEAN_APP" -eq 1 ]; then
  section "🗄️  應用快取（--app）"
  remove_path "${TRADINGAGENTS_DATA_CACHE_DIR:-tradingagents/dataflows/data_cache}"

  # 不清 task:*，以免中斷正在跑的分析
  PATTERNS="cache:* ratelimit:*"

  REDIS_URL_VALUE="${REDIS_URL:-}"
  if [ -z "$REDIS_URL_VALUE" ] && [ -f .env ]; then
    REDIS_URL_VALUE="$(grep -E '^REDIS_URL=' .env | tail -1 | cut -d= -f2- || true)"
  fi
  # 只動本機的 Redis：.env 若指向雲端（例如 Railway 正式環境），一律不清
  REDIS_HOST="$(printf '%s' "$REDIS_URL_VALUE" | sed -E 's#^[a-z]+://([^@]*@)?([^:/]+).*#\2#')"

  REDIS_CMD=""
  if [ -n "$REDIS_URL_VALUE" ]; then
    case "$REDIS_HOST" in
      localhost | 127.0.0.1 | ::1 | redis)
        if command -v redis-cli >/dev/null 2>&1; then
          REDIS_CMD="redis-cli -u $REDIS_URL_VALUE"
        fi
        ;;
      *)
        echo "  - REDIS_URL 指向 ${REDIS_HOST}（不是本機），為了安全不清它。"
        echo "    要清正式環境的快取，請到 Railway 後台操作。"
        ;;
    esac
  elif command -v docker >/dev/null 2>&1 &&
    docker compose ps --status running --services 2>/dev/null | grep -qx redis; then
    REDIS_CMD="docker compose exec -T redis redis-cli"
  fi

  if [ -z "$REDIS_CMD" ]; then
    echo "  - 沒有可連線的本機 Redis：本機開發時任務與快取存在後端行程的記憶體裡，"
    echo "    重新啟動後端（python -m backend）即會清空。"
  else
    for pattern in $PATTERNS; do
      count="$($REDIS_CMD --scan --pattern "$pattern" | wc -l | tr -d ' ')"
      if [ "$count" -eq 0 ]; then
        echo "  - ${pattern}：沒有資料"
      elif [ "$DRY_RUN" -eq 1 ]; then
        echo "  [預覽] ${pattern}：$count 筆"
      else
        $REDIS_CMD --scan --pattern "$pattern" | xargs -n 100 $REDIS_CMD DEL >/dev/null
        echo "  ✓ ${pattern}：刪除 $count 筆"
      fi
    done
  fi
fi

echo ""
echo "================================"
if [ "$DRY_RUN" -eq 1 ]; then
  echo "🔍 預覽完成：共 $REMOVED 個項目會被刪除（Redis 鍵值另計）"
else
  echo "✅ 清理完成：共刪除 $REMOVED 個項目"
fi
if [ "$CLEAN_DEEP" -eq 1 ] && [ "$DRY_RUN" -eq 0 ]; then
  echo ""
  echo "💡 依賴已刪除，請重新安裝："
  echo "   bun install"
  echo "   (cd frontend && bun install)"
  echo "   conda activate tradingagents && pip install -e ."
fi
