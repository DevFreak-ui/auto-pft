
import { IconArrowRight, IconChecks, IconEmergencyBed, IconFileDescription } from "@tabler/icons-react"
import { Button } from "@/components/ui/button"

interface ReportProgressStepperProps {
    step?: 1 | 2 | 3
    canViewReport?: boolean
    onViewReportClick?: () => void
}

const ReportProgressStepper = ({ step = 1, canViewReport = false, onViewReportClick }: ReportProgressStepperProps) => {

    const stagesData = {
        1: {"title": "Extracting data from your uploaded document"},
        2: {"title": "Analyzing the extracted data"},
        3: {"title": "Generating your report"},
    }

    return (
        <div className="flex flex-col items-center justify-center mt-20">
            <h1 className="text-3xl font-bold dark:text-white/90">Sit tight, we're generating your report</h1>

            <ol className="flex items-center justify-center w-3/5 mt-18">
                {/* Stage 1 */}
                <li className={`flex w-full items-center after:content-[''] after:w-full after:h-1 after:border-b after:border-6 after:inline-block ${step > 1 ? 'after:border-green dark:after:border-green' : 'after:border-blue-100 dark:after:border-green/50'} text-blue-600 dark:text-blue-500`}>
                    <span className={`relative flex items-center justify-center w-14 h-14 rounded-full lg:h-14 lg:w-14 shrink-0 border-2 ${step > 1 ? 'border-green' : step === 1 ? 'bg-[#121418]/80 border-green dark:bg-green/10' : 'bg-gray-200 border-gray-300 dark:bg-green/10'}`}>
                        <div className={`relative flex items-center justify-center w-12 h-12 rounded-full ${step > 1 ? 'bg-green' : step === 1 ? 'bg-green/5' : 'bg-gray-300'}`}>
                            {step === 1 && (
                                <span className="absolute size-12 bg-green/80 rounded-full animate-ping"></span>
                            )}

                            {step === 1 ? (
                                <LoadingBubble />
                            ) : (
                                <IconChecks className={`w-8 h-8 text-background`} />
                            )}
                        </div>
                        <div className="absolute text-sm dark:text-green -bottom-24 left-1/2 -translate-x-1/2 w-44 ml-8">
                            <p className={`text-sm ${step === 1 ? 'text-muted-foreground' : ' text-muted-foreground/40'}`}>
                                {stagesData[1].title}
                            </p>
                        </div>
                    </span>
                </li>
                {/* Stage 2 */}
                <li className={`flex w-full items-center after:content-[''] after:w-full after:h-1 after:border-b after:border-6 after:inline-block ${step > 2 ? 'after:border-green dark:after:border-green' : 'after:border-gray-100 dark:after:border-[#222b30]'}`}>
                    <span className={`relative flex items-center justify-center w-14 h-14 rounded-full lg:h-14 lg:w-14 shrink-0 border-2 ${step > 2 ? 'border-green' : step === 2 ? 'bg-blue-100 border-green dark:bg-green/10' : 'bg-gray-200/30 border-gray-300/30 dark:bg-green/10'}`}>
                        <div className={`flex items-center justify-center w-12 h-12 rounded-full ${step > 2 ? 'bg-green' : step === 2 ? 'bg-green/80 animate-ping' : 'bg-gray-700/10'}`}></div>
                        {step === 2 ? (
                            <IconEmergencyBed className="absolute w-6 h-6 text-green animate-bounce"/>
                        ) : step >= 2 ? (
                            <IconChecks className={`absolute w-8 h-8 text-background`} />
                        ) : (
                            <IconEmergencyBed className="absolute w-6 h-6 text-white/10"/>
                        )}
                        <div className="absolute text-sm dark:text-green -bottom-24 left-1/2 -translate-x-1/2 w-44 ml-12">
                            <p className={`text-sm ${step === 2 ? 'text-muted-foreground' : ' text-muted-foreground/40'}`}>
                                {stagesData[2].title}
                            </p>
                        </div>
                    </span>
                </li>
                {/* Stage 3 */}
                <li className="flex items-center">
                    <span className={`relative flex items-center justify-center w-14 h-14 rounded-full lg:h-14 lg:w-14 shrink-0 border-2 ${step === 3 ? 'bg-blue-100 border-green dark:bg-green/10' : step > 3 ? 'bg-green border-green' : 'bg-gray-200/30 border-gray-300/30 dark:bg-green/10'}`}> 
                        <div className={`w-12 h-12 rounded-full ${step === 3 ? 'bg-green/80 animate-ping' : step > 3 ? 'bg-green' : 'bg-gray-700/20'}`}></div>
                        
                        {step === 3 ? (
                            <IconFileDescription className="absolute w-6 h-6 text-green animate-bounce"/>
                        ) : step >= 3 ? (
                            <IconChecks className={`absolute w-8 h-8 text-background`} />
                        ) : (
                            <IconFileDescription className="absolute w-6 h-6 text-white/10"/>
                        )}

                        <div className="absolute text-sm dark:text-green -bottom-24 left-1/2 -translate-x-1/2 w-44 ml-12">
                            <p className={`text-sm ${step === 3 ? 'text-muted-foreground' : ' text-muted-foreground/40'}`}>
                                {stagesData[3].title}
                            </p>
                        </div>
                    </span>
                </li>
            </ol>
            {/* Only show the View Report button when canViewReport is true */}
            {canViewReport && (
              <div className="flex justify-center w-3/5 mt-44">
                  <Button variant="outline" className="flex gap-3 cursor-pointer" onClick={onViewReportClick}>
                      <span>View Report</span>
                      <IconArrowRight />
                  </Button>
              </div>
            )}
        </div>
    )

}

const LoadingBubble = () => {
    return (
        <div className="flex justify-center items-center space-x-2 bg-green/5">
            <div className="w-2 h-2 bg-green/60 rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-green/60 rounded-full animate-bounce delay-100"></div>
            <div className="w-2 h-2 bg-green/60 rounded-full animate-bounce delay-200"></div>
        </div>
    )
}

export default ReportProgressStepper;