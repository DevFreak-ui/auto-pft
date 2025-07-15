import AppRoutes from "@/routes"
import { BrowserRouter } from "react-router-dom"
import { ThemeProvider } from "@/components/theme-provider"

const App = () => {
    return (
        <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
            <BrowserRouter>
                <AppRoutes />
            </BrowserRouter>
        </ThemeProvider>
    )
}

export default App