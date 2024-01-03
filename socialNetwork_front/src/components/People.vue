<template>
  <div class="p-4 bg-white border border-gray-200 rounded-lg">
    <h3 class="mb-6 text-xl">People you may know</h3>

    <div v-for="user in users" :key="user.id" class="space-y-4 col">
      <RouterLink
        :to="{ name: 'profile', params: { id: user.id } }"
        class="flex items-center justify-between my-2"
      >
        <div class="flex items-center space-x-2">
          <img :src="user.get_avatar" class="w-[30px] rounded-full" />

          <p class="text-xs">
            <strong>{{ user.name }}</strong>
          </p>
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { RouterLink } from "vue-router";

const users = ref([]);

onMounted(() => {
  getSuggestions();
});

async function getSuggestions() {
  console.log("getting suggestions friends");
  await axios
    .get("api/friends/suggested/")
    .then((response) => {
      console.log("response data get suggestions:", response.data);
      users.value = response.data;
    })
    .catch((error) => {
      console.log("error get suggestions:", error);
    });
}
</script>
