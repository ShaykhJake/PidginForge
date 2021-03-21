<template>
  <v-row v-if="elementObject" dense wrap>
    <v-col>
      <v-card class="desertsand">
        <v-card-title class="calligraphy desertsand--text py-1">
          Transcripts:
          <v-btn
            v-if="!userHasTranscript"
            class="primary--text text--lighten-2"
            outlined
            @click="loadTranscript(0)"
            >Add Transcript<v-icon right>mdi-plus-circle</v-icon></v-btn
          >
          <v-btn
            v-if="userHasTranscript && !userTranscriptLoaded"
            outlined
            class="primary--text text--lighten-2"
            @click="loadTranscript(elementObject.user_transcript)"
            >Your Transcript<v-icon right>mdi-pencil</v-icon></v-btn
          >
          <v-btn
            :loading="fetchingElementObject"
            :disabled="numberOfTranscripts === 0"
            @click="showTranscriptList = true"
            outlined
            class="desertsand--text ma-1"
          >
            All Transcripts
            <v-badge
              :content="numberOfTranscripts"
              color="calligraphy lighten-1"
            >
              <v-icon>mdi-script-text-outline</v-icon>
            </v-badge>
          </v-btn>

          <v-dialog v-model="showTranscriptList" width="395">
            <template> </template>
            <TranscriptListModal
              @closeDialog="showTranscriptList = false"
              :transcript-list="elementObject.transcripts"
              @loadTranscript="loadTranscript"
            />
          </v-dialog>
        </v-card-title>

        <v-card-text v-if="transcriptLoaded" class="px-2">
          <v-row dense wrap no-gutters>
            <v-col cols="12">
              By
              <span class="primary--text font-weight-black mx-1">
                {{ transcript.curator.username }}
              </span>
              on {{ transcript.curationdate }}

              <ElementVoter
                @updateVote="updateVote"
                :up-vote-count="transcript.upvote_count"
                :down-vote-count="transcript.downvote_count"
                :user-vote="transcript.user_vote"
                :elementid="transcript.id"
                element-type="Transcript"
                text-typography="body-1"
              />
            </v-col>
            <v-col cols="12" class="overline" v-if="!transcript.published">
              ...this transcript is currently in draft and not visible to
              others...
            </v-col>
            <v-col
              small
              cols="12"
              class="overline"
              v-if="transcript.forkparent"
            >
              ...this transcript was forked from
              <a
                class="primary--text font-weight-black"
                @click.prevent="loadTranscript(transcript.forkparent)"
                >Transcript ID: {{ transcript.forkparent }}</a
              >...
            </v-col>
            <v-col cols="12">
              <v-toolbar dense v-if="!isCurator" flat class="calligraphy pa-0">
                <v-btn
                  small
                  :loading="submittingFork"
                  color="elements desertsand--text"
                  @click="
                    userHasTranscript
                      ? (forkOverwriteDialog = true)
                      : forkTranscript()
                  "
                >
                  Fork
                  <v-badge
                    :content="transcript.forks_count"
                    color="elements darken-2"
                  >
                    <v-icon>
                      mdi-source-fork
                    </v-icon>
                  </v-badge>
                </v-btn>

                <v-dialog
                  v-model="forkOverwriteDialog"
                  persistent
                  max-width="300"
                >
                  <v-card class="calligraphy desertsand--text">
                    <v-card-title class="headline"
                      >Delete Your Transcript?</v-card-title
                    >
                    <v-card-text class="desertsand calligraphy--text pt-1">
                      You've already started a transcript for this source item.
                      In order to fork a new transcript, you must first delete
                      your old. Confirm delete and proceed with fork?
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                        small
                        color="garbage desertsand--text"
                        @click="forkOverwriteDialog = false"
                        >Cancel <v-icon right>mdi-cancel</v-icon></v-btn
                      >
                      <v-btn
                        small
                        color="error desertsand--text"
                        @click="forkTranscript"
                        >Proceed <v-icon right>mdi-source-fork</v-icon></v-btn
                      >
                    </v-card-actions>
                  </v-card>
                </v-dialog>

                <v-btn disabled text class="mr-1">
                  QC
                </v-btn>
                <v-spacer></v-spacer>
                <v-btn
                  class="elements desertsand--text mx-2"
                  small
                  @click="showTranslation = !showTranslation"
                >
                  <v-badge
                    :content="
                      transcript.translations
                        ? transcript.translations.length
                        : '0'
                    "
                  >
                    Show Translations
                  </v-badge>
                </v-btn>
              </v-toolbar>
              <v-toolbar dense v-if="isCurator" flat class="calligraphy pa-0">
                <v-btn
                  v-if="editing"
                  small
                  class="primary desertsand--text mr-1"
                  @click="submitSave"
                  :loading="submittingSave"
                  :disabled="!unsavedChanges"
                >
                  Save
                  <v-icon right>mdi-content-save</v-icon>
                </v-btn>
                <v-btn
                  v-if="editing"
                  small
                  class="garbage desertsand--text mr-1"
                  @click="checkEdits"
                >
                  Close Edit
                  <v-icon right>mdi-close</v-icon>
                </v-btn>
                <v-btn
                  v-if="!editing"
                  class="primary mr-1"
                  @click="openEdit"
                  small
                >
                  Edit
                  <v-icon right>
                    mdi-pencil
                  </v-icon>
                </v-btn>

                <v-dialog
                  v-model="unsavedChangesDialog"
                  persistent
                  max-width="300"
                >
                  <v-card class="calligraphy desertsand--text">
                    <v-card-title class="headline"
                      >Unsaved Changes</v-card-title
                    >
                    <v-card-text class="desertsand calligraphy--text pt-1">
                      You have made changes to your transcript. Would you like
                      to save them, or throw them away?
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                        small
                        color="primary desertsand--text"
                        @click="saveEditsThenClose"
                        >Save<v-icon right>mdi-content-save</v-icon></v-btn
                      >
                      <v-btn
                        small
                        color="garbage desertsand--text"
                        @click="trashEditsThenClose"
                        >Trash<v-icon right>mdi-delete</v-icon></v-btn
                      >
                    </v-card-actions>
                  </v-card>
                </v-dialog>

                <v-dialog
                  v-model="confirmDeleteDialog"
                  persistent
                  max-width="300"
                >
                  <v-card class="calligraphy desertsand--text">
                    <v-card-title class="headline"
                      >Confirm Delete?</v-card-title
                    >
                    <v-card-text class="desertsand calligraphy--text pt-1">
                      You've worked so hard; are you sure that you want to flush
                      all of that work down the toilet and deprive the world of
                      your masterpiece?
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                        small
                        color="primary desertsand--text"
                        @click="confirmDeleteDialog = false"
                        >Cancel<v-icon right>mdi-content-save</v-icon></v-btn
                      >
                      <v-btn
                        small
                        color="garbage desertsand--text"
                        @click="deleteTranscript"
                        :loading="submittingDelete"
                        >Delete<v-icon right>mdi-delete</v-icon></v-btn
                      >
                    </v-card-actions>
                  </v-card>
                </v-dialog>

                <v-btn
                  small
                  class="elements desertsand--text mr-1"
                  v-if="!transcript.published && !editing"
                  @click="togglePublish"
                >
                  Publish<v-icon right>mdi-eye</v-icon>
                </v-btn>
                <v-btn
                  small
                  class="elements desertsand--text mr-1"
                  v-if="transcript.published && !editing"
                  @click="togglePublish"
                >
                  Return to Draft<v-icon right>mdi-eye-off</v-icon>
                </v-btn>
                <v-btn
                  small
                  v-if="!editing"
                  class="garbage desertsand--text mr-1"
                  @click="confirmDeleteDialog = true"
                >
                  Delete
                  <v-icon right>
                    mdi-delete
                  </v-icon>
                </v-btn>

                <v-spacer></v-spacer>
                <v-btn
                  class="elements desertsand--text mx-2"
                  small
                  @click="showTranslation = !showTranslation"
                >
                  <v-badge
                    :content="
                      transcript.translations
                        ? transcript.translations.length
                        : '0'
                    "
                  >
                    <span v-if="!showTranslation">Show Translations</span
                    ><span v-if="showTranslation">Hide Translations</span>
                  </v-badge>
                </v-btn>
              </v-toolbar>
            </v-col>

            <v-col cols="12">
              <editor-menu-bar
                v-if="isCurator && editing"
                :editor="editor"
                v-slot="{ commands, isActive }"
              >
                <div class="desertsand--text">
                  <v-toolbar dense flat class="calligraphy">
                    <v-btn
                      small
                      icon
                      color="sandstone"
                      :class="{ 'is-active': isActive.bold() }"
                      @click="commands.bold"
                    >
                      <v-icon>
                        mdi-format-bold
                      </v-icon>
                    </v-btn>
                    <v-btn
                      icon
                      small
                      color="sandstone"
                      :class="{ 'is-active': isActive.italic() }"
                      @click="commands.italic"
                    >
                      <v-icon>
                        mdi-format-italic
                      </v-icon>
                    </v-btn>
                    <v-divider class="mx-1" inset vertical></v-divider>
                    <v-btn
                      icon
                      small
                      color="sandstone"
                      :class="{ 'is-active': isActive.paragraph() }"
                      @click="commands.paragraph"
                    >
                      <v-icon>
                        mdi-format-paragraph
                      </v-icon>
                    </v-btn>
                    <v-btn
                      icon
                      small
                      color="sandstone"
                      :class="{ 'is-active': isActive.heading({ level: 1 }) }"
                      @click="commands.heading({ level: 1 })"
                    >
                      <v-icon>
                        mdi-format-header-1
                      </v-icon>
                    </v-btn>
                    <v-btn
                      icon
                      small
                      color="sandstone"
                      :class="{ 'is-active': isActive.heading({ level: 2 }) }"
                      @click="commands.heading({ level: 2 })"
                    >
                      <v-icon>
                        mdi-format-header-2
                      </v-icon>
                    </v-btn>
                    <v-btn
                      icon
                      small
                      color="sandstone"
                      :class="{ 'is-active': isActive.heading({ level: 3 }) }"
                      @click="commands.heading({ level: 3 })"
                    >
                      <v-icon>
                        mdi-format-header-3
                      </v-icon>
                    </v-btn>

                    <v-divider class="mx-1" inset vertical></v-divider>

                    <v-btn
                      icon
                      small
                      color="sandstone"
                      :class="{
                        'is-active': isActive.alignment({ orientation: 'left' })
                      }"
                      @click="commands.alignment({ orientation: 'left' })"
                    >
                      <v-icon>
                        mdi-format-align-left
                      </v-icon>
                    </v-btn>

                    <v-btn
                      icon
                      small
                      color="sandstone"
                      :class="{
                        'is-active': isActive.alignment({
                          orientation: 'center'
                        })
                      }"
                      @click="commands.alignment({ orientation: 'center' })"
                    >
                      <v-icon>
                        mdi-format-align-center
                      </v-icon>
                    </v-btn>

                    <v-btn
                      icon
                      small
                      color="sandstone"
                      :class="{
                        'is-active': isActive.alignment({
                          orientation: 'right'
                        })
                      }"
                      @click="commands.alignment({ orientation: 'right' })"
                    >
                      <v-icon>
                        mdi-format-align-right
                      </v-icon>
                    </v-btn>

                    <v-btn
                      icon
                      small
                      color="sandstone"
                      :class="{
                        'is-active': isActive.text_direction({
                          direction: 'ltr'
                        })
                      }"
                      @click="commands.text_direction({ direction: 'ltr' })"
                    >
                      <v-icon>
                        mdi-format-textdirection-l-to-r
                      </v-icon>
                    </v-btn>
                    <v-btn
                      icon
                      small
                      color="sandstone"
                      :class="{
                        'is-active': isActive.text_direction({
                          direction: 'rtl'
                        })
                      }"
                      @click="commands.text_direction({ direction: 'rtl' })"
                    >
                      <v-icon>
                        mdi-format-textdirection-r-to-l
                      </v-icon>
                    </v-btn>

                    <v-divider class="mx-1" inset vertical></v-divider>

                    <v-btn
                      icon
                      small
                      color="primary"
                      :class="{ 'is-active': isActive.highlighter() }"
                      @click="commands.highlighter"
                    >
                      <v-icon>
                        mdi-marker
                      </v-icon>
                    </v-btn>

                    <v-divider class="mx-1" inset vertical></v-divider>

                    <v-btn icon @click="triggerTimeStamp" color="sandstone">
                      <v-icon>
                        mdi-timer
                      </v-icon>
                    </v-btn>
                  </v-toolbar>
                </div>
              </editor-menu-bar>
              <editor-content
                :editor="editor"
                :style="editorFontClass"
                class="editor-box"
                id="transcripteditorbox"
              />
              <v-card-actions>
                <v-btn icon @click="changeEditorFontSize('down')">
                  <v-icon>mdi-magnify-minus</v-icon>
                </v-btn>
                Text Size
                <v-btn icon @click="changeEditorFontSize('up')">
                  <v-icon>mdi-magnify-plus</v-icon>
                </v-btn>
                <v-btn icon @click="printText"
                  ><v-icon>mdi-printer</v-icon></v-btn
                >
              </v-card-actions>
              <div v-text="jsonText"></div>
              <div v-text="htmlText"></div>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <v-overlay
        :value="loadingTranscript"
        absolute
        color="calligraphy"
        opacity="0.75"
      >
        <v-progress-circular indeterminate size="64"></v-progress-circular>
      </v-overlay>

      <v-snackbar
        top
        v-model="snackbar"
        :color="snackColor"
        :timeout="snackTimeout"
      >
        {{ snackText }}
        <v-btn class="desertsand--text" text @click="snackbar = false">
          Close
        </v-btn>
      </v-snackbar>
    </v-col>

    <v-col
      cols="12"
      md="6"
      v-if="showTranslation && transcriptLoaded"
      id="translationcolumn"
    >
      <TranslationEditor
        ref="translationeditor"
        :passed-source="transcript"
        source-type="transcript"
      />
    </v-col>
  </v-row>
