<template>
  <div class="text-micro" v-if="textElement && !textElement.user_has_hidden">
    <v-hover>
      <template v-slot:default="{ hover }">
        <v-card class="pa-0 desertsand">
          <v-card-text class="pa-0">
            <v-row dense class="ma-0 pa-0">
              <v-col cols="12" class="pa-0">
                <v-img
                  src="https://jakesdesk-media.s3.amazonaws.com/media/public/text_files/text_default.jpg"
                  class="cardimg"
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
                    {{ textElement.curator.username }}</span
                  >
                  on {{ textElement.curationdate }}</span
                ><br />
              </v-col>
              <v-col cols="12">
                <span class="subtitle-2">{{ shortTitle }}</span>
              </v-col>
            </v-row>
          </v-card-title>
          <v-card-text>
            <v-row dense>
              <v-col cols="12" class="text-justify"> </v-col>
              <v-col cols="12" class="pa-0 text-center">
                <p class="overline font-weight-light mb-1">
                  <span class="languages--text"> {{ textElement.language }} </span>
                  |<span class="topics--text"> {{ textElement.topic }}</span> |
                  ><br />
                </p>

                <div>
                  <v-btn icon>
                    <v-icon :class="upClass">
                      mdi-arrow-up-circle-outline
                    </v-icon>
                  </v-btn>
                  <span class="green--text font-weight-bold">{{
                    textElement.upvote_count
                  }}</span>
                  /
                  <span class="red--text font-weight-bold">{{
                    textElement.downvote_count
                  }}</span>
                  <v-btn icon>
                    <v-icon :class="downClass">
                      mdi-arrow-down-circle-outline
                    </v-icon>
                  </v-btn>
                </div>

                <p class="primary--text caption mb-0">
                  {{ textElement.saved_count }} Saves - {{ textElement.translations.length || 0 }} Translations - 0 Lessons
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
                  name: 'Text-Viewer',
                  params: {
                    elementslug: textElement.slug
                  }
                }"
                >View Text <v-icon right>mdi-play-circle</v-icon></v-btn
              >
              <v-btn
                block
                class="mb-2 saves"
                @click="toggleSave"
                :loading="saving"
              >
                <span :hidden="textElement.user_has_saved"
                  >Save Text<v-icon right>mdi-heart</v-icon></span
                >
                <span :hidden="!textElement.user_has_saved"
                  >Unsave Text<v-icon right>mdi-heart-broken</v-icon></span
                >
              </v-btn>


              <v-btn
                block
                class="mb-2 garbage desertsand--text"
                @click="toggleHide"
                :loading="hiding"
              >
                <span :hidden="textElement.user_has_hidden"
                  >Hide Text<v-icon right>mdi-eye-off</v-icon></span
                >
                <span :hidden="!textElement.user_has_hidden"
                  >Unhide Text<v-icon right>mdi-eye</v-icon></span
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
// import ElementVoter from "@/components/elements/ElementVoter.vue";
export default {
  name: "TextElementMicro",
  props: {
    textElement: Object
  },
  components: {

  },
  data() {
    return {
      loading: false,
      overlay: false,
      snackbar: false,
      saving: false,
      snacktext: "",
      snacktimeout: 1500,
      hiding: false,
    };
  },
  computed: {
    upClass() {
      if (this.textElement.user_vote === 1) {
        return "success--text";
      } else {
        return "";
      }
    },
    downClass() {
      if (this.textElement.user_vote === -1) {
        return "error--text";
      } else {
        return "";
      }
    },
    shortTitle() {
      let title = this.textElement.title;
      if (title.length > 55) {
        let short = this.textElement.title.slice(0, 55);
        return short + "...";
      } else {
        return title;
      }
    },
    shortPurpose() {
      let purpose = this.textElement.purpose;
      if (purpose.length > 75) {
        let short = this.textElement.purpose.slice(0, 75);
        return short + "...";
      } else {
        return purpose;
      }
    }
  },

  methods: {
    // Get Current User
    // Save / Unsave Item
    toggleSave() {
      this.saving = true;
      let endpoint = `api/elements/text/save/`;
      try {
        apiService(endpoint, "POST", { pk: this.textElement.id }).then(data => {
          if (data != null) {
            if (data.success == true) {
              // this.$emit("hideElement")
              this.textElement.user_has_saved = !this.textElement.user_has_saved;
              if (this.textElement.user_has_saved) {
                this.textElement.saved_count += 1;
                this.snackbar = true;
                this.snacktext = "Item added to your saved list!";
              } else {
                this.textElement.saved_count -= 1;
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
      this.hiding=true;
      let endpoint = `api/elements/text/hide/`;
      try {
        apiService(endpoint, "POST", { pk: this.textElement.id }).then(data => {
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
          this.hiding=false;
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
</style>
