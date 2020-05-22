<template>
  <v-dialog
    v-model="editorDialog"
    scrollable
    persistent
    fullscreen
    hide-overlay
    transition="dialog-bottom-transition"
  >
    <v-card class="ma-0 desertsand" max-width="500">
      <v-card-title class="pb-1 calligraphy desertsand--text">
        <v-spacer></v-spacer>
        <span v-if="isNewElement">Import Text Element</span>
        <span v-else>Edit Text Element</span>
        <v-spacer></v-spacer>
      </v-card-title>
      <v-card-text class="pa-1 desertsand">
        <v-row wrap dense justify="center">
          <v-col cols="12" sm="10" md="8" lg="6">
            <p class="body-2 mx-2 black--text text-justify text-wrap">
              It is the responsibility of the uploader of this text element to
              ensure that copyright permissions have been properly secured with
              the content's creator. All imported material must have an
              appropriate source citation included. If it is the curator's own
              original work, or it is public domain, please cite that.
            </p>

            <v-row wrap dense no-gutters>
              <v-col cols="12"> </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-form
                  ref="details"
                  v-model="valid"
                  @submit.prevent
                  v-if="loaded"
                >
                  <v-text-field
                    v-model="newTextElement.title"
                    name="texttitle"
                    label="Element Title*"
                    placeholder="give this item a title"
                    :rules="[rules.requiredTitle]"
                    outlined
                    class="pb-0 mb-0"
                  ></v-text-field>

                  <editor-menu-bar
                    v-if="loaded"
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
                          :class="{
                            'is-active': isActive.heading({ level: 1 })
                          }"
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
                          :class="{
                            'is-active': isActive.heading({ level: 2 })
                          }"
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
                          :class="{
                            'is-active': isActive.heading({ level: 3 })
                          }"
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
                            'is-active': isActive.alignment({
                              orientation: 'left'
                            })
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
                        <v-btn
                          color="calligraphy"
                          icon
                          @click="changeEditorFontSize('down')"
                        >
                          <v-icon>mdi-magnify-minus</v-icon>
                        </v-btn>
                        Text Size
                        <v-btn
                          icon
                          color="calligraphy"
                          @click="changeEditorFontSize('up')"
                        >
                          <v-icon>mdi-magnify-plus</v-icon>
                        </v-btn>

                        <v-divider class="mx-1" inset vertical></v-divider>
                        <v-spacer></v-spacer>
                        Count: {{ characterCount }}
                      </v-toolbar>
                    </div>
                  </editor-menu-bar>
                  <editor-content
                    :editor="editor"
                    :style="editorFontClass"
                    class="editor-box"
                  />
                  <v-select
                    v-model="newTextElement.language"
                    name="textlanguage"
                    :items="allLanguages"
                    label="Target Language*"
                    placeholder="choose a target language"
                    :rules="[rules.requiredLanguage]"
                    required
                    :loading="loadingLanguages"
                    outlined
                    class="mt-5"
                  ></v-select>

                  <v-select
                    v-model="newTextElement.topic"
                    name="audiotopic"
                    :items="allTopics"
                    label="Primary Topic*"
                    placeholder="choose the primary topic"
                    :rules="[rules.requiredTopic]"
                    required
                    :loading="loadingTopics"
                    outlined
                  ></v-select>

                  <v-textarea
                    outlined
                    name="learningpurpose"
                    label="Language Learning Purpose*"
                    v-model="newTextElement.purpose"
                    :rules="[rules.requiredPurpose]"
                    counter
                    rows="3"
                    maxlength="300"
                  ></v-textarea>

                  <v-textarea
                    outlined
                    name="sourcecitation"
                    label="Source Citation*"
                    v-model="newTextElement.citation"
                    :rules="[rules.requiredCitation]"
                    counter
                    rows="3"
                    maxlength="300"
                  ></v-textarea>

                  <v-textarea
                    outlined
                    name="textnotes"
                    label="Curator Notes"
                    v-model="newTextElement.notes"
                    value=""
                    rows="3"
                    counter
                    maxlength="300"
                  ></v-textarea>
                  <v-combobox
                    label="Additional Topic Tags"
                    name="texttags"
                    v-model="newTextElement.tags"
                    chips
                    clearable
                    hint="Hit <enter> or <tab> after each entry (max of 5 tags allowed)"
                    persistent-hint
                    multiple
                    :rules="[rules.maxTags]"
                    outlined
                    counter
                  >
                    <template
                      v-slot:selection="{ attrs, item, select, selected }"
                    >
                      <v-chip
                        v-bind="attrs"
                        :input-value="selected"
                        close
                        class="calligraphy desertsand--text"
                        @click="select"
                        @click:close="removeTag(item)"
                      >
                        <strong>{{ item }}</strong
                        >&nbsp;
                      </v-chip>
                    </template>
                  </v-combobox>
                </v-form>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions class="calligraphy">
        <v-spacer></v-spacer>
        <v-btn color="garbage desertsand--text" @click="closeDialog"
          >Cancel<v-icon right>mdi-close</v-icon></v-btn
        >
        <v-btn
          color="success"
          @click="submitTextElement"
          :disabled="!valid || !loaded"
          :loading="submitting"
          >Submit<v-icon right>mdi-thumb-up</v-icon></v-btn
        >
        <v-spacer></v-spacer>
        <!-- TODO: need to ensure that the user information is reloaded after saving -->
      </v-card-actions>
    </v-card>
  </v-dialog>
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

