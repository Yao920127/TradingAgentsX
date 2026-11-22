"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAnalysisContext } from "@/context/AnalysisContext";
import { useLanguage } from "@/contexts/LanguageContext";
import { Button } from "@/components/ui/button";
import { ResultsView } from "@/components/analysis/ResultsView";

export default function AnalysisResultsPage() {
  const router = useRouter();
  const { analysisResult, marketType } = useAnalysisContext();
  const { t } = useLanguage();

  // Redirect back to the form when there is nothing to show.
  useEffect(() => {
    if (!analysisResult) router.push("/analysis");
  }, [analysisResult, router]);

  if (!analysisResult) {
    return (
      <div className="container mx-auto px-4 py-12">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">{t.results.noResults}</h1>
          <p className="text-muted-foreground mb-4">{t.results.runAnalysisFirst}</p>
          <Button onClick={() => router.push("/analysis")}>{t.results.backToAnalysis}</Button>
        </div>
      </div>
    );
  }

  return (
    <ResultsView
      analysisResult={analysisResult}
      marketType={marketType}
    />
  );
}
