import { Skeleton } from "@/components/ui/skeleton"
import PageLayout from "./PageContainer"

const Dashboard = () => {
    return (
        <PageLayout>

            {/* Content */}
            <div className="p-4 lg:p-6 my-6">
                <div className="flex flex-col lg:flex-row gap-4 p-4">
                    <Skeleton className="h-[125px] w-[250px] rounded-xl grid auto-rows-min gap-4 md:grid-cols-3" />
                    <Skeleton className="h-[125px] w-[250px] rounded-xl grid auto-rows-min gap-4 md:grid-cols-3" />
                    <Skeleton className="h-[125px] w-[250px] rounded-xl grid auto-rows-min gap-4 md:grid-cols-3" />
                    <Skeleton className="h-[125px] w-[250px] rounded-xl grid auto-rows-min gap-4 md:grid-cols-3" />
                </div>
            </div>

        </PageLayout>
    )
}


export default Dashboard