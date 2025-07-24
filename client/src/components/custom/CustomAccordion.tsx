interface CustomAccordionProps {

    children: React.ReactNode
    title: string
    open?: boolean
}

const CustomAccordion = ({ children, title, open = true }: CustomAccordionProps) => {
    return (
        <details open={open}>
            <summary className="border border-gray-200/20 bg-white/5 rounded-md p-2 w-full mb-2 text-sm cursor-pointer">
                {title}
            </summary>
            <div className="p-4">
                {children}
            </div>
        </details>
    )
}

export default CustomAccordion