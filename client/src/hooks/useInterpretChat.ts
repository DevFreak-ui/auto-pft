import { useState, useCallback } from 'react';
import { explainReport } from '@/services/interpretReport';

// Interface for chat messages
export interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
}

// Interface for the hook parameters
export interface UseInterpretChatProps {
  report_id?: string;
}

/**
 * Custom hook for managing report interpretation chat
 * Handles sending messages, receiving responses, and managing chat state
 */
export function useInterpretChat({ report_id }: UseInterpretChatProps) {
    console.log("[useInterpretChat] Hook initialized with report_id:", report_id);
    
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

  /**
   * Send a message to the interpretation API
   * @param text - The user's question/message
   */
  const sendMessage = useCallback(async (text: string) => {
    if (!report_id) {
      console.error("[useInterpretChat] No report_id provided");
      setError("No report context available");
      return;
    }

    if (!text.trim()) {
      console.warn("[useInterpretChat] Empty message, ignoring");
      return;
    }

    console.log("[useInterpretChat] Sending message:", { report_id, text });

    // Add user message to chat
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      text: text.trim(),
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setLoading(true);
    setError(null);

    try {
      // Call the interpretation API
      const response = await explainReport(report_id, text.trim());
      
      console.log("[useInterpretChat] Received response:", response);

             // Add assistant response to chat
       const assistantMessage: ChatMessage = {
         id: (Date.now() + 1).toString(),
         text: response.answer || response.response || "No response received",
         sender: 'assistant',
         timestamp: new Date(),
       };

      setMessages(prev => [...prev, assistantMessage]);
      
    } catch (err: any) {
      console.error("[useInterpretChat] Error sending message:", err);
      
      // Add error message to chat
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        text: `Error: ${err.message || 'Failed to get response'}`,
        sender: 'assistant',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
      setError(err.message || 'Failed to get response');
    } finally {
      setLoading(false);
    }
  }, [report_id]);

  /**
   * Clear all chat messages
   */
  const clearMessages = useCallback(() => {
    console.log("[useInterpretChat] Clearing messages");
    setMessages([]);
    setError(null);
  }, []);

  /**
   * Get the last message in the chat
   */
  const getLastMessage = useCallback(() => {
    return messages[messages.length - 1];
  }, [messages]);

  return {
    messages,
    loading,
    error,
    sendMessage,
    clearMessages,
    getLastMessage,
  };
} 