<template>
  <div class="textelement sandstone">
    <v-container fluid>
      <v-card class="desertsand">
        <v-card-title class="pb-1">
          <v-row wrap dense no-gutters class="pa-1">
            <v-col cols="12">
              {{ elementObject.title }}
            </v-col>
            <v-col cols="12">
              <p class="overline mb-2">
                Curated by
                    <v-btn
                      @click="profileDialog=true"
                      text
                      small
                      class="primary--text font-weight-bold px-0 py-0"
                    >
                      {{ curatorName }}
                    </v-btn>
                  <ProfileSnippet
                    v-if="profileDialog"
                    :curator-object="elementObject.curator"
                    @closeDialog="closeProfileDialog"
                  />
                on {{ elementObject.curationdate }} <br />
              </p>
            </v-col>
          </v-row>
        </v-card-title>
        <v-card-text class="pt-1">
          <v-row dense no-gutters>
            <v-col cols="12" sm="7" class="pr-5">
              <v-card class="sandstone">

                  <editor-menu-bar
                    v-if="editor.editable"
                    :editor="editor"
                    v-slot="{ commands, isActive }"
                  >
                    <div class="desertsand--text">
                      <v-toolbar dense flat class="sandstone">
                          <v-btn
                            small
                            icon
                            color="calligraphy"
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
                            color="calligraphy"
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
                            color="calligraphy"
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
                            color="calligraphy"
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
                            color="calligraphy"
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
                            color="calligraphy"
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
                            color="calligraphy"
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
                            color="calligraphy"
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
                            color="calligraphy"
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
                            color="calligraphy"
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
                            color="calligraphy"
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


                          <v-divider class="mx-1" inset vertical></v-divider>
                        <v-spacer></v-spacer>
                        Count: {{ characterCount }}
                      </v-toolbar>
                    </div>
                  </editor-menu-bar>

                  <editor-content :editor="editor" :style="editorFontClass" class="editor-box" id="editorbox" />
                  <v-card-actions>
                    <v-btn color="calligraphy" icon @click="changeEditorFontSize('down')">
                      <v-icon>mdi-magnify-minus</v-icon>
                    </v-btn>
                      Text Size
                    <v-btn icon color="calligraphy" @click="changeEditorFontSize('up')">
                      <v-icon>mdi-magnify-plus</v-icon>
                    </v-btn>
                    <v-btn icon @click="printText"><v-icon>mdi-printer</v-icon></v-btn>
                    <v-spacer></v-spacer>
                  </v-card-actions>
              </v-card>

            </v-col>
            <v-col cols="12" sm="5" align="center">
              <p align="left">
                <span class="font-weight-bold">Learning Purpose:</span>
                {{ elementObject.purpose }}
              </p>
              <ElementVoter
                @updateVote="updateVote"
                :up-vote-count="elementObject.upvote_count"
                :down-vote-count="elementObject.downvote_count"
                :user-vote="elementObject.user_vote"
                :slug="elementslug"
                element-type="Text"
              />
              <hr />
              Target Language:
              <v-chip outlined small class="languages languages--text">{{
                elementObject.language
              }}</v-chip
              ><br />
              Primary Topic:
              <v-chip outlined small class="topics topics--text">{{
                elementObject.topic
              }}</v-chip
              ><br />
              Tag(s):
              <v-chip
                outlined
                small
                class="tags tags--text"
                v-for="tag in elementObject.tags"
                :key="tag.id"
                >{{ tag }}</v-chip
              >
              <hr />

              <v-btn
                class="mr-1 mb-1 saves desertsand--text"
                @click="toggleSave"
                :loading="saving"
                icon
              >
                <v-badge
                  color="saves lighten-2"
                  :content="elementObject.saved_count"
                >
                  <v-icon v-if="!elementObject.user_has_saved">mdi-heart</v-icon>
                  <v-icon v-else>mdi-heart-broken</v-icon>
                </v-badge>
              </v-btn>
              <v-btn
                class="mr-1 mb-1 garbage desertsand--text"
                @click="toggleHide"
                :loading="hiding"
                icon
              >
                <v-icon v-if="!elementObject.user_has_hidden">mdi-eye-off</v-icon>
                <v-icon v-else>mdi-eye</v-icon>
              </v-btn>

              <v-btn
                @click="textEditorDialog=true"
                class="mr-1 mb-1 primary desertsand--text"
                icon
              >
                <v-icon>
                  mdi-pencil
                </v-icon>
              </v-btn>

              <v-btn
                @click="flaggerDialog = true"
                :disabled="elementObject.user_has_flagged"
                class="mr-1 mb-1 error white--text"
                icon
              >
                <v-badge
                  color="error lighten-1 white--text"
                  :content="elementObject.flag_count"
                >
                  <v-icon>mdi-flag</v-icon>
                </v-badge>
              </v-btn>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-btn v-if="!showMarkups" class="sandstone" @click="showMarkups=!showMarkups">
            Show Markups<v-icon>mdi-marker</v-icon>
          </v-btn>
          <v-btn v-else class="sandstone" @click="showMarkups=!showMarkups">
            Hide Markups<v-icon>mdi-eye</v-icon>
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn v-if="!showTranslations" class="sandstone" @click="showTranslations=!showTranslations">
            <v-badge
              :content="elementObject.translations.length || '0'"
            >
              Show Translations<v-icon>mdi-script-text-outline</v-icon>
            </v-badge>
          </v-btn>
          <v-btn v-else class="sandstone" @click="showTranslations=!showTranslations">
            Hide Translations<v-icon>mdi-eye-off</v-icon>
          </v-btn>

        </v-card-actions>
      </v-card>

      <v-row dense no-gutters wrap class="d-none d-sm-flex">
        <v-col cols="12">

          <TextElementEditor
            v-if="textEditorDialog"
            :editor-dialog="textEditorDialog"
            :is-new-element="false"
            :old-text-element="elementObject"
            @closeDialog="textEditorDialog = false"
          />
          <ContentFlagger
            :flagger-dialog="flaggerDialog"
            @closeDialog="flaggerDialog = false"
            @flagSuccess="elementObject.user_has_flagged=true; elementObject.flag_count += 1"
            content-type="Text"
            :contentid="elementObject.id"
          />

        </v-col>
      </v-row>
      <v-row>
        <v-col v-if="showMarkups">
          <MarkupEditor 
            ref="markupeditor"
            :passed-source="elementObject"
            source-type="TextElement"
            @updateSource="getTextElement"

          />
        </v-col>
        <v-col v-if="showTranslations">
          <TranslationEditor 
            ref="translationeditor"
            :passed-source="elementObject"
            source-type="TextElement"
            @updateSource="getTextElement"
          />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
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

