/**
 * Minimal Server-Sent Events reader built on fetch.
 *
 * EventSource cannot send request headers, which forces auth tokens into the URL
 * (and therefore into server access logs). Reading the stream with fetch lets the
 * token travel in the Authorization header instead.
 */

export interface SseEvent {
  event: string;
  data: string;
}

/** Parse one SSE block (the text between blank lines). Returns null for comments/heartbeats. */
export function parseSseBlock(block: string): SseEvent | null {
  let event = "message";
  const dataLines: string[] = [];

  for (const line of block.split(/\r?\n/)) {
    if (!line || line.startsWith(":")) continue;
    const separator = line.indexOf(":");
    const field = separator === -1 ? line : line.slice(0, separator);
    const value = separator === -1 ? "" : line.slice(separator + 1).replace(/^ /, "");
    if (field === "event") event = value;
    else if (field === "data") dataLines.push(value);
  }

  if (event === "message" && dataLines.length === 0) return null;
  return { event, data: dataLines.join("\n") };
}

/**
 * Open an SSE stream and call onEvent for each event until the stream ends.
 * Resolves when the server closes the stream; rejects on network/HTTP errors
 * or when the signal aborts.
 */
export async function readSseStream(
  url: string,
  headers: Record<string, string>,
  signal: AbortSignal,
  onEvent: (event: SseEvent) => void
): Promise<void> {
  const response = await fetch(url, {
    headers: { ...headers, Accept: "text/event-stream" },
    cache: "no-store",
    signal,
  });
  if (!response.ok || !response.body) {
    throw new Error(`SSE request failed with status ${response.status}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) return;
    buffer += decoder.decode(value, { stream: true });

    const blocks = buffer.split(/\r?\n\r?\n/);
    buffer = blocks.pop() ?? "";
    for (const block of blocks) {
      const parsed = parseSseBlock(block);
      if (parsed) onEvent(parsed);
    }
  }
}
