<template>
  <v-card class="desertsand">
    <v-card-title class="pa-0">
      <v-img :src="profile.avatar">
        <v-btn
          icon
          fab
          small
          class="calligraphy white--text"
          @click="closeDialog"
          ><v-icon>mdi-close</v-icon>
        </v-btn>
      </v-img>
    </v-card-title>

    <v-card-text class="pt-2 pl-4 desertsand calligraphy--text">
      <v-row dense>
        <v-col align="center">
          <h2>{{ username }}</h2>
          <v-chip outlined small class="primary primary--text">{{
            userPointsText
          }}</v-chip>
          <v-chip outlined small class="languages languages--text"
            >Native: {{ profile.language }}</v-chip
          >
          <v-chip outlined small class="languages languages--text"
            >Learning: Django, French</v-chip
          >
        </v-col>
        <v-col>
          <p>
            <span class="font-weight-bold">User Bio:</span>
            {{ profile.biography }}
          </p>

          <v-btn block class="my-1 primary desertsand--text"
            >View Curated Works</v-btn
          >

          <v-btn
            block
            v-if="!isProfileOwner"
            @click="toggleFollow"
            class="my-1 saves desertsand--text"
            :loading="following"
          >
            <v-badge color="blue" :content="profile.followers_count">
              <span v-if="!profile.user_has_followed">
                Follow<v-icon right>mdi-heart</v-icon>
              </span>
              <span v-else>
                Unfollow<v-icon right>mdi-heart-broken</v-icon>
              </span>
            </v-badge>
          </v-btn>

          <v-btn
            block
            v-if="!isProfileOwner"
            @click="toggleHide"
            class="my-1 garbage desertsand--text"
            :loading="hiding"
          >
            <span v-if="!profile.user_has_hidden">
              Hide<v-icon right>mdi-eye-off</v-icon>
            </span>
            <span v-else> Unhide<v-icon right>mdi-eye</v-icon> </span>
          </v-btn>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>
<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "ProfileSnippet",
  components: {},
  props: {
    username: String
  },
  data: () => ({
    loading: true,
    profile: Object,
    following: false,
    hiding: false
  }),
  computed: {
    userPointsText() {
      return `Points: ${this.profile.points}`;
    },
    isProfileOwner() {
      // return this.question.author.username === this.requestUser;
      return this.username === window.localStorage.getItem("username");
      // return true;
    }
  },
  methods: {
    closeDialog() {
      this.$emit("closeDialog");
    },
    getProfileSnippet() {
      this.loading = true;
      let endpoint = `/api/users/snippet/${this.username}`;
      apiService(endpoint).then(data => {
        if (data) {
          this.profile = data;
          this.loading = false;
        } else {
          this.profile = null;
          this.setPageTitle("404 - Page Note Found");
          this.loading = false;
        }
      });
    },
    toggleFollow() {
      this.following = true;
      let endpoint = `api/users/follow/`;
      try {
        apiService(endpoint, "POST", { username: this.profile.username }).then(
          data => {
            if (data != null) {
              if (data.success == true) {
                // this.$emit("hideElement")
                this.profile.user_has_followed = !this.profile
                  .user_has_followed;
                if (this.profile.user_has_followed) {
                  this.profile.followers_count += 1;
                } else {
                  this.profile.followers_count -= 1;
                }
                // console.log(data.message)
              } else {
                // this.alertType = 'error';
              }
            } else {
              // this.alertType = 'error';
            }
            this.following = false;
          }
        );
      } catch (err) {
        console.log(err);
      }
    },
    toggleHide() {
      this.hiding = true;
      let endpoint = `api/users/hide/`;
      try {
        apiService(endpoint, "POST", { username: this.profile.username }).then(
          data => {
            if (data != null) {
              if (data.success == true) {
                this.profile.user_has_hidden = !this.profile.user_has_hidden;
                console.log("This profile has been hidden");
              } else {
                this.alertType = "error";
              }
            } else {
              this.alertType = "error";
            }
            this.hiding = false;
          }
        );
      } catch (err) {
        console.log(err);
      }
    } // Hide from List
    //
  },
  created() {
    this.getProfileSnippet();
  }
};
</script>
<style lang="stylus"></style>
