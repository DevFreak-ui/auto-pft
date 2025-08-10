interface CustomAccordionProps {

    children: React.ReactNode
    title: string
    open?: boolean
}

const CustomAccordion = ({ children, title, open = true }: CustomAccordionProps) => {
    return (
        <div>
            <h1 className="border-b border-gray-500/30 text-2xl text-white/80 font-bold  p-2 w-full mb-2 cursor-pointer">
                {title}
            </h1>
            <div className="p-4">
                {children}
            </div>
        </div>
    )
}

export default CustomAccordion