export default {
  name: "TextElementEditor",
  components: {
    EditorContent,
    EditorMenuBar
  },
  props: {
    editorDialog: {
      type: Boolean,
      default: false
    },
    isNewElement: {
      type: Boolean,
      default: false
    },
    oldTextElement: {
      type: Object,
      required: false
    }
  },
  data: () => ({
    // userData: Object,
    newTextElement: {},
    loaded: false,
    existingSlug: "",
    existingTitle: "",
    newAudioID: "",
    audioFile: "",
    audioFileName: "",
    duration: "",
    submitting: false,
    valid: true,
    success: false,
    fitParent: true,
    alertType: "success",
    alertMessage: "It's all good!",
    alertActive: false,
    allLanguages: [],
    loadingLanguages: false,
    loadingTopics: false,
    allTopics: [],
    rules: {
      requiredTitle: value =>
        (value || "").length > 5 ||
        "You must provide a title of at least 6 characters.",
      requiredLanguage: languagevalue =>
        (languagevalue || "").length > 0 ||
        "You must choose at least 1 language.",
      requiredTopic: topicvalue =>
        (topicvalue || "").length > 0 || "You must choose a primary topic.",
      requiredPurpose: purposevalue =>
        !!purposevalue || "You must provied a learning purpose.",
      requiredCitation: citationvalue =>
        !!citationvalue || "You must provied a source citation.",
      maxTags: tagsvalue =>
        (tagsvalue || "").length < 6 || "Maximum of 5 tags allowed!",
      maxAudioSize: value =>
        !value || value.size < 5000000 || "Audio file should be under 5MB!"
    },
    editorFontSize: 1,
    editor: new Editor({
      editable: true,
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
         `
    })
  }),
  computed: {
    editorFontClass() {
      return `font-size:${this.editorFontSize}em`;
    },
    characterCount() {
      return this.editor.view.state.doc.textContent.length;
    }
    // justText(){  // SAVE THIS FOR USING LATER!!!
    //   return this.editor.view.state.doc.textContent
    // }
  },
  methods: {
    closeDialog() {
      this.$emit("closeDialog");
    },
    chooseNewFile() {
      this.loadNewFile = true;
    },
    removeTag(item) {
      this.newTextElement.tags.splice(
        this.newTextElement.tags.indexOf(item),
        1
      );
      this.newTextElement.tags = [...this.newTextElement.tags];
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
    clearWarnings() {
      this.alertActive = false;
    },
    passDuration(duration) {
      this.duration = duration;
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
    },
    updateViewer(textElement) {
      this.$emit("updateViewer", textElement);
    },

    submitTextElement() {
      // The following grabs the blob, converts to a JPEG, wraps it, and sends it to the API
      this.submitting = true;
      let endpoint = `/api/elements/textz/`;
      let method = "POST";
      if (this.newTextElement.slug !== undefined) {
        endpoint += `${this.newTextElement.slug}/`;
        method = "PATCH";
      }
      this.newTextElement.content = this.editor.getJSON();
      this.newTextElement.rawtext = this.editor.view.state.doc.textContent;
      this.newTextElement.charactercount = this.editor.view.state.doc.textContent.length;
      console.log(this.newTextElement);
      apiService(endpoint, method, this.newTextElement).then(data => {
        console.log(data);
        if (data.slug) {
          if (this.isNewElement) {
            this.$router.push({
              name: "Text-Viewer",
              params: { elementslug: data.slug }
            });
          } else {
            // this.alertActive = false;
            this.updateViewer(data);
            this.closeDialog();
          }
        } else {
          console.log(data);
          console.log("There was a major problem with the request.");
          // console.log(data.message);
        }
        this.submitting = false;
      });
    }
  },
  mounted() {
    if (this.oldTextElement) {
      this.newTextElement = this.oldTextElement;
      this.editor.setContent(this.oldTextElement.content);
    } else {
      this.newTextElement = {};
    }
    this.loaded = true;
  },
  created() {
    this.getLanguages();
    this.getTopics();
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
  font-size: 1.25em;
  font-family: Arial, Helvetica, sans-serif;
  line-height: 1.5;
}

.is-active {
  border-color: orange;
  background-color: black;
  border-style: solid;
  border-width: 2px;
}
</style>
