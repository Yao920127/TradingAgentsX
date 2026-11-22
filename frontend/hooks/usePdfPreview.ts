"use client";

import { useCallback, useMemo, useState } from "react";
import type { AnalysisResponse } from "@/lib/types";
import { buildPdfRequestBody } from "@/lib/pdf-request";
import type { PdfPreviewModalProps } from "@/components/analysis/PdfPreviewModal";

export function usePdfPreview(result: AnalysisResponse) {
  const [isOpen, setIsOpen] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [tempId, setTempId] = useState<string | null>(null);
  const [filename, setFilename] = useState("");
  const [error, setError] = useState<string | null>(null);

  const body = useMemo(() => buildPdfRequestBody(result), [result]);

  const generate = useCallback(async () => {
    if (!body) return;
    setGenerating(true);
    setError(null);
    setTempId(null);
    setFilename(`${result.ticker}_Report_${result.analysis_date}.pdf`);
    try {
      const response = await fetch("/api/pdf/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        throw new Error(data.detail || `PDF generation failed (${response.status})`);
      }
      const data = (await response.json()) as { temp_id: string; filename: string };
      setTempId(data.temp_id);
      setFilename(data.filename);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "PDF generation failed");
    } finally {
      setGenerating(false);
    }
  }, [body, result.ticker, result.analysis_date]);

  const open = useCallback(() => {
    setIsOpen(true);
    void generate();
  }, [generate]);

  const close = useCallback(() => {
    setIsOpen(false);
    if (tempId) fetch(`/api/pdf/temp/${tempId}`, { method: "DELETE" }).catch(() => {});
    setTempId(null);
    setError(null);
  }, [tempId]);

  const modal: PdfPreviewModalProps = {
    isOpen,
    generating,
    error,
    filename,
    tempId,
    onClose: close,
    onRetry: generate,
  };

  return { open, generating, canGenerate: body !== null, modal };
}
