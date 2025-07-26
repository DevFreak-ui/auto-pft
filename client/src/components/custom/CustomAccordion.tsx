interface CustomAccordionProps {

    children: React.ReactNode
    title: string
    open?: boolean
}

const CustomAccordion = ({ children, title, open = true }: CustomAccordionProps) => {
    return (
        <div>
            <h1 className="border-b border-gray-500/50 text-2xl text-white font-bold  p-2 w-full mb-2 cursor-pointer">
                {title}
            </h1>
            <div className="p-4">
                {children}
            </div>
        </div>
    )
}

export default CustomAccordion