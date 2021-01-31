<template>
  <div class="sandstone">
    <v-container fill-height fluid>
      <v-row>
        <v-col cols="12">
          <v-container fluid class="text-align">
            <h1 class="font-weight-black">Curate & Create</h1>
            <hr />
            <h2 class=""></h2>
          </v-container>
        </v-col>
      </v-row>
      <v-row wrap dense>
        <v-col cols="12" sm="6" lg="4" xl="3">
          <v-card class="mx-auto desertsand" max-width="310">
            <v-card-text>
              <div>Create or Curate New Elements</div>
              <p class="headline text--primary">
                ELEMENTS <v-icon>scatter_plot</v-icon>
              </p>
              <div class="wordz--text">
                Elements are building blocks, simple language objects such as an
                audio passage, a video, a text, etc.
              </div>
            </v-card-text>
            <v-card-actions>
              <v-container>
                <v-btn
                  class="mb-2 primary"
                  block
                  large
                  @click="loadYouTubeEditor"
                  >YouTube<v-icon right>mdi-video</v-icon></v-btn
                >
                <v-btn class="mb-2 primary" block large @click="loadAudioEditor"
                  >Audio <v-icon right>audiotrack</v-icon></v-btn
                >
                <v-btn
                  class="mb-2 primary"
                  block
                  @click="textEditorDialog = true"
                  large
                  >Text <v-icon right>text_fields</v-icon></v-btn
                >
                <v-btn class="mb-2 primary" block :disabled="true" large
                  >Lexemes & Terms<v-icon right>mdi-card-text-outline</v-icon></v-btn
                >
                <v-btn class="mb-2 primary" block 
                  @click="$router.push({name: 'Stacks-Viewer'})"
                  large
                  >Vocab Card Stacks<v-icon right>mdi-cards</v-icon></v-btn
                >
              </v-container>
            </v-card-actions>
          </v-card>
        </v-col>

        <v-col cols="12" sm="6" lg="4" xl="3">
          <v-card class="mx-auto desertsand" max-width="310">
            <v-card-text>
              <div>Create or Curate New Lessons</div>
              <p class="headline text--primary">
                INSTRUCTION <v-icon>menu_book</v-icon>
              </p>
              <div class="text--primary">
                Lessons are short learning modules that are 5 to 90 minutes in
                length. They are meant to convey a limited number of concepts.
                They combine elements with some form of instruction, and they
                form the building blocks for units and courses.
              </div>
            </v-card-text>
            <v-card-actions>
              <v-container>
                <v-btn
                  block
                  class="mb-2 elements desertsand--text"
                  :to="{
                    name: 'Lesson-Builder',
                    params: {
                      elementslug: null
                    }
                  }"
                  large
                  >Lesson Builder</v-btn
                >
                <v-btn
                  block
                  class="mb-2 elements desertsand--text"
                  :disabled="true"
                  large
                  >Explicit Grammar</v-btn
                >
                <v-btn
                  block
                  class="mb-2 elements desertsand--text"
                  :disabled="true"
                  large
                  >Reading<br />Comprehension</v-btn
                >
                <v-btn
                  block
                  class="mb-2 elements desertsand--text"
                  :disabled="true"
                  large
                  >Listening<br />
                  Comprehension</v-btn
                >
                <v-btn
                  block
                  class="mb-2 elements desertsand--text"
                  :disabled="true"
                  large
                  >Assessments</v-btn
                >
              </v-container>
            </v-card-actions>
          </v-card>
        </v-col>

        <v-col cols="12" sm="6" lg="4" xl="3">
          <v-card class="mx-auto desertsand" max-width="310">
            <v-card-text>
              <div>Further Curate & Improve Your Work</div>
              <p class="headline text--primary">
                IMPROVE <v-icon>child_friendly</v-icon>
              </p>
              <div class="text--primary">
                Please take time to improve the materials you've curated by
                reviewing feedback of others.
              </div>
            </v-card-text>
            <v-card-actions>
              <v-container>
                <v-btn
                  block
                  class="mb-2"
                  large
                  :loading="loadingQC"
                  :disabled="needsQC == 0"
                  >Quality<br />
                  Control
                  <v-chip class="ml-1" color="primary" text-color="white" small>
                    {{ needsQC }}
                  </v-chip>
                </v-btn>
                <v-btn
                  block
                  class="mb-2"
                  large
                  :loading="loadingTranslation"
                  :disabled="needsTranslation == 0"
                  >Needs<br />
                  Translation
                  <v-chip class="ml-1" color="primary" text-color="white" small>
                    {{ needsTranslation }}
                  </v-chip>
                </v-btn>
                <v-btn
                  block
                  class="mb-2"
                  large
                  :loading="loadingTranscription"
                  :disabled="needsTranscription == 0"
                  >Needs<br />
                  Transcription
                  <v-chip class="ml-1" color="primary" text-color="white" small>
                    {{ needsTranscription }}
                  </v-chip>
                </v-btn>
                <v-btn
                  block
                  class="mb-2"
                  large
                  :loading="loadingViolations"
                  :disabled="violations == 0"
                  >Triage<br />
                  Violations
                  <v-chip class="ml-1" color="red" text-color="white" small>
                    {{ violations }}
                  </v-chip>
                </v-btn>
              </v-container>
            </v-card-actions>
          </v-card>
        </v-col>

        <v-col cols="12" sm="6" lg="4" xl="3">
          <v-card class="mx-auto desertsand" max-width="310">
            <v-card-text>
              <div>Help Care for Orphaned Objects</div>
              <p class="headline text--primary">
                ORPHANS <v-icon>child_friendly</v-icon>
              </p>
              <div class="text--primary">
                Elements are building blocks, simple language objects such as an
                audio passage, a video, a text, etc.
              </div>
            </v-card-text>
            <v-card-actions>
              <v-container>
                <v-btn
                  block
                  class="mb-2"
                  large
                  :loading="loadingQC"
                  :disabled="needsQC == 0"
                  >Quality<br />
                  Control
                  <v-chip class="ml-1" color="primary" text-color="white" small>
                    {{ needsQC }}
                  </v-chip>
                </v-btn>
                <v-btn
                  block
                  class="mb-2"
                  large
                  :loading="loadingTranslation"
                  :disabled="needsTranslation == 0"
                  >Needs<br />
                  Translation
                  <v-chip class="ml-1" color="primary" text-color="white" small>
                    {{ needsTranslation }}
                  </v-chip>
                </v-btn>
                <v-btn
                  block
                  class="mb-2"
                  large
                  :loading="loadingTranscription"
                  :disabled="needsTranscription == 0"
                  >Needs<br />
                  Transcription
                  <v-chip class="ml-1" color="primary" text-color="white" small>
                    {{ needsTranscription }}
                  </v-chip>
                </v-btn>
                <v-btn
                  block
                  class="red mb-2"
                  large
                  :loading="loadingViolations"
                  :disabled="violations == 0"
                  >Triage<br />
                  Violations
                  <v-chip class="ml-1" color="red" text-color="white" small>
                    {{ violations }}
                  </v-chip>
                </v-btn>
              </v-container>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <YouTubeElementEditor
      v-if="youTubeEditorLoaded"
      :editor-dialog="showYouTubeEditor"
      :editing="false"
      :video="blankVideo"
      :key="youTubeKey"
      @closeDialog="showYouTubeEditor = false"
      @rerenderYouTube="rerenderYouTube"
    />
    <AudioElementEditor
      v-if="audioEditorLoaded"
      :editor-dialog="showAudioEditor"
      :editing="false"
      :audio="blankAudio"
      :key="audioKey"
      @closeDialog="showAudioEditor = false"
      @rerenderAudio="rerenderAudio"
    />
    <TextElementEditor
      v-if="textEditorDialog"
      :editor-dialog="textEditorDialog"
      :is-new-element="true"
      :key="textKey"
      @closeDialog="textEditorDialog = false"
    />
  </div>
