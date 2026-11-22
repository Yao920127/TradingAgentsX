"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Sparkles } from "lucide-react";
import { useLanguage } from "@/contexts/LanguageContext";
import { Button } from "@/components/ui/button";
import { ResultsView } from "@/components/analysis/ResultsView";
import type { AnalysisResponse } from "@/lib/types";

const DEMO_URLS: Record<string, string> = {
  "zh-TW": "/demo/nvda-zh-TW.json",
  en: "/demo/nvda-en.json",
};
const DEFAULT_DEMO_URL = DEMO_URLS.en;

interface LoadedDemo {
  url: string;
  data: AnalysisResponse;
}

export default function DemoPage() {
  const router = useRouter();
  const { t, locale } = useLanguage();
  const demoUrl = DEMO_URLS[locale] ?? DEFAULT_DEMO_URL;
  const [loaded, setLoaded] = useState<LoadedDemo | null>(null);
  const [failedUrl, setFailedUrl] = useState<string | null>(null);

  // The demo report exists in each UI language; refetch when the locale changes.
  useEffect(() => {
    const controller = new AbortController();
    fetch(demoUrl, { signal: controller.signal })
      .then((res) => {
        if (!res.ok) throw new Error(String(res.status));
        return res.json() as Promise<AnalysisResponse>;
      })
      .then((data) =>
        setLoaded({ url: demoUrl, data: { ...data, market_type: data.market_type ?? "us" } }),
      )
      .catch(() => {
        if (!controller.signal.aborted) setFailedUrl(demoUrl);
      });
    return () => controller.abort();
  }, [demoUrl]);

  const result = loaded?.url === demoUrl ? loaded.data : null;
  const failed = failedUrl === demoUrl;

  if (failed) {
    return (
      <div className="container mx-auto px-4 py-12 text-center">
        <p className="text-muted-foreground">{t.demo.loadFailed}</p>
        <Button className="mt-4" onClick={() => router.push("/")}>
          {t.results.backButton}
        </Button>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center text-muted-foreground">
        {t.demo.loading}
      </div>
    );
  }

  return (
    <ResultsView
      analysisResult={result}
      marketType="us"
      banner={
        <div className="flex flex-col gap-3 rounded-2xl border border-border bg-muted/50 p-4 sm:flex-row sm:items-center sm:justify-between">
          <p className="flex items-start gap-2 text-sm text-muted-foreground">
            <Sparkles className="mt-0.5 h-4 w-4 shrink-0" />
            <span>{t.demo.banner}</span>
          </p>
          <Button size="sm" onClick={() => router.push("/analysis")}>
            {t.demo.startOwn} →
          </Button>
        </div>
      }
    />
  );
}
