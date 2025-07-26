import { IconSend } from "@tabler/icons-react"
import { shortenReportId } from "@/herlpers"

interface ChatBoxProp {
    type?: "mini" | "max"
    report?: string
}

const ChatBox = ({type, report}: ChatBoxProp) => {

    const repport_id = report !== undefined ? shortenReportId(report) : undefined;

    return (
        <div className={`stickybottom-0  left-0 w-full z-10`}>
            <div className="flex flex-col w-full gap-0">
                <div className={`flex align-self-end bg-white/5 border-2 border-green/10 rounded-[8px] p-4 w-full min-w-54 ${type === "mini" ? 'h-28' : 'h-32'}`}>
                    <textarea 
                        rows={3}
                        className="w-full h-full flex justify-start text-start outline-none border-none bg-transparent resize-none placeholder:text-white/30"
                        placeholder="Set a report as context or start a new chat ..." 
                    />
                    <div className="bg-white/8 text-white/30 rounded-sm p-2 cursor-pointer max-h-10">
                        <IconSend />
                    </div>
                </div>
                
                <div className="block bg-white/3 text-white/50 border-x border-b rounded-b-[8px] border-green/10 text-xs p-1 mx-5 text-center">
                    Context Report ID: {repport_id} - Name: Prince Mireku
                </div>
            </div>
        </div>
    )
}

export default ChatBox