</template>
<script>
// import { apiService } from "@/common/api.service.js";
export default {
  name: "Curate",
  components: {
    YouTubeElementEditor: () =>
      import(
        /* webpackPrefetch: true */ "@/components/elements/YouTubeElementEditor.vue"
      ),
    AudioElementEditor: () =>
      import(
        /* webpackPrefetch: true */ "@/components/elements/AudioElementEditor.vue"
      ),
    TextElementEditor: () =>
      import(
        /* webpackPrefetch: true */ "@/components/elements/TextElementEditor.vue"
      )
  },
  data() {
    return {
      youTubeKey: 0,
      youTubeEditorLoaded: false,
      showYouTubeEditor: false,
      blankVideo: {},
      audioKey: 0,
      audioEditorLoaded: false,
      showAudioEditor: false,
      blankAudio: {},
      thinking: false,
      needsQC: 0,
      loadingQC: true,
      needsTranslation: 0,
      loadingTranslation: true,
      needsTranscription: 0,
      loadingTranscription: true,
      violations: 0,
      loadingViolations: true,
      textEditorDialog: false
    };
  },
  props: {},
  methods: {
    // Force Rerenders
    rerenderYouTube() {
      this.youTubeKey += 1;
    },
    rerenderAudio() {
      this.audioKey += 1;
    },
    loadTester() {
      this.testDialog = !this.testDialog;
      this.testing = true;
    },
    loadYouTubeEditor() {
      this.youTubeEditorLoaded = true;
      this.showYouTubeEditor = !this.showYouTubeEditor;
    },
    loadAudioEditor() {
      this.audioEditorLoaded = true;
      this.showAudioEditor = !this.showAudioEditor;
    },
    // Check for QC
    countQC() {
      this.loadingQC = false;
    },

    // Check for Translation
    countTranslations() {
      this.loadingTranslation = false;
    },
    // Check for Transcription
    countTranscriptions() {
      this.loadingTranscription = false;
    },

    // Check for Triage Violations
    countViolations() {
      this.loadingViolations = false;
    }
  },
  created() {
    this.countQC();
    this.countTranslations();
    this.countTranscriptions();
    this.countViolations();
  }
};
</script>
