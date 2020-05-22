<template>
  <div class="lesson-micro" v-if="lesson && !lesson.user_has_hidden">
    <v-hover>
      <template v-slot:default="{ hover }">
        <v-card class="pa-0 desertsand">
          <v-card-text class="pa-0">
            <v-row dense class="ma-0 pa-0">
              <v-col cols="12" class="pa-0">
                <v-img
                  src="https://jakesdesk-media.s3.amazonaws.com/media/public/lesson_files/defaultlesson.jpg"
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
                    {{ lesson.curator.username }}</span
                  >
                  on {{ lesson.curationdate }}</span
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
                  <span class="languages--text"> {{ lesson.native_language }} -> {{lesson.target_language}} </span>
                  |<span class="topics--text"> {{ lesson.topic }}</span> |
                  ><br />
                </p>

                <div>
                  <v-btn icon>
                    <v-icon :class="upClass">
                      mdi-arrow-up-circle-outline
                    </v-icon>
                  </v-btn>
                  <span class="green--text font-weight-bold">{{
                    lesson.upvote_count
                  }}</span>
                  /
                  <span class="red--text font-weight-bold">{{
                    lesson.downvote_count
                  }}</span>
                  <v-btn icon>
                    <v-icon :class="downClass">
                      mdi-arrow-down-circle-outline
                    </v-icon>
                  </v-btn>
                </div>

                <p class="primary--text caption mb-0">
                  {{ lesson.saved_count }} Saves -
                  # of Quizzes
                  # of Vocabulary
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
                  name: 'Lesson-Viewer',
                  params: {
                    lessonslug: lesson.slug
                  }
                }"
                >View Lesson <v-icon right>mdi-play-circle</v-icon></v-btn
              >
              <v-btn
                block
                class="mb-2 saves"
                @click="toggleSave"
                :loading="saving"
              >
                <span :hidden="lesson.user_has_saved"
                  >Save Lesson<v-icon right>mdi-heart</v-icon></span
                >
                <span :hidden="!lesson.user_has_saved"
                  >Unsave Lesson<v-icon right>mdi-heart-broken</v-icon></span
                >
              </v-btn>

              <v-btn
                block
                class="mb-2 garbage desertsand--text"
                @click="toggleHide"
                :loading="hiding"
              >
                <span :hidden="lesson.user_has_hidden"
                  >Hide Lesson<v-icon right>mdi-eye-off</v-icon></span
                >
                <span :hidden="!lesson.user_has_hidden"
                  >Unhide Lesson<v-icon right>mdi-eye</v-icon></span
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
  name: "LessonMicro",
  props: {
    lesson: Object
  },
  components: {
    // AudioUpDownVote
  },
  data() {
    return {
      loading: false,
      overlay: false,
      snackbar: false,
      saving: false,
      snacktext: "",
      snacktimeout: 1500,
      hiding: false
    };
  },
  computed: {
    upClass() {
      if (this.lesson.user_vote === 1) {
        return "success--text";
      } else {
        return "";
      }
    },
    downClass() {
      if (this.lesson.user_vote === -1) {
        return "error--text";
      } else {
        return "";
      }
    },
    shortTitle() {
      let title = this.lesson.title;
      if (title.length > 55) {
        let short = this.lesson.title.slice(0, 55);
        return short + "...";
      } else {
        return title;
      }
    },
    shortObjective() {
      let objective = this.lesson.objective;
      if (objective.length > 75) {
        let short = this.lesson.objective.slice(0, 75);
        return short + "...";
      } else {
        return objective;
      }
    }
  },

  methods: {
    // Get Current User
    // Save / Unsave Item
    toggleSave() {
      this.saving = true;
      let endpoint = `api/lessons/save/`;
      try {
        apiService(endpoint, "POST", { pk: this.lesson.id }).then(data => {
          if (data != null) {
            if (data.success == true) {
              this.lesson.user_has_saved = !this.lesson.user_has_saved;
              if (this.lesson.user_has_saved) {
                this.lesson.saved_count += 1;
                this.snackbar = true;
                this.snacktext = "Item added to your saved list!";
              } else {
                this.lesson.saved_count -= 1;
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
      this.hiding = true;
      let endpoint = `api/lessons/hide/`;
      try {
        apiService(endpoint, "POST", { pk: this.lesson.id }).then(data => {
          this.hiding = true;
          if (data != null) {
            if (data.success == true) {
              this.$emit("hideLesson");
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
</style>
