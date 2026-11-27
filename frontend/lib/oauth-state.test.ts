import { describe, expect, test } from "bun:test";
import { consumeOAuthState, createOAuthState } from "./oauth-state";

function memoryStorage(): Storage {
  const data = new Map<string, string>();
  return {
    get length() {
      return data.size;
    },
    clear: () => data.clear(),
    getItem: (key) => data.get(key) ?? null,
    key: (index) => Array.from(data.keys())[index] ?? null,
    removeItem: (key) => void data.delete(key),
    setItem: (key, value) => void data.set(key, value),
  };
}

describe("oauth state", () => {
  test("created state is stored and accepted exactly once", () => {
    const storage = memoryStorage();
    const state = createOAuthState(storage);

    expect(state.length).toBeGreaterThanOrEqual(32);
    expect(consumeOAuthState(state, storage)).toBe(true);
    expect(consumeOAuthState(state, storage)).toBe(false);
  });

  test("each login attempt gets a different state", () => {
    const storage = memoryStorage();
    const first = createOAuthState(storage);
    const second = createOAuthState(storage);
    expect(first).not.toBe(second);
  });

  test("a mismatching state is rejected and the stored one is discarded", () => {
    const storage = memoryStorage();
    const state = createOAuthState(storage);

    expect(consumeOAuthState("attacker-supplied", storage)).toBe(false);
    expect(consumeOAuthState(state, storage)).toBe(false);
  });

  test("missing received state is rejected", () => {
    const storage = memoryStorage();
    createOAuthState(storage);
    expect(consumeOAuthState(null, storage)).toBe(false);
    expect(consumeOAuthState("", storage)).toBe(false);
  });

  test("no stored state means rejection, even for an empty received value", () => {
    const storage = memoryStorage();
    expect(consumeOAuthState("anything", storage)).toBe(false);
    expect(consumeOAuthState(null, storage)).toBe(false);
  });
});
