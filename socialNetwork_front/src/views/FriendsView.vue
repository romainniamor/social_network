<template>
  <div class="max-w-7xl mx-auto grid grid-cols-5 gap-4">
    <div class="main-left col-span-1">
      <div
        class="p-4 bg-white border border-gray-200 flex-col justify items-center rounded-lg"
      >
        <img :src="user.get_avatar" class="mb-6 rounded-full" />
        <div class="flex items-center justify-center gap-2">
          <p>
            <strong>{{ user.name }}</strong>
          </p>
        </div>
      </div>
    </div>

    <div
      class="main-center bg-white border-gray-200 rounded-lg p-4 col-span-3 space-y-4 flex-col"
    >
      <div
        v-if="friendsRequests.length"
        v-for="friendRequest in friendsRequests"
        :key="friendRequest.id"
        class="p-4 text-center bg-gray-100 rounded-lg flex items-center gap-6"
      >
        <img
          :src="friendRequest.created_by.get_avatar"
          class="rounded-full w-[40px]"
        />

        <RouterLink
          :to="{ name: 'profile', params: { id: friendRequest.created_by.id } }"
        >
          <strong>{{ friendRequest.created_by.name }}</strong>
        </RouterLink>

        <div class="flex space-x-4 justify-around">
          <p class="text-xs text-gray-500">
            {{ friendRequest.created_by.friends_counter }} friends
          </p>
          <p class="text-xs text-gray-500">
            {{ friendRequest.created_by.posts_counter }} posts
          </p>
        </div>
        <div v-if="visible" class="flex-1 space-x-4 justify-right">
          <button
            @click="handleRequest('accepted', friendRequest.created_by.id)"
            class="text-s bg-sky-500 rounded-lg text-white px-4 py-2"
          >
            Accept
          </button>
          <button
            @click="handleRequest('declined', friendRequest.created_by.id)"
            class="text-s border-2 border-sky-500 rounded-lg text-sky-500 px-4 py-2"
          >
            Decline
          </button>
        </div>
      </div>

      <div
        v-if="friends.length"
        v-for="user in friends"
        :key="user.id"
        class="p-4 text-center bg-gray-100 rounded-lg flex items-center gap-6"
      >
        <img :src="user.get_avatar" class="rounded-full w-[40px]" />

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

    <div class="main-right col-span-1 space-y-4">
      <People />
      <Trends />
    </div>
  </div>
</template>

<script setup>
import People from "../components/People.vue";
import Trends from "../components/Trends.vue";
import PostedPost from "@/components/PostedPost.vue";
import axios from "axios";
import { ref, onMounted, watch } from "vue";
import { useUserStore } from "@/stores/user";
import { useModalStore } from "@/stores/modal";

import { useRouter } from "vue-router";

const posts = ref([]);
const userStore = useUserStore();
const modal = useModalStore();

const route = useRouter();
const user = ref({});
const friends = ref([]);
const friendsRequests = ref([]);
const visible = ref(true);

onMounted(() => {
  getFriends();
});

async function getFriends() {
  axios
    .get(`/api/friends/${route.currentRoute.value.params.id}/`)
    .then((response) => {
      friendsRequests.value = response.data.requests;
      friends.value = response.data.friends;
      user.value = response.data.user;
      console.log("response get friends:", response.data);
    })
    .catch((error) => {
      console.error("error get mes friends: ", error);
    });
}

async function handleRequest(status, pk) {
  console.log("handle request", status);
  axios
    .post(`/api/friends/${pk}/${status}/`)
    .then((response) => {
      console.log("response post handlerequest friends:", response.data);
      if (response.data.message === "friends updated") {
        modal.showModal(5000, "New friend added", "bg-green-300");
        visible.value = false;
      }
    })
    .catch((error) => {
      console.error("error post handlerequest friends: ", error);
    });
}
</script>
