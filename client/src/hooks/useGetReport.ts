import { useCallback, useState } from "react";
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