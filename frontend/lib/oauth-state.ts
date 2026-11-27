/**
 * OAuth `state` 參數：防止登入 CSRF（攻擊者誘使受害者用攻擊者的 authorization code 登入）。
 * 登入前產生隨機值存進 sessionStorage，Google 導回後必須帶回同一個值，且只能使用一次。
 */

const STATE_STORAGE_KEY = "oauth_state";
const STATE_BYTES = 16;

function randomHex(byteLength: number): string {
  const bytes = new Uint8Array(byteLength);
  crypto.getRandomValues(bytes);
  return Array.from(bytes, (byte) => byte.toString(16).padStart(2, "0")).join("");
}

export function createOAuthState(storage: Storage = sessionStorage): string {
  const state = randomHex(STATE_BYTES);
  storage.setItem(STATE_STORAGE_KEY, state);
  return state;
}

/** 比對收到的 state；無論成功與否都會清除已儲存的值，因此同一個 state 不可重複使用。 */
export function consumeOAuthState(received: string | null, storage: Storage = sessionStorage): boolean {
  const expected = storage.getItem(STATE_STORAGE_KEY);
  storage.removeItem(STATE_STORAGE_KEY);
  return Boolean(expected) && Boolean(received) && expected === received;
}
