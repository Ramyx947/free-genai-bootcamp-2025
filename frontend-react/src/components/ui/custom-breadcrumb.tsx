
import * as React from "react";
import { Link, useLocation } from "react-router-dom";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { ChevronLeft } from "lucide-react";

export interface BreadcrumbItem {
  label: string;
  path?: string;
  state?: Record<string, any>;
}

interface CustomBreadcrumbProps {
  items: BreadcrumbItem[];
}

export const CustomBreadcrumb = ({ items }: CustomBreadcrumbProps) => {
  const location = useLocation();

  return (
    <Breadcrumb>
      <BreadcrumbList>
        {items.map((item, index) => (
          <React.Fragment key={index}>
            <BreadcrumbItem>
              {index === 0 ? (
                <BreadcrumbLink asChild>
                  <Link 
                    to={item.path!} 
                    state={item.state || location.state}
                    className="flex items-center"
                  >
                    <ChevronLeft className="h-4 w-4 mr-1" />
                    {item.label}
                  </Link>
                </BreadcrumbLink>
              ) : index === items.length - 1 ? (
                <BreadcrumbPage>{item.label}</BreadcrumbPage>
              ) : (
                <BreadcrumbLink asChild>
                  <Link 
                    to={item.path!}
                    state={item.state || location.state}
                  >
                    {item.label}
                  </Link>
                </BreadcrumbLink>
              )}
            </BreadcrumbItem>
            {index < items.length - 1 && <BreadcrumbSeparator />}
          </React.Fragment>
        ))}
      </BreadcrumbList>
    </Breadcrumb>
  );
};
