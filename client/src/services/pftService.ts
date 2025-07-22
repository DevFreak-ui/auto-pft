const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export interface PftUploadParams {
  file: File;
  patient_id: string;
  age: string;
  gender: string;
  height: string;
  weight: string;
  priority?: string;
  ethnicity?: string;
  smoking_status?: string;
  requesting_physician?: string;
}

export async function uploadPftFile(params: PftUploadParams) {
  const {
    file,
    patient_id,
    age,
    gender,
    height,
    weight,
    priority = "routine",
    ethnicity = "",
    smoking_status = "",
    requesting_physician = "",
  } = params;

  const query = new URLSearchParams({
    patient_id,
    age,
    gender,
    height,
    weight,
    priority,
    ethnicity,
    smoking_status,
    requesting_physician,
  });

  const url = `${BASE_URL}/pft/upload?${query.toString()}`;
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(url, {
    method: "POST",
    body: formData,
  });
  if (!response.ok) throw new Error("Upload failed");
  return response.json();
}

export async function getPftStatus(request_id: string) {
  const url = `${BASE_URL}/pft/status/${request_id}`;
  const response = await fetch(url);
  if (!response.ok) throw new Error("Failed to get status");
  return response.json();
}
export async function getPftReport(request_id: string) {
  const endpoint = import.meta.env.VITE_REPORT_ENDPOINT || "/pft/report";
  const url = `${BASE_URL}${endpoint}/${request_id}`;
  const response = await fetch(url);
  if (!response.ok) throw new Error("Failed to get report");
  return response.json();
}
export async function interpretPft(data: { /* ... */ }) { /* ... */ }
export async function submitFeedback(data: { /* ... */ }) { /* ... */ }
