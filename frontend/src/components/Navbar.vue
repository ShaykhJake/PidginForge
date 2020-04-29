<template>
  <nav>
    <v-app-bar app flat dense class="desertsand">
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn
            fab
            text
            class="mt-2"
            v-on="on"
            router
            :to="{ name: 'Home' }"
            exact
          >
          <a>
            <v-avatar>
              <img
                src="https://jakesdesk-media.s3.amazonaws.com/static/images/firepigeon_transparent.png"
                class="logo-img"
                alt=""
              />
            </v-avatar>
          </a>
          </v-btn>
        </template>
        <span>Home</span>
      </v-tooltip>

      <v-toolbar-title class="hidden-xs-and-down ml-1">
        <span class="font-weight-light">Pidgin</span
        ><span class="primary--text font-weight-black">Forge</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <!-- <v-btn class="primary" router to:"confirm-logout"> -->

      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn
            small
            fab
            class="mx-1 calligraphy"
            v-on="on"
            router
            :to="{ name: 'Home' }"
            exact
          >
            <v-icon class="desertsand--text">home</v-icon>
          </v-btn>
        </template>
        <span>Home</span>
      </v-tooltip>

      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn
            disabled
            small
            fab
            class="mx-1 calligraphy"
            v-on="on"
            router
            :to="{ name: 'Learn' }"
          >
            <v-icon class="desertsand--text">school</v-icon>
          </v-btn>
        </template>
        <span>Learn</span>
      </v-tooltip>

      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn
            small
            fab
            class="mx-1 calligraphy"
            v-on="on"
            router
            :to="{ name: 'Curate' }"
          >
            <v-icon class="desertsand--text">library_add</v-icon>
          </v-btn>
        </template>
        <span>Create & Curate</span>
      </v-tooltip>

      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn
            disabled
            small
            fab
            class="mx-1 calligraphy"
            v-on="on"
            router
            :to="{ name: 'Collaborate' }"
          >
            <v-icon class="desertsand--text">question_answer</v-icon>
          </v-btn>
        </template>
        <span>Collaborate</span>
      </v-tooltip>
      <v-btn text fab class="calligraphy mt-2" @click="drawer = !drawer">
        <v-avatar>
          <v-img class="elevation-6" :src="userData.avatar ? userData.avatar : 'https://jakesdesk-media.s3.amazonaws.com/media/public/profile_pics/default.jpg' "></v-img>
        </v-avatar>
      </v-btn>

    </v-app-bar>

    <v-navigation-drawer floating temporary right app v-model="drawer" class="calligraphy" xs12>
      <v-container fluid class="pa-0">
        <v-row>
          <v-col>
            <v-container fluid>

              <v-card dense class="center mt-0" mx-0>
                <v-img :src="userData.image ? userData.image : '' ">
                </v-img>
                <v-card-title class="sandstone calligraphy--text py-2">
                  {{ userData.user.username }}
                </v-card-title>
                <v-card-text class="desertsand pt-2">
                  User Points: {{ userData.points }}
                  <hr>
                  Followers: {{ userData.follower_count }}
                  <hr>
                  Vocab Stack: 0
                </v-card-text>
                <v-card-actions class="sandstone">
                  <v-spacer></v-spacer>
                  <v-tooltip bottom class="font-weight-bold">
                    <template v-slot:activator="{ on }">
                      <v-btn disabled small fab color="primary" v-on="on"
                        ><v-icon>dashboard</v-icon></v-btn
                      >
                    </template>
                    <span>User Dashboard</span>
                  </v-tooltip>
                  <v-spacer></v-spacer>
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on: on }">
                      <v-btn
                        small
                        fab
                        class="primary"
                        v-on="on"
                        @click="profileUpdateDialog=true"
                      >
                        <v-icon>settings</v-icon>
                      </v-btn>
                    </template>
                    <span>Update Profile</span>
                  </v-tooltip>
                  <v-spacer></v-spacer>
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on: on }">
                      <v-btn
                        small
                        fab
                        class="primary"
                        v-on="on"
                        @click="confirmLogoutDialog=true"
                      >
                        <v-icon>mdi-exit-run</v-icon>
                      </v-btn>
                    </template>
                    <span>Logout</span>
                  </v-tooltip>
                  <v-spacer></v-spacer>
                </v-card-actions>
              </v-card>
            </v-container>
          </v-col>
        </v-row>
      </v-container>
      <v-list class="calligraphy">
        <v-list-item
          v-for="link in links"
          :key="link.text"
          router
          :to="link.route"
        >
          <v-list-item-action>
            <v-icon>{{ link.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title class="desertsand--text">{{
              link.text
            }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <ProfileUpdate
      v-if="profileUpdateDialog"
      :show-dialog="profileUpdateDialog"
      :user-data="userData"
      @closeDialog="profileUpdateDialog=false"
      @emitUserDataChange="emitUserDataChange"
    />
    <ConfirmLogout 
      v-if="confirmLogoutDialog"
      :show-dialog="confirmLogoutDialog"
      @closeDialog="confirmLogoutDialog=false"
    />

  </nav>
</template>

<script>
import ConfirmLogout from "@/components/profile/ConfirmLogout.vue";

export default {
  name: "NavbarComponent",
  data() {
    return {
      profileUpdateDialog: false,
      confirmLogoutDialog: false,
      drawer: false,
      username: null,
      links: [
        // { icon: "school", text: "Learn", route: "/" },
        // { icon: "add_box", text: "Curate", route: "/" },
        // { icon: "group", text: "Collaborate", route: "/" },
        // { icon: "settings", text: "Account Settings", route: "/" }
      ]
    };
  },
  props: {
    userData: Object
  },
  components: {
    ConfirmLogout,
    ProfileUpdate: () =>
      import(
        /* webpackPrefetch: true */ "@/components/profile/ProfileUpdate.vue"
      )
  },
  methods: {
    emitUserDataChange() {
      this.$emit("emitUserDataChange");
    },
    closeProfileUpdateDialog() {
      this.profileUpdateDialog = false;
    }
  },
  created() {}
};
</script>

<style scoped>
html,
body {
  height: 100%;
}
a {
  text-decoration: none;
}
.my-navbar {
  border-bottom: 1px solid gray;
}
.navbar-brand {
  font-weight: bold;
  font-size: 130%;
  color: white;
}
.navbar-brand:hover {
  color: #c96e16;
}
.logo-img {
  height: 90%;
}
</style>
