<template>
  <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
    <div class="main-left">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h1 class="mb-6 text-2xl">Log in</h1>

        <p class="mb-6 text-gray-500">
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Autem a
          excepturi.
        </p>

        <div class="flex gap-2">
          <p class="font-semibold">Don't have an account?</p>
          <RouterLink
            :to="{ name: 'signup' }"
            class="text-sky-500 font-semibold"
            >Sign Up</RouterLink
          >
        </div>
      </div>
    </div>

    <div class="main-right">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <form class="space-y-6" @submit.prevent="submitForm">
          <div>
            <label>E-mail</label><br />
            <input
              v-model="form.email"
              type="email"
              placeholder="Your e-mail address"
              class="w-full mt-2 py-4 outline-blue-600 px-6 border border-gray-200 rounded-lg"
            />
          </div>

          <div>
            <label>Password</label><br />
            <input
              v-model="form.password"
              type="password"
              placeholder="Your password"
              class="w-full mt-2 outline-blue-600 py-4 px-6 border border-gray-200 rounded-lg"
            />
          </div>

          <div>
            <button class="py-4 px-6 bg-sky-500 text-white rounded-lg">
              Log in
            </button>
          </div>
          <p
            v-if="errors.length > 0"
            class="py-4 px-6 bg-red-300 text-white rounded-lg"
          >
            {{ errors[0] }}
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "@/stores/user";
import { useModalStore } from "@/stores/modal";
// import { RouterLink } from "vue-router";
import router from "../router";
// import { ref } from "vue";

export default {
  setup() {
    const userStore = useUserStore();
    const modalStore = useModalStore();
    return {
      userStore,
      modalStore,
    };
  },
  data() {
    return {
      form: {
        email: "",
        password: "",
      },
      errors: [],
    };
  },
  methods: {
    async submitForm() {
      // Réinitialisation des erreurs
      this.errors = [];

      // Vérification des champs
      if (this.form.email === "") {
        this.errors.push("Email is missing");
      }
      if (this.form.password === "") {
        this.errors.push("Password is missing");
      }

      if (this.errors.length === 0) {
        await axios
          .post("/api/login/", this.form)
          .then((response) => {
            console.log("response login post:", response.data.access);
            this.userStore.setToken(response.data);
            axios.defaults.headers.common["Authorization"] =
              "Bearer " + response.data.access;
          })
          .catch((error) => {
            console.log("error signin:", error);
            this.errors.push("Email or password incorrect.");
          });

        await axios
          .get("/api/me/")
          .then((response) => {
            this.userStore.setUserInfo(response.data);
            //routage vers profile
            this.$router.push(`/profile/${this.userStore.user.id}`);
          })
          .catch((error) => {
            console.log("error:", error);
          });
      }
    },
  },
};
</script>
