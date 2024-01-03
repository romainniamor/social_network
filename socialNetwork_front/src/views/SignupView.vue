<template>
  <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
    <div class="main-left">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h1 class="mb-6 text-2xl">Sign up</h1>

        <p class="mb-6 text-gray-500">
          Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
        </p>

        <div class="flex gap-2">
          <p class="font-semibold">Already have an account?</p>
          <RouterLink to="/login" class="text-sky-500 font-semibold"
            >Login</RouterLink
          >
        </div>
      </div>
    </div>

    <div class="main-right">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <form @submit.prevent="submitForm" class="space-y-6">
          <div>
            <label>Name</label><br />
            <input
              v-model="form.name"
              type="text"
              placeholder="Your name"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
            />
          </div>

          <div>
            <label>E-mail</label><br />
            <input
              v-model="form.email"
              type="email"
              placeholder="Your e-mail address"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
            />
          </div>

          <div>
            <label>Password</label><br />
            <input
              v-model="form.password1"
              type="password"
              placeholder="Your password"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
            />
          </div>

          <div>
            <label>Repeat password</label><br />
            <input
              v-model="form.password2"
              type="password"
              placeholder="Repeat your password"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
            />
          </div>

          <div v-if="errors.length > 0">
            <div class="bg-red-300 text-white rounded-lg p-6 text-sm">
              <p v-for="error in errors" :key="error">{{ error }}</p>
            </div>
          </div>

          <div>
            <button class="py-4 px-6 bg-sky-500 text-white rounded-lg">
              Sign up
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useModalStore } from "@/stores/modal";
// import { RouterLink } from "vue-router";

// import { ref } from "vue";

export default {
  setup() {
    const modalStore = useModalStore();

    return {
      modalStore,
    };
  },
  data() {
    return {
      form: {
        name: "",
        email: "",
        password1: "",
        password2: "",
      },
      errors: [],
    };
  },
  methods: {
    submitForm() {
      // Réinitialisation des erreurs
      this.errors = [];

      // Vérification des champs
      if (this.form.name === "") {
        this.errors.push("Name is missing");
      }
      if (this.form.email === "") {
        this.errors.push("Email is missing");
      }
      if (this.form.password1 === "") {
        this.errors.push("Password is missing");
      }
      if (this.form.password2 === "") {
        this.errors.push("Verification password is missing");
      }
      if (this.form.password1 !== this.form.password2) {
        this.errors.push("Passwords are different");
      }

      if (this.errors.length === 0) {
        axios
          .post("/api/signup/", this.form)
          .then((response) => {
            console.log("response:", response);
            console.log("response:", response.data);
            console.log("response message:", response.data.message);
            if (response.data.message === "success") {
              //renvoi vers login
              this.$router.push("/login/");
              //affichage modal en vert
              this.modalStore.showModal(
                5000,
                "You are registered. Please login now.",
                " bg-green-300"
              );
              // Réinitialisation des champs du formulaire
              this.form.name = "";
              this.form.email = "";
              this.form.password1 = "";
              this.form.password2 = "";
            } else {
              this.modalStore.showModal(
                5000,
                "An error occured. Please try again.",
                " bg-red-300"
              );
            }
          })
          .catch((error) => {
            console.log("error signup:", error);
          });
      }
    },
  },
};
</script>
