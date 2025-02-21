
import * as React from "react";
import { cn } from "@/lib/utils";
import {
  Card as BaseCard,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Link } from "react-router-dom";

// Omit the title property from HTMLAttributes to avoid conflict
interface CustomCardProps extends Omit<React.HTMLAttributes<HTMLDivElement>, 'title'> {
  title: React.ReactNode;
  description?: string;
  pronunciation?: string;
  to?: string;
  footer?: React.ReactNode;
  children?: React.ReactNode;
}

export const CustomCard = ({
  title,
  description,
  pronunciation,
  to,
  footer,
  className,
  children,
  ...props
}: CustomCardProps) => {
  const CardWrapper = to ? Link : React.Fragment;
  const wrapperProps = to ? { to, className: "block h-full" } : {};

  return (
    <CardWrapper {...wrapperProps}>
      <BaseCard
        className={cn(
          // Base styles
          "relative transition-all duration-300 ease-in-out h-full",
          // Light mode
          "bg-white text-black",
          "hover:shadow-[0_8px_16px_-6px_rgba(0,0,0,0.2),0_8px_24px_-12px_rgba(0,0,0,0.15)]",
          "hover:-translate-y-1",
          // Dark mode
          "dark:bg-gradient-to-br dark:from-gray-900 dark:to-gray-800",
          "dark:text-white dark:border-gray-700",
          "dark:hover:shadow-[0_0_20px_rgba(255,255,255,0.1)]",
          "dark:hover:border-gray-600",
          // Gamification elements in dark mode
          "dark:after:absolute dark:after:inset-0",
          "dark:after:rounded-lg dark:after:bg-gradient-to-tr",
          "dark:after:from-purple-500/5 dark:after:via-transparent dark:after:to-orange-500/5",
          "dark:after:opacity-0 dark:hover:after:opacity-100",
          "dark:after:transition-opacity dark:after:duration-500",
          className
        )}
        {...props}
      >
        <CardHeader className="flex-grow-0">
          <CardTitle 
            className={cn(
              "text-2xl font-bold tracking-tight",
              "transition-colors duration-300",
              "hover:text-primary",
              "dark:text-white dark:hover:text-primary"
            )}
          >
            {title}
          </CardTitle>
          {description && (
            <CardDescription 
              className={cn(
                "text-gray-700",
                "transition-colors duration-300",
                "group-hover:text-primary/80",
                "dark:text-gray-300 dark:group-hover:text-primary/80"
              )}
            >
              {description}
            </CardDescription>
          )}
        </CardHeader>
        {children && <CardContent className="flex-grow">{children}</CardContent>}
        {footer && <CardFooter>{footer}</CardFooter>}
      </BaseCard>
    </CardWrapper>
  );
};