</template>

<script>
// Import the editor
import TranscriptListModal from "@/components/transcript/TranscriptListModal.vue";
import { apiService } from "@/common/api.service.js";
import ElementVoter from "@/components/elements/ElementVoter.vue";

import { Editor, EditorContent, EditorMenuBar } from "tiptap";
import {
  Blockquote,
  HardBreak,
  Heading,
  Bold,
  Italic,
  Link,
  Strike,
  Underline,
  History
} from "tiptap-extensions";

import { default as Alignment } from "@/components/tiptaptoo/Alignment.js";
import { default as TextDirection } from "@/components/tiptaptoo/TextDirection.js";
import { default as TimeStamp } from "@/components/tiptaptoo/TimeStamp.js";
import { default as Highlighter } from "@/components/tiptaptoo/Highlighter.js";

export default {
  name: "TranscriptEditor",
  components: {
    EditorContent,
    EditorMenuBar,
    ElementVoter,
    TranscriptListModal,
    TranslationEditor: () =>
      import(
        /* webpackPrefetch: true */ "@/components/translation/TranslationEditor.vue"
      )
  },
  props: {
    elementType: {
      type: String,
      required: true
    },
    elementSlug: {
      type: String,
      required: true
    },
    passedObject: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      elementObject: {},
      fetchingElementObject: false,
      showTranscriptList: false,

      showTranscript: false,

      userScriptLoaded: false,
      transcriptLoaded: false,
      loadedTranscript: 0,
      loadingTranscript: false,

      transcript: {},
      transcripts: {},
      editorFontSize: 1,
      showTranslationsList: false,
      showTranslation: false,
      translations: {},
      jsonText: "",
      htmlText: "",
      snackbar: false,
      snackColor: "primary desertsand--text",
      snackTimeout: 2000,
      snackText: "",
      submittingFork: false,
      submittingSave: false,
      submittingDelete: false,
      forkOverwriteDialog: false,
      editing: false,
      unsavedChangesDialog: false,
      confirmDeleteDialog: false,
      unsavedChanges: false,
      currentContent: ``,

      editor: new Editor({
        editable: false,
        extensions: [
          new Blockquote(),
          new HardBreak(),
          new Heading({ levels: [1, 2, 3] }),
          new Bold(),
          new Alignment(),
          new TextDirection(),
          new Italic(),
          new Link(),
          new Strike(),
          new Underline(),
          new History(),
          new TimeStamp(),
          new Highlighter()
        ],
        editorProps: {
          handleClickOn: (view, pos, node, nodePos, event) => {
            if (node.type.name === "timestamp") {
              // console.log(`Skip to ${node.attrs.timehack}`);
              this.$emit("skipToTime", node.attrs.timehack);
            } else {
              return view, pos, node, nodePos, event;
            }
          }
        },
        content: `
          Loading
         `,
        onUpdate: () => {
          this.unsavedChanges = true;
          // console.log("Unsaved changes");
        },
        handleDOMEvents: {}
      })
    };
  },
  computed: {
    isCurator() {
      return (
        this.transcript.curator.username ===
        window.localStorage.getItem("username")
      );
    },
    editorFontClass() {
      return `font-size:${this.editorFontSize}em`;
    },
    userTranscriptLoaded() {
      return this.transcript.id === this.elementObject.user_transcript;
    },
    numberOfTranscripts() {
      if (this.elementObject) {
        return this.elementObject.transcripts
          ? this.elementObject.transcripts.length
          : "0";
      } else {
        return 0;
      }
    },
    userHasTranscript() {
      return this.elementObject.user_transcript > 0 ? true : false;
    }
  },

  methods: {
    printText() {
      var html = document.getElementById("transcripteditorbox").innerHTML;
      var a = window.open("", "", "height=300, width=300");
      var dateStamp = new Date();
      a.document.write(
        `
          <html>
          <head>
          <title>PF Printer...</title>
          </head>
            <style>
              .header {
                position: fixed;
                top: 0;
                left: 50%;
                transform: translate(-50%, 0);
              }
              .footer {
                position: fixed;
                bottom: 0;
                left: 50%;
                transform: translate(-50%, 0);
              }
              .content {
                margin-top: 35px;
                margin-bottom: 35px;
                margin-left: 25px;
                margin-right: 25px;
                font-family:Arial, Helvetica, sans-serif;
                line-height: 1.5;
                font-size: ${this.editorFontSize}em;
              }
            </style>
            <body>
                <div class="header">(Source Title: ${
                  this.elementObject.title
                })</div>
                <div class="content">${html}</div>
                <div class="footer">(PidginForge on ${dateStamp.toLocaleString()})</div>
            </body>  
          </html>
          <style>
          `
      );
      a.print();
    },
    triggerTimeStamp() {
      this.$emit("triggerTimeStamp");
    },

    recordTimeStamp(currenttime) {
      if (this.editing) {
        var newstamp = parseInt(currenttime);
        this.editor.commands.timestamp({ timehack: newstamp });
      } else {
        console.log("Transcript is locked");
      }
    },

    updateVote(data) {
      this.transcript.user_vote = data.newuservote;
      this.transcript.downvote_count = data.newdowncount;
      this.transcript.upvote_count = data.newupcount;
    },
    checkEdits() {
      if (this.unsavedChanges) {
        this.unsavedChangesDialog = true;
      } else {
        this.closeEdit();
      }
    },
    saveEditsThenClose() {
      this.unsavedChangesDialog = false;
      if (this.submitSave()) {
        this.closeEdit();
      } else {
        console.log("error saving");
      }
    },
    trashEditsThenClose() {
      this.unsavedChangesDialog = false;
      this.editor.setContent(this.currentContent);
      this.closeEdit();
    },
    closeEdit() {
      this.editing = false;
      this.editor.setOptions({
        editable: this.editing
      });
    },
    openEdit() {
      this.editing = true;
      this.editor.setOptions({
        editable: this.editing
      });
    },
    loadImage: function(command) {
      command({
        src:
          "https://66.media.tumblr.com/dcd3d24b79d78a3ee0f9192246e727f1/tumblr_o00xgqMhPM1qak053o1_400.gif"
      });
    },
    togglePublish() {
      this.publishing = true;
      let endpoint = "/api/elements/transcript/publish/";

      try {
        apiService(endpoint, "POST", { pk: this.transcript.id }).then(data => {
          if (data != null) {
            if (data.success == true) {
              // this.$emit("hideElement")
              this.transcript.published = data.published;
              this.fetchElementObject();
            } else {
              // this.alertType = 'error';
            }
          } else {
            // this.alertType = 'error';
          }
          this.publishing = false;
        });
      } catch (err) {
        console.log(err);
      }
    },
    changeEditorFontSize(direction) {
      if (direction === "up") {
        if (this.editorFontSize < 3.5) {
          this.editorFontSize += 0.15;
        }
      } else {
        if (this.editorFontSize > 0.5) {
          this.editorFontSize -= 0.15;
        }
      }
    },
    loadTranscript(transcriptid) {
      this.loadingTranscript = true;
      if (transcriptid === 0) {
        // CREATE A NEW TRANSCRIPT IF THERE ISN'T ONE
        // console.log("Creating new transcript...")
        let endpoint = `/api/elements/transcriptz/`;
        let payload = {
          elementtype: this.elementType,
          elementslug: this.elementSlug,
          content: "new transcript",
          notes: "",
          usertranscript: 0
        };

        apiService(endpoint, "POST", payload).then(data => {
          if (data) {
            this.transcript = data;
            this.showTranslation = false;
            this.elementObject.user_transcript = this.transcript.id;
            this.transcriptLoaded = true;
            this.feedSnack(
              "success darken-1 desertsand--text body-1",
              "New transcript created!",
              2750
            );
            this.currentContent = this.transcript.content;
            this.editor.setContent(this.currentContent);
          } else {
            console.log("Something went wrong");
            this.transcriptLoaded = false;
          }
          this.loadingTranscript = false;
        });
      } else {
        // Try to load existing transcript
        let endpoint = `/api/elements/transcriptz/${transcriptid}/`;
        apiService(endpoint).then(data => {
          if (data.id) {
            // console.log(data);
            this.transcript = data;
            this.transcriptLoaded = true;
            this.currentContent = this.transcript.content;
            this.editor.setContent(this.currentContent);
            this.loadingTranscript = false;
            this.showTranslation = false;
          } else {
            if (data.message) {
              this.feedSnack(
                "elements darken-1 desertsand--text body-1",
                data.message,
                2750
              );
            } else {
              this.feedSnack(
                "elements darken-1 desertsand--text body-1",
                "Unknown error loading transcript!",
                2750
              );
            }
            this.transcript = {};
            this.transcriptLoaded = false;
            this.showTranscript = false;
          }
          this.loadingTranscript = false;
        });
        // this.$refs.scripteditor.loadTranscript(transcriptid);
      }
    },

    async submitSave() {
      // CREATE A NEW TRANSCRIPT...
      this.submittingSave = true;
      let content = (this.currentContent = this.editor.getJSON());
      let endpoint = `/api/elements/transcriptz/${this.transcript.id}/`;
      let payload = {
        content: content,
        notes: ""
      };
      apiService(endpoint, "PATCH", payload).then(data => {
        if (data) {
          this.unsavedChanges = false;
          this.submittingSave = false;
          this.feedSnack(
            "success darken-1 desertsand--text body-1",
            "Edits have been saved!",
            2250
          );
          return true;
        } else {
          this.submittingSave = false;
          return false;
        }
      });
    },
    deleteTranscript() {
      this.submittingDelete = true;
      let endpoint = `/api/elements/transcriptz/${this.transcript.id}/`;
      try {
        apiService(endpoint, "DELETE").then(() => {
          this.feedSnack(
            "garbage darken-1 desertsand--text body-1",
            "Transcript deleted! :-(",
            2750
          );
          this.fetchElementObject();

          // this.$router.go()
          this.submittingDelete = false;
          this.confirmDeleteDialog = false;
          this.transcriptLoaded = false;
        });
      } catch (err) {
        console.log(err);
      }
    },
    forkTranscript() {
      // CREATE A NEW TRANSCRIPT...
      this.submittingFork = true;
      let content = this.editor.getJSON();
      let endpoint = `/api/elements/transcriptz/`;
      let dateStamp = new Date();
      let payload = {
        elementtype: this.elementType,
        elementslug: this.elementSlug,
        forkparent: this.transcript.id,
        usertranscript: this.elementObject.user_transcript,
        content: content,
        notes: `This transcript was forked from ${
          this.transcript.curator
        }'s transcript on ${dateStamp.toDateString()}`
      };

      apiService(endpoint, "POST", payload).then(data => {
        if (data) {
          this.loadTranscript(data.id);
          this.fetchElementObject();
        } else {
          console.log("There was a problem");
        }
        this.submittingFork = false;
      });
    },

    fetchElementObject() {
      this.fetchingElementObject = true;
      let endpoint = ``;
      if (this.elementType === "YouTube") {
        endpoint = `/api/elements/youtubez/${this.elementSlug}/`;
      } else if (this.elementType === "Audio") {
        endpoint = `/api/elements/audioz/${this.elementSlug}/`;
      }
      if (endpoint) {
        apiService(endpoint).then(data => {
          if (data) {
            this.elementObject = data;
            // console.log(this.elementObject.user_transcript);
          } else {
            console.log("Problem");
          }
          this.fetchingElementObject = false;
        });
      }
    },
    feedSnack(scheme, message, timeout) {
      this.snackColor = scheme;
      this.snackText = message;
      this.snackTimeout = timeout;
      this.snackbar = true;
    }
  },
  beforeDestroy() {
    this.editor.destroy();
  },
  mounted() {
    this.elementObject = this.passedObject;
    // this.fetchElementObject();
  }
};
</script>
<style>
.editor-box > * {
  border-color: sandstone;
  color: black;
  background-color: white;
  border-style: solid;
  border-width: 1px;
  padding: 4px, 4px;
  width: 100%;
  height: 300px;
  overflow-x: hidden;
  overflow-x: auto;
  font-size: 1.5em;
  font-family: Arial, Helvetica, sans-serif;
  line-height: 1.5;
}

.is-active {
  border-color: orange;
  background-color: black;
  border-style: solid;
  border-width: 1px;
}

.v-card__text,
.v-card__title {
  word-break: keep-all; /* maybe !important  */
  word-wrap: normal;
}
</style>
