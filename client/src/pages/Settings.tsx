import PageLayout from "./PageContainer"

import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Checkbox } from "@/components/ui/checkbox"

const Settings = () => {
    return (
        <PageLayout>

            <div className="w-3/5 mx-auto">
                <Card className="bg-transparent border-none">
                    <CardHeader>
                        <CardTitle>General</CardTitle>
                        {/* <CardDescription>Manage your cookie settings here.</CardDescription> */}
                    </CardHeader>
                    <CardContent className="grid gap-6 text-muted-foreground">
                        <div className="flex items-center justify-between gap-4">
                        <Label htmlFor="necessary" className="flex flex-col items-start">
                            <span>Strictly Necessary</span>
                            <span className="leading-snug font-normal">
                            These cookies are essential in order to use the website and use
                            its features.
                            </span>
                        </Label>
                        <Switch id="necessary" defaultChecked aria-label="Necessary" />
                        </div>
                        <div className="flex items-center justify-between gap-4">
                        <Label htmlFor="functional" className="flex flex-col items-start">
                            <span>Functional Cookies</span>
                            <span className="text-muted-foreground leading-snug font-normal">
                            These cookies allow the website to provide personalized
                            functionality.
                            </span>
                        </Label>
                        <Switch id="functional" aria-label="Functional" />
                        </div>
                    </CardContent>


                    <CardHeader className="border-t border-gray-400/10 pt-8">
                        <CardTitle>
                            Report Visible Options
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="grid gap-6 text-muted-foreground">
                        <div className="flex flex-col gap-6">
                            <div className="flex items-center gap-3">
                                <Checkbox id="terms" />
                                <Label htmlFor="terms">Accept terms and conditions</Label>
                            </div>
                            <div className="flex items-start gap-3">
                                <Checkbox id="terms-2" defaultChecked />
                                <div className="grid gap-2">
                                <Label htmlFor="terms-2">Accept terms and conditions</Label>
                                <p className="text-muted-foreground text-sm">
                                    By clicking this checkbox, you agree to the terms and conditions.
                                </p>
                                </div>
                            </div>
                            <div className="flex items-start gap-3">
                                <Checkbox id="toggle" disabled />
                                <Label htmlFor="toggle">Enable notifications</Label>
                            </div>
                            <Label className="hover:bg-accent/50 flex items-start gap-3 rounded-lg border p-3 has-[[aria-checked=true]]:border-blue-600 has-[[aria-checked=true]]:bg-blue-50 dark:has-[[aria-checked=true]]:border-blue-900 dark:has-[[aria-checked=true]]:bg-blue-950">
                                <Checkbox
                                id="toggle-2"
                                defaultChecked
                                className="data-[state=checked]:border-blue-600 data-[state=checked]:bg-blue-600 data-[state=checked]:text-white dark:data-[state=checked]:border-blue-700 dark:data-[state=checked]:bg-blue-700"
                                />
                                <div className="grid gap-1.5 font-normal">
                                <p className="text-sm leading-none font-medium">
                                    Enable notifications
                                </p>
                                <p className="text-muted-foreground text-sm">
                                    You can enable or disable notifications at any time.
                                </p>
                                </div>
                            </Label>
                        </div>
                    </CardContent>

                    <CardHeader className="border-t border-gray-400/10 pt-8">
                        <CardTitle>
                            Include(s) in Finalized Report
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="grid gap-3 text-muted-foreground">
                        <div className="flex items-center gap-3">
                            <Checkbox id="terms" />
                            <Label htmlFor="terms">A</Label>
                        </div>
                        <div className="flex items-center gap-3">
                            <Checkbox id="terms" />
                            <Label htmlFor="terms">B</Label>
                        </div>
                        <div className="flex items-center gap-3">
                            <Checkbox id="terms" />
                            <Label htmlFor="terms">C</Label>
                        </div>
                        <div className="flex items-center gap-3">
                            <Checkbox id="terms" />
                            <Label htmlFor="terms">D</Label>
                        </div>
                        <div className="flex items-center gap-3">
                            <Checkbox id="terms" />
                            <Label htmlFor="terms">E</Label>
                        </div>
                    </CardContent>


                    <CardFooter className="mt-6 flex justify-end">
                        <Button className="cursor-pointer">
                            Save preferences
                        </Button>
                    </CardFooter>
                </Card>
            </div>

        </PageLayout>
    )
}

export default Settings