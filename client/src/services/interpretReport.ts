const BASE_URL = import.meta.env.VITE_API_BASE_URL;

// Interface for the explain request
export interface ExplainRequest {
  report_id: string;
  question: string;
}

// Interface for the explain response
export interface ExplainResponse {
  answer: string;
  confidence: number;
  sources: string[];
  key_points: string[];
  clinical_pearls: string[];
  related_concepts: string[];
  follow_up_questions: string[];
  limitations: string[];
  recommendations: string[];
  educational_content: string;
  complexity_level: string;
  specialty_consultation: boolean;
  // Fallback for backward compatibility
  response?: string;
  status?: string;
}

/**
 * Send a question about a specific report to get interpretation
 * @param report_id - The ID of the report to explain
 * @param question - The user's question about the report
 * @returns Promise with the explanation response
 */
export async function explainReport(report_id: string, question: string): Promise<ExplainResponse> {
  console.log("[interpretReport] Sending explain request:", { report_id, question });
  
  const url = `${BASE_URL}/chat/explain/${report_id}`;
  
  const queryParams = new URLSearchParams({
    question: question
  });
  
  const fullUrl = `${url}?${queryParams.toString()}`;
  
  try {
    const response = await fetch(fullUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      console.error("[interpretReport] API error:", response.status, response.statusText);
      throw new Error(`Failed to get explanation: ${response.status}`);
    }
    
    const data = await response.json();
    console.log("[interpretReport] Received response:", data);
    
    return data;
  } catch (error) {
    console.error("[interpretReport] Network error:", error);
    throw error;
  }
}
