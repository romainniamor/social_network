<template>
  <div class="p-4 bg-white border border-gray-200 rounded-lg">
    <div class="mb-6 flex items-center justify-between">
      <div class="flex items-center space-x-6 text-xs">
        <img
          :src="comment.created_by.get_avatar"
          class="w-[20px] h-[20px] rounded-full"
        />

        <RouterLink
          :to="{ name: 'profile', params: { id: comment.created_by.id } }"
        >
          <p>
            <strong>{{ comment.created_by.name }}</strong>
          </p>
        </RouterLink>
      </div>

      <p class="text-gray-600 text-xs">{{ comment.created_at_formated }} ago</p>
    </div>

    <p class="text-xs">
      {{ comment.body }}
    </p>
  </div>
</template>

<script>
import axios from "axios";

import { RouterLink } from "vue-router";

export default {
  props: {
    comment: Object,
  },
  methods: {},
  components: { RouterLink },
};
</script>
