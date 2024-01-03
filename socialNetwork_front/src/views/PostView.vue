<template>
  <div class="max-w-5xl mx-auto grid grid-cols-3 gap-4">
    <div class="main-center col-span-2 space-y-4">
      <!-- <div class="p-4 bg-white border border-gray-200 rounded-lg">
        <div class="mb-6 flex items-center justify-between">
          <div class="flex items-center space-x-6">
            <img
              src="https://i.pravatar.cc/300?img=55"
              class="w-[40px] rounded-full"
            />

            <p><strong>John Doe</strong></p>
          </div>

          <p class="text-gray-600">1 minutes ago</p>
        </div>

        <img
          src="https://images.unsplash.com/photo-1661956602868-6ae368943878?ixlib=rb-4.0.3&amp;ixid=MnwxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&amp;auto=format&amp;fit=crop&amp;w=2670&amp;q=80"
          class="w-full rounded-lg"
        />

        <div class="my-6 flex justify-between">
          <div class="flex space-x-6">
            <div class="flex items-center space-x-2">
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
                ></path>
              </svg>

              <span class="text-gray-500 text-xs">2 likes</span>
            </div>

            <div class="flex items-center space-x-2">
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
                  d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z"
                ></path>
              </svg>

              <span class="text-gray-500 text-xs">0 comments</span>
            </div>
          </div>

          <div>
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
                d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z"
              ></path>
            </svg>
          </div>
        </div>
      </div> -->

      <div v-if="post.id">
        <PostedPost :post="post" />
      </div>
      <form
        method="POST"
        @submit.prevent="submitComment"
        class="relative bg-white border border-gray-200 rounded-lg"
      >
        <div class="p-3 bg-white border border-gray-200 rounded-lg flex">
          <input
            v-model="body"
            class="px-3 w-full h-12 outline-none resize-none"
            placeholder="Let a comment..."
          />

          <div class="flex inline items-center space-x-2">
            <svg
              @click="toggleEmojiPicker"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="w-9 h-9 text-cyan-700"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M15.182 15.182a4.5 4.5 0 01-6.364 0M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9.75 9.75c0 .414-.168.75-.375.75S9 10.164 9 9.75 9.168 9 9.375 9s.375.336.375.75zm-.375 0h.008v.015h-.008V9.75zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75zm-.375 0h.008v.015h-.008V9.75z"
              />
            </svg>

            <button
              class="inline-block py-2 px-6 bg-sky-500 text-white rounded-lg"
            >
              Comment
            </button>
          </div>
        </div>
        <EmojiPicker
          v-if="emojiPickerVisible"
          class="absolute right-0"
          @select="onSelectEmoji"
        />
      </form>
      <div
        class="bg-white border border-gray-200 rounded-lg"
        v-for="comment in post.comments"
        :key="comment.id"
      >
        <Comment :comment="comment"></Comment>
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
import Comment from "@/components/comment.vue";
import EmojiPicker from "vue3-emoji-picker";
import "vue3-emoji-picker/css";

const post = ref({ id: null, comments: [] });
const route = useRouter();

let emojiPickerVisible = ref(false);

let body = ref("");

onMounted(() => {
  getPost();
});

async function getPost() {
  axios
    .get(`/api/posts/${route.currentRoute.value.params.id}/`)
    .then((response) => {
      post.value = response.data.post;
      console.log("response", response.data);
    })
    .catch((error) => {
      console.error("error get post: ", error);
    });
}

async function submitComment() {
  console.log("submitting comment", body.value);
  axios
    .post(`/api/posts/${route.currentRoute.value.params.id}/comment/`, {
      body: body.value,
    })
    .then((response) => {
      console.log("response", response);
      //!push car tableau comments, unshift permet d'add par debut
      post.value.comments.unshift(response.data);
      body.value = "";
      emojiPickerVisible = false;
      post.value.comments_count += 1;
    })
    .catch((error) => {
      console.log(error);
    });
}

function onSelectEmoji(emoji) {
  console.log(emoji);
  body.value += emoji.i;
}

const toggleEmojiPicker = () => {
  emojiPickerVisible.value = !emojiPickerVisible.value;
};
</script>
