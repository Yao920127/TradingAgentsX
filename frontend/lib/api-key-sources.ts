/**
 * Where users can obtain each API key. Rendered as a "get your key" link
 * under every key field in the settings dialog.
 */
export interface ApiKeySource {
  url: string;
  /** Site name shown as the link text */
  site: string;
}

export const API_KEY_SOURCES = {
  openai_api_key: { url: "https://platform.openai.com/api-keys", site: "OpenAI Platform" },
  anthropic_api_key: { url: "https://console.anthropic.com/settings/keys", site: "Anthropic Console" },
  google_api_key: { url: "https://aistudio.google.com/apikey", site: "Google AI Studio" },
  grok_api_key: { url: "https://console.x.ai", site: "xAI Console" },
  deepseek_api_key: { url: "https://platform.deepseek.com/api_keys", site: "DeepSeek Platform" },
  qwen_api_key: {
    url: "https://www.alibabacloud.com/help/en/model-studio/get-api-key",
    site: "Alibaba Cloud Model Studio",
  },
  alpha_vantage_api_key: { url: "https://www.alphavantage.co/support/#api-key", site: "Alpha Vantage" },
  finmind_api_key: { url: "https://finmindtrade.com/", site: "FinMind" },
  finnhub_api_key: { url: "https://finnhub.io/register", site: "Finnhub" },
  marketaux_api_key: { url: "https://www.marketaux.com/register", site: "Marketaux" },
  newsapi_api_key: { url: "https://newsapi.org/register", site: "NewsAPI.org" },
  jina_api_key: { url: "https://jina.ai/reader/", site: "Jina AI" },
  apify_api_token: { url: "https://console.apify.com/settings/integrations", site: "Apify Console" },
  lunarcrush_api_key: {
    url: "https://lunarcrush.com/developers/api/authentication",
    site: "LunarCrush Developers",
  },
} as const satisfies Record<string, ApiKeySource>;

export type ApiKeySourceField = keyof typeof API_KEY_SOURCES;
