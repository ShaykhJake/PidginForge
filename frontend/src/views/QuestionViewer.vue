<template>
  <div class="single-question pt-2 sandstone">
    <v-container v-if="!loadingQuestion" fill-height fluid>
      <v-row wrap dense no-gutters>
        <v-col cols="12">
          <v-card>
            <v-card-title class="calligraphy desertsand--text pa-1">
              <v-row dense no-gutters>
                <v-col cols="1" class="pa-0">
                  <v-avatar class="mr-2" size="42">
                    <v-img
                      class="elevation-6"
                      :src="question.author.user_profile.avatar"
                    ></v-img>
                  </v-avatar>
                </v-col>
                <v-col class="pa-0">
                  <v-chip
                    class="desertsand languages--text text--darken-1 mr-1"
                    x-small
                  >
                    {{ question.nativelanguage }} &#8594;
                    {{ question.learninglanguage }}
                  </v-chip>
                  <v-chip
                    class="desertsand topics--text text--darken-1"
                    x-small
                  >
                    {{ question.topic }}
                  </v-chip>
                  <p class="pa-0 ma-0">
                    On {{ question.created_at }},

                    <v-dialog v-model="profileDialog" width="275">
                      <template v-slot:activator="{ on }">
                        <a
                          v-on="on"
                          text
                          small
                          class="primary--text font-weight-bold px-0 py-0"
                        >
                          {{ question.author.username }}
                        </a>
                      </template>
                      <ProfileSnippet
                        :username="question.author.username"
                        @closeDialog="profileDialog = false"
                      />
                    </v-dialog>

                    asked...
                  </p>
                </v-col>
              </v-row>
            </v-card-title>
            <v-card-text class="desertsand black--text">
              <p class="subtitle-1">"{{ question.content }}""</p>
            </v-card-text>
            <v-card-actions class="desertsand">
              <v-row>
                <v-col cols="12" v-if="isQuestionAuthor">
                  <QuestionAuthorActions
                    :slug="slug"
                    :question="question"
                    @updateQuestion="updateQuestion"
                  />
                </v-col>
                <v-col cols="12" v-if="!isQuestionAuthor">
                  <v-btn
                    small
                    @click="answering = true"
                    class="primary desertsand--text mr-1"
                    :disabled="question.user_has_answered"
                  >
                    Answer
                    <v-icon right>mdi-reply</v-icon>
                  </v-btn>

                  <v-btn
                    class="mr-1 saves desertsand--text"
                    @click="toggleSave"
                    :loading="saving"
                    small
                  >
                    <v-badge
                      color="saves lighten-1"
                      :content="question.saved_count"
                    >
                      <span :hidden="question.user_has_saved"
                        >Save<v-icon>mdi-heart</v-icon></span
                      >
                      <span :hidden="!question.user_has_saved"
                        >Unsave<v-icon>mdi-heart-broken</v-icon></span
                      >
                    </v-badge>
                  </v-btn>

                  <v-btn
                    small
                    @click="flaggerDialog = true"
                    :disabled="question.user_has_flagged"
                    class="error desertsand--text mr-1"
                  >
                    <v-badge
                      color="error lighten-1 white--text"
                      :content="question.flag_count"
                    >
                      Flag<v-icon right>mdi-flag</v-icon>
                    </v-badge>
                  </v-btn>
                </v-col>
                <v-col cols="12" v-if="answering">
                  <v-form ref="newAnswer" v-model="valid" class="mt-2">
                    <v-textarea
                      v-model="newAnswer.content"
                      block
                      outlined
                      label="Answer Content*"
                      :rules="[rules.contentMin]"
                      counter
                      rows="3"
                      maxlength="240"
                    ></v-textarea>
                  </v-form>
                  <v-btn
                    small
                    class="success mr-1"
                    @click="submitAnswer"
                    :disabled="!valid"
                    :loading="submittingAnswer"
                  >
                    Submit <v-icon right>mdi-reply</v-icon>
                  </v-btn>
                  <v-btn
                    small
                    class="garbage mr-1 desertsand--text "
                    @click="answering = false"
                  >
                    Cancel<v-icon right>mdi-cancel</v-icon>
                  </v-btn>
                </v-col>
              </v-row>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <v-row wrap dense>
        <v-col v-for="answer in answers" :key="answer.id" cols="12">
          <AnswerView
            :answer="answer"
            :slug="slug"
            @delete-answer="deleteAnswer"
          />
        </v-col>
      </v-row>
    </v-container>
    <ContentFlagger
      :flagger-dialog="flaggerDialog"
      @flagSuccess="flagSuccess"
      @closeDialog="flaggerDialog = false"
      content-type="question"
      :contentid="question.id"
    />
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import AnswerView from "@/components/questions/AnswerView.vue";
import ContentFlagger from "@/components/ContentFlagger.vue";
// import AnswerComponent from "@/components/Answer.vue";
import QuestionAuthorActions from "@/components/questions/QuestionAuthorActions.vue";
export default {
  name: "Question",
  props: {
    // userData: Object,
    slug: {
      type: String,
      required: true
    }
  },
  components: {
    // AnswerComponent,
    QuestionAuthorActions,
    AnswerView,
    ContentFlagger,
    ProfileSnippet: () =>
      import(
        /* webpackPrefetch: true */ "@/components/profile/ProfileSnippet.vue"
      )
  },
  data() {
    return {
      flaggerDialog: false,
      loadingQuestion: false,
      loadingAnswers: false,
      profileDialog: false,
      question: Object,
      answers: [],
      next: null,
      initializing: true,
      questionReady: false,
      error: null,
      showForm: false,
      saving: false,
      requestUser: null,
      newAnswer: {
        content: ""
      },
      answering: false,
      submittingAnswer: false,
      rules: {
        contentMin: value =>
          (value || "").length > 9 || "You must type at least 10 characters!"
      }
    };
  },
  computed: {
    isQuestionAuthor() {
      // return this.question.author.username === this.requestUser;
      return this.question.author.username === this.requestUser;
      // return true;
    }
  },
  methods: {
    setPageTitle(title) {
      document.title = "PidginForge: " + title;
    },
    setRequestUser() {
      return (this.requestUser = window.localStorage.getItem("username"));
    },
    updateQuestion(data) {
      this.question.content = data.content;
      this.question.nativelanguage = this.nativelanguage;
      this.question.learninglanguage = this.learninglanguage;
      this.question.topic = this.topic;
      this.question.tags = this.tags;
    },
    // getQuestionData() {
    //     this.userHasAnswered = this.question.user_has_answered;
    //     this.setPageTitle(this.question.content);
    //     this.questionReady = true;
    // },
    getQuestionData() {
      this.loadingQuestion = true;
      let endpoint = `/api/questions/${this.slug}/`;
      apiService(endpoint).then(data => {
        if (data) {
          this.question = data;
          // this.question = data;
          // this.userHasAnswered = data.user_has_answered;
          // this.setPageTitle(data.content);
          // this.questionReady = true;
          this.loadingQuestion = false;
        } else {
          this.question = null;
          this.setPageTitle("404 - Page Not Found");
          this.loadingQuestion = false;
        }
      });
    },
    getQuestionAnswers() {
      this.loadingAnswers = true;
      let endpoint = `/api/questions/${this.slug}/answers/`;
      if (this.next) {
        endpoint = this.next;
      }
      this.loadingAnswers = true;
      apiService(endpoint).then(data => {
        this.loadingAnswers = false;
        this.answers.push(...data.results);
        this.loadingAnswers = false;
        if (data.next) {
          this.next = data.next;
        } else {
          this.next = null;
        }
      });
    },
    onSubmit() {
      if (this.newAnswerBody) {
        let endpoint = `/api/questions/${this.slug}/answer/`;
        apiService(endpoint, "POST", { body: this.newAnswerBody }).then(
          data => {
            this.answers.unshift(data);
          }
        );
        this.newAnswerBody = null;
        this.showForm = false;
        this.question.user_has_answered = true;
        if (this.error) {
          this.error = null;
        }
      } else {
        this.error = "You can't submit an empty answer!";
      }
    },
    submitAnswer() {
      let endpoint = `/api/questions/${this.slug}/answer/`;
      this.submittingAnswer = true;
      console.log(this.newAnswer.content);
      apiService(endpoint, "POST", { content: this.newAnswer.content }).then(
        data => {
          this.answers.unshift(data);
          this.question.user_has_answered = true;
          this.answering = false;
          this.submittingAnswer = false;
        }
      );
    },
    async deleteAnswer(answer) {
      let endpoint = `/api/answers/${answer.id}/`;
      console.log("deleting");
      try {
        await apiService(endpoint, "DELETE");
        this.$delete(this.answers, this.answers.indexOf(answer));
        this.question.user_has_answered = false;
      } catch (err) {
        // console.log(err)
      }
    },
    toggleSave() {
      this.saving = true;
      let endpoint = `api/question/save/`;
      try {
        apiService(endpoint, "POST", { slug: this.question.slug }).then(
          data => {
            if (data != null) {
              if (data.success == true) {
                // this.$emit("hideElement")
                this.question.user_has_saved = !this.question.user_has_saved;
                if (this.question.user_has_saved) {
                  this.question.saved_count += 1;
                } else {
                  this.question.saved_count -= 1;
                }
                // console.log(data.message)
              } else {
                // this.alertType = 'error';
              }
            } else {
              // this.alertType = 'error';
            }
            this.saving = false;
          }
        );
      } catch (err) {
        console.log(err);
      }
    },
    flagSuccess() {
      this.flaggerDialog = false;
      this.question.user_has_flagged = true;
      this.question.flag_count += 1;
    }
  },
  created() {
    this.setRequestUser();
    this.getQuestionData();
    this.getQuestionAnswers();
  }
};
</script>

<style scoped></style>
