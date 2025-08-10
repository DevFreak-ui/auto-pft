// General Chat Service - Updated
const BASE_URL = import.meta.env.VITE_API_BASE_URL;

// Interface for the chat request - matches server ChatMessage model
export interface ChatRequest {
  message_id: string;
  session_id: string;
  user_id: string;
  message: string;
  timestamp?: string;
  report_id?: string;
}

// Interface for the chat response
export interface ChatResponse {
  message_id: string;
  response: string;
  confidence: number;
  sources: string[];
  timestamp: string;
}

/**
 * Send a general chat message
 * @param message - The user's message
 * @param user_id - User ID (required)
 * @param session_id - Session ID (required)
 * @param report_id - Optional report ID for context
 * @returns Promise with the chat response
 */
export async function sendGeneralChat(message: string, user_id: string, session_id: string, report_id?: string): Promise<ChatResponse> {
  console.log("[generalChat] Sending chat message:", { message, user_id, session_id, report_id });
  
  const url = `${BASE_URL}/chat`;
  
  // Generate a unique message ID
  const message_id = `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  
  const requestBody: ChatRequest = {
    message_id,
    session_id,
    user_id,
    message: message.trim(),
    timestamp: new Date().toISOString(),
    ...(report_id && { report_id })
  };
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });
    
    if (!response.ok) {
      console.error("[generalChat] API error:", response.status, response.statusText);
      throw new Error(`Failed to send message: ${response.status}`);
    }
    
    const data = await response.json();
    console.log("[generalChat] Received response:", data);
    
    return data;
  } catch (error) {
    console.error("[generalChat] Network error:", error);
    throw error;
  }
}

// Force rebuild
export const VERSION = "1.0.0";