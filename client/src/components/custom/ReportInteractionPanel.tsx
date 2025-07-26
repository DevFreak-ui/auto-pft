import { IconMessageChatbot, IconX, IconEyeDotted, IconMessage } from "@tabler/icons-react";
import { useState } from "react";
import ChatBox from "./ChatBox";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";

interface ReportInteractionPanelProps {
    report_id: string;
}

const ReportInteractionPanel = ({ report_id }: ReportInteractionPanelProps) => {
    const [activeTab, setActiveTab] = useState("chat");
    
    // Review form state
    const [reviewer, setReviewer] = useState("");
    const [approvalStatus, setApprovalStatus] = useState("");
    const [reviewComments, setReviewComments] = useState("");
    
    // Feedback form state
    const [feedback, setFeedback] = useState("");
    
    const reviewStatus = [
        "Approved",
        "Need Changes",
        "Rejected"
    ];

    const handleReviewSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        console.log("[ReportInteractionPanel] Submitting review:", {
            report_id,
            reviewer,
            approvalStatus,
            reviewComments
        });
        // TODO: Implement review submission
    };

    const handleFeedbackSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        console.log("[ReportInteractionPanel] Submitting feedback:", {
            report_id,
            feedback
        });
        // TODO: Implement feedback submission
    };

    return (
        <div className="h-full flex flex-col w-full overflow-x-hidden">
            {/* Header */}
            <div className="flex justify-between items-center text-muted-foreground dark:bg-white/10 rounded-t-md py-2 px-3">
                <h1 className="text-sm font-semibold">Report Interaction</h1>
                <span className="p-1.5 cursor-pointer">
                    <IconX size={17} />
                </span>
            </div>

            {/* Tabs */}
            <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col px-2">
                <TabsList className="grid w-full grid-cols-3 mt-2">
                    <TabsTrigger value="chat" className="flex items-center gap-1">
                        <IconMessageChatbot size={14} />
                        Chat
                    </TabsTrigger>
                    <TabsTrigger value="review" className="flex items-center gap-1">
                        <IconEyeDotted size={14} />
                        Review
                    </TabsTrigger>
                    <TabsTrigger value="feedback" className="flex items-center gap-1">
                        <IconMessage size={14} />
                        Feedback
                    </TabsTrigger>
                </TabsList>

                {/* Chat Tab */}
                <TabsContent value="chat" className="flex-1 flex flex-col mt-2">
                    <ChatBox type="mini" report_id={report_id} />
                </TabsContent>

                {/* Review Tab */}
                <TabsContent value="review" className="flex-1 flex flex-col mt-2 p-3">
                    <div className="flex-1 overflow-y-auto">
                        <form onSubmit={handleReviewSubmit} className="flex flex-col gap-4">
                            <div className="flex flex-col gap-2">
                                <Label htmlFor="reviewer" className="text-sm">Reviewer</Label>
                                <Input 
                                    id="reviewer" 
                                    placeholder="Enter your name" 
                                    value={reviewer}
                                    onChange={(e) => setReviewer(e.target.value)}
                                    className="text-sm"
                                />
                            </div>
                            
                            <div className="flex flex-col gap-2">
                                <Label htmlFor="status" className="text-sm">Approval Status</Label>
                                <Select value={approvalStatus} onValueChange={setApprovalStatus}>
                                    <SelectTrigger className="w-full text-sm">
                                        <SelectValue placeholder="Select an option" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectGroup>
                                            <SelectLabel>Choose</SelectLabel>
                                            {reviewStatus.map((item, index) => (
                                                <SelectItem value={item} key={index}>
                                                    {item}
                                                </SelectItem>
                                            ))}
                                        </SelectGroup>
                                    </SelectContent>
                                </Select>
                            </div>
                            
                            <div className="flex flex-col gap-2">
                                <Label htmlFor="comments" className="text-sm">Comments</Label>
                                <Textarea 
                                    id="comments" 
                                    placeholder="Add comments (optional)" 
                                    value={reviewComments}
                                    onChange={(e) => setReviewComments(e.target.value)}
                                    className="text-sm min-h-[100px]"
                                />
                            </div>
                            
                            <div className="flex gap-2 mt-auto">
                                <Button type="submit" className="flex-1 text-sm">
                                    Submit Review
                                </Button>
                            </div>
                        </form>
                    </div>
                </TabsContent>

                {/* Feedback Tab */}
                <TabsContent value="feedback" className="flex-1 flex flex-col mt-2 p-3">
                    <div className="flex-1 overflow-y-auto">
                        <form onSubmit={handleFeedbackSubmit} className="flex flex-col gap-4 h-full">
                            <div className="flex flex-col gap-2">
                                <Label htmlFor="feedback" className="text-sm">Feedback</Label>
                                <Textarea 
                                    placeholder="Type your message here." 
                                    id="feedback"
                                    value={feedback}
                                    onChange={(e) => setFeedback(e.target.value)}
                                    className="text-sm flex-1 min-h-[200px]"
                                />
                                <p className="text-muted-foreground text-xs">
                                    Your feedback will be used as guidance by our Agent.
                                </p>
                            </div>
                            
                            <div className="flex gap-2 mt-auto">
                                <Button type="submit" className="flex-1 text-sm">
                                    Send Feedback
                                </Button>
                            </div>
                        </form>
                    </div>
                </TabsContent>
            </Tabs>
        </div>
    );
};

export default ReportInteractionPanel; 