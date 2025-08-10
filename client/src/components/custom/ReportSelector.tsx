import { useState } from 'react';
import { ChevronDown } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { useGeneratedReports } from '@/hooks/useGetReport';
import { shortenReportId, formatReportDate } from '@/herlpers';

interface ReportSelectorProps {
  selectedReportId: string | null;
  onReportSelect: (reportId: string | null) => void;
}

export default function ReportSelector({ selectedReportId, onReportSelect }: ReportSelectorProps) {
  const { reports, loading } = useGeneratedReports();
  const [open, setOpen] = useState(false);

  const handleSelectReport = (reportId: string | null) => {
    onReportSelect(reportId);
    setOpen(false);
  };

  const selectedReport = reports.find(report => report.id === selectedReportId);

  return (
    <div className="flex flex-col gap-2">
      <label className="text-sm font-medium text-muted-foreground">
        Select Report Context (Optional)
      </label>
      <DropdownMenu open={open} onOpenChange={setOpen}>
        <DropdownMenuTrigger asChild>
          <Button 
            variant="outline" 
            className="w-full justify-between text-left"
            disabled={loading}
          >
            {loading ? (
              'Loading reports...'
            ) : selectedReport ? (
              <div className="flex flex-col items-start">
                <span className="font-medium">
                  {shortenReportId(selectedReport.id)}
                </span>
                <span className="text-xs text-muted-foreground">
                  {formatReportDate(selectedReport.generated_at)}
                </span>
              </div>
            ) : (
              'No report selected'
            )}
            <ChevronDown className="ml-2 h-4 w-4" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className="w-full min-w-[300px]" align="start">
          <DropdownMenuItem onClick={() => handleSelectReport(null)}>
            <div className="flex flex-col items-start">
              <span className="font-medium">No Report Context</span>
              <span className="text-xs text-muted-foreground">
                General medical questions
              </span>
            </div>
          </DropdownMenuItem>
          {reports.length > 0 && (
            <>
              <DropdownMenuItem disabled className="text-xs text-muted-foreground px-2 py-1">
                ──────────────────
              </DropdownMenuItem>
              {reports.map((report) => (
                <DropdownMenuItem 
                  key={report.id} 
                  onClick={() => handleSelectReport(report.id)}
                  className="flex flex-col items-start"
                >
                  <div className="flex flex-col items-start">
                    <span className="font-medium">
                      {shortenReportId(report.id)}
                    </span>
                    <span className="text-xs text-muted-foreground">
                      {formatReportDate(report.generated_at)} • {report.severity}
                    </span>
                  </div>
                </DropdownMenuItem>
              ))}
            </>
          )}
          {reports.length === 0 && !loading && (
            <DropdownMenuItem disabled className="text-muted-foreground">
              No reports available
            </DropdownMenuItem>
          )}
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}
