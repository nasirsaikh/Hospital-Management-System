import { useToastStore } from "@/store/toast";

export function useToast() {
  const toast = useToastStore();

  return {
    success: toast.success,
    error: toast.error,
    info: toast.info,
  };
}
