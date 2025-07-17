
import { IconChecks, IconEmergencyBed } from "@tabler/icons-react"

interface ReportProgressStepperProps {
    step?: 1 | 2 | 3
}

const ReportProgressStepper = ({ step = 1 }: ReportProgressStepperProps) => {

    const stagesData = {
        1: {"title": "Our Data Specialist will analyze your data to extract the relevant information"},
        2: {"title": "Stage Two"},
        3: {"title": "Stage Three"},
    }

    return (
        <div className="flex flex-col items-center justify-center mt-20">
            <h1 className="text-4xl font-bold dark:text-white/70">Sit tight, we're generating your report</h1>

                <ol className="flex items-center justify-center w-3/5 mt-18">
                    {/* Stage 1 */}
                    <li className={`flex w-full items-center after:content-[''] after:w-full after:h-1 after:border-b after:border-6 after:inline-block ${step > 1 ? 'after:border-green dark:after:border-green' : 'after:border-blue-100 dark:after:border-green/50'} text-blue-600 dark:text-blue-500`}>
                        <span className={`relative flex items-center justify-center w-14 h-14 rounded-full lg:h-14 lg:w-14 shrink-0 border-2 ${step > 1 ? 'bg-green border-green' : step === 1 ? 'bg-[#121418]/80 border-blue-600 dark:bg-green/10' : 'bg-gray-200 border-gray-300 dark:bg-green/10'}`}>
                            <div className={`flex items-center justify-center w-12 h-12 rounded-full ${step > 1 ? 'bg-green' : step === 1 ? 'bg-green' : 'bg-gray-300'}`}>
                                <IconChecks className={`w-8 h-8 ${step > 1 ? 'text-background' : step === 1 ? 'text-background' : 'text-gray-400'}`} />
                            </div>
                            <div className="absolute text-sm dark:text-green -bottom-24 left-1/2 -translate-x-1/2 w-44 ml-8">
                                <p className="text-sm text-muted-foreground/40">
                                    {stagesData[1].title}
                                </p>
                            </div>
                        </span>
                    </li>
                    {/* Stage 2 */}
                    <li className={`flex w-full items-center after:content-[''] after:w-full after:h-1 after:border-b after:border-6 after:inline-block ${step > 2 ? 'after:border-green dark:after:border-green' : 'after:border-gray-100 dark:after:border-[#222b30]'}`}>
                        <span className={`relative flex items-center justify-center w-14 h-14 rounded-full lg:h-14 lg:w-14 shrink-0 border-2 ${step > 2 ? 'bg-green border-green' : step === 2 ? 'bg-blue-100 border-blue-600 dark:bg-green/10' : 'bg-gray-200 border-gray-300 dark:bg-green/10'}`}>
                            <div className={`flex items-center justify-center w-12 h-12 rounded-full ${step > 2 ? 'bg-green' : step === 2 ? 'bg-green/80 animate-ping' : 'bg-gray-300'}`}></div>
                            <IconEmergencyBed className={`absolute w-6 h-6 ${step >= 2 ? 'text-green/80' : 'text-gray-400'}`} />
                            <div className="absolute text-sm dark:text-green -bottom-24 left-1/2 -translate-x-1/2 w-44 ml-12">
                                <p className="text-sm text-muted-foreground/40">
                                    {stagesData[2].title}
                                </p>
                            </div>
                        </span>
                    </li>
                    {/* Stage 3 */}
                    <li className="flex items-center">
                        <span className={`flex items-center justify-center w-14 h-14 rounded-full lg:h-14 lg:w-14 shrink-0 border-2 ${step === 3 ? 'bg-blue-100 border-blue-600 dark:bg-green/10' : step > 3 ? 'bg-green border-green' : 'bg-gray-200 border-gray-300 dark:bg-green/10'}`}> 
                            <div className={`w-12 h-12 rounded-full ${step === 3 ? 'bg-green/80 animate-ping' : step > 3 ? 'bg-green' : 'bg-gray-300'}`}></div>
                        </span>
                    </li>
                </ol>

        </div>
    )

}

export default ReportProgressStepper;