<template>
  <div class="p-4 bg-white border border-gray-200 rounded-lg">
    <h3 class="mb-6 text-xl">Trends of the day</h3>

    <div class="space-y-4">
      <div
        v-for="trend in trends"
        :key="trend.id"
        class="flex items-center justify-between"
      >
        <p class="text-xs">
          <strong>#{{ trend.hashtag }}</strong
          ><br />
          <span class="text-gray-500">{{ trend.occurence }} posts</span>
        </p>

        <RouterLink
          :to="{ name: 'trend', params: { id: trend.hashtag } }"
          class="py-2 px-3 bg-sky-500 text-white text-xs rounded-lg"
          >View</RouterLink
        >
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { RouterLink } from "vue-router";

let trends = ref([]);

onMounted(() => {
  getTrends();
});

async function getTrends() {
  console.log("getting trends");
  await axios
    .get("api/posts/trends/")
    .then((response) => {
      console.log("response data get trends:", response.data);
      trends.value = response.data;
    })
    .catch((error) => {
      console.log("error get trends:", error);
    });
}
</script>
