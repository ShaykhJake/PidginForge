<template>
  <div>
    <v-card class="calligraphy" dense v-if="sourceObject.id">
      <v-card-title class="py-1 desertsand--text">
        Markups:
        <v-btn
          outlined
          v-if="!userHasMarkup"
          class="primary desertsand--text ma-1"
          @click="loadMarkup(0)"
          >Add New<v-icon right>mdi-plus-circle</v-icon></v-btn
        >
        <v-btn
          v-if="userHasMarkup && !userMarkupLoaded"
          class="desertsand--text ma-1"
          outlined
          @click="loadMarkup(sourceObject.user_markup)"
          >View Yours<v-icon right>mdi-pencil</v-icon></v-btn
        >
        <v-btn
          :loading="fetchingSource"
          :disabled="numberOfMarkups < 1"
          @click="showMarkupList = true"
          class="desertsand--text ma-1"
          outlined
        >
          View Published
          <v-badge :content="numberOfMarkups" color="calligraphy darken-1">
            <v-icon>mdi-script-text-outline</v-icon>
          </v-badge>
        </v-btn>

        <v-dialog v-model="showMarkupList" width="395">
          <template> </template>
          <MarkupListModal
            @closeDialog="showMarkupList = false"
            :markup-list="sourceObject.markups"
            @loadMarkup="loadMarkup"
          />
        </v-dialog>
      </v-card-title>

      <v-card-text
        class="desertsand calligraphy--text px-2 ma-0"
        v-if="markupLoaded"
      >
        <v-row dense wrap no-gutters>
          <v-col cols="12">
            By
            <span class="primary--text font-weight-black mx-1">
              {{ markup.curator.username }}
            </span>
            on {{ markup.curationdate }}
            <v-chip outlined small color="languages" class="mx-2">{{
              markup.targetlanguage
            }}</v-chip>

            <ElementVoter
              @updateVote="updateVote"
              :up-vote-count="markup.upvote_count"
              :down-vote-count="markup.downvote_count"
              :user-vote="markup.user_vote"
              :elementid="markup.id"
              element-type="Markup"
              text-typography="body-1"
            />
            
          </v-col>
          <v-col cols="12" class="overline" v-if="!markup.published">
            ...this markup is currently in draft and not visible to
            others...
          </v-col>
          <v-col cols="12" class="overline" v-if="markup.forkparent">
            ...this markup was forked from
            <a
              class="primary--text font-weight-black"
              @click.prevent="loadMarkup(markup.forkparent)"
              >Markup ID: {{ markup.forkparent }}</a
            >...
          </v-col>

          <v-col cols="12">
            <v-toolbar dense v-if="!isCurator" flat class="calligraphy pa-0">
              <v-btn
                small
                color="elements desertsand--text"
                @click="
                  userHasMarkup
                    ? (forkOverwriteDialog = true)
                    : forkMarkup
                "
              >
                Fork
                <v-badge
                  :content="markup.forks_count"
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
                    >Delete Your Markup?</v-card-title
                  >
                  <v-card-text class="desertsand calligraphy--text pt-1">
                    You've already started a markup for this source item.
                    In order to fork a new markup, you must first delete
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
                      @click="forkMarkup"
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
                    You have made changes to your markup. Would you like to
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
                      @click="deleteMarkup"
                      :loading="submittingDelete"
                      >Delete<v-icon right>mdi-delete</v-icon></v-btn
                    >
                  </v-card-actions>
                </v-card>
              </v-dialog>

              <v-btn
                small
                class="elements desertsand--text mr-1"
                v-if="!markup.published && !editing"
                @click="togglePublish"
              >
                Publish<v-icon right>mdi-eye</v-icon>
              </v-btn>
              <v-btn
                small
                class="elements desertsand--text mr-1"
                v-if="markup.published && !editing"
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
                    v-model="markup.targetlanguage"
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
            <editor-content :editor="editor" :style="editorFontClass" class="editor-box" id="markupeditorbox" />
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
      :value="loadingMarkup"
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
// import MarkupListModal from "@/components/markup/MarkupListModal.vue";
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
  name: "MarkupEditor",
  components: {
    EditorContent,
    EditorMenuBar,
    ElementVoter,
    // MarkupEditor: () =>
    //   import(
    //     /* webpackPrefetch: true */ "@/components/markup/MarkupEditor.vue"
    //   ),
    MarkupListModal: () =>
      import(
        /* webpackPrefetch: true */ "@/components/textmarkup/MarkupListModal.vue"
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
      markup: {
        targetlanguage: ""
      },
      fetchingSource: false,

      showMarkupList: false,
      showMarkup: false,

      editorFontSize: 1,
      languageDialog: false,
      allLanguages: [],
      loadingLanguages: false,

      markupLoaded: false,
      loadedMarkup: 0,
      loadingMarkup: false,

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
      if (this.markup.curator) {
        return (
          this.markup.curator.username ===
          window.localStorage.getItem("username")
        );
      } else {
        return false;
      }
    },
    editorFontClass(){
      return `font-size:${this.editorFontSize}em`
    },
    numberOfMarkups() {
      if (this.sourceObject.markups) {
        return this.sourceObject.markups.length;
      } else {
        return 0;
      }
    },
    userHasMarkup() {
      return this.sourceObject.user_markup > 0 ? true : false;
    },
    userMarkupLoaded() {
      return this.markup.id === this.sourceObject.user_markup;
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
    printText(){
        var html = document.getElementById("markupeditorbox").innerHTML
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
      this.markup.user_vote = data.newuservote;
      this.markup.downvote_count = data.newdowncount;
      this.markup.upvote_count = data.newupcount;
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
      let endpoint = "/api/elements/markup/publish/";

      try {
        apiService(endpoint, "POST", { pk: this.markup.id }).then(data => {
          if (data != null) {
            if (data.success == true) {
              // console.log(data);
              this.markup.published = data.published;
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

    loadMarkup(markupid) {
      this.loadingMarkup = true;
      if (markupid === 0) {
        // CREATE A NEW MARKUP IF THERE ISN'T ONE
        // console.log("Creating new markup...")
        let endpoint = `/api/elements/markupz/`;
        let payload = {
          // elementtype: this.sourceType,
          // elementslug: this.elementSlug,
          sourceid: this.sourceObject.id,
          sourcetype: this.sourceType,
          content: "...new markup...",
          // TODO - Fix the language so it defaults to the User's native language
          targetlanguage: "English"
          // usertranscript: 0
        };
        console.log(payload);
        apiService(endpoint, "POST", payload).then(data => {
          if (data) {
            console.log(data)
            this.markup = data;
            console.log(this.markup.content)
            this.sourceObject.user_markup = this.markup.id;
            this.markupLoaded = true;
            // this.isNewMarkup = true;
            this.feedSnack(
              "success darken-1 desertsand--text body-1",
              "New markup created!",
              2750
            );
            this.currentContent = this.markup.content;
            this.editor.setContent(this.currentContent);
          } else {
            console.log("Something went wrong");
            this.markupLoaded = false;
          }
          this.loadingMarkup = false;
        });
      } else {
        // Try to load existing markup
        let endpoint = `/api/elements/markupz/${markupid}/`;
        try {
          apiService(endpoint).then(data => {
            if (data.id) {
              this.markup = data;
              this.markupLoaded = true;
              this.currentContent = this.markup.content;
              this.editor.setContent(this.currentContent);
            } else {
              this.feedSnack(
                "elements darken-1 desertsand--text body-1",
                "Error loading markup!",
                2750
              );
              this.markup = {};
              this.markupLoaded = false;
              // this.markup = {};
              // this.markupLoaded = false;
              // this.showMarkup = false;
            }
            this.loadingMarkup = false;
          });
        } catch (err) {
          console.log(err);
          this.loadMarkup = false;
        }

        // this.$refs.scripteditor.loadMarkup(markupid);
      }
    },
    async submitSave() {
      // CREATE A NEW markup...
      this.submittingSave = true;
      let content = (this.currentContent = this.editor.getJSON());
      let endpoint = `/api/elements/markupz/${this.markup.id}/`;
      let payload = {
        content: content,
        // notes: "",
        targetlanguage: this.markup.targetlanguage
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
    deleteMarkup() {
      this.submittingDelete = true;
      let endpoint = `/api/elements/markupz/${this.markup.id}/`;
      try {
        apiService(endpoint, "DELETE").then(() => {
          this.feedSnack(
            "garbage darken-1 desertsand--text body-1",
            "Markup deleted! :-(",
            2750
          );
          this.sourceObject.user_markup = 0;
          // this.$emit("updateSource");
          // this.$router.go()
          this.submittingDelete = false;
          this.confirmDeleteDialog = false;
          this.markupLoaded = false;
        });
      } catch (err) {
        console.log(err);
      }
    },
    forkMarkup() {
      this.submittingFork = true;
      let endpoint = `/api/elements/markup/fork/`;
      let payload = {
        sourceid: this.sourceObject.id,
        forkparent: this.markup.id,
      };
      apiService(endpoint, "POST", payload).then(data => {
        if (data) {
          this.forkOverwriteDialog = false; 
          this.loadMarkup(data.id);
          this.sourceObject.user_markup = data.id;
          // this.refetchSourceElement();
        } else {
          console.log("There was a problem");
        }
        this.forkOverwriteDialog = false; 
        this.submittingFork = false;
      });
    },
    submitLanguage() {
      console.log("submitting");
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
