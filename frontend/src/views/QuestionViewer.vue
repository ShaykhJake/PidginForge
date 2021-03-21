<template>
  <div class="pt-2 sandstone">
    <v-container v-if="!loadingQuestion" fill-height fluid>
      <v-row wrap dense no-gutters>
        <v-col cols="12">
          <v-card>
            <v-card-title class="calligraphy desertsand--text pa-1">
              <v-row dense no-gutters>
                <v-col cols="auto" class="pa-0 ma-0">
                  <QuestionUpDownVote
                    @updateVote="updateVote"
                    :up-vote-count="question.upvote_count"
                    :down-vote-count="question.downvote_count"
                    :user-vote="question.user_vote"
                    :disabled="isQuestionAuthor"
                    :question_id="question.id"
                  />
                </v-col>

                <v-col cols="auto" class="pa-0">
                  <v-card class="calligraphy pa-1 ma-1" outlined>
                    <v-card-text class="pa-0 calligraphy" align="center">
                      <v-avatar class="mr-2" size="42">
                        <v-img
                          class="elevation-6"
                          :src="question.author.user_profile.avatar"
                        ></v-img>
                      </v-avatar>
                    </v-card-text>
                    <v-card-actions align="center">
                      <p class="caption pa-0 ma-0">
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
                            v-if="profileDialog"
                            :profileObject="question.author"
                            :profileDialog="profileDialog"
                            @closeDialog="profileDialog = false"
                          />
                        </v-dialog>
                      </p>
                    </v-card-actions>
                  </v-card>
                </v-col>
                <v-col class="pa-0">
                  <p class="caption mb-0">{{ question.created_at }}</p>
                  <span class="title mb-0">{{ question.title }}</span
                  ><br />
                  <v-chip
                    class="desertsand languages--text text--darken-1 mr-1"
                    x-small
                  >
                    {{ question.nativelanguage }} &#8594;
                    {{ question.learninglanguage }}
                  </v-chip>

                  <v-chip
                    outlined
                    x-small
                    class="sandstone sandstone--text text--lighten-2 ml-1"
                    v-for="tag in question.tags"
                    :key="tag.id"
                    >{{ tag }}</v-chip
                  >
                </v-col>
              </v-row>
            </v-card-title>
            <v-card-text class="desertsand black--text pa-0">
              <editor-content :editor="editor" />
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
                    @click="answerQuestion"
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
                  <AnswerPost
                    v-if="answering"
                    @submitAnswer="submitAnswer"
                    @cancelEdit="cancelEdit"
                  />
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
import AnswerPost from "@/components/questions/AnswerPost.vue";
import ContentFlagger from "@/components/ContentFlagger.vue";
import QuestionUpDownVote from "@/components/questions/QuestionUpDownVote.vue";
import QuestionAuthorActions from "@/components/questions/QuestionAuthorActions.vue";
import { Editor, EditorContent } from "tiptap";
import {
  Blockquote,
  HardBreak,
  Heading,
  Bold,
  Italic,
  Link,
  Strike,
  Underline
} from "tiptap-extensions";
import { default as Alignment } from "@/components/tiptaptoo/Alignment.js";
import { default as TextDirection } from "@/components/tiptaptoo/TextDirection.js";

export default {
  name: "QuestionViewer",
  props: {
    // userData: Object,
    slug: {
      type: String,
      required: true
    }
  },
  components: {
    // AnswerComponent,
    EditorContent,
    QuestionAuthorActions,
    QuestionUpDownVote,
    AnswerView,
    AnswerPost,
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
      },
      editorFontSize: 1,
      editor: new Editor({
        editable: false,
        extensions: [
          new Blockquote(),
          new HardBreak(),
          new Heading({ levels: [3] }),
          new Bold(),
          new Alignment(),
          new TextDirection(),
          new Italic(),
          new Link(),
          new Strike(),
          new Underline()
        ],
        content: `
                            ...loading...
                           `
      })
    };
  },
  computed: {
    editorFontClass() {
      return `font-size:${this.editorFontSize}em`;
    },
    isQuestionAuthor() {
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
    updateVote(data) {
      this.question.user_vote = data.newuservote;
      this.question.downvote_count = data.newdowncount;
      this.question.upvote_count = data.newupcount;
    },
    updateQuestion(data) {
      this.question.title = data.title;
      this.question.rich_text = data.rich_text;
      this.question.nativelanguage = data.nativelanguage;
      this.question.learninglanguage = data.learninglanguage;
      this.question.tags = data.tags;
      this.editor.setContent(this.question.rich_text);
    },

    getQuestionData() {
      this.loadingQuestion = true;
      let endpoint = `/api/questions/questions/${this.slug}/`;
      apiService(endpoint).then(data => {
        if (data) {
          this.question = data;
          this.editor.setContent(this.question.rich_text);
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
      let endpoint = `/api/questions/questions/${this.slug}/answers/`;
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
        let endpoint = `/api/quesetions/questions/${this.slug}/answer/`;
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
    submitAnswer(details) {
      let endpoint = `/api/questions/questions/${this.slug}/answer/`;
      this.submittingAnswer = true;
      console.log(details);
      apiService(endpoint, "POST", { details: details }).then(data => {
        this.answers.unshift(data);
        this.question.user_has_answered = true;
        this.answering = false;
        this.submittingAnswer = false;
      });
    },
    async deleteAnswer(answer) {
      let endpoint = `/api/questions/answers/${answer.id}/`;

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
      let endpoint = `api/questions/question/save/`;
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
    },
    answerQuestion() {
      this.answering = true;
    },
    cancelEdit() {
      this.answering = false;
    }
  },
  created() {
    this.setRequestUser();
    this.getQuestionData();
    this.getQuestionAnswers();
  },
  beforeDestroy() {
    this.editor.destroy();
  }
};
</script>
<style scoped>
>>> .ProseMirror {
  color: black;
  background-color: none;
  padding: 5px 5px 5px 5px;
  height: auto;
  font-size: 1.15em;
  line-height: 1.35em;
  overflow: auto;
  resize: vertical;
  border-color: black;
  border-style: none;
  border-width: 0px;
  border-radius: 5px;
}
>>> .ProseMirror:focus {
  outline: none;
}
</style>
