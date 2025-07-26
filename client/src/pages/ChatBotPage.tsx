import { IconSparkles } from "@tabler/icons-react"
import PageLayout from "./PageContainer"
import ChatBox from "@/components/custom/ChatBox"

const ChatBotPage = () => {
    return (
        <PageLayout>

            <div className="flex flex-col items-center justify-center mt-8 w-3/5 mx-auto px-4 min-h-[80vh]">

                {/* Header */}
                <div className="text-center">
                    <IconSparkles className="w-full flex justify-center mb-4" />
                    <h1 className="text-4xl text-green/80 font-bold my-2">Transparency Builds Trust</h1>
                    <p className="max-w-4/5 mx-auto text-muted-foreground text-sm">
                        Understand why/how our Agent arrived at a particular conclusion or their chain of reasoning behind the reults
                    </p>
                </div>
                
                {/* Action Cards */}
                <div className="flex gap-3 text-sm text-white/80 font-normal mt-10">
                    <div className="bg-white/5 border-2 border-green/10 rounded-[8px] p-4 max-w-52 h-auto cursor-pointer">
                        Ask a general medical question
                    </div>
                    <div className="bg-green/10 border-2 border-green/30 rounded-[8px] p-4 text-sm max-w-52 cursor-pointer">
                        Curios about the results in a report? Start asking questions specific to a generated report!
                    </div>
                </div>

                {/* Spacer to push chat input to bottom */}
                <div className="flex-1" />

                {/* Chat Input - sticky bottom */}
                <ChatBox />

            </div>

        </PageLayout>
    )
}

export default ChatBotPage