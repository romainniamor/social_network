<template>
  <nav class="py-5 px-7 border-b border-gray-200">
    <div>
      <div class="flex items-center justify-between">
        <div class="menu-left font-light">
          <Logo></Logo>
        </div>

        <div
          v-if="userStore.user.isAuthenticated"
          class="menu-right flex space-x-6 items-center"
        >
          <RouterLink to="/" class="text-sky-500">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="item w-6 h-6"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25"
              />
            </svg>
          </RouterLink>

          <RouterLink to="/chat">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="item w-6 h-6"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M8.625 9.75a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375m-13.5 3.01c0 1.6 1.123 2.994 2.707 3.227 1.087.16 2.185.283 3.293.369V21l4.184-4.183a1.14 1.14 0 01.778-.332 48.294 48.294 0 005.83-.498c1.585-.233 2.708-1.626 2.708-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z"
              ></path>
            </svg>
          </RouterLink>

          <RouterLink to="/search">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="item w-6 h-6"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"
              ></path>
            </svg>
          </RouterLink>
          <RouterLink
            :to="{ name: 'friends', params: { id: userStore.user.id } }"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="w-6 h-6"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"
              />
            </svg>
          </RouterLink>
          <RouterLink
            :to="{ name: 'profile', params: { id: userStore.user.id } }"
          >
            <img
              :src="userStore.user.avatar"
              class="item rounded-full w-[40px] h-[40px] object-cover"
            />
          </RouterLink>
        </div>
        <template v-else>
          <div class="menu-right flex space-x-4 items-center text-white">
            <RouterLink
              to="/signup/"
              class="inline-block py-4 px-6 bg-cyan-700 text-white rounded-lg"
              >Sign Up</RouterLink
            >
            <RouterLink
              to="/login/"
              class="inline-block py-4 px-6 bg-sky-500 text-white rounded-lg"
              >Log In</RouterLink
            >
          </div>
        </template>
      </div>
    </div>
  </nav>
  <main class="py-5 px-7 bg-gray-100 flex-grow"><RouterView /></main>
  <Modal></Modal>
</template>

<script>
import { RouterLink, RouterView } from "vue-router";
import { useUserStore } from "@/stores/user";
import Modal from "@/components/Modal.vue";
import Logo from "@/components/Logo.vue";
import axios from "axios";

export default {
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },

  components: {
    Modal,
    Logo,
  },

  beforeCreate() {
    console.log("before create call");
    try {
      this.userStore.initStore();
      const token = this.userStore.user.access;
      const id = this.userStore.user.id;
      console.log("token:", token);
      console.log("id:", id);
      if (id === "") {
        console.log("probleme id perdu");
      }

      if (token) {
        axios.defaults.headers.common["Authorization"] = "Bearer " + token;
      } else {
        axios.defaults.headers.common["Authorization"] = "";
      }
    } catch (error) {
      console.log("erreur before Create", error);
    }
  },
};
</script>

<style scoped>
.item {
  transition: transform 0.2s ease-in;
}

.item:hover {
  transform: rotate(4deg) scale(1.2);
}
</style>
