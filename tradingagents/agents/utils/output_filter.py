# -*- coding: utf-8 -*-
"""
LLM Output Post-Processing Filter
Fixes common LLM output errors including character corruption and format issues
"""
import re


def _normalize_content(text) -> str:
    """
    Normalize LLM response content to a plain string.

    Some providers (e.g. Gemini via the OpenAI-compatible endpoint) return
    response.content as a list of content blocks rather than a plain string:
        [{'type': 'text', 'text': '...', 'extras': {...}}]

    This helper extracts and joins the text so downstream functions always
    receive a str.
    """
    if text is None:
        return ""
    if isinstance(text, str):
        return text
    if isinstance(text, list):
        parts = []
        for block in text:
            if isinstance(block, dict):
                # Standard content-block format used by Gemini / OpenAI multimodal
                parts.append(block.get("text", "") or block.get("content", ""))
            elif isinstance(block, str):
                parts.append(block)
        return "".join(parts)
    # Fallback: coerce to string (should not normally reach here)
    return str(text)


# 各供應商「輸出達到 max_tokens 上限」的停止原因
# Claude: stop_reason=max_tokens；OpenAI 相容: finish_reason=length；Gemini: finish_reason=MAX_TOKENS
TRUNCATED_STOP_REASONS = {"max_tokens", "length", "MAX_TOKENS"}

TRUNCATION_NOTICES = {
    "zh-TW": "\n\n註：本報告因模型輸出長度上限而被截斷，最後一段可能不完整。",
    "en": "\n\nNote: this report was cut off by the model's output length limit; the last section may be incomplete.",
}


def is_truncated(response) -> bool:
    metadata = getattr(response, "response_metadata", None) or {}
    reason = metadata.get("stop_reason") or metadata.get("finish_reason")
    return reason in TRUNCATED_STOP_REASONS


def report_text(response, agent_name: str, language: str = "zh-TW") -> str:
    """取出 LLM 回應的報告文字；若因長度上限被截斷，記錄警告並在文末加註。"""
    text = _normalize_content(response.content)
    if not is_truncated(response):
        return text
    print(f"警告：{agent_name} 的輸出達到長度上限被截斷（{len(text)} 字元）")
    return text + TRUNCATION_NOTICES.get(language, TRUNCATION_NOTICES["en"])


def count_chinese_words(text: str) -> int:
    """
    Count Chinese characters in text (excluding markdown and tables)
    
    Args:
        text: Input text
        
    Returns:
        Number of Chinese characters
    """
    # Remove code blocks
    clean_text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # Remove tables
    clean_text = re.sub(r'\|.*?\|', '', clean_text, flags=re.MULTILINE)
    # Remove markdown formatting
    clean_text = re.sub(r'[#\*_`~\[\]\(\)]', '', clean_text)
    
    # Count Chinese characters (CJK Unified Ideographs)
    return len([c for c in clean_text if '\u4e00' <= c <= '\u9fff'])


def strip_preamble(text: str) -> str:
    """
    Strip AI-generated acknowledgment sentences that appear before the actual report.
    These are phrases the model produces when transitioning from tool-use to report writing,
    e.g. "完美。我已收集完數據，現在為您提供..." or "根據我獲取的近期新聞數據，現在為您提供..."

    Args:
        text: LLM output text

    Returns:
        Text with preamble sentences removed
    """
    # Patterns that match common preamble openers (Chinese)
    zh_preamble_patterns = [
        # "完美。..." / "完美！..." style
        r'^完美[。！,，][^\n]{0,120}\n+',
        # "根據我獲取..." / "根據收集到的數據..." / "根據獲取的..."
        r'^根據(?:我)?(?:收集|獲取)[^\n]{0,120}\n+',
        # "我已[蒐收]集..." / "我已獲取..."
        r'^我已[蒐收獲][^\n]{0,120}\n+',
        # "現在讓我為您..." / "現在為您提供..."
        r'^現在(?:讓我)?為您[^\n]{0,100}\n+',
        # "以下是..." opener that's just a transition phrase (short)
        r'^以下是.{0,30}報告[：:]\s*\n+',
        # "好的，" / "好的！" opener
        r'^好的[，,。！!][^\n]{0,80}\n+',
        # "為您提供..." opener
        r'^為您提供[^\n]{0,100}\n+',
    ]

    # Patterns for English preamble
    en_preamble_patterns = [
        r'^(?:Perfect|Great|Excellent)[.,!][^\n]{0,120}\n+',
        r'^(?:I have|I\'ve) (?:collected|gathered|obtained)[^\n]{0,120}\n+',
        r'^(?:Now|Let me) (?:I\'ll )?provide[^\n]{0,100}\n+',
        r'^Based on (?:the )?(?:data|news|information) (?:I\'ve |I have )?(?:collected|gathered)[^\n]{0,100}\n+',
    ]

    all_patterns = zh_preamble_patterns + en_preamble_patterns

    # Only strip from the very beginning of the text (up to 3 preamble lines)
    for _ in range(3):
        stripped = False
        for pattern in all_patterns:
            new_text = re.sub(pattern, '', text, count=1, flags=re.IGNORECASE)
            if new_text != text:
                text = new_text.lstrip('\n')
                stripped = True
                break
        if not stripped:
            break

    return text


