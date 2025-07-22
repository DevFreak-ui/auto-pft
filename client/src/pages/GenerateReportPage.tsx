import { useCallback } from "react"
import { useDropzone } from "react-dropzone"
import PageLayout from "./PageContainer"
import ReportProgressStepper from "@/components/custom/ReportProgressStepper"
import { Button } from "@/components/ui/button"
import { usePftUpload } from "@/hooks/usePftUpload"
import { useGetReport } from "@/hooks/useGetReport"

const GenerateReportPage = () => {
  const {
    upload,
    uploadStatus,
    requestId,
    progress,
    step,
    currentStep,
    canViewReport,
    error,
    pollStatus,
  } = usePftUpload();

  const { getReport } = useGetReport();

  // Handle file drop
  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;
    const file = acceptedFiles[0];
    try {
      const reqId = await upload({
        file,
        patient_id: "232",
        age: "23",
        gender: "male",
        height: "170",
        weight: "70",
        priority: "routine",
        ethnicity: "",
        smoking_status: "",
        requesting_physician: ""
      });
      // Start polling for status after upload
      pollStatus(reqId);
    } catch (e) {
      // error is handled in hook
    }
  }, [upload, pollStatus]);

  const handleViewReport = useCallback(async () => {
    if (!requestId) return;
    const report = await getReport(requestId);
    console.log(report);
  }, [getReport, requestId]);

  const { getRootProps, getInputProps, isDragActive, acceptedFiles } = useDropzone({
    onDrop,
    accept: { 'application/pdf': [], 'text/csv': [], 'text/plain': [], 'text/json': [] },
    multiple: false
  })

  return (
    <PageLayout>
      {uploadStatus === "success" || uploadStatus === "uploading" ? (
        <ReportProgressStepper step={step} canViewReport={canViewReport} onViewReportClick={handleViewReport} />
      ) : (
        <div className="flex flex-col items-center justify-center mt-20">
          <h1 className="text-4xl text-/70 font-bold">PFT Report Made Easy</h1>
          <p className="text-sm text-muted-foreground mt-2">
            Upload your documents and let AutoPFT generate a PFT report for you.
          </p>

          {/* Dropzone */}
          <div className="flex items-center justify-center w-3/5 mx-auto mt-10">
            <div
              {...getRootProps()}
              className={`flex flex-col items-center justify-center w-4/5 h-54 border border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50/20 dark:hover:bg-gray-700/10 dark:bg-gray-800/10 dark:border-green/50 dark:hover:border-green/80 ${
                isDragActive ? "border-blue-500" : ""
              }`}
            >
              <input {...getInputProps()} />
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                <svg className="w-8 h-8 mb-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                  <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"/>
                </svg>
                <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
                  <span className="font-semibold">Click to upload</span> or drag and drop
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">PDF, XLSX, CSV, TXT, etc.</p>
                {isDragActive && (
                  <p className="text-blue-500 mt-2">Drop the files here ...</p>
                )}
              </div>
            </div>
          </div>

          {/* Show selected files */}
          {acceptedFiles.length > 0 && (
            <div className="mt-6 w-1/2 mx-auto">
              <h2 className="text-lg font-semibold mb-2">Selected file:</h2>
              <Button variant="outline" className="flex gap-3 cursor-pointer">
                {acceptedFiles.map((file) => (
                  <span key={file.name} className="text-sm">
                    {file.name} ({Math.round(file.size / 1024)} KB)
                  </span>
                ))}
                {uploadStatus && (
                  <span className="ml-4 text-xs text-gray-500">{uploadStatus}</span>
                )}
                {error && (
                  <span className="ml-4 text-xs text-red-500">{error}</span>
                )}
              </Button>
            </div>
          )}
        </div>
      )}
    </PageLayout>
  )
}

export default GenerateReportPage;