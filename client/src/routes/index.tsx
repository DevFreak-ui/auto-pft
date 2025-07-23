import { Route, Routes } from "react-router-dom"
import Dashboard from "@/pages/Dashboard"
import GenerateReportPage from "@/pages/GenerateReportPage"
import NotFound from "@/pages/NotFound"
import Reports from "@/pages/Reports"
import Settings from "@/pages/Settings"
import ChatBotPage from "@/pages/ChatBotPage"
import PricePage from "@/pages/Prices"
import ReportDetails from "@/pages/ReportDetails"

const AppRoutes = () => {

    return (
        <Routes>
            <Route index element={<GenerateReportPage />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/chatbot" element={<ChatBotPage />} />
            <Route path="/prices" element={<PricePage />} />
            <Route path="/report-details/:reportId" element={<ReportDetails />} />
            
            <Route path="*" element={<NotFound />} />
        </Routes>
    )
}

export default AppRoutes