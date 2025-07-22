import PageLayout from "./PageContainer"

const PricePage = () => {
    return (
        <PageLayout>
           
            <div className="space-y-4 text-center">
                <h1 className="text-4xl font-medium">
                    Subscribe
                </h1>
                <p>Generate Unlimited Report when you are on PRO!</p>
            </div>

            <div className="mx-auto flex w-fit rounded-full bg-[#F3F4F6] p-1 dark:bg-[#222] my-6">
                <button className="relative w-fit px-4 py-2 text-sm font-semibold capitalize text-foreground transition-colors">
                    <span className="relative z-10">monthly</span>
                    <span className="absolute inset-0 z-0 rounded-full bg-background shadow-sm"></span>
                </button>
                <button className="relative w-fit px-4 py-2 text-sm font-semibold capitalize text-foreground transition-colors flex items-center justify-center gap-2.5">
                    <span className="relative z-10">yearly</span>
                    <div className="inline-flex items-center rounded-md border px-2.5 py-0.5 font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent relative z-10 whitespace-nowrap text-xs text-black shadow-none bg-gray-300 hover:bg-gray-300">Save 35%</div>
                </button>
            </div>

            {/* OPTIONS */}
            <div className="flex justify-center items-center w-3/5 gap-5 mx-auto">
                <div className="w-64 relative flex flex-col gap-8 overflow-hidden rounded-2xl border p-6 shadow bg-background text-foreground">
                    <h2 className="flex items-center gap-3 text-xl font-medium capitalize">Free</h2>
                    <div className="relative h-12 flex">
                        <h1 className="text-4xl font-medium">$0</h1>
                        <small className="align-bottom">.00</small>
                    </div>
                    <div className="flex-1 space-y-2">
                        <h3 className="text-sm font-medium">For your hobby projects</h3>
                        <ul className="space-y-2">
                            <li className="flex items-center gap-2 text-sm font-medium text-foreground/60">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" className="lucide lucide-badge-check">
                                    <path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"></path>
                                    <path d="m9 12 2 2 4-4"></path>
                                </svg>
                                Free email alerts
                            </li>
                            <li className="flex items-center gap-2 text-sm font-medium text-foreground/60">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" className="lucide lucide-badge-check">
                                    <path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"></path>
                                    <path d="m9 12 2 2 4-4"></path>
                                </svg>
                                3-minute checks
                            </li>
                            <li className="flex items-center gap-2 text-sm font-medium text-foreground/60">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" className="lucide lucide-badge-check">
                                <path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"></path>
                                <path d="m9 12 2 2 4-4"></path></svg>Automatic data enrichment</li>
                            <li className="flex items-center gap-2 text-sm font-medium text-foreground/60">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" className="lucide lucide-badge-check">
                                    <path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"></path>
                                    <path d="m9 12 2 2 4-4"></path>
                                </svg>
                                10 monitors
                            </li>
                            <li className="flex items-center gap-2 text-sm font-medium text-foreground/60">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" className="lucide lucide-badge-check">
                                    <path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"></path>
                                    <path d="m9 12 2 2 4-4"></path>
                                </svg>
                                Up to 3 seats
                            </li>
                        </ul>
                    </div>
                    <button 
                        disabled
                        className="inline-flex items-center justify-center whitespace-nowrap text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 group relative text-foreground border border-white/15 px-4 py-2 h-fit w-full rounded-lg">
                        free
                        <div className="w-0 translate-x-[100%] pl-0 opacity-0 transition-all duration-200 *:size-4 group-hover:w-5 group-hover:translate-x-0 group-hover:pl-2 group-hover:opacity-100">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" className="lucide lucide-arrow-right">
                                <path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path>
                            </svg>
                        </div>
                    </button>
                </div>

                <div className="w-64 relative flex flex-col gap-8 overflow-hidden rounded-2xl border p-6 shadow bg-background text-foreground outline outline-[rgba(120,119,198)]">
                    <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.1),rgba(255,255,255,0))] dark:bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.3),rgba(255,255,255,0))]"></div>
                    <h2 className="flex items-center gap-3 text-xl font-medium capitalize">Pro
                        <div className="inline-flex items-center rounded-md border text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent shadow mt-1 bg-orange-900 px-1 py-0 text-white hover:bg-orange-900">🔥 Recommended</div>
                    </h2>
                    <div className="relative h-12">
                        <span className="text-4xl font-medium">$90</span>
                        <p className="-mt-2 text-xs font-medium">Per month/user</p>
                    </div>
                    <div className="flex-1 space-y-2">
                        <h3 className="text-sm font-medium">Great for small businesses</h3>
                        <ul className="space-y-2">
                            <li className="flex items-center gap-2 text-sm font-medium text-foreground/60">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-badge-check"><path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"></path><path d="m9 12 2 2 4-4"></path></svg>Unlimited phone calls
                            </li>
                            <li className="flex items-center gap-2 text-sm font-medium text-foreground/60">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-badge-check"><path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"></path><path d="m9 12 2 2 4-4"></path></svg>30 second checks
                            </li>
                            <li className="flex items-center gap-2 text-sm font-medium text-foreground/60">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-badge-check"><path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"></path><path d="m9 12 2 2 4-4"></path></svg>Single-user account
                            </li>
                            <li className="flex items-center gap-2 text-sm font-medium text-foreground/60">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-badge-check"><path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"></path><path d="m9 12 2 2 4-4"></path></svg>20 monitors
                            </li>
                            <li className="flex items-center gap-2 text-sm font-medium text-foreground/60">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-badge-check"><path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"></path><path d="m9 12 2 2 4-4"></path></svg>Up to 6 seats
                            </li>
                        </ul>
                    </div>
                    <button className="inline-flex items-center justify-center whitespace-nowrap text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 group relative text-primary-foreground bg-primary hover:bg-primary/90 px-4 py-2 h-fit w-full rounded-lg">
                        Get started
                        <div className="w-0 translate-x-[100%] pl-0 opacity-0 transition-all duration-200 *:size-4 group-hover:w-5 group-hover:translate-x-0 group-hover:pl-2 group-hover:opacity-100">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-arrow-right">
                                <path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path>
                            </svg>
                        </div>
                    </button>
                </div>
            </div>

        </PageLayout>
    )
}

export default PricePage