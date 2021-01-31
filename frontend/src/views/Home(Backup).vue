<template>
  <div class="sandstone">
    <v-container class="pa-2 pt-2 mx-auto" fill-height fluid>
      <v-row justify-center dense wrap>

        <v-col cols="12" sm="6" md="4" lg="3">
          <v-card max-width="335" class="desertsand">
            <v-toolbar class="desertsand calligraphy--text" dense elevation="6">
              <v-toolbar-title>Recent Lessons</v-toolbar-title>
              <v-spacer></v-spacer>

              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn
                    icon
                    v-on="on"
                    @click="lessonPreferenceFilter = !lessonPreferenceFilter"
                    :class="
                      !lessonPreferenceFilter ? 'elements--text' : 'elements'
                    "
                  >
                    <v-icon>filter_list</v-icon>
                  </v-btn>
                </template>
                <span>Filter By Preferences</span>
              </v-tooltip>

              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn
                    v-on="on"
                    icon
                    :to="{
                      name: 'Lesson-Builder',
                    }"
                  >
                    <v-icon color="elements">library_add</v-icon>
                  </v-btn>
                </template>
                <span>Add Lesson</span>
              </v-tooltip>

              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn
                    v-on="on"
                    icon
                    @click="showLessons = !showLessons"
                    class="garbage--text"
                  >
                    <v-icon v-if="!showLessons">mdi-eye</v-icon>
                    <v-icon v-if="showLessons">mdi-eye-off</v-icon>
                  </v-btn>
                </template>
                <span v-if="!showLessons">View Lessons</span>
                <span v-else>Hide Lessons</span>
              </v-tooltip>
            </v-toolbar>
            <v-card-text
              v-show="showLessons"
              class="content-box calligraphy pa-1"
            >
              <LessonList :preference-filter="lessonPreferenceFilter" />
            </v-card-text>
          </v-card>
        </v-col>



        <v-col cols="12" sm="6" md="4" lg="3">
          <v-card max-width="335">
            <v-toolbar class="desertsand calligraphy--text" dense>
              <v-toolbar-title>Recent Videos</v-toolbar-title>
              <v-spacer></v-spacer>

              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn
                    icon
                    v-on="on"
                    @click="videoPreferenceFilter = !videoPreferenceFilter"
                    :class="
                      !videoPreferenceFilter ? 'elements--text' : 'elements'
                    "
                  >
                    <v-icon>filter_list</v-icon>
                  </v-btn>
                </template>
                <span>Filter By Preferences</span>
              </v-tooltip>

              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn
                    v-on="on"
                    icon
                    @click="showYouTubeEditor = !showYouTubeEditor"
                  >
                    <v-icon color="elements">library_add</v-icon>
                  </v-btn>
                </template>
                <span>Add Video</span>
              </v-tooltip>

              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn
                    v-on="on"
                    icon
                    @click="showVideos = !showVideos"
                    class="garbage--text"
                  >
                    <v-icon v-if="!showVideos">mdi-eye</v-icon>
                    <v-icon v-if="showVideos">mdi-eye-off</v-icon>
                  </v-btn>
                </template>
                <span v-if="!showVideos">View Videos</span>
                <span v-else>Hide Videos</span>
              </v-tooltip>
            </v-toolbar>
            <v-card-text
              v-show="showVideos"
              class="content-box calligraphy pa-1"
            >
              <YouTubeList :preference-filter="videoPreferenceFilter" />
            </v-card-text>
          </v-card>
        </v-col>

        <v-col  cols="12" sm="6" md="4" lg="3">
          <v-card max-width="335">
            <v-toolbar class="desertsand calligraphy--text" dense>
              <v-toolbar-title>Recent Audio</v-toolbar-title>
              <v-spacer></v-spacer>

              <v-btn
                icon
                @click="audioPreferenceFilter = !audioPreferenceFilter"
                :class="!audioPreferenceFilter ? 'elements--text' : 'elements'"
              >
                <v-icon>filter_list</v-icon>
              </v-btn>

              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn v-on="on" icon @click="showAudioEditor = true">
                    <v-icon color="elements">library_add</v-icon>
                  </v-btn>
                </template>
                <span>Add Audio</span>
              </v-tooltip>

              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn
                    v-on="on"
                    icon
                    @click="showAudios = !showAudios"
                    class="garbage--text"
                  >
                    <v-icon v-if="!showAudios">mdi-eye</v-icon>
                    <v-icon v-if="showAudios">mdi-eye-off</v-icon>
                  </v-btn>
                </template>
                <span v-if="!showAudios">View Audio List</span>
                <span v-else>Hide Audio List</span>
              </v-tooltip>
            </v-toolbar>

            <v-card-text
              v-show="showAudios"
              class="content-box calligraphy  pa-1"
            >
              <AudioList :preference-filter="audioPreferenceFilter" />
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" sm="6" md="4" lg="3">
          <v-card max-width="335" outlined>
            <v-toolbar class="desertsand calligraphy--text" dense>
              <v-toolbar-title>Recent Texts</v-toolbar-title>
              <v-spacer></v-spacer>

              <v-btn
                icon
                @click="textPreferenceFilter = !textPreferenceFilter"
                :class="!textPreferenceFilter ? 'elements--text' : 'elements'"
              >
                <v-icon>filter_list</v-icon>
              </v-btn>

              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn v-on="on" icon @click="showTextElementEditor = true">
                    <v-icon color="elements">library_add</v-icon>
                  </v-btn>
                </template>
                <span>Add Text Element</span>
              </v-tooltip>

              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn
                    v-on="on"
                    icon
                    @click="showTextElements = !showTextElements"
                    class="garbage--text"
                  >
                    <v-icon v-if="!showTextElements">mdi-eye</v-icon>
                    <v-icon v-if="showTextElements">mdi-eye-off</v-icon>
                  </v-btn>
                </template>
                <span v-if="!showTextElements">View Audio List</span>
                <span v-else>Hide Audio List</span>
              </v-tooltip>
            </v-toolbar>

            <v-card-text
              v-show="showTextElements"
              class="content-box calligraphy  pa-1"
            >
              <TextElementList :preference-filter="textPreferenceFilter" />
            </v-card-text>
          </v-card>
        </v-col>

        <v-col  cols="12" sm="6" md="4" lg="3">
          <v-card max-width="335">
            <v-toolbar class="desertsand calligraphy--text" dense>
              <v-toolbar-title>Recent Questions</v-toolbar-title>
              <v-spacer></v-spacer>

              <v-btn
                icon
                @click="questionPreferenceFilter = !questionPreferenceFilter"
                :class="!questionPreferenceFilter ? 'primary--text' : 'primary'"
              >
                <v-icon>filter_list</v-icon>
              </v-btn>

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
            <v-card-text
              v-show="showQuestions"
              class="content-box calligraphy  pa-1"
            >
              <QuestionsList :preference-filter="questionPreferenceFilter" />
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <QuestionEditor
        v-if="questionEditorLoaded"
        :editor-dialog="showQuestionEditor"
        @closeDialog="showQuestionEditor = false"
      />
      <YouTubeElementEditor
        v-if="showYouTubeEditor"
        :editor-dialog="showYouTubeEditor"
        :editing="false"
        :video="blankVideo"
        @closeDialog="showYouTubeEditor = false"
      />
      <AudioElementEditor
        v-if="showAudioEditor"
        :editor-dialog="showAudioEditor"
        :editing="false"
        :audio="blankAudio"
        @closeDialog="showAudioEditor = false"
      />
      <TextElementEditor
        v-if="showTextElementEditor"
        :editor-dialog="showTextElementEditor"
        :is-new-element="true"
        @closeDialog="showTextElementEditor = false"
      />
    </v-container>
  </div>
