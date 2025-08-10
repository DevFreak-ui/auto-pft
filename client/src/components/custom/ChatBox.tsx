import { IconMessageChatbot, IconSend } from "@tabler/icons-react"
import { shortenReportId } from "@/herlpers"
import { useInterpretChat } from "@/hooks/useInterpretChat"
import { useState } from "react"

interface ChatBoxProp {
    type?: "mini" | "max"
    report_id?: string
}

const ChatBox = ({type, report_id}: ChatBoxProp) => {
    console.log("[ChatBox] Component mounted with report_id:", report_id);
    
    const repport_id = report_id !== undefined ? shortenReportId(report_id) : undefined;
    
    // Initialize the chat hook with the report_id
    const { messages, sendMessage, loading, error } = useInterpretChat({ report_id });
    const [input, setInput] = useState("");

    // Handle sending a message
    const handleSend = async () => {
        if (!input.trim() || loading) return;
        
        console.log("[ChatBox] Sending message:", input);
        await sendMessage(input);
        setInput(""); // Clear input after sending
    };

    // Handle Enter key press
    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="h-full flex flex-col" style={{maxHeight: "calc(100vh - 200px)"}}>
            {/* Chat messages area - takes up all remaining space */}
            <div className="flex-1 flex flex-col gap-2 overflow-y-auto p-2">
                {/* Welcome message - only show if no messages yet */}
                {type !== "max" && messages.length === 0 && !loading && (
                    <div className="flex flex-col justify-center items-center h-full">
                        <IconMessageChatbot size={50} className="text-green/60" />
                        <h1 className="text-muted-foreground text-center mt-2">
                            Ask me <span className="underline text-green/60 font-semibold">anything</span> about this report
                        </h1>
                    </div>
                )}
                
                {/* Chat messages */}
                {messages.map((msg) => (
                    <div
                        key={msg.id}
                        className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
                    >
                        <div
                            className={`max-w-[80%] rounded-lg px-3 py-2 text-[12px] text-white/80 ${
                                msg.sender === "user"
                                    ? "bg-white/10 text-white"
                                    : "bg-transparent text-white"
                            }`}
                        >
                            {msg.text}
                        </div>
                    </div>
                ))}
                
                {/* Loading indicator */}
                {loading && (
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

            {/* Fixed bottom section - input area and context */}
            <div className="flex flex-col p-2 w-100 justify-center items-center">
                {/* Input area */}
                <div className={`flex align-self-end bg-white/5 border-2 border-green/10 rounded-[8px] p-4 ${type === "mini" ? 'w-full h-28' : 'w-[150%] h-32'}`}>
                    <textarea 
                        rows={3}
                        className="w-full h-full flex justify-start text-start outline-none border-none bg-transparent resize-none placeholder:text-white/30"
                        placeholder={"Start a new chat ..."}
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        disabled={loading}
                    />
                    <div 
                        className={`bg-white/8 text-white/30 rounded-sm p-2 cursor-pointer max-h-10 flex items-center justify-center ${
                            loading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-white/12'
                        }`}
                        onClick={handleSend}
                    >
                        <IconSend />
                    </div>
                </div>
                
                {/* Context information */}
                {type === "mini" && (
                    <div className="block bg-white/3 text-white/50 border-x border-b rounded-b-[8px] border-green/10 text-xs p-1 mx-5 text-center">
                        Context Report ID: {repport_id || 'None'}
                    </div>
                )}
            </div>
        </div>
    )
}

export default ChatBox