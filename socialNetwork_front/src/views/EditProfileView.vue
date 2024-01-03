<template>
  <div
    class="p-4 bg-white border border-gray-200 flex-col justify items-center rounded-lg max-w-xl mx-auto gap-4"
  >
    <div class="p-12">
      <form @submit.prevent="submitForm" class="space-y-6 relative">
        <div v-if="url" id="preview" class="h-[230px]">
          <img
            :src="url"
            alt="img-preview"
            class="mx-auto rounded-full w-[230px] h-[230px] object-cover"
          />
        </div>
        <div v-else class="h-[230px]">
          <img
            :src="form.avatar"
            class="mx-auto rounded-full w-[230px] h-[230px] object-cover"
          />
        </div>

        <div class="absolute top-0 right-16 flex justify pointer">
          <label class="flex p-5 mx-auto bg-cyan-900 text-white rounded-full">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="w-10 h-10"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L6.832 19.82a4.5 4.5 0 01-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 011.13-1.897L16.863 4.487zm0 0L19.5 7.125"
              />
            </svg>

            <input type="file" ref="file" @change="onFileChange" />
          </label>
        </div>
        <div>
          <label>Name</label><br />
          <input
            v-model="form.name"
            type="text"
            placeholder="Your name"
            class="w-full outline-blue-600 mt-2 py-4 px-6 border border-gray-200 rounded-lg"
          />
        </div>

        <div>
          <label>E-mail</label><br />
          <input
            v-model="form.email"
            type="email"
            placeholder="Your e-mail address"
            class="w-full outline-blue-600 mt-2 py-4 px-6 border border-gray-200 rounded-lg"
          />
        </div>

        <div v-if="errors.length > 0">
          <div class="bg-red-300 text-white rounded-lg p-6 text-sm">
            <p v-for="error in errors" :key="error">{{ error }}</p>
          </div>
        </div>

        <div class="text-center">
          <button class="py-4 mt-6 px-6 bg-sky-500 text-white rounded-lg">
            Edit Profile
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useModalStore } from "@/stores/modal";
import { useUserStore } from "@/stores/user";

// import { RouterLink } from "vue-router";

// import { ref } from "vue";

export default {
  setup() {
    const modalStore = useModalStore();
    const userStore = useUserStore();

    return {
      modalStore,
      userStore,
    };
  },
  data() {
    return {
      form: {
        name: this.userStore.user.name,
        email: this.userStore.user.email,
        avatar: this.userStore.user.avatar,
      },
      errors: [],
      url: "",
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

      if (this.errors.length === 0) {
        let formData = new FormData();
        formData.append("avatar", this.$refs.file.files[0]);
        formData.append("name", this.form.name);
        formData.append("email", this.form.email);

        console.log("formData", formData);

        axios
          .post("/api/editprofile/", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          })
          .then((response) => {
            if (response.data.message === "profile updated") {
              //maj les info user du store
              this.userStore.setUserInfo({
                id: this.userStore.user.id,
                name: this.form.name,
                email: this.form.email,
                avatar: response.data.user.get_avatar,
              });
              //renvoi vers login
              this.$router.back();
              //affichage modal en vert
              this.modalStore.showModal(
                5000,
                "Profile updated successfuly",
                " bg-green-300"
              );
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
    onFileChange(e) {
      const file = e.target.files[0];
      this.url = URL.createObjectURL(file);
    },
  },
};
</script>

<style scoped>
input[type="file"] {
  display: none;
}
</style>
