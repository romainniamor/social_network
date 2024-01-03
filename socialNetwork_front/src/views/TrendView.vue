<template>
  <div class="max-w-5xl mx-auto grid grid-cols-3 gap-4">
    <div class="main-center col-span-2 space-y-4">
      <div v-for="post in posts" :key="post.id">
        <PostedPost :post="post" />
      </div>
    </div>

    <div class="main-right col-span-1 space-y-4">
      <People />
      <Trends />
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted, watch } from "vue";
import People from "@/components/People.vue";
import Trends from "@/components/Trends.vue";
import PostedPost from "@/components/PostedPost.vue";

import { useRouter } from "vue-router";

const posts = ref([]);

const route = useRouter();

onMounted(() => {
  getPosts();
});

//IMPORTANT. Sans le watch le trend ne se met pas a jour dans trendview.
watch(
  () => route.currentRoute.value.params.id,
  (newVal, oldVal) => {
    getPosts();
  },
  { deep: true, immediate: true }
);

async function getPosts() {
  axios
    .get(`/api/posts/?trend=${route.currentRoute.value.params.id}`)
    .then((response) => {
      posts.value = response.data;
    })
    .catch((error) => {
      console.error("error get post: ", error);
    });
}
</script>
