import { IconX } from "@tabler/icons-react";

interface InReportChatProps {
    report_id: any
}

const InReportChat = ({ report_id }: InReportChatProps) => {
    return (
        <div>
            <div className="flex justify-between items-center text-muted-foreground dark:bg-white/10 rounded-t-md py-2 px-3">
                <h1 className="text-sm font-semibold">Chat</h1>
                <span className="p-1.5 cursor-pointer">
                    <IconX size={17} />
                </span>
            </div>
            <div className="text-[10px] text-white p-1 border border-white/10 my-2 m-3 font-semibold rounded-md">
                <p>Context: <span className="text-muted-foreground">{report_id}</span></p>
            </div>

            <div className="px-3 p-5">
                Main Content
            </div>
        </div>
    )
}

export default InReportChat;