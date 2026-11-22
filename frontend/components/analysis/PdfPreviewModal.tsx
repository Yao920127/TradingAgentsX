"use client";

import { useEffect, useState } from "react";
import { Download, FileText, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useLanguage } from "@/contexts/LanguageContext";

export interface PdfPreviewModalProps {
  isOpen: boolean;
  generating: boolean;
  error: string | null;
  filename: string;
  tempId: string | null;
  onClose: () => void;
  onRetry: () => void;
}

const FALLBACK_LOAD_MS = 3000;

export function PdfPreviewModal({
  isOpen,
  generating,
  error,
  filename,
  tempId,
  onClose,
  onRetry,
}: PdfPreviewModalProps) {
  const { t } = useLanguage();
  const [loaded, setLoaded] = useState(false);
  const url = tempId ? `/api/pdf/serve/${tempId}` : null;

  // <embed> may not fire onLoad in every browser; never leave the spinner stuck.
  useEffect(() => {
    setLoaded(false);
    if (!url) return;
    const timer = setTimeout(() => setLoaded(true), FALLBACK_LOAD_MS);
    return () => clearTimeout(timer);
  }, [url]);

  if (!isOpen) return null;

  const handleDownload = () => {
    if (!url) return;
    const link = document.createElement("a");
    link.href = `${url}?download=true`;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
      <div className="relative flex h-[90vh] w-full max-w-5xl flex-col rounded-2xl bg-card">
        <div className="flex shrink-0 items-center justify-between border-b border-border px-5 py-4">
          <div className="flex min-w-0 items-center gap-2">
            <FileText className="h-5 w-5 shrink-0" />
            <span className="truncate text-sm font-semibold">{filename}</span>
          </div>
          <button
            onClick={onClose}
            className="ml-3 shrink-0 rounded-full p-1.5 transition-colors hover:bg-muted"
            aria-label={t.common.close}
          >
            <X className="h-5 w-5 text-muted-foreground" />
          </button>
        </div>

        <div className="relative flex-1 overflow-hidden bg-muted">
          {generating && (
            <div className="absolute inset-0 z-10 flex flex-col items-center justify-center gap-4 bg-card">
              <div className="h-16 w-16 animate-spin rounded-full border-4 border-border border-t-foreground" />
              <p className="font-medium text-muted-foreground">{t.results.pdfGenerating}</p>
              <p className="text-sm text-muted-foreground">{t.results.pdfGeneratingHint}</p>
            </div>
          )}
          {!generating && error && (
            <div className="absolute inset-0 z-10 flex flex-col items-center justify-center gap-4 bg-card p-8 text-center">
              <p className="font-medium text-destructive">{t.results.pdfFailed}</p>
              <p className="text-sm text-muted-foreground">{error}</p>
              <Button variant="outline" onClick={onRetry}>
                {t.results.pdfRetry}
              </Button>
            </div>
          )}
          {url && !loaded && !generating && !error && (
            <div className="absolute inset-0 z-10 flex items-center justify-center bg-card">
              <div className="h-10 w-10 animate-spin rounded-full border-4 border-border border-t-foreground" />
            </div>
          )}
          {url && (
            <embed
              key={url}
              src={url}
              type="application/pdf"
              className="h-full w-full"
              onLoad={() => setLoaded(true)}
            />
          )}
        </div>

        <div className="flex shrink-0 items-center justify-end gap-3 border-t border-border px-5 py-4">
          <Button onClick={handleDownload} disabled={!tempId || generating || !!error} className="gap-2">
            <Download className="h-4 w-4" />
            {t.results.pdfDownload}
          </Button>
        </div>
      </div>
    </div>
  );
}
