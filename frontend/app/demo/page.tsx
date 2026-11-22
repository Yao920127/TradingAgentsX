"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Sparkles } from "lucide-react";
import { useLanguage } from "@/contexts/LanguageContext";
import { Button } from "@/components/ui/button";
import { ResultsView } from "@/components/analysis/ResultsView";
import type { AnalysisResponse } from "@/lib/types";

const DEMO_URL = "/demo/nvda.json";

export default function DemoPage() {
  const router = useRouter();
  const { t } = useLanguage();
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    const controller = new AbortController();
    fetch(DEMO_URL, { signal: controller.signal })
      .then((res) => {
        if (!res.ok) throw new Error(String(res.status));
        return res.json() as Promise<AnalysisResponse>;
      })
      .then((data) => setResult({ ...data, market_type: data.market_type ?? "us" }))
      .catch((err: unknown) => {
        if (!controller.signal.aborted) setFailed(true);
        void err;
      });
    return () => controller.abort();
  }, []);

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
