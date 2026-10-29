/**
 * Report markdown normalisation for display.
 *
 * Mirrors tradingagents/utils/report_format.py so reports saved before the
 * backend started normalising (and any that slip through) render the same way:
 * - strips the model's "thinking out loud" opener
 *   (e.g. 「數據已全數取得，現在進行深度整合分析並撰寫完整技術報告。」)
 * - removes horizontal rules (---, ***, —-)
 * - unifies headings: section headings → "##", sub-headings → "###"
 * - turns ▸ / • style bullets into markdown bullets
 * - adds blank lines around tables and before "**標籤：**" lines so they don't merge
 */

const MAX_BOLD_HEADING_CHARS = 40;
const MAX_PREAMBLE_CHARS = 80;
const MAX_PREAMBLE_LINES = 2;
const SENTENCE_ENDINGS = ["。", "！", "？", ".", "!", "?"];

const CHINESE_SECTION = /^[一二三四五六七八九十]{1,3}[、．.]\s*\S/;
const WHOLE_BOLD = /^\*\*([^*]+?)\*\*\s*[:：]?$/;
const HEADING = /^(#{1,6})\s+(.+)$/;
const HORIZONTAL_RULE = /^\s*[-—–*_=]{2,}\s*$/;
const BULLET_SYMBOL = /^\s*[▸►▶•●▪◆·∙]\s*/;
const LABEL_LINE = /^\*\*[^*]{1,30}?(?:[:：]\*\*|\*\*\s*[:：])/;

const PREAMBLE = new RegExp(
  [
    "(?:^|[，,。])\\s*(?:數據|資料|新聞|所有|相關|工具)?[^\\n]{0,12}" +
      "(?:已(?:經)?(?:全數|全部|成功|順利)?(?:取得|獲取|收集|蒐集|齊全|備齊)" +
      "|(?:現在|接下來|下面|讓我|我將|我會|我來)(?:開始|來)?(?:進行|撰寫|整理|為您|提供|產出|彙整|分析))",
    "^(?:Now|Next),? (?:I(?:'ll| will)|let me)",
    "^(?:I have|I've) (?:now )?(?:gathered|collected|obtained|got)",
    "^Let me (?:now )?(?:write|compile|analy[sz]e|put together)",
  ].join("|"),
  "i",
);
// A real opener always mentions the data or the report itself
const PREAMBLE_SUBJECT = /報告|分析|資料|數據|新聞|data|report|analysis/i;

function stripBold(text: string): string {
  return text.replaceAll("**", "").trim();
}

function isPreamble(line: string): boolean {
  const stripped = line.trim();
  return (
    stripped.length > 0 &&
    stripped.length <= MAX_PREAMBLE_CHARS &&
    !/^[#|*-]/.test(stripped) &&
    PREAMBLE.test(stripped) &&
    PREAMBLE_SUBJECT.test(stripped)
  );
}

function stripPreamble(lines: string[]): string[] {
  let start = 0;
  let removed = 0;
  while (start < lines.length && removed < MAX_PREAMBLE_LINES) {
    const line = lines[start];
    if (!line.trim() || HORIZONTAL_RULE.test(line)) {
      start += 1;
      continue;
    }
    if (!isPreamble(line)) break;
    start += 1;
    removed += 1;
  }
  return lines.slice(start);
}

/** Returns the normalised heading line, or null when the line is not a heading. */
function normalizeHeading(line: string): string | null {
  const stripped = line.trim();
  if (!stripped || /^(\||- |\* |> )/.test(stripped)) return null;

  const heading = stripped.match(HEADING);
  if (heading) {
    const text = stripBold(heading[2]);
    const level = CHINESE_SECTION.test(text) ? 2 : Math.min(Math.max(2, heading[1].length), 3);
    return `${"#".repeat(level)} ${text}`;
  }

  const bold = stripped.match(WHOLE_BOLD);
  const plain = bold ? stripBold(bold[1]) : stripped;
  if (CHINESE_SECTION.test(plain) && plain.length <= MAX_BOLD_HEADING_CHARS) return `## ${plain}`;
  const isSentence = SENTENCE_ENDINGS.some((ending) => plain.endsWith(ending));
  if (bold && plain.length <= MAX_BOLD_HEADING_CHARS && !isSentence) return `### ${plain}`;
  return null;
}

export function normalizeReportMarkdown(text: string): string {
  if (!text || !text.trim()) return text;

  const output: string[] = [];
  for (const rawLine of stripPreamble(text.split("\n"))) {
    if (HORIZONTAL_RULE.test(rawLine)) continue;
    const line = rawLine.replace(BULLET_SYMBOL, "- ");
    const heading = normalizeHeading(line);
    const previous = output.length ? output[output.length - 1].trim() : "";

    if (heading === null) {
      const isTable = line.trim().startsWith("|");
      const needsGap =
        previous && (isTable !== previous.startsWith("|") || LABEL_LINE.test(line.trim()));
      if (needsGap) output.push("");
      output.push(line);
      continue;
    }
    if (previous) output.push("");
    output.push(heading, "");
  }
  return output.join("\n").replace(/\n{3,}/g, "\n\n").trim();
}
