"use client";

import { ExternalLink } from "lucide-react";
import { useLanguage } from "@/contexts/LanguageContext";
import { API_KEY_SOURCES, type ApiKeySourceField } from "@/lib/api-key-sources";

type Props = {
  field: ApiKeySourceField;
};

/** "Get your key: <site>" link shown under an API key field. */
export function ApiKeyHelpLink({ field }: Props) {
  const { t } = useLanguage();
  const source = API_KEY_SOURCES[field];

  return (
    <span className="block mt-1 text-xs">
      {t.settings.getKeyAt}
      <a
        href={source.url}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center gap-0.5 font-medium text-blue-600 dark:text-blue-400 underline underline-offset-2 hover:text-blue-800 dark:hover:text-blue-300"
      >
        {source.site}
        <ExternalLink className="h-3 w-3" aria-hidden="true" />
      </a>
    </span>
  );
}
