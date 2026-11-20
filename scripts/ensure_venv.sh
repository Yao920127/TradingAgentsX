#!/usr/bin/env bash
# ========================================
# TradingAgentsX：確保 uv 虛擬環境存在並啟用
#
#   ./scripts/ensure_venv.sh            找不到 .venv 就用 uv 建立，依賴檔有變動才重新安裝
#   source ./scripts/ensure_venv.sh     同上，並在目前的 shell 啟用虛擬環境
#
# 虛擬環境位於專案根目錄的 .venv，提示名稱為 (tradingagents)。
# 所有 Python 套件操作一律透過 uv（uv venv / uv pip），不使用 pip 或 conda。
#
# 由 Claude Code 的 SessionStart hook 呼叫時（有 CLAUDE_ENV_FILE），
# 會把啟用環境的 export 寫進該檔，讓之後每個 Bash 指令都在虛擬環境中執行。
# ========================================

# 在函式外取得腳本路徑：bash 用 BASH_SOURCE，zsh 被 source 時 $0 即為腳本路徑
_TA_SELF="${BASH_SOURCE[0]:-$0}"
_TA_SOURCED=0
if [ -n "${ZSH_EVAL_CONTEXT:-}" ]; then
  case "$ZSH_EVAL_CONTEXT" in *:file*) _TA_SOURCED=1 ;; esac
elif [ -n "${BASH_SOURCE[0]:-}" ] && [ "${BASH_SOURCE[0]}" != "$0" ]; then
  _TA_SOURCED=1
fi

_ta_ensure_venv() {
  local root venv stamp py_version
  root="$(cd "$(dirname "$_TA_SELF")/.." && pwd)"
  venv="$root/.venv"
  stamp="$venv/.deps-installed"

  if ! command -v uv >/dev/null 2>&1; then
    echo "找不到 uv，請先安裝：curl -LsSf https://astral.sh/uv/install.sh | sh" >&2
    return 1
  fi

  if [ ! -x "$venv/bin/python" ]; then
    py_version="$(cat "$root/.python-version" 2>/dev/null || echo 3.13)"
    echo "建立虛擬環境 tradingagents（Python ${py_version}）於 ${venv} ..." >&2
    uv venv "$venv" --prompt tradingagents --python "$py_version" >&2 || return 1
  fi

  # 只在依賴檔比上次安裝新時才重新安裝，避免每次開 session 都跑一次
  if [ ! -f "$stamp" ] \
    || [ "$root/pyproject.toml" -nt "$stamp" ] \
    || [ "$root/backend/requirements.txt" -nt "$stamp" ]; then
    echo "安裝依賴（uv pip install -e . -r backend/requirements.txt）..." >&2
    uv pip install --python "$venv/bin/python" -e "$root" -r "$root/backend/requirements.txt" >&2 \
      || return 1
    touch "$stamp"
  fi

  if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
    {
      echo "export VIRTUAL_ENV=\"$venv\""
      echo "export PATH=\"$venv/bin:\$PATH\""
      echo "unset CONDA_PREFIX CONDA_DEFAULT_ENV PYTHONHOME"
    } >>"$CLAUDE_ENV_FILE"
  fi

  # 被 source 時，在目前的 shell 啟用
  if [ "$_TA_SOURCED" = 1 ]; then
    # shellcheck disable=SC1091
    . "$venv/bin/activate"
  fi

  echo "Python 虛擬環境 tradingagents 已就緒：${venv}（套件操作請用 uv pip）"
}

_ta_ensure_venv
_ta_status=$?
unset -f _ta_ensure_venv
unset _TA_SELF _TA_SOURCED
if [ "$_ta_status" != 0 ]; then
  unset _ta_status
  return 1 2>/dev/null || exit 1
fi
unset _ta_status
