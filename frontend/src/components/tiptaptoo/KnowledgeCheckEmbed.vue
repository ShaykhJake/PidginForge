<template>
  <div>
    <v-card class="calligraphy desertsand--text" min-width="300">
      <v-card-title class="py-1" v-show="editing">
        <v-spacer />
        <v-icon color="elements">mdi-arrow-all</v-icon>
        <v-spacer />
      </v-card-title>
      <v-card-text class="pa-0 desertsand--text">
        <h1>{{ quizObject.title }}</h1>

        <div v-for="question in quizObject.questions" :key="question.index">
          <v-radio-group
            v-model="question.selection"
            column
            class="desertsand--text"
          >
            {{ question.text }}
            {{
              question.selection === question.answerkey
                ? "Winner winner!"
                : "Loser!"
            }}
            <v-radio
              v-for="choice in question.choices"
              :label="choice.text"
              :value="choice.key"
              :key="choice.key"
            ></v-radio>
          </v-radio-group>
        </div>
      </v-card-text>
      <v-card-actions v-show="editing">
        <v-btn small icon @click="updateWrap('left')"
          ><v-icon :color="float === 'left' ? 'primary' : 'desertsand'"
            >mdi-arrow-collapse-left</v-icon
          ></v-btn
        >
        <v-spacer />
        <v-btn small icon @click="updateWrap('none')"
          ><v-icon :color="float === 'none' ? 'primary' : 'desertsand'"
            >mdi-format-wrap-top-bottom</v-icon
          ></v-btn
        >
        <v-spacer />
        <v-btn small icon @click="updateWrap('right')"
          ><v-icon :color="float === 'right' ? 'primary' : 'desertsand'"
            >mdi-arrow-collapse-right</v-icon
          ></v-btn
        >
      </v-card-actions>
    </v-card>
  </div>
</template>
<script>
// import VueYouTubeEmbed from 'vue-youtube-embed'
export default {
  name: "KnowledgeCheckEmbed",
  props: {
    src: String,
    float: String,
    videoid: String,
    editing: {
      type: Boolean,
      default: true
    }
  },
  components: {},
  data() {
    return {
      heightText: "Start",
      youTubeEditorLoaded: false,
      showYouTubeEditor: false,
      showAudioEditor: false,
      audioEditorLoaded: false,
      editorDialog: false,
      profileDialog: false,
      quizObject: {
        title: "Quiz about Food",
        questions: [
          {
            text: "Corn is evil.",
            type: "tf",
            choices: [
              { key: "1", text: "True" },
              { key: "2", text: "False" }
            ],
            answerkey: "1"
          },
          {
            text: "Pizza is delicious.",
            type: "tf",
            choices: [
              { key: "1", text: "True" },
              { key: "2", text: "False" }
            ],
            answerkey: "1"
          },
          {
            text: "What is the best cookie?",
            type: "mc",
            choices: [
              { key: "1", text: "Chocolate Chip" },
              { key: "2", text: "Oatmeal" },
              { key: "3", text: "Peanut Butter" },
              { key: "4", text: "Coconut" }
            ],
            answerkey: "2"
          },
          {
            text: "What is the best cookie?",
            type: "mc",
            choices: [
              { key: "1", text: "Chocolate Chip" },
              { key: "2", text: "Oatmeal" },
              { key: "3", text: "Peanut Butter" },
              { key: "4", text: "Coconut" }
            ],
            answerkey: "3"
          }
        ]
      }
    };
  },
  methods: {
    updateWrap(direction) {
      this.$emit("updateWrap", direction);
    }
  },
  mounted() {},
  beforeDestroy() {
    document.removeEventListener("keydown", this._keyListener);
  }
};
</script>
<style type="text/css"></style>
