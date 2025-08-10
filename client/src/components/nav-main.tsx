import { IconPencilStar, type Icon } from "@tabler/icons-react"
import { BsStars } from "react-icons/bs";
import { Link } from "react-router-dom";

import { Button } from "@/components/ui/button"
import {
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"

export function NavMain({
  items,
}: {
  items: {
    title: string
    url: string
    icon?: Icon
    isFutureFeature?: boolean
  }[]
}) {
  return (
    <SidebarGroup>
      <SidebarGroupContent className="flex flex-col gap-2">
        <SidebarMenu>
          <Link to="/">
            <SidebarMenuItem className="flex items-center gap-2">
              <SidebarMenuButton
                tooltip="Generate PFT Report"
                className="bg-primary text-primary-foreground hover:bg-primary/90 hover:text-primary-foreground active:bg-primary/90 active:text-primary-foreground min-w-8 h-10 duration-200 ease-linear cursor-pointer"
              >
                <BsStars />
                <span>Generate PFT Report</span>
              </SidebarMenuButton>
              <Button
                size="icon"
                className="size-10 group-data-[collapsible=icon]:opacity-0"
                variant="outline"
              >
                <IconPencilStar />
                <span className="sr-only">Inbox</span>
              </Button>
            </SidebarMenuItem>
          </Link>
        </SidebarMenu>
        <SidebarMenu>
          {items.map((item) => (
            <Link to={item.url} key={item.title}>
              <SidebarMenuItem>
                <SidebarMenuButton tooltip={item.title} className="cursor-pointer">
                  {item.icon && <item.icon />}
                  <span>{item.title}</span>
                  {item.isFutureFeature && (
                    <span className="ml-auto text-[10px] bg-blue-100/50 text-blue-800 dark:bg-orange-500/10 dark:border dark:border-orange-500/50 dark:text-blue-200 px-2 py-1 rounded-full">
                      Coming Soon
                    </span>
                  )}
                </SidebarMenuButton>
              </SidebarMenuItem>
            </Link>
          ))}
        </SidebarMenu>
      </SidebarGroupContent>
    </SidebarGroup>
  )
}
