<template>
  <div
    v-if="modalStore.visible"
    class="z-10 transition ease-in-out delay-300 duration-500 px-6 py-6 fixed bottom-8 right-8 rounded-xl shadow-xl border-gray-200 text-white"
    :class="modalStore.classes"
  >
    {{ modalStore.message }}
  </div>
</template>

<script setup>
import { useModalStore } from "@/stores/modal";

const modalStore = useModalStore();
</script>
