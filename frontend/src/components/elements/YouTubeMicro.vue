<template>
  <div class="youtube-micro" v-if="youTubeElement">
    <v-hover>
      <template v-slot:default="{ hover }">
        <v-card class="pa-0 desertsand">
          <v-card-text class="pa-0">
            <v-row dense class="ma-0 pa-0">
              <v-col cols="12" class="pa-0">
                <v-img
                  :src="youTubeElement.thumbURL"
                  class="cardimg"
                  :aspect-ratio="16 / 9"
                >
                </v-img>
              </v-col>
            </v-row>
          </v-card-text>

          <v-card-title class="py-1">
            <v-row dense wrap no-gutters>
              <v-col cols="12">
                <span block class="overline font-weight-light mb-0"
                  ><span class="font-weight-black primary--text">
                    {{ youTubeElement.curator.username }}</span
                  >
                  on {{ youTubeElement.curationdate }}</span
                ><br />
              </v-col>
              <v-col cols="12">
                <span class="subtitle-2">{{ shortTitle }}</span>
              </v-col>
            </v-row>
          </v-card-title>
          <v-card-text>
            <v-row dense no-gutters>
              <v-col cols="12" class="text-justify"> </v-col>
              <v-col cols="12" class="pa-0 text-center">
                <p class="overline font-weight-light mb-1">
                  <span class="languages--text">
                    {{ youTubeElement.language }}
                  </span>
                  |<span class="topics--text"> {{ youTubeElement.topic }}</span>
                  | <span class="calligraphy--text"> Length: {{ length }}</span
                  ><br />
                </p>

                <div>
                  <v-btn icon>
                    <v-icon :class="upClass">
                      mdi-arrow-up-circle-outline
                    </v-icon>
                  </v-btn>
                  <span class="green--text font-weight-bold">{{
                    youTubeElement.upvote_count
                  }}</span>
                  /
                  <span class="red--text font-weight-bold">{{
                    youTubeElement.downvote_count
                  }}</span>
                  <v-btn icon>
                    <v-icon :class="downClass">
                      mdi-arrow-down-circle-outline
                    </v-icon>
                  </v-btn>
                </div>

                <p class="primary--text caption mb-0">
                  {{ youTubeElement.saved_count }} Saves - 0 Transcripts - 0
                  Lessons
                </p>
              </v-col>
            </v-row>
          </v-card-text>

          <v-fade-transition>
            <v-overlay v-if="hover" absolute color="calligraphy" opacity="0.7">
              <v-btn
                block
                class="mb-2 elements"
                :to="{
                  name: 'Media-Viewer',
                  params: {
                    elementtype: 'YouTube',
                    elementslug: youTubeElement.slug
                  }
                }"
                >View Video <v-icon right>mdi-play-circle</v-icon></v-btn
              >
              <v-btn
                block
                class="mb-2 saves"
                @click="toggleSave"
                :loading="saving"
              >
                <span :hidden="youTubeElement.user_has_saved"
                  >Save Video<v-icon right>mdi-heart</v-icon></span
                >
                <span :hidden="!youTubeElement.user_has_saved"
                  >Unsave Video<v-icon right>mdi-heart-broken</v-icon></span
                >
              </v-btn>

              <v-btn
                block
                class="mb-2 garbage desertsand--text"
                @click="toggleHide"
                :loading="hiding"
              >
                <span :hidden="youTubeElement.user_has_hidden"
                  >Hide Video<v-icon right>mdi-eye-off</v-icon></span
                >
                <span :hidden="!youTubeElement.user_has_hidden"
                  >Unhide Video<v-icon right>mdi-eye</v-icon></span
                >
              </v-btn>

            </v-overlay>
          </v-fade-transition>
        </v-card>
      </template>
    </v-hover>
    <v-snackbar v-model="snackbar" :timeout="snacktimeout" top color="success">
      {{ snacktext }}
      <v-btn color="garbage" text @click="snackbar = false">
        Close
      </v-btn>
    </v-snackbar>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "YouTubeMicro",
  props: {
    youTubeElement: Object
  },
  components: {},
  data() {
    return {
      hiding: false,
      loading: false,
      overlay: false,
      snackbar: false,
      saving: false,
      snacktext: "",
      snacktimeout: 1500
    };
  },
  computed: {
    length() {
      let totalseconds = this.youTubeElement.duration;
      var hours = totalseconds / 3600,
        minutes = (hours % 1) * 60,
        seconds = (minutes % 1) * 60;
      let hoursText = "";
      let minutesText = "";
      let secondsText = "";
      if(hours === 0){
        hoursText = "0"
      } else {
        hoursText = Math.floor(hours)
      }
      if(minutes === 0){
        minutesText = "00"
      } else if (minutes < 10) {
        minutesText = `0${Math.floor(minutes)}`
      } else {
        minutesText = Math.floor(minutes)
      }
      if(seconds === 0){
        secondsText = "00"
      } else if (seconds < 10) {
        secondsText = `0${Math.floor(seconds)}`
      } else {
        secondsText = Math.floor(seconds)
      }
      return `${hoursText}:${minutesText}:${secondsText}`
    },
    shortTitle() {
      let title = this.youTubeElement.title;
      if (title.length > 55) {
        let short = this.youTubeElement.title.slice(0, 55);
        return short + "...";
      } else {
        return title;
      }
    },
    shortPurpose() {
      let purpose = this.youTubeElement.purpose;
      if (purpose.length > 75) {
        let short = this.youTubeElement.purpose.slice(0, 75);
        return short + "...";
      } else {
        return purpose;
      }
    },
    upClass() {
      if (this.youTubeElement.user_vote === 1) {
        return "success--text";
      } else {
        return "";
      }
    },
    downClass() {
      if (this.youTubeElement.user_vote === -1) {
        return "error--text";
      } else {
        return "";
      }
    }
  },

  methods: {
    // Get Current User
    // Save / Unsave Item
    toggleSave() {
      this.saving = true;
      let endpoint = `api/elements/youtube/save/`;
      try {
        apiService(endpoint, "POST", { pk: this.youTubeElement.id }).then(
          data => {
            if (data != null) {
              if (data.success == true) {
                // this.$emit("hideElement")
                this.youTubeElement.user_has_saved = !this.youTubeElement
                  .user_has_saved;
                if (this.youTubeElement.user_has_saved) {
                  this.youTubeElement.saved_count += 1;
                  this.snackbar = true;
                  this.snacktext = "Item added to your saved list!";
                } else {
                  this.youTubeElement.saved_count -= 1;
                  this.snackbar = true;
                  this.snacktext = "Item removed from your saved list!";
                }
              } else {
                this.alertType = "error";
              }
            } else {
              this.alertType = "error";
              this.saving = false;
            }
            this.saving = false;
          }
        );
      } catch (err) {
        console.log(err);
      }
    },
    toggleHide() {
      let endpoint = `api/elements/youtube/hide/`;
      try {
        apiService(endpoint, "POST", { pk: this.youTubeElement.id }).then(
          data => {
            this.hiding = true;
            if (data != null) {
              if (data.success == true) {
                this.$emit("hideElement");
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
    }
  }
};
</script>
<style scoped>
a {
  text-decoration: none;
}
.cardimg {
  opacity: 1;
}
</style>
