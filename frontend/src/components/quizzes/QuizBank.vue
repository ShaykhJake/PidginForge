<template>
  <div>
  <v-data-table
    :headers="headers"
    :items="quizzes"
    sort-by="quiz"
    class="elevation-5 mb-2 desertsand"
  >
    <template v-slot:top>
      <v-toolbar flat color="desertsand">
        <v-toolbar-title>Quizzes</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>

          <v-menu offset-y>
            <template v-slot:activator="{ on }">
              <v-btn 
                small 
                class="primary desertsand--text mx-1" 
                v-on="on">
                Add Quiz
                <v-icon right>mdi-plus</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item
                v-for="(quizType, index) in quizTypes"
                :key="index"
                @click="addNewQuiz(quizType.quiz_type)"
                :disabled="!quizType.available"
              >
                <v-list-item-title>{{ quizType.name }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>



          <v-dialog v-model="dialog" max-width="500px">
            <v-card>
              <v-card-title>
                <span class="headline">{{ formTitle }}</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="editedItem.quiz"
                        label="Quiz"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="editedItem.translation"
                        label="Translation"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="editedItem.partofspeech"
                        label="Part of Speech"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="editedItem.root"
                        label="Root"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="editedItem.context"
                        label="Context"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
                <v-btn color="blue darken-1" text @click="save">Save</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon small class="mr-2" @click="editItem(item)">
        mdi-pencil
      </v-icon>
      <v-icon small @click="deleteItem(item)">
        mdi-delete
      </v-icon>
    </template>
    <template v-slot:no-data>
      <v-btn color="primary" @click="initialize">Reset</v-btn>
    </template>
  </v-data-table>





    <v-card v-show="false">
      <v-card-title class="sandstone py-1">
        {{`Quiz Bank (${this.quizPackage.length}) `}}
        <v-spacer></v-spacer>
        <v-btn
          small
          class="primary desertsand--text"
          @click="previewMode=!previewMode"
        >
          <span v-if="!previewMode">Preview Mode</span>
          <span v-if="previewMode">Edit Mode</span>
        </v-btn>
        <v-btn fab icon class="mx-1 primary--text" @click="showingQuizBank=!showingQuizBank">
            <v-icon v-if="showingQuizBank">mdi-menu-up</v-icon>
            <v-icon v-else>mdi-menu-down</v-icon>
        </v-btn>
        
      </v-card-title>



      <v-card-text v-if="quizPackage.length > 0" v-show="showingQuizBank" class="desertsand pa-2">
        <div           
          v-for="(quiz, index) in quizPackage" 
          :key="index"
        >
        </div>
      </v-card-text>
    </v-card>

    <v-card v-if="previewMode">
      LET'S PREVIEW!
    </v-card>
    <MCQEditor
      v-if="MCQEditorDialog"
      :editor-dialog="MCQEditorDialog"
      :slug="MCQSlug"
      @closeDialog="MCQEditorDialog=false"
    />

  </div>
</template>

<script>
import MCQEditor from "@/components/quizzes/MCQEditor.vue";
export default {
  name: "QuizBank",
  components: {
    MCQEditor
  },
  data: () => ({

    showingQuizBank: true,
    previewMode: false,

    dialog: false,
    MCQEditorDialog: false,
    MCQSlug: null,
    
    returnCommand: function() {},
    headers: [
      {
        text: "Quiz",
        align: "start",
        value: "title"
      },
      { text: "# of Items", value: "items_count" },
      { text: "Published", value: "published" },
      { text: "Times Taken", value: "attempts" },
      { text: "Average Score", value: "average_score" },
      { text: "Actions", value: "actions", sortable: false }
    ],
    quizs: [],
    editedIndex: -1,
    editedItem: {
      quiz: "",
      translation: "",
      partofspeech: "",
      root: "",
      context: ""
    },
    defaultItem: {
      quiz: "",
      translation: "",
      partofspeech: "",
      root: "",
      context: ""
    },

    quizTypes: [
      { name: "Multiple Choice", quiz_type: "multiple_choice", icon: "mdi-close", available: true, },
      { name: "Cloze Exercise", quiz_type: "cloze", icon: "mdi-close", available: false, },
      { name: "Transcription", quiz_type: "transcription", icon: "mdi-close", available: false, },
      { name: "Translation", quiz_type: "translation", icon: "mdi-close", available: false,},
      { name: "Constructed Response", quiz_type: "constructed_response", icon: "mdi-close", available: false, },
    ],
    mcActivities: [],
    clozeActivities: [],
    translationActivities: [],
    transcriptionActivites: [],
    crActivities: [],
    quizPackage: [
        { 
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
          "question_set": [
            { 
              "id": "1",
              "multiple_select":true,
              "rich_content": {
                 "enabled":false,
                 "content_type":"", // Audio/Video/Text/Photo
                 "content":{} // (Audio: URL, Video: URL, Text: JSON Pack, Photo: URL)
               },
              "stem":"Which of the following is/are non-essential nutrients?",
              "stem_rtl":false,
              "alternatives_rtl":false,
              "randomize_alternatives": false,
              "alternatives":[
                { 
                  "text":"pizza",
                  "id":"0",
                  "feedback":"a human can live for at least 100 years without pizza; it is not essential",
                },
                { 
                  "text":"carbohydrates",
                  "id":"1",
                  "feedback":"despite what fascists say, the human body does not need carbohydrates",
                },
                { 
                  "text":"fat",
                  "id":"2",
                  "feedback":"fat is essential",
                },
                { 
                  "text":"protein",
                  "id":"3",
                  "feedback":"protein is essential",
                },
              ],
              "answer_key": ["0", "1",],
              "explanation": "Only protein and fat are essential; humans can get by without pizza and carbs!",
            },
            { 
              "id": "2",
              "multiple_select":false,
              "rich_content": {
                 "enabled":false,
                 "content_type":"", // Audio/Video/Text/Photo
                 "content":{} // (Audio: URL, Video: URL, Text: JSON Pack, Photo: URL)
               },              "stem":"I am a tree.",
              "stem_rtl":false,
              "alternatives_rtl":false,
              "randomize_alternatives": false,
              "alternatives":[
                { 
                  "text":"True",
                  "id":"0",
                  "feedback":"",
                },
                { 
                  "text":"False",
                  "id":"1",
                  "feedback":"",
                },
              ],
              "answer_key": "1",
              "explanation": "I am not a tree, I am a person.",
            },
            { 
              "id": "3",
              "multiple_select":false,
              "rich_content": {
                 "enabled":false,
                 "content_type":"", // Audio/Video/Text/Photo
                 "content":{} // (Audio: URL, Video: URL, Text: JSON Pack, Photo: URL)
               },              "stem":"شو اسمك يا كريم؟",
              "stem_rtl":true,
              "alternatives_rtl":true,
              "randomize_alternatives": false,
              "alternatives":[
                { 
                  "text":"كريم",
                  "id":"0",
                  "feedback":"",
                },
                { 
                  "text":"يعقوب",
                  "id":"1",
                  "feedback":"",
                },
                { 
                  "text":"عبدلله",
                  "id":"2",
                  "feedback":"",
                },
                { 
                  "text":"ما فيه اسم",
                  "id":"3",
                  "feedback":"",
                },

              ],
              "answer_key": "0",
              "explanation": "You should know that your name is كريم!",
            },
          ]
        },
        // {
        //   "activitiy_type": "cloze",
        // },
        // {
        //   "activitiy_type": "translation",
        // },
        // {
        //   "activitiy_type": "transcription",
        // },
        // {
        //   "activitiy_type": "constructed_response",
        // },
      ]

  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Quiz" : "Edit Quiz";
    }
  },
  
  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  created() {
    this.initialize();
  }, 
  methods: {
    updateMCQuiz(quiz){
      this.quizPackage.multiple_choice = quiz;
    },
    deleteQuiz(index){
        this.quizPackage.splice(index,1);
    },
    addNewQuiz(quizType){
      if(quizType=="multiple_choice"){
        this.MCQEditorDialog=true;
      } else {
        return false;
      }
    },
    changeQuizOrder(payload){
        if (payload.direction === "up"){
          let tmp = this.quizPackage[payload.index];
          this.quizPackage.splice(payload.index,1);
          this.quizPackage.splice(payload.index-1,0,tmp);
        } else {
          let tmp = this.quiz[payload.index];
          this.quizPackage.splice(payload.index,1);
          this.quizPackage.splice(payload.index+1,0,tmp);
        }
    },

    initialize() {
      this.quizzes = [
        {
          title: "اشترك في",
          id: 1,
          published: false,
          quiz_type: "Multiple Choice",
          items_count: 5,
          attempts: 10,
          average_score: "25%",
        },
        {
          title: "Fun Stuff",
          id: 2,
          published: true,
          quiz_type: "Close Exercise",
          items_count: 5,
          attempts: 10,
          average_score: "25%",
        },
        {
          title: "اشترك في",
          id: 3,
          published: false,
          quiz_type: "Multiple Choice",
          items_count: 5,
          attempts: 10,
          average_score: "25%",
        }
      ];
    },

    addQuiz(command, newQuiz) {
      this.dialog = true;
      this.returnCommand = command;
      this.editedItem = {
        quiz: newQuiz.quiz,
        translation: "",
        partofspeech: "",
        root: "",
        context: ""
      };
    },
    editItem(quiz) {
      this.editedIndex = this.quizs.indexOf(quiz);
      this.editedItem = Object.assign({}, quiz);
      this.dialog = true;
    },

    deleteItem(quiz) {
      const index = this.quizs.indexOf(quiz);
      confirm("Are you sure you want to delete this quiz?") &&
        this.quizs.splice(index, 1);
    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.quizs[this.editedIndex], this.editedItem);
      } else {
        this.quizs.push(this.editedItem);
      }
      if (this.returnCommand) {
        console.log(this.returnCommand);
        let quizPackage = {
          editedItem: this.editedItem,
          returnCommand: this.returnCommand
        };
        this.$emit("setQuizDefinition", quizPackage);
      }
      this.close();
    }


  },
};
</script>

<style></style>
