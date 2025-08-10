import PageLayout from "./PageContainer"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { useReportSettings } from "@/hooks/useReportSettings"
import { toast } from "sonner"

const Settings = () => {
    const {
        settings,
        toggleSection,
        isSectionEnabled,
        resetToDefaults,
        enableAllSections,
        disableAllSections,
        sections
    } = useReportSettings();

    const [saving, setSaving] = useState(false);

    const handleSavePreferences = async () => {
        setSaving(true);
        try {
            // Simulate saving (settings are already saved automatically via the hook)
            await new Promise(resolve => setTimeout(resolve, 500));
            toast.success("Report preferences saved successfully!");
        } catch (error) {
            toast.error("Failed to save preferences");
        } finally {
            setSaving(false);
        }
    };

    const handleResetToDefaults = () => {
        resetToDefaults();
        toast.success("Reset to default preferences");
    };

    const handleEnableAll = () => {
        enableAllSections();
        toast.success("All sections enabled");
    };

    const handleDisableAll = () => {
        disableAllSections();
        toast.success("All sections disabled");
    };

    // Split sections into two columns
    const leftColumn = sections.slice(0, Math.ceil(sections.length / 2));
    const rightColumn = sections.slice(Math.ceil(sections.length / 2));

    return (
        <PageLayout>
            <div className="w-3/5 mx-auto">
                <Card className="bg-transparent border-none">
                    <CardHeader>
                        <CardTitle>
                            <h1 className="text-lg font-semibold">Include(s) in Finalized Report</h1>
                            <p className="text-sm text-muted-foreground mt-1">
                                Select which sections to include in your PDF reports
                            </p>
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="grid gap-6 text-muted-foreground">
                        {/* Action buttons */}
                        <div className="flex gap-2 flex-wrap">
                            <Button 
                                variant="outline" 
                                size="sm" 
                                onClick={handleEnableAll}
                                className="text-xs"
                            >
                                Enable All
                            </Button>
                            <Button 
                                variant="outline" 
                                size="sm" 
                                onClick={handleDisableAll}
                                className="text-xs"
                            >
                                Disable All
                            </Button>
                            <Button 
                                variant="outline" 
                                size="sm" 
                                onClick={handleResetToDefaults}
                                className="text-xs"
                            >
                                Reset to Defaults
                            </Button>
                        </div>

                        {/* Two-column layout for checkboxes */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            {/* Left Column */}
                            <div className="space-y-4">
                                {leftColumn.map((section) => (
                                    <div key={section.id} className="flex items-start gap-3">
                                        <Checkbox 
                                            id={section.id}
                                            checked={isSectionEnabled(section.id)}
                                            onCheckedChange={() => toggleSection(section.id)}
                                            className="mt-1"
                                        />
                                        <div className="grid gap-1">
                                            <Label 
                                                htmlFor={section.id} 
                                                className="text-sm font-medium cursor-pointer"
                                            >
                                                {section.label}
                                            </Label>
                                            <p className="text-xs text-muted-foreground">
                                                {section.description}
                                            </p>
                                        </div>
                                    </div>
                                ))}
                            </div>

                            {/* Right Column */}
                            <div className="space-y-4">
                                {rightColumn.map((section) => (
                                    <div key={section.id} className="flex items-start gap-3">
                                        <Checkbox 
                                            id={section.id}
                                            checked={isSectionEnabled(section.id)}
                                            onCheckedChange={() => toggleSection(section.id)}
                                            className="mt-1"
                                        />
                                        <div className="grid gap-1">
                                            <Label 
                                                htmlFor={section.id} 
                                                className="text-sm font-medium cursor-pointer"
                                            >
                                                {section.label}
                                            </Label>
                                            <p className="text-xs text-muted-foreground">
                                                {section.description}
                                            </p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Summary */}
                        <div className="pt-4 border-t border-gray-400/10">
                            <p className="text-sm text-muted-foreground">
                                <span className="font-medium">
                                    {settings.enabledSections.length} of {sections.length}
                                </span> sections will be included in your PDF reports
                            </p>
                        </div>
                    </CardContent>

                    <CardFooter className="mt-6 flex justify-end">
                        <Button 
                            className="cursor-pointer"
                            onClick={handleSavePreferences}
                            disabled={saving}
                        >
                            {saving ? "Saving..." : "Save preferences"}
                        </Button>
                    </CardFooter>
                </Card>
            </div>
        </PageLayout>
    )
}

export default Settings