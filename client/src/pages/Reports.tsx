
import PageLayout from "./PageContainer"
import data from "@/data/data.json"
import { DataTable } from "@/components/data-table"

const Reports = () => {
    return (
        <PageLayout>
           
           <DataTable data={data} />

        </PageLayout>
    )
}

export default Reports