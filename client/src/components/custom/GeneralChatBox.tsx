import { IconMessageChatbot, IconSend, IconRefresh } from "@tabler/icons-react"
import { useGeneralChat } from "@/hooks/useGeneralChat"
import { useState, useEffect, useCallback } from "react"

interface GeneralChatBoxProp {
    type?: "mini" | "max"
    reportId?: string | null
    onMessageSent?: () => void
    hasMessages?: boolean
    onResetChat?: () => void
}

const GeneralChatBox = ({type, reportId, onMessageSent, hasMessages, onResetChat}: GeneralChatBoxProp) => {
    console.log("[GeneralChatBox] Component rendering with type:", type, "reportId:", reportId);
    
    // Initialize the general chat hook
    const { messages, sendMessage, isLoading, error, clearMessages, clearError, setReportContext } = useGeneralChat();
    const [input, setInput] = useState("");

    // Set report context when reportId changes
    useEffect(() => {
        if (reportId !== undefined) {
            setReportContext(reportId);
        }
    }, [reportId, setReportContext]);

    // Handle sending a message
    const handleSend = async () => {
        if (!input.trim() || isLoading) return;
        
        console.log("[GeneralChatBox] Sending message:", input);
        await sendMessage(input);
        setInput(""); // Clear input after sending
        
        // Notify parent that a message was sent
        if (onMessageSent) {
            onMessageSent();
        }
    };

    // Handle Enter key press
    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    // Handle clearing chat and resetting state
    const handleClearChat = () => {
        clearMessages();
        if (onResetChat) {
            onResetChat();
        }
    };

    return (
        <div className="h-full flex flex-col" style={{maxHeight: "calc(100vh - 200px)"}}>
            {/* Chat messages area - takes up all remaining space */}
            <div className="flex-1 flex flex-col gap-2 overflow-y-auto p-2">
                {/* Report context indicator - show when report is selected */}
                {type === "max" && reportId && (
                    <div className="flex justify-center mb-4">
                        <div className="bg-green/10 border border-green/30 rounded-lg px-3 py-2 text-sm text-green/80">
                            📋 Report Context: {reportId.slice(0, 8)}...
                        </div>
                    </div>
                )}

                {/* Clear chat button - show when there are messages */}
                {type === "max" && hasMessages && messages.length > 0 && (
                    <div className="flex justify-center mb-4">
                        <button 
                            onClick={handleClearChat}
                            className="bg-white/10 hover:bg-white/20 text-white/80 hover:text-white rounded-lg px-4 py-2 text-sm transition-colors flex items-center gap-2"
                        >
                            <IconRefresh size={16} />
                            Clear Chat & Start Over
                        </button>
                    </div>
                )}
                
                {/* Welcome message - only show if no messages yet */}
                {!hasMessages && messages.length === 0 && !isLoading && (
                    <div className="flex flex-col justify-center items-center h-full">
                        <IconMessageChatbot size={50} className="text-green/60" />
                        <h1 className="text-muted-foreground text-center mt-2">
                            {reportId ? (
                                <>
                                    Ask me about the <span className="underline text-green/60 font-semibold">selected report</span>
                                </>
                            ) : (
                                <>
                                    Ask me <span className="underline text-green/60 font-semibold">anything</span> about medical topics
                                </>
                            )}
                        </h1>
                    </div>
                )}
                
                {/* Chat messages */}
                {messages.map((msg) => (
                    <div
                        key={msg.id}
                        className={`flex ${msg.isUser ? "justify-end" : "justify-start"}`}
                    >
                        <div
                            className={`max-w-[80%] rounded-lg px-3 py-2 text-[12px] text-white/80 ${
                                msg.isUser
                                    ? "bg-white/10 text-white"
                                    : "bg-transparent text-white"
                            }`}
                        >
                            {msg.text}
                        </div>
                    </div>
                ))}
                
                {/* Loading indicator */}
                {isLoading && (
                    <div className="flex justify-start">
                        <div className="bg-transparent text-white/60 rounded-lg px-3 py-2 text-sm">
                            <div className="flex items-center gap-2">
                                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                                Thinking...
                            </div>
                        </div>
                    </div>
                )}
                
                {/* Error display */}
                {error && (
                    <div className="flex justify-start">
                        <div className="bg-red-500/20 text-red-400 rounded-lg px-3 py-2 text-sm">
                            {error}
                        </div>
                    </div>
                )}
            </div>

            {/* Fixed bottom section - input area and controls */}
            <div className="flex flex-col p-2 w-full justify-center items-center">
                {/* Input area */}
                <div className={`flex bg-white/5 border-2 border-green/10 rounded-[8px] p-4 ${type === "mini" ? 'w-full h-28' : 'w-full max-w-2xl h-32'}`}>
                    <textarea 
                        rows={3}
                        className="w-full h-full flex justify-start text-start outline-none border-none bg-transparent resize-none placeholder:text-white/30"
                        placeholder={reportId ? "Ask me about the selected report..." : "Ask me anything about medical topics..."}
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        disabled={isLoading}
                    />
                    <div 
                        className={`bg-white/8 text-white/30 rounded-sm p-2 cursor-pointer max-h-10 flex items-center justify-center ${
                            isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-white/12'
                        }`}
                        onClick={handleSend}
                    >
                        <IconSend />
                    </div>
                </div>
                
                {/* Controls */}
                {type === "mini" && (
                    <div className="flex justify-between items-center bg-white/3 text-white/50 border-x border-b rounded-b-[8px] border-green/10 text-xs p-2 mx-5">
                        <span>
                            {reportId ? `Report Context: ${reportId.slice(0, 8)}...` : "General Medical Chat"}
                        </span>
                        <button 
                            onClick={handleClearChat}
                            className="flex items-center gap-1 hover:text-white/80 transition-colors"
                            title="Clear chat messages"
                        >
                            <IconRefresh size={12} />
                            Clear
                        </button>
                    </div>
                )}
            </div>
        </div>
    )
}

export default GeneralChatBox
