<template>
  <v-app>
    <v-content>
      <div id="app" class="sandstone">
        <NavbarComponent
          v-if="!loadingUser"
          :user-data="userData"
          @emitUserDataChange="reloadUserData"
        />
        <keep-alive :max="1">
          <router-view :key="$route.fullPath" />
        </keep-alive>
      </div>
    </v-content>
  </v-app>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import NavbarComponent from "@/components/Navbar.vue";
export default {
  name: "App",
  components: {
    NavbarComponent
  },
  data: function() {
    return {
      loadingUser: true,
      userData: Object
    };
  },
  methods: {
    syncUserData(userData) {
      this.userData = userData;
      if(!this.userData.image){
        this.userData.image="https://jakesdesk-media.s3.amazonaws.com/media/public/profile_pics/default.jpg"
      }
      if(!this.userData.avatar){
        this.userData.avatar="https://jakesdesk-media.s3.amazonaws.com/media/public/avatars/default.jpg"
      }
      localStorage.setItem("username", userData.user.username);
    },
    initializeUser() {
      apiService(`api/users/profile/`).then(data => {
        this.syncUserData(data);
        this.loadingUser = false;
      }).catch(err => {
        console.log(err);
      });
    },
    reloadUserData() {
      apiService(`api/users/profile/`).then(data => {
        this.syncUserData(data);
      });
    }
  },
  created() {
    this.initializeUser();
  }
};
</script>

<style type="text/css">
html,
span {
  color: calligraphy;
}

.v-card__text,
.v-card__title {
  word-break: keep-all; /* maybe !important  */
  word-wrap: normal;
}
p {
  color: calligraphy;
}
body {
  background: #dbd4c4;
  background-color: #dbd4c4;
  height: 100%;
}
.btn:focus {
  box-shadow: none !important;
}
#app {
  height: 100vh;
  background-color: #dbd4c4;
}
</style>
