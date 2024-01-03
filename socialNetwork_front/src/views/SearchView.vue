<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-3 space-y-4">
      <div class="bg-white border border-gray-200 rounded-lg">
        <form @submit.prevent="submitForm" class="p-4 flex space-x-4">
          <input
            v-model="query"
            type="search"
            class="p-4 w-full bg-gray-100 rounded-lg outline-blue-600"
            placeholder="Who are you looking for?"
          />

          <button
            class="inline-block py-4 px-6 bg-sky-500 text-white rounded-lg"
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
                d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"
              ></path>
            </svg>
          </button>
        </form>
      </div>

      <div
        class="p-4 bg-white border border-gray-200 rounded-lg flex-col space-y-4"
      >
        <div
          v-for="user in users"
          :key="user.id"
          class="p-4 text-center bg-gray-100 rounded-lg flex items-center gap-6"
        >
          <img :src="user.get_avatar" class="w-[70px] h-[70px] rounded-full" />

          <RouterLink :to="{ name: 'profile', params: { id: user.id } }">
            <strong>{{ user.name }}</strong>
          </RouterLink>

          <div class="flex space-x-4 justify-around">
            <p class="text-xs text-gray-500">
              {{ user.friends_counter }} friends
            </p>
            <p class="text-xs text-gray-500">{{ user.posts_counter }} posts</p>
          </div>
        </div>
      </div>

      <div v-for="post in posts" :key="post.id">
        <PostedPost :post="post"></PostedPost>
      </div>
    </div>

    <div class="main-right col-span-1 space-y-4">
      <People />
      <Trends />
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
import People from "@/components/People.vue";
import Trends from "@/components/Trends.vue";
import PostedPost from "@/components/PostedPost.vue";
import axios from "axios";
import { useUserStore } from "@/stores/user";

import { onMounted, ref } from "vue";

let query = ref("");
let users = ref([]);
let posts = ref([]);

const userStore = useUserStore();

async function submitForm() {
  console.log("submitting form", query.value);
  await axios
    .post("api/search/", {
      query: query.value,
    })
    .then((response) => {
      console.log("response", response.data);
      users = response.data.user;
      posts = response.data.posts;
      query.value = "";
    })
    .catch((error) => {
      console.log("error post query to back", error);
    });
}
</script>