</template>

<script>
import LessonList from "@/components/lessons/LessonList.vue";
import YouTubeList from "@/components/elements/YouTubeList.vue";
import AudioList from "@/components/elements/AudioList.vue";
import QuestionsList from "@/components/questions/QuestionsList.vue";
import TextElementList from "@/components/elements/TextElementList.vue";
export default {
  name: "Home",
  data() {
    return {
      questions: [],
      next: null,
      loadingQuestions: false,
      askQuestionDialog: false,
      questionEditorLoaded: false,
      showQuestionEditor: false,
      questionPreferenceFilter: false,

      showTextElementEditor: false,
      textPreferenceFilter: false,
      lessonPreferenceFilter: false,
      loadingLessons: false,

      showLessons: true,
      showQuestions: true,
      showVideos: true,
      showAudios: true,
      showTextElements: true,

      youTubeKey: 0,
      youTubeEditorLoaded: false,
      showYouTubeEditor: false,
      blankVideo: {},
      videoPreferenceFilter: false,

      audioKey: 0,
      audioEditorLoaded: false,
      showAudioEditor: false,
      blankAudio: {},
      audioPreferenceFilter: false,

      tab: null,
      items: ["Appetizers", "Entrees", "Deserts", "Cocktails"],
      text:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",

      thinking: false
    };
  },
  components: {
    LessonList,
    YouTubeList,
    QuestionsList,
    AudioList,
    TextElementList,
    YouTubeElementEditor: () =>
      import(
        /* webpackPrefetch: true */ "@/components/elements/YouTubeElementEditor.vue"
      ),
    AudioElementEditor: () =>
      import(
        /* webpackPrefetch: true */ "@/components/elements/AudioElementEditor.vue"
      ),
    QuestionEditor: () =>
      import(
        /* webpackPrefetch: true */ "@/components/questions/QuestionEditor.vue"
      ),
    TextElementEditor: () =>
      import(
        /* webpackPrefetch: true */ "@/components/elements/TextElementEditor.vue"
      )
  },
  methods: {
    loadQuestionEditor() {
      this.questionEditorLoaded = true;
      this.showQuestionEditor = !this.showQuestionEditor;
    }
  },
  created() {
    document.title = "PidginForge: Home";
  }
};
</script>
<style scoped>
.content-box > * {
  width: 100%;
  max-height: 650px;
  overflow-x: hidden;
  overflow-x: auto;
  /* overflow-y: hidden; */
  /* overflow-x: auto; */

  position: relative;
  /* position: absolute; */
  /* width: 100%; */
}
</style>
