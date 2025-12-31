import { defineStore } from "pinia";

export const useToastStore = defineStore("toast", {
  state: () => ({
    toasts: []
  }),

  actions: {
    show(message, type = "info", duration = 3000) {
      const id = Date.now();

      this.toasts.push({ id, message, type });

      setTimeout(() => {
        this.remove(id);
      }, duration);
    },

    success(msg) {
      this.show(msg, "success");
    },

    error(msg) {
      this.show(msg, "error");
    },

    info(msg) {
      this.show(msg, "info");
    },

    remove(id) {
      this.toasts = this.toasts.filter((t) => t.id !== id);
    }
  }
});
