import { IconSend, IconSparkles } from "@tabler/icons-react"
import PageLayout from "./PageContainer"

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
                <div className="sticky bottom-0 left-0 w-full z-10">
                    <div className="flex flex-col w-full gap-0">
                        <div className="flex align-self-end bg-white/5 border-2 border-green/10 rounded-[8px] p-4 w-full h-32 min-w-54">
                            <textarea 
                                rows={8}
                                className="w-full h-full flex justify-start text-start outline-none border-none bg-transparent resize-none placeholder:text-white/30"
                                placeholder="Set a report as context or start a new chat ..." 
                            />
                            <div className="bg-white/8 text-white/30 rounded-sm p-2 cursor-pointer max-h-10">
                                <IconSend />
                            </div>
                        </div>
                        <div className="block bg-white/3 text-white/50 border-x border-b rounded-b-[8px] border-green/10 text-xs p-2 mx-5">
                            Context Report ID: P2345 - Name: Prince Mireku - Generated at: 12/07/2025
                        </div>
                    </div>
                </div>

            </div>

        </PageLayout>
    )
}

export default ChatBotPage