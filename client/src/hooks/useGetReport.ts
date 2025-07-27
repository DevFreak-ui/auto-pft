import { useCallback, useState, useEffect } from "react";
import { getPftStatus, getPftReport } from "@/services/pftService";

export function useGetReport() {
  const [report, setReport] = useState<any>(null);
  const [status, setStatus] = useState<"idle" | "loading" | "error" | "success">("idle");
  const [error, setError] = useState<string | null>(null);

  const getReport = useCallback(async (request_id: string) => {
    setStatus("loading");
    setError(null);
    try {
      const stat = await getPftStatus(request_id);
      if (stat.current_step === "Processing completed successfully") {
        const rep = await getPftReport(request_id);
        setReport(rep.report);
        setStatus("success");
        return rep;
      } else {
        setStatus("error");
        setError("Report is not ready yet.");
        return null;
      }
    } catch (err: any) {
      setStatus("error");
      setError(err.message || "Unknown error");
      return null;
    }
  }, []);

  return { getReport, report, status, error };
}

export function useGeneratedReports() {
  const [reports, setReports] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchReports() {
      setLoading(true);
      let ids: string[] = [];
      try {
        const stored = localStorage.getItem("GeneratedReportIds");
        if (stored) ids = JSON.parse(stored);
      } catch {}
      if (!ids.length) {
        setReports([]);
        setLoading(false);
        return;
      }
      const results = await Promise.all(
        ids.map(async (id) => {
          try {
            const rep = await getPftReport(id);
            const report = rep.report || rep;
            return {
              id,
              generated_by: report.generated_by,
              generated_at: report.generated_at,
              status: report.quality_assessment?.approval_status,
              severity: report.interpretation?.severity || 'N/A',
              reviewer: report.quality_assessment?.reviewer || null,
            };
          } catch {
            return null;
          }
        })
      );
      setReports(results.filter(Boolean));
      setLoading(false);
    }
    fetchReports();
  }, []);

  return { reports, loading };
} 