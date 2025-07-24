import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { 
    DrawerContent, 
    DrawerHeader, 
    DrawerTitle, 
    DrawerDescription, 
    DrawerFooter, 
    DrawerClose 
} from "@/components/ui/drawer"
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"

const CustomDrawerContent = () => {

    const reviewStatus = [
        "Approved",
        "Need Changes",
        "Rejected"
    ]

    return (
        <DrawerContent>
            <DrawerHeader>
                <DrawerTitle>Review & Approve Report</DrawerTitle>
                <DrawerDescription>Review the report, approve, or leave feedback.</DrawerDescription>
            </DrawerHeader>
            <Tabs defaultValue="review" className="flex flex-col gap-4 px-4">
                <TabsList>
                    <TabsTrigger value="review">Review & Approve</TabsTrigger>
                    <TabsTrigger value="feedback">Feedback</TabsTrigger>
                </TabsList>
                <TabsContent value="review" className="!py-4">
                    <form className="flex flex-col gap-4">
                        <div className="flex flex-col gap-2">
                            <Label htmlFor="reviewer">Reviewer</Label>
                            <Input id="reviewer" placeholder="Enter your name" />
                        </div>
                        <div className="flex flex-col gap-2">
                            <Label htmlFor="status">Approval Status</Label>
                            <Select>
                                <SelectTrigger className="w-full">
                                    <SelectValue placeholder="Select an option" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectGroup>
                                    <SelectLabel>Choose</SelectLabel>
                                    {reviewStatus.map((item, index) => (
                                        <SelectItem value={item} key={index}> {item} </SelectItem>
                                    ))}
                                    </SelectGroup>
                                </SelectContent>
                            </Select>
                        </div>
                        <div className="flex flex-col gap-2">
                            <Label htmlFor="comments">Comments</Label>
                            <Input id="comments" placeholder="Add comments (optional)" />
                        </div>
                        <DrawerFooter>
                            <Button type="submit">Submit Review</Button>
                            <DrawerClose asChild>
                                <Button variant="outline" type="button">Cancel</Button>
                            </DrawerClose>
                        </DrawerFooter>
                    </form>
                </TabsContent>
                <TabsContent value="feedback" className="py-4">
                    <form className="flex flex-col gap-4">
                        <div className="flex flex-col gap-2">
                            <Label htmlFor="feedback">Feedback</Label>
                            <Textarea placeholder="Type your message here." id="message-2" />
                            <p className="text-muted-foreground text-sm">
                                Your feedback will be used as guidance by our Agent.
                            </p>
                        </div>
                        <DrawerFooter>
                            <Button type="submit">Send Feedback</Button>
                            <DrawerClose asChild>
                                <Button variant="outline" type="button">Cancel</Button>
                            </DrawerClose>
                        </DrawerFooter>
                    </form>
                </TabsContent>
            </Tabs>
        </DrawerContent>
    )
}

export default CustomDrawerContent