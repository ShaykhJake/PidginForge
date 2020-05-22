<template>
  <v-dialog
    v-model="editorDialog"
    scrollable
    persistent
    fullscreen
    hide-overlay
    transition="dialog-bottom-transition"
  >
    <v-card class="calligraphy desertsand--text mb-2">
      <v-card-title class="py-1">
        Multiple Choice Quiz: "{{ quiz.title ? quiz.title.substr(0,25) : 'Untitled'}}"
      </v-card-title>
      <v-card-text v-show="showingQuiz" class="px-2 pt-0">
        <v-card class="desertsand">
          <v-card-title>
            Metadata
            <v-spacer></v-spacer>
            <v-btn fab icon class="mx-1 primary--text" @click="showingMetadata=!showingMetadata">
              <v-icon v-if="showingMetadata">mdi-menu-up</v-icon>
              <v-icon v-else>mdi-menu-down</v-icon>
            </v-btn>

          </v-card-title>
          <v-card-text v-show="showingMetadata">
            <v-form
              ref="mcametadata"
              v-model="metadataValid"
              @submit.prevent
            >
              <v-text-field
                v-model="quiz.title"
                name="quiztitle"
                label="Quiz Title*"
                placeholder="Give your quiz a title..."
                :rules="[rules.requiredTitle]"
                outlined
                class="pb-0 mb-0"
              ></v-text-field>

              <v-textarea
                outlined
                name="objective"
                label="Learning Objective*"
                placeholder="What is the learning objective of your quiz?"
                v-model="quiz.objective"
                :rules="[rules.requiredObjective]"
                counter
                rows="3"
                maxlength="400"
              ></v-textarea>

              <v-autocomplete
                v-model="quiz.native_language"
                name="nativelanguage"
                :items="allLanguages"
                label="Native Language*"
                placeholder="choose a native language"
                :rules="[rules.requiredLanguage]"
                required
                :loading="loadingLanguages"
                outlined
              ></v-autocomplete>

              <v-autocomplete
                v-model="quiz.target_language"
                name="targetlanguage"
                :items="allLanguages"
                label="Target Language*"
                placeholder="choose a target language"
                :rules="[rules.requiredLanguage]"
                required
                :loading="loadingLanguages"
                outlined
              ></v-autocomplete>

              <v-autocomplete
                v-model="quiz.topic"
                name="eventtopic"
                :items="allTopics"
                label="Primary Topic*"
                placeholder="choose the primary topic"
                :rules="[rules.requiredTopic]"
                required
                :loading="loadingTopics"
                outlined
              ></v-autocomplete>

              <v-switch
                v-model="quiz.test_direction_rtl"
                label="Test Direction Right-to-Left"
                color="primary"
                hint="Turning this on will affect the display of navigation buttons"
                persistent-hint
              ></v-switch>

              <v-switch
                v-model="quiz.randomize_questions"
                label="Randomize Question Order"
                color="primary"
                hint="Leave This Off to Preserve Question Order"
                persistent-hint
              ></v-switch>

              <br><br>
              <span class="body-1">Allowed Number of Retest Attempts</span>
              <v-slider
                v-model="quiz.retest_attempts"
                min="0"
                max="3"
                step="1"
                ticks="always"
                tick-size="8"
                :tick-labels="retest_attempts_options"
              >
              </v-slider>
              <br>
              <span class="body-1">Feedback Granularity</span>
              <v-slider
                v-model="quiz.feedback_granularity"
                min="0"
                max="2"
                step="1"
                ticks="always"
                tick-size="8"
                :tick-labels="feedback_options"
              >
              </v-slider>

            </v-form>
            <br>
            <p v-if="isNewQuiz" class="primary--text text--darken-2 mb-0">
              You must submit valid metadata in order to
              build a new quiz prior to attaching questions.
            </p>
          </v-card-text>
          <v-card-actions v-if="isNewQuiz">
            <v-spacer />
            <v-btn 
              class="primary desertsand--text" 
              :disabled="!metadataValid"
              :loading="building"
              @click="buildNewQuiz"
            >
              Build Quiz
              <v-icon right>mdi-domain</v-icon>
            </v-btn>
            <v-spacer />
          </v-card-actions>
          </v-card>
          <v-card v-if="!isNewQuiz" class="desertsand mt-3">
            <v-card-title>
              Question Set ({{ questionSet.length }})
              <v-spacer></v-spacer>
              <v-btn 
                small 
                class="primary desertsand--text ml-2 mb-1"
                @click="addQuestion"
              >
                Add Question
                <v-icon>mdi-plus-circle</v-icon>
              </v-btn>
              <v-btn fab icon class="mx-1 primary--text" @click="showingQuestions=!showingQuestions">
                <v-icon v-if="showingQuestions">mdi-menu-up</v-icon>
                <v-icon v-else>mdi-menu-down</v-icon>
              </v-btn>
            </v-card-title>

            <v-card-text v-show="showingQuestions" class="px-2"> 

                <MCQQuestionEditor
                  v-for="(question, index) in questionSet"
                  :key="index"
                  :question-index="index"
                  :total-questions="questionSet.length"
                  :question="question"
                  @updateQuestion="updateQuestion"
                  @deleteQuestion="deleteQuestion"
                  @changeQuestionOrder="changeQuestionOrder"
                />         
            </v-card-text>
          </v-card>
      </v-card-text>
      <v-card-actions class="calligraphy">
        <v-spacer></v-spacer>
        <v-btn color="garbage desertsand--text" @click="closeDialog"
          >Cancel<v-icon right>mdi-close</v-icon>
        </v-btn>

        <v-btn
          color="success"
          @click="saveMCQ"
          :disabled="!metadataValid || !isNewQuiz"
          :loading="saving"
          >Save<v-icon right>mdi-thumb-up</v-icon></v-btn
        >
        <v-spacer></v-spacer>
        <!-- TODO: need to ensure that the user information is reloaded after saving -->
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
// import VueYouTubeEmbed from 'vue-youtube-embed'
import { apiService } from "@/common/api.service.js";
import MCQQuestionEditor from "@/components/quizzes/MCQQuestionEditor.vue";
export default {
  name: "MCQEditor",
  props: {
    editorDialog: {
      type: Boolean,
      default: false,
    },
    slug: {
      type: String,
      required: false,
    },
  },
  components: {
    MCQQuestionEditor,
  },
  data() {
    return {
      quiz: {},
      isNewQuiz: true,
      questionSet: {},
      editing: true,
      loaded: false,
      saving: false,
      building: false,
      valid: false,

      loadingLanguages: false,
      loadingTopics: false,
      showingQuiz: true,
      allTopics: [],
      allLanguages: [],

      metadataValid: false,

      showingMetadata: true,
      showingQuestions: true,
      retest_attempts_options: [
        'None',
        '1',
        '2',
        'Infinite',
      ],
      feedback_options: [
        'Score Only',
        'By Question',
        'By Individual Alternative',
      ],
      editorFontSize: 1,

      selectTypes: ["single",
                    "multiple", 
      ],
      rules: {
        requiredTitle: value =>
          (value || "").length > 3 ||
          "Title length must be at least 4 characters.",

        requiredObjective: value =>
          (value || "").length > 9 ||
          "Objective length must be at least 9 characters.",

        requiredType: typevalue =>
          (typevalue || "").length > 0 || "You must choose an event type.",

        requiredSkillLevel: languagevalue =>
          (languagevalue || "").length > 0 || "You must choose a skill level.",
        
        requiredLanguage: languagevalue =>
          (languagevalue || "").length > 0 || "You must choose a language.",

        requiredTopic: topicvalue =>
          (topicvalue || "").length > 0 || "You must choose a primary topic.",

      },
    };
  },
  computed: {

  },
  methods: {
      updateQuestion(payload){
        this.questionSet[payload.questionIndex]=payload.question;
        this.$emit("updateQuiz", this.quiz)
        console.log(payload)
      },
      closeDialog(){
        this.$emit("closeDialog");
      },
      discardNewQuiz(){
        this.quiz={};
        this.isNewQuiz=true;
        this.loaded=false;
        this.closeDialog();
      },
      buildNewQuiz(){
        // check validity
        // creat API Payload
        // Submit Payload, wait for data
        this.isNewQuiz=false;
        // push New Quiz Up to parent
        this.questionSet=[];
      },
      addQuestion(){
         var questionIDs = [];
         for(let i = 0; i < this.questionSet.length; i++){
            questionIDs.push(this.questionSet[i].id)
         }
         for(let i = 0; i < this.questionSet.length + 1; i++){
            if(!questionIDs.includes(i.toString())){
               var newQuestionID = i.toString();
               break
            }
         };
         let newQuestion={
            id: newQuestionID,
            multiple_select:false,
            rich_content: {
                "enabled":false,
                "content_type":"", // Audio/Video/Text/Photo
                "content":{} // (Audio: URL, Video: URL, Text: JSON Pack, Photo: URL)
              },
            stem:"New question...",
            stem_rtl:false,
            alternatives_rtl:false,
            randomize_alternatives: false,
            alternatives:[],
         }
         this.questionSet.push(newQuestion);
      },
      deleteQuestion(index){
          this.questionSet.splice(index,1);
      },

      changeQuestionOrder(payload){
         if (payload.direction === "up"){
            let tmp = this.questionSet[payload.index];
            this.questionSet.splice(payload.index,1);
            this.questionSet.splice(payload.index-1,0,tmp);
         } else {
            let tmp = this.questionSet[payload.index];
            this.questionSet.splice(payload.index,1);
            this.questionSet.splice(payload.index+1,0,tmp);
         }
      },
      deleteQuiz(index){
        this.$emit("deleteQuiz", index);
      },
      changeQuizOrder(direction, index){
         this.$emit("changeQuizOrder", { direction: direction, index: index})
      },
      saveMCQ(){
        return false;
      },
      getLanguages() {
      var localLanguages = localStorage.getItem("languages");
      if (localLanguages.length > 1) {
        console.log("Shop local!");
        this.allLanguages = JSON.parse(localLanguages);
      } else {
        this.loadingLanguages = true;
        let endpoint = `/api/categories/languages/`;
        try {
          apiService(endpoint).then(data => {
            if (data != null) {
              this.allLanguages = data;
              this.error = false;
            } else {
              console.log("Something bad happened...");
              this.error = true;
            }
            this.loadingLanguages = false;
          });
        } catch (err) {
          console.log(err);
        }
      }
    },

    getTopics() {
      var localTopics = localStorage.getItem("topics");
      if (localTopics.length > 1) {
        console.log("Shop local!");
        this.allTopics = JSON.parse(localTopics);
      } else {
        this.loadingTopics = true;
        let endpoint = `/api/categories/topics/`;
        try {
          apiService(endpoint).then(data => {
            if (data != null) {
              this.allTopics = data;
              this.error = false;
            } else {
              console.log("Something bad happened...");
              this.error = true;
            }
            this.loadingTopics = false;
          });
        } catch (err) {
          console.log(err);
        }
      }
    }
  },
  mounted(){
    this.getLanguages();
    this.getTopics();
    if(!this.slug){
      // test data
      this.quiz={
        "quiz_type": "multiple_choice",
        "title":"Test Title",
        "objective":"testing user retention",
        "native_language":"English",
        "target_language":"Arabic-MSA",
        "topic":"crafts",
        "test_direction_rtl":false,
        "randomize_questions":true,
        "retest_attempts": "3", // 0 = off, 1, 2, 3 = infinite
        "feedback_granularity": "2", // 0= "score", 1="by_question", 2="all"
      }
      this.isNewQuiz=true;
    } else {
      this.isNewQuiz=false;
      // load quiz by slug...
    }
    this.loaded = true;

  },
  beforeDestroy() {

  }
};
</script>
<style type="text/css"></style>
