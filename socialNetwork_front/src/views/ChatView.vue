<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-1">
      <div
        v-if="conversations.length"
        class="p-4 bg-white space-y-4 border border-gray-200 rounded-lg"
      >
        <div
          v-for="conversation in conversations"
          :key="conversation.id"
          @click="setActiveConversation(conversation.id)"
          class="space-y-4"
        >
          <div class="flex items-center justify-between cursor-pointer">
            <div class="flex items-center space-x-2">
              <template v-for="user in conversation.users" v-bind:key="user.id">
                <p
                  v-if="user.id !== userStore.user.id"
                  class="text-xs font-semibold"
                >
                  {{ user.name }}
                </p>
              </template>
            </div>
            <img src="" class="w-[40px] rounded-full" />

            <span class="text-xs text-gray-500"
              >{{ conversation.modified_at_formated }} ago</span
            >
          </div>
        </div>
      </div>
      <p
        class="p-4 text-white bg-blue-600 border border-gray-200 rounded-lg"
        v-else
      >
        No active conversation yet
      </p>
    </div>

    <div class="main-center col-span-3 space-y-4">
      <div class="bg-white min-h-[50vh] border border-gray-200 rounded-lg">
        <div class="flex flex-col flex-grow p-4">
          <template
            v-for="message in activeConversations.messages"
            :key="message.id"
          >
            <div
              v-if="message.created_by.id != userStore.user.id"
              class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end"
            >
              <div>
                <div class="bg-gray-300 p-3 rounded-l-lg rounded-br-lg">
                  <p class="text-sm">
                    {{ message.body }}
                  </p>
                </div>
                <span class="text-xs text-gray-500 leading-none"
                  >{{ message.created_at_formated }} ago</span
                >
              </div>
              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                <img
                  :src="message.created_by.get_avatar"
                  class="w-[40px] rounded-full"
                />
              </div>
            </div>

            <div v-else class="flex w-full mt-2 space-x-3 max-w-md">
              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                <img
                  :src="message.created_by.get_avatar"
                  class="w-[40px] rounded-full"
                />
              </div>
              <div>
                <div
                  class="bg-blue-600 text-white p-3 rounded-r-lg rounded-bl-lg"
                >
                  <p class="text-sm">
                    {{ message.body }}
                  </p>
                </div>
                <span class="text-xs text-gray-500 leading-none"
                  >{{ message.created_at_formated }} ago</span
                >
              </div>
            </div>
          </template>
        </div>
      </div>

      <form
        v-if="formVisible"
        @submit.prevent="submitForm"
        class="bg-white relative flex border border-gray-200 rounded-lg p-4"
      >
        <input
          v-model="body"
          class="px-3 w-full h-12 outline-none resize-none"
          placeholder="Write a message..."
        />

        <div class="flex inline items-center space-x-2">
          <svg
            @click="toggleEmojiPicker"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-9 h-9 text-cyan-700 cursor-pointer"
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
            Send
          </button>
        </div>

        <EmojiPicker
          v-if="emojiPickerVisible"
          class="absolute right-0 bottom-full"
          @select="onSelectEmoji"
        />
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useUserStore } from "@/stores/user";
import EmojiPicker from "vue3-emoji-picker";
import "vue3-emoji-picker/css";

const userStore = useUserStore();
const conversations = ref([]);
const activeConversations = ref({});
let body = ref("");
let emojiPickerVisible = ref(false);
let formVisible = ref(false);

onMounted(() => {
  getConversations();
  getMessages();
});

function setActiveConversation(id) {
  activeConversations.value.id = id;
  getMessages();
  formVisible.value = true;
}

async function getConversations() {
  console.log("get conversations");

  await axios
    .get("api/chat/")
    .then((response) => {
      console.log(response.data);
      conversations.value = response.data;

      if (conversations.value.length) {
        activeConversations.value = conversations.value[0];
      }
      console.log("active conversation", activeConversations.value);

      getMessages();
    })
    .catch((error) => {
      console.log(error);
    });
}

async function getMessages() {
  console.log("get messages");
  console.log("id converstion active", activeConversations.value);
  await axios
    .get(`api/chat/${activeConversations.value.id}/`)
    .then((response) => {
      console.log("get messages conversation active:", response.data);
      activeConversations.value = response.data;
    })
    .catch((error) => {
      console.log(error);
    });
}

async function submitForm() {
  console.log("clik submit", body.value);
  await axios
    .post(`api/chat/${activeConversations.value.id}/send/`, {
      body: body.value,
    })
    .then((response) => {
      console.log("send message", response.data);
      activeConversations.value.messages.push(response.data);
      body.value = "";
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
