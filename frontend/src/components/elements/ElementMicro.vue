<template>
  <div class="element-micro" v-if="element">
    <v-hover>
      <template v-slot:default="{ hover }">
        <v-card class="pa-0 desertsand">
          <v-card-text class="pa-0">
            <v-row dense class="ma-0 pa-0">
              <v-col cols="12" class="pa-0">
                <v-img
                  :src="element.element.thumb"
                  class="cardimg"
                  :aspect-ratio="16 / 9"
                >
                  <span class="type-span">{{ element.sub_type }}</span>
                </v-img>
              </v-col>
            </v-row>
          </v-card-text>

          <v-card-title class="py-1">
            <v-row dense wrap no-gutters>
              <v-col cols="12">
                <span block class="overline font-weight-light mb-0"
                  ><span class="font-weight-black primary--text">
                    {{ element.curator.username }}</span
                  >
                  on {{ element.curation_date }}</span
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
                    {{ element.language }}
                  </span>
                  |<span
                    v-for="tag in element.tags"
                    class="topics--text"
                    :key="tag.uuid"
                  >
                    {{ tag }}</span
                  >
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
                    element.upvote_count
                  }}</span>
                  /
                  <span class="red--text font-weight-bold">{{
                    element.downvote_count
                  }}</span>
                  <v-btn icon>
                    <v-icon :class="downClass">
                      mdi-arrow-down-circle-outline
                    </v-icon>
                  </v-btn>
                </div>

                <p class="primary--text caption mb-0">
                  {{ element.saved_count }} Saves -
                  {{ element.comment_count }} Comments - 0 Transcripts - 0
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
                  name: 'Element-Viewer',
                  params: {
                    slug: element.slug
                  }
                }"
                >View Element <v-icon right>mdi-play-circle</v-icon></v-btn
              >
              <v-btn
                block
                class="mb-2 saves"
                @click="toggleSave"
                :loading="saving"
              >
                <span :hidden="element.user_has_saved"
                  >Save Element<v-icon right>mdi-heart</v-icon></span
                >
                <span :hidden="!element.user_has_saved"
                  >Unsave Element<v-icon right>mdi-heart-broken</v-icon></span
                >
              </v-btn>

              <v-btn
                block
                class="mb-2 garbage desertsand--text"
                @click="toggleHide"
                :loading="hiding"
              >
                <span :hidden="element.user_has_hidden"
                  >Hide Element<v-icon right>mdi-eye-off</v-icon></span
                >
                <span :hidden="!element.user_has_hidden"
                  >Unhide Element<v-icon right>mdi-eye</v-icon></span
                >
              </v-btn>
            </v-overlay>
          </v-fade-transition>
        </v-card>
      </template>
    </v-hover>
    <v-snackbar v-model="snackbar" :timeout="snacktimeout" top color="success">
      {{ snacktext }}
      <v-btn color="garbage" text @click="snackbar = false"> Close </v-btn>
    </v-snackbar>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "ElementMicro",
  props: {
    element: Object
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
      if (
        this.element.sub_type === "Audio" ||
        this.element.sub_type === "YouTube"
      ) {
        let totalseconds = this.element.element.duration;
        var hours = totalseconds / 3600,
          minutes = (hours % 1) * 60,
          seconds = (minutes % 1) * 60;
        let hoursText = "";
        let minutesText = "";
        let secondsText = "";
        if (hours === 0) {
          hoursText = "0";
        } else {
          hoursText = Math.floor(hours);
        }
        if (minutes === 0) {
          minutesText = "00";
        } else if (minutes < 10) {
          minutesText = `0${Math.floor(minutes)}`;
        } else {
          minutesText = Math.floor(minutes);
        }
        if (seconds === 0) {
          secondsText = "00";
        } else if (seconds < 10) {
          secondsText = `0${Math.floor(seconds)}`;
        } else {
          secondsText = Math.floor(seconds);
        }
        return `${hoursText}:${minutesText}:${secondsText}`;
      } else {
        return 0;
      }
    },
    shortTitle() {
      let title = this.element.title;
      if (title.length > 55) {
        let short = this.element.title.slice(0, 55);
        return short + "...";
      } else {
        return title;
      }
    },
    shortDescription() {
      let description = this.element.description;
      if (description.length > 75) {
        let short = this.element.description.slice(0, 75);
        return short + "...";
      } else {
        return description;
      }
    },
    upClass() {
      if (this.element.user_vote === 1) {
        return "success--text";
      } else {
        return "";
      }
    },
    downClass() {
      if (this.element.user_vote === -1) {
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
      let endpoint = `api/elements/save/element/`;
      try {
        apiService(endpoint, "POST", { pk: this.element.id }).then(data => {
          if (data != null) {
            if (data.success == true) {
              // this.$emit("hideElement")
              this.element.user_has_saved = !this.element.user_has_saved;
              if (this.element.user_has_saved) {
                this.element.saved_count += 1;
                this.snackbar = true;
                this.snacktext = "Item added to your saved list!";
              } else {
                this.element.saved_count -= 1;
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
        });
      } catch (err) {
        console.log(err);
      }
    },
    toggleHide() {
      let endpoint = `api/elements/hide/element/`;
      try {
        apiService(endpoint, "POST", { pk: this.element.id }).then(data => {
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
        });
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

.type-span {
  background-color: black;
  color: white;
  opacity: 0.8;
  padding-left: 2px;
  padding-right: 2px;
  border-bottom-left-radius: 5px;
  font-weight: bold;
  margin-right: 0;
  float: right;
}
</style>
