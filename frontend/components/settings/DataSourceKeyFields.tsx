"use client";

import type { Control, FieldValues, Path } from "react-hook-form";
import { useLanguage } from "@/contexts/LanguageContext";
import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import type { TranslationKeys } from "@/lib/i18n";
import type { ApiKeySourceField } from "@/lib/api-key-sources";
import { ApiKeyHelpLink } from "./ApiKeyHelpLink";

type SettingsText = TranslationKeys["settings"];

type DataSourceField = {
  name: ApiKeySourceField;
  label: keyof SettingsText;
  description: keyof SettingsText;
};

// News & social data keys — all optional; a source without a key is skipped.
const DATA_SOURCE_FIELDS: DataSourceField[] = [
  { name: "finnhub_api_key", label: "finnhubKey", description: "finnhubDesc" },
  { name: "marketaux_api_key", label: "marketauxKey", description: "marketauxDesc" },
  { name: "newsapi_api_key", label: "newsapiKey", description: "newsapiDesc" },
  { name: "jina_api_key", label: "jinaKey", description: "jinaDesc" },
  { name: "apify_api_token", label: "apifyKey", description: "apifyDesc" },
  { name: "lunarcrush_api_key", label: "lunarcrushKey", description: "lunarcrushDesc" },
];

type Props<T extends FieldValues> = {
  control: Control<T>;
};

export function DataSourceKeyFields<T extends FieldValues>({ control }: Props<T>) {
  const { t } = useLanguage();

  return (
    <div className="space-y-4 border-t pt-4">
      <h3 className="text-lg font-semibold text-muted-foreground">
        {t.settings.dataSourceApis}
      </h3>
      <p className="text-sm text-muted-foreground">{t.settings.dataSourceApisHint}</p>

      {DATA_SOURCE_FIELDS.map(({ name, label, description }) => (
        <FormField
          key={name}
          control={control}
          name={name as Path<T>}
          render={({ field }) => (
            <FormItem>
              <FormLabel>{t.settings[label]}</FormLabel>
              <FormControl>
                <Input type="password" placeholder={t.settings.keyPlaceholder} {...field} />
              </FormControl>
              <FormDescription>
                {t.settings[description]}
                <ApiKeyHelpLink field={name} />
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
      ))}
    </div>
  );
}
