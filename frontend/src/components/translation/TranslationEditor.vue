<template>
  <div>
    <v-card class="calligraphy" dense v-if="sourceObject.id">
      <v-card-title class="py-1 desertsand--text">
        Translations:
        <v-btn
          outlined
          v-if="!userHasTranslation"
          class="primary desertsand--text ma-1"
          @click="loadTranslation(0)"
          >Add New<v-icon right>mdi-plus-circle</v-icon></v-btn
        >
        <v-btn
          v-if="userHasTranslation && !userTranslationLoaded"
          class="desertsand--text ma-1"
          outlined
          @click="loadTranslation(sourceObject.user_translation)"
          >View Yours<v-icon right>mdi-pencil</v-icon></v-btn
        >
        <v-btn
          :loading="fetchingSource"
          :disabled="numberOfTranslations < 1"
          @click="showTranslationList = true"
          class="desertsand--text ma-1"
          outlined
        >
          View Published
          <v-badge :content="numberOfTranslations" color="calligraphy darken-1">
            <v-icon>mdi-script-text-outline</v-icon>
          </v-badge>
        </v-btn>

        <v-dialog v-model="showTranslationList" width="395">
          <template> </template>
          <TranslationListModal
            @closeDialog="showTranslationList = false"
            :translation-list="sourceObject.translations"
            @loadTranslation="loadTranslation"
          />
        </v-dialog>
      </v-card-title>

      <v-card-text
        class="desertsand calligraphy--text px-2 ma-0"
        v-if="translationLoaded"
      >
        <v-row dense wrap no-gutters>
          <v-col cols="12">
            By
            <span class="primary--text font-weight-black mx-1">
              {{ translation.curator.username }}
            </span>
            on {{ translation.curationdate }}
            <v-chip outlined small color="languages" class="mx-2">{{
              translation.targetlanguage
            }}</v-chip>

            <ElementVoter
              @updateVote="updateVote"
              :up-vote-count="translation.upvote_count"
              :down-vote-count="translation.downvote_count"
              :user-vote="translation.user_vote"
              :elementid="translation.id"
              element-type="Translation"
              text-typography="body-1"
            />
          </v-col>
          <v-col cols="12" class="overline" v-if="!translation.published">
            ...this translation is currently in draft and not visible to
            others...
          </v-col>
          <v-col cols="12" class="overline" v-if="translation.forkparent">
            ...this translation was forked from
            <a
              class="primary--text font-weight-black"
              @click.prevent="loadTranslation(translation.forkparent)"
              >Translation ID: {{ translation.forkparent }}</a
            >...
          </v-col>

          <v-col cols="12">
            <v-toolbar dense v-if="!isCurator" flat class="calligraphy pa-0">
              <v-btn
                small
                color="elements desertsand--text"
                @click="
                  userHasTranslation
                    ? (forkOverwriteDialog = true)
                    : forkTranslation
                "
              >
                Fork
                <v-badge
                  :content="translation.forks_count"
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
                    >Delete Your Translation?</v-card-title
                  >
                  <v-card-text class="desertsand calligraphy--text pt-1">
                    You've already started a translation for this source item.
                    In order to fork a new translation, you must first delete
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
                      @click="forkTranslation"
                      >Proceed <v-icon right>mdi-source-fork</v-icon></v-btn
                    >
                  </v-card-actions>
                </v-card>
              </v-dialog>

              <v-btn disabled text class="mr-1">
                QC
              </v-btn>
            </v-toolbar>

            <v-toolbar v-if="isCurator" dense flat class="calligraphy pa-0">
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
                  <v-card-title class="headline">Unsaved Changes</v-card-title>
                  <v-card-text class="desertsand calligraphy--text pt-1">
                    You have made changes to your translation. Would you like to
                    save them, or throw them away?
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
                  <v-card-title class="headline">Confirm Delete?</v-card-title>
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
                      @click="deleteTranslation"
                      :loading="submittingDelete"
                      >Delete<v-icon right>mdi-delete</v-icon></v-btn
                    >
                  </v-card-actions>
                </v-card>
              </v-dialog>

              <v-btn
                small
                class="elements desertsand--text mr-1"
                v-if="!translation.published && !editing"
                @click="togglePublish"
              >
                Publish<v-icon right>mdi-eye</v-icon>
              </v-btn>
              <v-btn
                small
                class="elements desertsand--text mr-1"
                v-if="translation.published && !editing"
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

                  <v-overflow-btn
                    @change="unsavedChanges = true"
                    :items="allLanguages"
                    v-model="translation.targetlanguage"
                    :loading="loadingLanguages"
                    editable
                    dense
                    color="sandstone calligraphy--text"
                    label="Select Language"
                    hide-details
                    class="pa-0"
                    overflow
                    item-color="primary"
                  ></v-overflow-btn>
                  <v-spacer></v-spacer>
                </v-toolbar>
              </div>
            </editor-menu-bar>
            <editor-content :editor="editor" :style="editorFontClass" class="editor-box" id="translationeditorbox" />
            <v-card-actions>
              <v-btn icon @click="changeEditorFontSize('down')">
                    <v-icon>mdi-magnify-minus</v-icon>
              </v-btn>
                Text Size
              <v-btn icon @click="changeEditorFontSize('up')">
                  <v-icon>mdi-magnify-plus</v-icon>
              </v-btn>
              <v-btn icon @click="printText"><v-icon>mdi-printer</v-icon></v-btn>
            </v-card-actions>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    <v-overlay
      :value="loadingTranslation"
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
  </div>
