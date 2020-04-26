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
                class="logo-img hidden-sm-and-down"
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
          <v-img class="elevation-6" :src="userData.avatar"></v-img>
        </v-avatar>
      </v-btn>

    </v-app-bar>

    <v-navigation-drawer floating temporary right app v-model="drawer" class="calligraphy" xs12>
      <v-container fluid class="pa-0">
        <v-row>
          <v-col xs12>
            <v-container fluid>
              <v-card dense class="center mt-0" mx-0>
                <v-img :src="userData.image">
                  <v-container fill-height fluid pa-1>
                    <v-row no-gutters class="align-center mt-auto">
                      <v-col xs12 align="center" outlined text>
                        <v-card
                          class="calligraphy darken-2"
                          style="opacity: 0.85"
                          outlined
                        >
                          <span
                            class="body-1 desertsand--text font-weight-bold"
                            >{{ userData.user.username }}</span
                          >
                        </v-card>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-img>

                <v-card-actions class="calligraphy darken-2">
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

                  <v-dialog
                    v-model="profileUpdateDialog"
                    scrollable
                    persistent
                    max-width="750px"
                  >
                    <template v-slot:activator="{ on: profileUpdateDialog }">
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on: tooltip }">
                          <v-btn
                            small
                            fab
                            class="primary"
                            v-on="{ ...tooltip, ...profileUpdateDialog }"
                          >
                            <v-icon>settings</v-icon>
                          </v-btn>
                        </template>
                        <span>Update Profile</span>
                      </v-tooltip>
                    </template>
                    <ProfileUpdate
                      :user-data="userData"
                      @closeDialog="closeProfileUpdateDialog"
                      @emitUserDataChange="emitUserDataChange"
                    />
                  </v-dialog>

                  <v-spacer></v-spacer>

                  <ConfirmLogout></ConfirmLogout>

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
  </nav>
</template>

<script>
import ConfirmLogout from "@/components/profile/ConfirmLogout.vue";

export default {
  name: "NavbarComponent",
  data() {
    return {
      profileUpdateDialog: false,
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
