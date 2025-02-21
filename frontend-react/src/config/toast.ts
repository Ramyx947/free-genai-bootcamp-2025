
import { ToastProps } from "@/components/ui/toast";

export const TOAST_DURATION = 5000; // 5 seconds

type ToastVariant = "default" | "destructive";

export const toastConfig: Partial<ToastProps> = {
  duration: TOAST_DURATION,
  className: "group toast"
};

export const getSuccessToast = (title: string, description?: string) => ({
  ...toastConfig,
  variant: "default" as ToastVariant,
  title,
  description,
});

export const getErrorToast = (title: string, description?: string) => ({
  ...toastConfig,
  variant: "destructive" as ToastVariant,
  title,
  description,
});
