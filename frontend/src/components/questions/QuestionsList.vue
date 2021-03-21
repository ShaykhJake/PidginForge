<template>
  <div>
    <v-card>
      <v-toolbar class="desertsand calligraphy--text" dense>
        <v-toolbar-title
          >New Community Questions
          <small v-if="totalCount > 0"
            >({{ questions.length }} of {{ totalCount }} loaded)</small
          >
          <small v-else>(no results)</small>
        </v-toolbar-title>
        <v-spacer></v-spacer>

        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" icon @click="setPreference" class="garbage--text">
              <v-icon v-if="!byPreference">toggle_off</v-icon>
              <v-icon class="primary--text" v-if="byPreference"
                >toggle_on</v-icon
              >
            </v-btn>
          </template>
          <span>Filter by Preference</span>
        </v-tooltip>

        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn icon v-on="on" class="primary--text" @click="refreshList">
              <v-icon>refresh</v-icon>
            </v-btn>
          </template>
          <span>Refresh List</span>
        </v-tooltip>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn
              icon
              v-on="on"
              class="primary--text"
              @click="loadQuestionEditor"
            >
              <v-icon>mdi-help</v-icon>
            </v-btn>
          </template>
          <span>Ask a Question</span>
        </v-tooltip>

        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn
              v-on="on"
              icon
              @click="showQuestions = !showQuestions"
              class="garbage--text"
            >
              <v-icon v-if="!showQuestions">mdi-eye</v-icon>
              <v-icon v-if="showQuestions">mdi-eye-off</v-icon>
            </v-btn>
          </template>
          <span v-if="!showQuestions">View Questions</span>
          <span v-else>Hide Questions</span>
        </v-tooltip>
      </v-toolbar>
      <v-card-text v-show="showQuestions" class="content-box calligraphy pa-1">
        <div class="questionlist">
          <v-row wrap dense v-if="questions.length < 1 && !loadingQuestions">
            <v-col cols="12">
              <v-card>
                <v-card-text class="desertsand calligraphy--text">
                  There are no questions which match your language/topic
                  preferences. You may need to update your profile to add
                  learning languages and topics...or maybe we just don't have
                  enough content yet!
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
          <v-row dense wrap v-if="questions.length > 0">
            <v-col
              cols="12"
              sm="6"
              md="4"
              lg="3"
              v-for="question in questions"
              :key="question.id"
            >
              <QuestionMicro :question="question" />
            </v-col>
          </v-row>
          <v-btn
            v-if="next"
            @click="getQuestions"
            :loading="loadingQuestions"
            class="primary desertsand--text"
            block
          >
            Load More Questions <v-icon right>mdi-chevron-down</v-icon>
          </v-btn>
          <v-overlay :value="loadingQuestions" absolute>
            <v-progress-circular indeterminate size="64"></v-progress-circular>
          </v-overlay>
        </div>
      </v-card-text>
    </v-card>

    <QuestionEditor
      v-if="showQuestionEditor"
      :editor-dialog="showQuestionEditor"
      @closeDialog="showQuestionEditor = false"
    />
  </div>
</template>

<script>
  import { apiService } from "@/common/api.service.js";
  import QuestionMicro from "@/components/questions/QuestionMicro.vue";
  export default {
    name: "QuestionsList",
    data() {
      return {
        questions: [],
        next: null,
        totalCount: 0,
        loadingQuestions: false,
        showQuestions: true,
        askQuestionDialog: false,
        questionEditorLoaded: false,
        showQuestionEditor: false,
        byPreference: true,
      };
    },
    components: {
      QuestionMicro,
      QuestionEditor: () =>
        import(
          /* webpackPrefetch: true */ "@/components/questions/QuestionEditor.vue"
        ),
    },
    computed: {},

    methods: {
      setPreference() {
        this.byPreference = !this.byPreference;
        this.questions = [];
        this.totalCount = 0;
        this.next = null;
        this.getQuestions();
      },
      loadQuestionEditor() {
        this.questionEditorLoaded = true;
        this.showQuestionEditor = !this.showQuestionEditor;
      },

      getQuestions() {
        let endpoint = String;
        if(this.byPreference){
          endpoint = "/api/questions/list/?by_preference=True";
        } else {
          endpoint = "/api/questions/list/";
        }
        if (this.next) {
          endpoint = this.next;
        }
        this.loadingQuestions = true;
        apiService(endpoint).then((data) => {
          this.totalCount = data.count;
          this.questions.push(...data.results);

          this.loadingQuestions = false;
          if (data.next) {
            this.next = data.next;
          } else {
            this.next = null;
          }
        });
      },
      refreshList() {
        this.questions = [];
        this.next = null;
        this.getQuestions();
      },
    },
    created() {
      this.getQuestions();
    },
  };
</script>
<style scoped>
  .question-author {
    font-weight: bold;
    color: maroon;
  }
  .question-link {
    font-weight: bold;
    color: black;
  }
  .question-link:hover {
    font-weight: bold;
    color: gray;
    text-decoration: none;
  }
</style>
