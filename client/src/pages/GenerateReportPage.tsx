import { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import PageLayout from "./PageContainer";

const GenerateReportPage = () => {
  // Handle file drop
  const onDrop = useCallback((acceptedFiles: File[]) => {
    // You can handle the uploaded files here
    // For example, upload to server or update state
    console.log(acceptedFiles);
  }, []);

  const { getRootProps, getInputProps, isDragActive, acceptedFiles } = useDropzone({
    onDrop,
    // You can add file type/size restrictions here if needed
    accept: { 'application/pdf': [], 'text/csv': [], 'text/plain': [], 'text/json': []}
  });

  return (
    <PageLayout>
      <div className="flex flex-col items-center justify-center mt-20">
        <h1 className="text-4xl font-bold">PFT Report Made Easy</h1>
        <p className="text-sm text-muted-foreground mt-2">
          Upload your documents and let AutoPFT generate a PFT report for you.
        </p>

        {/* Dropzone */}
        <div className="flex items-center justify-center w-3/5 mx-auto mt-10">
            <div
                {...getRootProps()}
                className={`flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-gray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600 ${
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
          <div className="mt-4 w-3/5 mx-auto">
            <h2 className="text-lg font-semibold mb-2">Selected files:</h2>
            <ul>
              {acceptedFiles.map((file) => (
                <li key={file.name} className="text-sm">
                  {file.name} ({Math.round(file.size / 1024)} KB)
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </PageLayout>
  );
};

export default GenerateReportPage;