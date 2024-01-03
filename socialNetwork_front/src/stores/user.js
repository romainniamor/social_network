import { defineStore } from "pinia";
import axios from "axios";

export const useUserStore = defineStore({
  id: "user",

  state: () => ({
    user: {
      isAuthenticated: false,
      id: null,
      name: null,
      email: null,
      access: null,
      refresh: null,
      avatar: null,
    },
  }),

  actions: {
    //initialisation du store, vérif s'il existe des données d'utilisateur stockées dans le localStorage du navigtr.
    initStore() {
      console.log("init store");

      if (localStorage.getItem("user.access")) {
        console.log("user access");
        this.user.access = localStorage.getItem("user.access");
        this.user.refresh = localStorage.getItem("user.refresh");
        this.user.id = localStorage.getItem("user.id");
        this.user.name = localStorage.getItem("user.name");
        this.user.email = localStorage.getItem("user.email");
        this.user.avatar = localStorage.getItem("user.avatar");
        this.user.isAuthenticated = true;

        this.refreshToken();
        console.log("user initialised:", this.user);
      }
    },

    //maj des info d'auth de l'user, tokens d'accès et de rafraîchissement

    setToken(data) {
      console.log("set token:", data);

      this.user.access = data.access;
      this.user.refresh = data.refresh;
      this.user.isAuthenticated = true;

      localStorage.setItem("user.access", data.access);
      localStorage.setItem("user.refresh", data.refresh);
    },

    //supp des données d acces a user
    removeToken() {
      console.log("removeToken");
      this.user.refresh = null;
      this.user.access = null;
      this.user.isAuthenticated = false;
      this.user.id = false;
      this.user.name = false;
      this.user.email = false;
      this.user.avatar = null;

      localStorage.setItem("user.access", "");
      localStorage.setItem("user.refresh", "");
      localStorage.setItem("user.id", "");
      localStorage.setItem("user.name", "");
      localStorage.setItem("user.email", "");
      localStorage.setItem("user.avatar", "");
    },

    //si login recup des info de token
    setUserInfo(user) {
      console.log("set info user:", user);

      this.user.id = user.id;
      this.user.name = user.name;
      this.user.email = user.email;
      this.user.avatar = user.avatar;

      localStorage.setItem("user.id", this.user.id);
      localStorage.setItem("user.name", this.user.name);
      localStorage.setItem("user.email", this.user.email);
      localStorage.setItem("user.avatar", this.user.avatar);
    },
    //recup access & refresh token
    refreshToken() {
      console.log("refresh token");
      axios
        .post("/api/refresh/", {
          refresh: this.user.refresh,
        })

        .then((response) => {
          this.user.access = response.data.access;
          localStorage.setItem("user.access", response.data.access);
          axios.defaults.headers.common["Authorization"] =
            "Bearer " + response.data.access;
        })
        .catch((error) => {
          console.log(error);
          this.removeToken();
        });
    },
  },
});