</template>

<script>
// Import the editor
// import TranslationListModal from "@/components/translation/TranslationListModal.vue";
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
import { default as Highlighter } from "@/components/tiptaptoo/Highlighter.js";

export default {
  name: "TranslationEditor",
  components: {
    EditorContent,
    EditorMenuBar,
    ElementVoter,
    // TranslationEditor: () =>
    //   import(
    //     /* webpackPrefetch: true */ "@/components/translation/TranslationEditor.vue"
    //   ),
    TranslationListModal: () =>
      import(
        /* webpackPrefetch: true */ "@/components/translation/TranslationListModal.vue"
      )
  },
  props: {
    sourceType: {
      type: String,
      required: true
    },
    passedSource: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      sourceObject: {},
      translation: {
        targetlanguage: ""
      },
      fetchingSource: false,

      showTranslationList: false,
      showTranslation: false,

      editorFontSize: 1,
      languageDialog: false,
      allLanguages: [],
      loadingLanguages: false,

      translationLoaded: false,
      loadedTranslation: 0,
      loadingTranslation: false,

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
      unsavedChanges: false,
      currentContent: ``,
      confirmDeleteDialog: false,
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
          new Highlighter()
        ],
        content: `
          Loading
         `,
        onUpdate: () => {
          this.unsavedChanges = true;
          // console.log("Unsaved changes");
        },
      })
    };
  },
  watch: {},
  computed: {
    isCurator() {
      if (this.translation.curator) {
        return (
          this.translation.curator.username ===
          window.localStorage.getItem("username")
        );
      } else {
        return false;
      }
    },
    editorFontClass(){
      return `font-size:${this.editorFontSize}em`
    },
    numberOfTranslations() {
      if (this.sourceObject.translations) {
        return this.sourceObject.translations.length;
      } else {
        return 0;
      }
    },
    userHasTranslation() {
      return this.sourceObject.user_translation > 0 ? true : false;
    },
    userTranslationLoaded() {
      return this.translation.id === this.sourceObject.user_translation;
    }
  },
  methods: {
    getLanguages() {
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
    },
    changeEditorFontSize(direction){
      if(direction==="up"){
        if(this.editorFontSize < 3.5){
          this.editorFontSize += 0.15
        }
      } else {
        if(this.editorFontSize > 0.5){
          this.editorFontSize -= 0.15
        }
      }
    },
    updateVote(data) {
      this.translation.user_vote = data.newuservote;
      this.translation.downvote_count = data.newdowncount;
      this.translation.upvote_count = data.newupcount;
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
      let endpoint = "/api/elements/translation/publish/";

      try {
        apiService(endpoint, "POST", { pk: this.translation.id }).then(data => {
          if (data != null) {
            if (data.success == true) {
              // console.log(data);
              // this.$emit("hideElement")
              this.translation.published = data.published;
              this.refetchSourceElement();
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

    loadTranslation(translationid) {
      this.loadingTranslation = true;
      if (translationid === 0) {
        // CREATE A NEW TRANSCRIPT IF THERE ISN'T ONE
        // console.log("Creating new translation...")
        let endpoint = `/api/elements/translationz/`;
        let payload = {
          // elementtype: this.sourceType,
          // elementslug: this.elementSlug,
          sourceid: this.sourceObject.id,
          sourcetype: this.sourceType,
          content: "new translation",
          targetlanguage: "English"
          // usertranscript: 0
        };
        // console.log(payload);
        apiService(endpoint, "POST", payload).then(data => {
          if (data) {
            this.translation = data;
            this.sourceObject.user_translation = this.translation.id;
            this.translationLoaded = true;
            // this.isNewTranslation = true;
            this.feedSnack(
              "success darken-1 desertsand--text body-1",
              "New translation created!",
              2750
            );
            this.currentContent = this.translation.content;
            this.editor.setContent(this.currentContent);
          } else {
            console.log("Something went wrong");
            this.translationLoaded = false;
          }
          this.loadingTranslation = false;
        });
      } else {
        // Try to load existing translation
        let endpoint = `/api/elements/translationz/${translationid}/`;
        try {
          apiService(endpoint).then(data => {
            if (data.id) {
              this.translation = data;
              this.translationLoaded = true;
              this.currentContent = this.translation.content;
              this.editor.setContent(this.currentContent);
            } else {
              this.feedSnack(
                "elements darken-1 desertsand--text body-1",
                "Error loading translation!",
                2750
              );
              this.translation = {};
              this.translationLoaded = false;
              // this.translation = {};
              // this.translationLoaded = false;
              // this.showTranslation = false;
            }
            this.loadingTranslation = false;
          });
        } catch (err) {
          console.log(err);
          this.loadTranslation = false;
        }

        // this.$refs.scripteditor.loadTranslation(translationid);
      }
    },
    async submitSave() {
      // CREATE A NEW translation...
      this.submittingSave = true;
      let content = (this.currentContent = this.editor.getJSON());
      let endpoint = `/api/elements/translationz/${this.translation.id}/`;
      let payload = {
        content: content,
        // notes: "",
        targetlanguage: this.translation.targetlanguage
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
    deleteTranslation() {
      this.submittingDelete = true;
      let endpoint = `/api/elements/translationz/${this.translation.id}/`;
      try {
        apiService(endpoint, "DELETE").then(() => {
          this.feedSnack(
            "garbage darken-1 desertsand--text body-1",
            "Translation deleted! :-(",
            2750
          );
          this.refetchSourceElement();
          // this.$router.go()
          this.submittingDelete = false;
          this.confirmDeleteDialog = false;
          this.translationLoaded = false;
        });
      } catch (err) {
        console.log(err);
      }
    },
    printText(){
        var html = document.getElementById("translationeditorbox").innerHTML
        var a = window.open('', '', 'height=300, width=300');
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
                font-family:Arial, Helvetica, sans-serif;
                line-height: 1.5;
                font-size: ${this.editorFontSize}em;
              }
            </style>
            <body>
                <div class="header">${this.sourceObject.title}</div>
                <div class="content">${html}</div>
                <div class="footer">PidginForge on ${dateStamp.toLocaleString()}</div>
            </body>  
          </html>
          <style>
          `
        );
        a.print();
    },
    forkTranslation() {
      // CREATE A NEW TRANSLATION...
      this.submittingFork = true;
      let content = this.editor.getJSON();
      let endpoint = `/api/elements/translationz/`;
      let dateStamp = new Date();
      let payload = {
        sourcetype: this.sourceType,
        sourceid: this.sourceObject.id,
        forkparent: this.translation.id,
        // usertranscript: this.sourceObject.user_transcript,
        content: content,
        notes: `This translation was forked from ${
          this.translation.curator
        }'s translation on ${dateStamp.toDateString()}`
      };
      apiService(endpoint, "POST", payload).then(data => {
        if (data) {
          this.loadTranslation(data.id);
          this.refetchSourceElement();
        } else {
          console.log("There was a problem");
        }
        this.submittingFork = false;
      });
    },
    submitLanguage() {
      console.log("submitting");
    },
    refetchSourceElement() {
      this.fetchingSource = true;
      let endpoint = ``;
      if (this.sourceType === "graphic") {
        endpoint = `/api/elements/graphicz/${this.sourceObject.id}/`;
      } else if (this.sourceType === "transcript") {
        endpoint = `/api/elements/transcriptz/${this.sourceObject.id}/`;
      }
      apiService(endpoint).then(data => {
        if (data) {
          this.sourceObject = data;

        } else {
          console.log("Problem");
        }
        this.fetchingSource = false;
      });
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
    this.sourceObject = this.passedSource;
    // this.refetchSourceElement();
  },
  created() {
    this.getLanguages();
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
  font-size:1.5em;
  font-family:Arial, Helvetica, sans-serif;
  line-height: 1.5;
}

.is-active {
  border-color: desertsand;
  background-color: black;
  border-style: solid;
  border-width: 2px;
}
</style>
