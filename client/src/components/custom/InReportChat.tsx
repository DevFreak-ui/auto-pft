import { IconMessageChatbot, IconX } from "@tabler/icons-react";
import ChatBox from "./ChatBox"

interface InReportChatProps {
    report_id: string
}

const InReportChat = ({ report_id }: InReportChatProps) => {
    return (
        <div className="h-full relative">
            <div className="flex justify-between items-center text-muted-foreground dark:bg-white/10 rounded-t-md py-2 px-3">
                <h1 className="text-sm font-semibold">Chat</h1>
                <span className="p-1.5 cursor-pointer">
                    <IconX size={17} />
                </span>
            </div>

            <div className="px-3 p-5 h-full relative">

                <div className="flex flex-col justify-center items-center h-[69%]">
                    <IconMessageChatbot size={50} className="text-green/60" />
                    <h1 className="text-muted-foreground">
                        Ask me <span className="underline text-green/60 font-semibold">anything</span> about this report
                    </h1>
                </div>

                <ChatBox type="mini" report={report_id}/>
            
            </div>
        </div>
    )
}

export default InReportChat;