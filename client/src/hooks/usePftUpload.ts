import { useState, useCallback } from "react";
import { uploadPftFile, getPftStatus } from "@/services/pftService";
import type { PftUploadParams } from "@/services/pftService";

export function usePftUpload() {
  const [uploadStatus, setUploadStatus] = useState<"idle" | "uploading" | "success" | "error">("idle");
  const [requestId, setRequestId] = useState<string | null>(null);
  const [progress, setProgress] = useState<number>(0);
  const [currentStep, setCurrentStep] = useState<string>("");
  const [step, setStep] = useState<1 | 2 | 3>(1);
  const [canViewReport, setCanViewReport] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const upload = useCallback(async (params: PftUploadParams) => {
    setUploadStatus("uploading");
    setError(null);
    try {
      const result = await uploadPftFile(params);
      setRequestId(result.request_id);
      setUploadStatus("success");
      return result.request_id;
    } catch (err: any) {
      setUploadStatus("error");
      setError(err.message || "Unknown error");
      throw err;
    }
  }, []);

  // Poll status and map progress to step
  const pollStatus = useCallback(async (id: string) => {
    let done = false;
    while (!done) {
      const stat = await getPftStatus(id);
      setProgress(stat.progress);
      setCurrentStep(stat.current_step);
      // Map progress to step
      if (stat.progress < 34) setStep(1);
      else if (stat.progress < 67) setStep(2);
      else setStep(3);
      if (stat.current_step === "Processing completed successfully") {
        setCanViewReport(true);
        done = true;
      } else if (stat.status === "failed") {
        setError(stat.error_message || "Processing failed");
        done = true;
      } else {
        await new Promise(res => setTimeout(res, 2000));
      }
    }
  }, []);

  return {
    upload,
    uploadStatus,
    requestId,
    progress,
    step,
    currentStep,
    canViewReport,
    error,
    pollStatus,
  };
} 