import { useState, useCallback, useEffect } from 'react';
import { sendGeneralChat } from '@/services/generalChat';
import type { ChatResponse } from '@/services/generalChat';

export interface GeneralChatMessage {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
}

export const useGeneralChat = () => {
  const [messages, setMessages] = useState<GeneralChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [reportId, setReportId] = useState<string | null>(null);

  // Generate default user ID and session ID if not provided
  const getDefaultUserId = useCallback(() => {
    let userId = localStorage.getItem('chat_user_id');
    if (!userId) {
      userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem('chat_user_id', userId);
    }
    return userId;
  }, []);

  const getDefaultSessionId = useCallback(() => {
    let sessionId = localStorage.getItem('chat_session_id');
    if (!sessionId) {
      sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem('chat_session_id', sessionId);
    }
    return sessionId;
  }, []);

  const setReportContext = useCallback((id: string | null) => {
    console.log("[useGeneralChat] Setting report context:", id);
    setReportId(id);
  }, []);

  const sendMessage = useCallback(async (text: string) => {
    if (!text.trim()) return;

    const userId = getDefaultUserId();
    const sessionId = getDefaultSessionId();

    // Add user message to chat
    const userMessage: GeneralChatMessage = {
      id: `user_${Date.now()}`,
      text: text.trim(),
      isUser: true,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      console.log("[useGeneralChat] Sending message:", { text, userId, sessionId, reportId });
      const response: ChatResponse = await sendGeneralChat(text.trim(), userId, sessionId, reportId || undefined);
      
      // Add bot response to chat
      const botMessage: GeneralChatMessage = {
        id: `bot_${Date.now()}`,
        text: response.response,
        isUser: false,
        timestamp: new Date(response.timestamp),
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMessage);
      console.error('[useGeneralChat] Error sending message:', err);
    } finally {
      setIsLoading(false);
    }
  }, [reportId, getDefaultUserId, getDefaultSessionId]);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    clearMessages,
    clearError,
    setReportContext,
    reportId,
  };
};
