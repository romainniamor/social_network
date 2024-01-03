<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-1">
      <div
        class="p-4 bg-white border border-gray-200 flex-col justify items-center rounded-lg"
      >
        <img
          :src="user.get_avatar"
          class="mb-6 mx-auto rounded-full w-[230px] h-[230px] object-cover"
        />
        <div class="flex items-center justify-center gap-2">
          <p>
            <strong>{{ user.name }}</strong>
          </p>
          <button
            v-if="user.id !== userStore.user.id && can_send_friend_request"
            @click="sendFriendRequest"
            class="inline-block py-1 px-3 bg-sky-500 text-2xl text-white font-semibold rounded-lg"
          >
            +
          </button>
        </div>

        <div
          class="my-6 flex space-x-6 items-center justify-around"
          v-if="user.id"
        >
          <div v-if="userStore.user.id === user.id">
            <RouterLink
              :to="{ name: 'friends', params: { id: user.id } }"
              class="text-xs text-gray-500"
              >{{ user.friends_counter }} friends</RouterLink
            >
          </div>
          <div v-else>
            <p class="text-xs text-gray-500">
              {{ user.friends_counter }} friends
            </p>
          </div>

          <div>
            <p class="text-xs text-gray-500">{{ postsCounter }} posts</p>
          </div>
        </div>
        <RouterLink to="/profile/edit" v-if="userStore.user.id === user.id">
          <button
            class="inline-block py-2 my-1 px-4 bg-sky-300 text-white rounded-lg w-full"
          >
            Edit Profile
          </button>
        </RouterLink>
        <button
          @click="logOut"
          v-if="userStore.user.id === user.id"
          class="inline-block py-2 my-1 px-4 bg-transparent border-2 border-sky-200 text-sky-200 rounded-lg w-full"
        >
          Log Out
        </button>
        <button
          @click="sendMessage"
          v-if="userStore.user.id !== user.id"
          class="inline-block py-2 my-3 px-4 bg-sky-300 text-white rounded-lg w-full"
        >
          Write a message
        </button>
      </div>
    </div>

    <div class="main-center col-span-2 space-y-4">
      <form
        v-if="userStore.user.id === user.id"
        method="POST"
        @submit.prevent="submitPost"
        class="bg-white border border-gray-200 rounded-lg relative"
      >
        <div class="p-4">
          <textarea
            v-model="body"
            class="p-4 w-full h-20 outline-blue-600 resize-none bg-gray-100 rounded-lg"
            placeholder="Post your message..."
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

            <input type="file" name="image" ref="file" @change="onFileChange"
          /></label>

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

<style scoped>
input[type="file"] {
  display: none;
}
</style>

<script>
import axios from "axios";

import PostedPost from "@/components/PostedPost.vue";
import EmojiPicker from "vue3-emoji-picker";

import "vue3-emoji-picker/css";
import People from "../components/People.vue";
import Trends from "../components/Trends.vue";

import { useUserStore } from "@/stores/user";
import { useModalStore } from "@/stores/modal";

export default {
  name: "HomeView",

  setup() {
    const userStore = useUserStore();
    const modalStore = useModalStore();

    return {
      userStore,
      modalStore,
    };
  },

  components: {
    People,
    Trends,
    PostedPost,
    EmojiPicker,
  },

  data() {
    return {
      posts: [],
      user: { id: null },
      postsCounter: "",
      body: "",
      url: "",
      emojiPickerVisible: false,
      can_send_friend_request: null,
    };
  },

  mounted() {
    this.getPosts();
  },

  watch: {
    "$route.params.id": {
      handler: function () {
        this.getPosts();
      },
      deep: true,
      immediate: true,
    },
  },

  methods: {
    async getPosts() {
      try {
        const response = await axios.get(
          `/api/posts/profile/${this.$route.params.id}`
        );
        this.posts = response.data.posts;
        this.user = response.data.user;
        this.postsCounter = response.data.posts_counter;
        this.can_send_friend_request = response.data.can_send_friend_request;
        console.log("data profile et post du backend:", response.data.user);
        console.log("http://127.0.0.1:8000" + this.user.avatar);
      } catch (error) {
        console.error("error get mes posts: ", error);
      }
    },

    async submitPost() {
      let formData = new FormData();
      const fileInput = this.$refs.file;
      if (fileInput.files.length > 0) {
        formData.append("image", fileInput.files[0]);
      }
      formData.append("body", this.body);

      try {
        const response = await axios.post("/api/posts/create/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });

        console.log("response", response);
        this.posts.unshift(response.data);
        this.postsCounter += 1;
        this.body = "";
        this.$refs.file.value = null;
        this.url = null;
        this.emojiPickerVisible = false;
      } catch (error) {
        console.error("error get mes posts: ", error);
      }
    },
    sendFriendRequest() {
      console.log("adding friend");
      console.log(`api/friends/${this.$route.params.id}/request/`);
      axios
        .post(`api/friends/${this.$route.params.id}/request/`)
        .then((response) => {
          console.log("response", response);
          this.user = response.data.user;
          this.can_send_friend_request = false;
          console.log("sending friend request:", response.data);
          if (response.data.message === "already requested") {
            this.modalStore.showModal(
              5000,
              "Request already sent",
              "bg-red-300"
            );
          } else {
            this.modalStore.showModal(5000, "Request sent", "bg-green-300");
          }
        })
        .catch((error) => {
          console.error("error sending request to friend: ", error);
        });
    },
    async sendMessage() {
      console.log("write a message");
      try {
        const response = await axios.get(
          `api/chat/${this.$route.params.id}/get-or-create/`
        );
        console.log("get or create conversation", response.data);
        this.$router.push("/chat");
      } catch (error) {
        console.log("error get create conversation", error);
      }
    },
    logOut() {
      this.userStore.removeToken();
      this.$router.push("/login");
    },

    onFileChange(e) {
      const file = e.target.files[0];
      this.url = URL.createObjectURL(file);
    },
    onSelectEmoji(emoji) {
      this.body += emoji.i;
    },

    toggleEmojiPicker() {
      this.emojiPickerVisible = !this.emojiPickerVisible;
    },
  },
};
</script>
