<template>
  <div class="max-w-5xl mx-auto grid grid-cols-3 gap-4">
    <div class="main-center col-span-2 space-y-4">
      <form
        method="POST"
        @submit.prevent="submitPost"
        class="bg-white relative border border-gray-200 rounded-lg"
      >
        <div class="p-4">
          <textarea
            v-model="body"
            class="p-4 outline-blue-600 w-full h-20 resize-none bg-gray-100 rounded-lg"
            placeholder="Post a message."
          ></textarea>
          <div v-if="url" id="preview">
            <img
              :src="url"
              alt="img-preview"
              class="rounded-lg w-[90px] my-3"
            />
          </div>
        </div>

        <div class="p-4 border-t border-gray-100 flex justify-between">
          <label class="inline-block p-4 bg-cyan-900 text-white rounded-full">
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
                d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5"
              />
            </svg>

            <input type="file" name="image" @change="onFileChange" />
          </label>

          <div class="flex items-center space-x-3">
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
              class="inline-block py-4 px-6 bg-sky-500 text-white rounded-lg"
            >
              Post
            </button>
            <EmojiPicker
              v-if="emojiPickerVisible"
              class="absolute right-0 top-full"
              @select="onSelectEmoji"
            />
          </div>
        </div>
      </form>

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
import EmojiPicker from "vue3-emoji-picker";
import "vue3-emoji-picker/css";

const posts = ref([]);

let body = ref("");
let emojiPickerVisible = ref(false);

const file = ref(null);
const url = ref(null);

// dif avec api option et this.$refs.file.files[0]
//gestionnaire d'event appelé lorsque l'user sélectionne un fichier => maj file selected

const onFileChange = (event) => {
  file.value = event.target.files[0];
  url.value = URL.createObjectURL(file.value);
};

onMounted(() => {
  getPosts();
});

async function getPosts() {
  axios
    .get("/api/posts/")
    .then((response) => {
      posts.value = response.data;
    })
    .catch((error) => {
      console.error("error get post: ", error);
    });
}

async function submitPost() {
  if (body.value.length !== 0) {
    let formData = new FormData();
    formData.append("image", file.value);
    formData.append("body", body.value);

    axios
      .post("/api/posts/create/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })

      .then((response) => {
        console.log("response", response);
        posts.value.unshift(response.data);
        body.value = "";
        file.value = null;
        url.value = null;
      })
      .catch((error) => {
        console.log(error);
      });
  } else {
    console.log("message vide");
  }
}

function onSelectEmoji(emoji) {
  console.log(emoji);
  body.value += emoji.i;
}

const toggleEmojiPicker = () => {
  emojiPickerVisible.value = !emojiPickerVisible.value;
};
</script>

<style scoped>
input[type="file"] {
  display: none;
}
</style>