def strip_word_counts_from_headings(text: str) -> str:
    """
    Strip word count annotations that models insert into section headings.
    Examples removed:
      - "核心論點(150字)"          → "核心論點"
      - "核心論點（約 150 字）"     → "核心論點"
      - "Core Arguments (~150 words)" → "Core Arguments"
      - "一、核心風險診斷（約150字）" → "一、核心風險診斷"

    Applies globally since these annotations only appear in headings by convention.
    """
    # Chinese: （約150字）（150字）（约150字）（150字以內）（约 150 字）
    text = re.sub(r'[（(][約约]?\s*\d+\s*[字][）)]', '', text)
    # English: (~150 words) (150 words) (approximately 150 words)
    text = re.sub(r'\s*\(~?\s*\d+\s*words?\)', '', text, flags=re.IGNORECASE)
    return text


def fix_common_llm_errors(text) -> str:
    """
    Fix common LLM character selection errors and strip preamble text.

    Args:
        text: LLM output text (str or list of content blocks from Gemini etc.)

    Returns:
        Corrected text as a plain string
    """
    # Normalize: handle Gemini-style list content (e.g. [{'type':'text','text':'...'}])
    text = _normalize_content(text)

    # Step 0: Strip AI preamble sentences before the actual report
    text = strip_preamble(text)

    # Step 0b: Strip word count annotations from headings (e.g. "核心論點（約150字）")
    text = strip_word_counts_from_headings(text)

    # Common character misuse patterns
    replacements = {
        # '煉' misuse - should be '練' (practice/train) in most contexts
        '煉習': '練習',
        '訓煉': '訓練',
        '**煉**': '**練**',
        '（煉': '（練',
        '煉）': '練）',

        # Other common errors (add as discovered)
        '絓驗': '經驗',  # We saw this corruption before
    }

    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)

    return text


def validate_and_warn(content, agent_name: str) -> list:
    """
    Validate report content and return list of warnings

    Args:
        content: Report content (str or list of content blocks from Gemini etc.)
        agent_name: Name of the agent

    Returns:
        List of warning messages
    """
    # Normalize: handle Gemini-style list content
    content = _normalize_content(content)
    warnings = []
    
    # Check for suspicious '煉' character
    # Only flag if not in proper contexts like "冶煉", "提煉", "鍛煉"
    if '煉' in content:
        proper_contexts = ['冶煉', '提煉', '鍛煉', '精煉', '修煉']
        is_proper = any(ctx in content for ctx in proper_contexts)
        if not is_proper:
            # Find context around '煉'
            idx = content.find('煉')
            context = content[max(0, idx-15):min(len(content), idx+15)]
            warnings.append(f"Suspicious '煉' character found. Context: ...{context}...")
    
    # Check for truncation markers that shouldn't be there
    truncation_markers = ['...(已截斷)', '...(內容已截斷)', '...(為控制長度已精簡)']
    for marker in truncation_markers:
        if marker in content:
            warnings.append(f"Found truncation marker: '{marker}'")
    
    if warnings:
        print(f"\n⚠️  {agent_name} Report Warnings:")
        for warning in warnings:
            print(f"   - {warning}")
    
    return warnings


def post_process_agent_output(content: str, agent_name: str, retry_callback=None) -> str:
    """
    Complete post-processing pipeline for agent output
    
    Args:
        content: Raw agent output
        agent_name: Name of the agent
        retry_callback: Optional function to call if validation fails
        
    Returns:
        Processed and validated content
    """
    # Step 1: Fix common errors
    content = fix_common_llm_errors(content)
    
    # Step 2: Validate and warn
    warnings = validate_and_warn(content, agent_name)
    
    return content


def ensure_min_length(content: str, min_words: int = 500, agent_name: str = "Agent") -> tuple:
    """
    確保報告達到字數要求範圍 (500-1000)，如果不符合則返回False觸發重試

    Args:
        content: The report content to check
        min_words: Minimum required word count (default: 500)
        agent_name: Name of the agent for logging

    Returns:
        tuple: (content, is_valid: bool)
    """
    word_count = count_chinese_words(content)

    if word_count < min_words:
        print(f"⚠️  [{agent_name}] Report too short")
        return content, False
    else:
        print(f"✅ [{agent_name}] Report meets requirements")
        return content, True

