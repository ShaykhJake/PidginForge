<template>
  <div class="question-micro">
    <v-hover>
      <template v-slot:default="{ hover }">
        <v-card class="pa-0 desertsand">
          <v-card-title class="py-1 desertsand">
            <v-row dense no-gutters>
              <v-col>
                <span class="overline">
                  <span class="primary--text font-weight-black">
                    {{ question.author.username }}</span
                  >
                  asked on {{ question.created_at }}:
                </span>
              </v-col>
            </v-row>
          </v-card-title>

          <v-card-text class="pa-0">
            <v-row dense class="ma-0 pa-0">
              <v-col cols="auto pr-2">
                <v-avatar mx-2 size="48">
                  <v-img
                    class="elevation-6"
                    :src="question.author.user_profile.avatar"
                  ></v-img>
                </v-avatar>
              </v-col>

              <v-col>
                <p class="subtitle-2 black--text">{{ shortQuestion }}</p>
              </v-col>
            </v-row>
          </v-card-text>

          <v-card-title>
            <v-row dense no-gutters>
              <v-col align="center">
                <p class="overline font-weight-light mb-0">
                  <span class="languages--text">
                    {{ question.nativelanguage }} &#8594;
                    {{ question.learninglanguage }}
                  </span>
                  |<span class="topics--text"> {{ question.topic }}</span
                  ><br />
                </p>
                <p class="primary--text overline mb-0">
                  {{ question.answers_count }} Answers
                </p>
              </v-col>
            </v-row>
          </v-card-title>

          <v-fade-transition>
            <v-overlay v-if="hover" absolute color="calligraphy" opacity="0.75">
              <v-btn
                block
                class="mb-2 primary"
                :to="{
                  name: 'Question-Viewer',
                  params: { slug: question.slug }
                }"
                >View Question <v-icon right>mdi-help-circle</v-icon></v-btn
              >
              <v-btn block class="mb-2 saves" @click="toggleSave">
                <span :hidden="question.user_has_saved"
                  >Like Question<v-icon right>mdi-heart</v-icon></span
                >
                <span :hidden="!question.user_has_saved"
                  >Unlike Video<v-icon right>mdi-heart-broken</v-icon></span
                >
              </v-btn>
            </v-overlay>
          </v-fade-transition>
        </v-card>
      </template>
    </v-hover>
  </div>
</template>

<script>
// import { apiService } from "@/common/api.service.js";
export default {
  name: "QuestionMicro",
  props: {
    question: Object
  },
  data() {
    return {
      loading: false,
      overlay: false
    };
  },
  computed: {
    shortQuestion() {
      let question = this.question.content;
      if (question.length > 100) {
        let short = this.question.content.slice(0, 100);
        return short + "...";
      } else {
        return question;
      }
    }
  },

  methods: {
    // Get Current User
    // Save / Unsave Item
    toggleSave() {
      // let endpoint=`api/elements/youtube/saved/`;
      // try {
      // apiService(endpoint, "POST", { pk: this.youTubeElement.id }).then(data => {
      //    this.submitting = false;
      //    if (data != null) {
      //       if (data.success == true){
      //          // this.$emit("hideElement")
      //          this.youTubeElement.user_has_saved = !this.youTubeElement.user_has_saved;
      //          if (this.youTubeElement.user_has_saved){
      //             this.youTubeElement.saved_count += 1
      //          } else {
      //             this.youTubeElement.saved_count -= 1
      //          }
      //          console.log(data.message)
      //       } else {
      //          this.alertType = 'error';
      //       }
      //    } else {
      //       this.alertType = 'error';
      //    }
      // });
      // } catch (err) {
      // console.log(err);
      // }
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