import ElementVoter from "@/components/elements/ElementVoter.vue";
import ContentFlagger from "@/components/ContentFlagger.vue";
export default {
  name: "TextElementViewer",
  components: {
    // YTUpDownVote,
    ElementVoter,
    ContentFlagger,
    EditorContent,
    EditorMenuBar,

    ProfileSnippet: () =>
      import(
        /* webpackPrefetch: true */ "@/components/profile/ProfileSnippet.vue"
      ),
    TextElementEditor: () =>
      import(
        /* webpackPrefetch: true */ "@/components/elements/TextElementEditor.vue"
      ),
    MarkupEditor: () =>
      import(
        /* webpackPrefetch: true */ "@/components/textmarkup/MarkupEditor.vue"
      ),
    TranslationEditor: () =>
      import(
        /* webpackPrefetch: true */ "@/components/translation/TranslationEditor.vue"
      ),

  },
  data() {
    return {
      textEditorDialog: false,
      profileDialog: false,
      elementObject: {
        curator: {},
        translations: {}
      },
      printContent: '',
      printing: false,
      output: null,
      max: 100,
      youTubePlayerKey: 0,
      next: null,
      flaggerDialog: false,
      showTranslations: false,
      showMarkups: false,
      loadingText: false,
      userHidden: false,
      saving: false,
      hiding: false,
      requestUser: "",
      userSaved: false,
      voteScore: 0,
      isProfileSnippetVisible: false,
      voteColor: "text--black font-weight-bold",
      editorFontSize: 1,
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
          ...type/paste text here...
         `,
      })

    };
  },
  props: {
    elementslug: {
      type: String,
      required: true
    }
  },
  computed: {
    curatorName() {
      return this.elementObject.curator.username;
    },
    userIsCurator() {
      return this.curatorName() === this.requestUser;
      // return false;
    },
    editorFontClass(){
      return `font-size:${this.editorFontSize}em`
    },

  },

  methods: {
    updateVote(data) {
      this.elementObject.user_vote = data.newuservote;
      this.elementObject.downvote_count = data.newdowncount;
      this.elementObject.upvote_count = data.newupcount;
    },
    closeProfileDialog() {
      this.profileDialog = false;
    },
    updateViewer(elementObject) {
      this.elementObject = elementObject;
    },
    setRequestUser() {
      return (this.requestUser = window.localStorage.getItem("username"));
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
    markupDeleted(){
      this.elementObject.user_markup = null
    },
    printText(){
        var html = document.getElementById("editorbox").innerHTML
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
                <div class="header">${this.elementObject.title}</div>
                <div class="content">${html}</div>
                <div class="footer">PidginForge on ${dateStamp.toLocaleString()}</div>
            </body>  
          </html>
          <style>
          `
        );
        a.print();
    },
    getTextElement() {
      this.loadingText = true;
      this.showMarkups = false;
      this.showMarkups = false;
      let endpoint = `/api/elements/textz/${this.elementslug}/`;
      apiService(endpoint).then(data => {
        if (data) {
          // console.log("Get Text:");
          // console.log(data);
          this.elementObject = data;
          this.editor.setContent(this.elementObject.content);
          //  this.loadingAudio = false;
          this.ready = true;
        } else {
          this.elementObject = null;
          this.setPageTitle("404 - Page Note Found");
        }
        this.loadingText = false;
      });
    },

    toggleSave() {
      this.saving = true;
      let endpoint = `api/elements/text/save/`;
      try {
        apiService(endpoint, "POST", { pk: this.elementObject.id }).then(
          data => {
            if (data != null) {
              if (data.success == true) {
                this.elementObject.user_has_saved = !this.elementObject
                  .user_has_saved;
                if (this.elementObject.user_has_saved) {
                  this.elementObject.saved_count += 1;
                } else {
                  this.elementObject.saved_count -= 1;
                }
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
    toggleHide() {
      this.hiding = true;
      let endpoint = `api/elements/text/hide/`;
      try {
        apiService(endpoint, "POST", { pk: this.elementObject.id }).then(
          data => {
            if (data != null) {
              if (data.success == true) {
                this.elementObject.user_has_hidden = !this.elementObject
                  .user_has_hidden;
              } else {
                this.alertType = "error";
              }
            } else {
              this.alertType = "error";
            }
            this.hiding = false;
          }
        );
      } catch (err) {
        console.log(err);
      }
    },
  },
  watch: {
  },
  mounted() {
    this.getTextElement();
  },
  beforeDestroy() {
  }
  // Get comments?? (this can probably just be part of the larger package
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
    font-size:1.25em;
    font-family:Arial, Helvetica, sans-serif;
    line-height: 1.5;
  }

  .is-active {
    border-color: orange;
    background-color: black;
    border-style: solid;
    border-width: 2px;
  }
</style>
