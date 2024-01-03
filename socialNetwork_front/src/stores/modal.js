import { ref, computed } from "vue";
import { defineStore } from "pinia";

export const useModalStore = defineStore({
  id: "modal",

  state: () => ({
    ms: 0,
    message: "",
    classes: "",
    visible: false,
  }),

  actions: {
    showModal(ms, message, classes) {
      this.ms = parseInt(ms);
      this.message = message;
      this.classes = classes;
      this.visible = true;

      setTimeout(() => {
        this.classes += " -translate-y-2";
      });

      setTimeout(() => {
        this.classes = this.classes.replace("-translate-y-28", "");
      }, this.ms);

      setTimeout(() => {
        this.visible = false;
      }, this.ms);
    },
  },
});
