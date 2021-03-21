<template>
  <v-row justify="center" class="ma-0">
    <v-dialog
      v-model="editorDialog"
      scrollable
      persistent
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card :loading="loadingLanguages || loadingQuestion" class="desertsand">
        <v-card-title v-if="editing">Edit Your Language Question</v-card-title>
        <v-card-title v-else>Ask a Language Question</v-card-title>
        <v-card-text>
          <v-form ref="questioncontent" v-model="valid" class="mt-2">
            <v-textarea
              v-model="title"
              outlined
              label="Question Title*"
              :rules="[rules.titleMin]"
              counter
              rows="1"
              maxlength="150"
            ></v-textarea>

            <v-select
              v-model="learninglanguage"
              :items="allLanguages"
              :loading="loadingLanguages"
              label="Learning Language (i.e. what this question is about)*"
              placeholder="choose the learning language"
              :rules="[rules.requiredLanguage]"
              required
              outlined
            ></v-select>

            <v-select
              v-model="nativelanguage"
              :items="allLanguages"
              label="Your Native Language*"
              placeholder="choose the native language"
              :rules="[rules.requiredLanguage]"
              required
              outlined
            ></v-select>

            <v-combobox
              label="Additional Topic Tags"
              v-model="tags"
              chips
              clearable
              hint="Hit <enter> or <tab> after each entry (max of 5 tags allowed)"
              persistent-hint
              multiple
              :rules="[rules.maxTags]"
              outlined
              counter
            >
              <template v-slot:selection="{ attrs, item, select, selected }">
                <v-chip
                  v-bind="attrs"
                  :input-value="selected"
                  close
                  @click="select"
                  @click:close="removeTag(item)"
                  class="calligraphy desertsand--text"
                >
                  <strong>{{ item }}</strong
                  >&nbsp;
                </v-chip>
              </template>
            </v-combobox>

            <editor-menu-bar :editor="editor" v-slot="{ commands, isActive }">
              <div class="desertsand--text">
                <v-toolbar dense flat class="sandstone">
                  <v-btn
                    small
                    icon
                    color="calligraphy"
                    :class="{ 'is-active': isActive.bold() }"
                    @click="commands.bold"
                  >
                    <v-icon> mdi-format-bold </v-icon>
                  </v-btn>
                  <v-btn
                    icon
                    small
                    color="calligraphy"
                    :class="{ 'is-active': isActive.italic() }"
                    @click="commands.italic"
                  >
                    <v-icon> mdi-format-italic </v-icon>
                  </v-btn>
                  <v-divider class="mx-1" inset vertical></v-divider>
                  <v-btn
                    icon
                    small
                    color="calligraphy"
                    :class="{ 'is-active': isActive.paragraph() }"
                    @click="commands.paragraph"
                  >
                    <v-icon> mdi-format-paragraph </v-icon>
                  </v-btn>
                  <v-btn
                    icon
                    small
                    color="calligraphy"
                    :class="{ 'is-active': isActive.heading({ level: 3 }) }"
                    @click="commands.heading({ level: 3 })"
                  >
                    <v-icon> mdi-format-header-3 </v-icon>
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
                    <v-icon> mdi-format-align-left </v-icon>
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
                    <v-icon> mdi-format-align-center </v-icon>
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
                    <v-icon> mdi-format-align-right </v-icon>
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
                    <v-icon> mdi-format-textdirection-l-to-r </v-icon>
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
                    <v-icon> mdi-format-textdirection-r-to-l </v-icon>
                  </v-btn>

                  <v-divider class="mx-1" inset vertical></v-divider>
                  <v-btn
                    color="calligraphy"
                    icon
                    @click="changeEditorFontSize('down')"
                  >
                    <v-icon>mdi-magnify-minus</v-icon>
                  </v-btn>
                  Zoom
                  <v-btn
                    icon
                    color="calligraphy"
                    @click="changeEditorFontSize('up')"
                  >
                    <v-icon>mdi-magnify-plus</v-icon>
                  </v-btn>

                  <v-divider class="mx-1" inset vertical></v-divider>
                  <v-spacer></v-spacer>
                  Count:
                  <span :class="characterCountClass">{{ characterCount }}</span>
                  / 500
                </v-toolbar>
              </div>
            </editor-menu-bar>
            <editor-content :editor="editor" :style="editorFontClass" />
          </v-form>
          <p v-if="error" class="muted mt-2">{{ error }}</p>
        </v-card-text>
        <v-card-actions class="calligraphy desertsand--text" justify="center">
          <v-spacer></v-spacer>
          <v-btn class="garbage desertsand--text" @click="closeDialog"
            >Cancel<v-icon right>mdi-close</v-icon></v-btn
          >
          <v-btn
            @click="onSubmit"
            class="green desertsand--text"
            :disabled="!valid"
            :loading="submitting"
            :hidden="submitted"
            >Submit<v-icon right>mdi-send</v-icon></v-btn
          >
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
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
  Underline
} from "tiptap-extensions";
import { default as Alignment } from "@/components/tiptaptoo/Alignment.js";
import { default as TextDirection } from "@/components/tiptaptoo/TextDirection.js";
export default {
  name: "QuestionEditor",
  components: {
    EditorContent,
    EditorMenuBar
  },
  props: {
    editing: {
      type: Boolean,
      default: false
    },
    slug: {
      type: String,
      required: false
    },
    question: {
      type: Object,
      required: false
    },
    editorDialog: {
      default: false
    }
  },
  data() {
    return {
      submitting: false,
      submitted: false,
      valid: false,
      loadingQuestion: false,
      loadingLanguages: false,
      error: null,
      author: "",
      title: "",
      content: "",
      nativelanguage: "",
      learninglanguage: "",
      allLanguages: [],
      tags: [],
      rules: {
        titleMin: value =>
          (value || "").length > 10 || "You must type at least 11 characters!",
        // contentMax: value => (value || '').length < 241 || "No more than 240 characters!",
        requiredLanguage: value =>
          !!value || "You must choose at least 1 language.",
        maxTags: value =>
          (value || "").length < 6 || "Maximum of 5 tags allowed!"
      },
      editorFontSize: 1,
      editor: new Editor({
        editable: true,
        extensions: [
          new Blockquote(),
          new HardBreak(),
          new Heading({ levels: [3] }),
          new Bold(),
          new Alignment(),
          new TextDirection(),
          new Italic(),
          new Link(),
          new Strike(),
          new Underline()
        ],
        content: `
                      ...type/paste question here...
                     `
      })
    };
  },
  computed: {
    characterCountClass() {
      if (this.characterCount > 500) {
        return "error";
      } else {
        return "";
      }
    },
    editorFontClass() {
      return `font-size:${this.editorFontSize}em`;
    },
    characterCount() {
      return this.editor.view.state.doc.textContent.length;
    }
  },

  methods: {
    closeDialog() {
      this.$emit("closeDialog");
    },
    onSubmit() {
      this.submitting = true;
      let endpoint = "/api/questions/questions/";
      let method = "POST";
      if (this.slug !== undefined) {
        endpoint += `${this.slug}/`;
        method = "PATCH";
      }
      let payload = {
        title: this.title,
        nativelanguage: this.nativelanguage,
        learninglanguage: this.learninglanguage,
        rich_text: this.editor.getJSON(),
        plain_text: this.editor.view.state.doc.textContent,
        // tags: []
        tags: this.tags
      };
      apiService(endpoint, method, payload).then(data => {
        if (this.editing === true) {
          this.$emit("updateQuestion", payload);
          this.$emit("closeDialog");
          console.log(payload);
          this.submitting = false;
        } else {
          this.submitted = true;
          this.$router.push({
            name: "Question-Viewer",
            params: { slug: data.slug }
          });
        }
      });
    },
    removeTag(item) {
      this.tags.splice(this.tags.indexOf(item), 1);
      this.tags = [...this.tags];
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

    getQuestionData() {
      if (this.editing) {
        (this.author = this.question.author),
          (this.title = this.question.title),
          (this.nativelanguage = this.question.nativelanguage),
          (this.learninglanguage = this.question.learninglanguage),
          (this.tags = this.question.tags);
        this.editor.setContent(this.question.rich_text);
        this.loadingQuestion = false;
      }
    },
    getQuestionData2() {
      if (this.editing) {
        this.loadingQuestion = true;
        let endpoint = `/api/questions/${this.slug}/`;
        apiService(endpoint).then(data => {
          if (data) {
            (this.author = data.author),
              (this.title = data.title),
              (this.nativelanguage = data.nativelanguage),
              (this.learninglanguage = data.learninglanguage),
              (this.tags = data.tags);
            this.loadingQuestion = false;
          } else {
            this.question = null;
            this.setPageTitle("404 - Page Note Found");
            this.loadingQuestion = false;
          }
        });
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
    }
  },
  created() {
    this.getQuestionData();
    this.getLanguages();
  }
};
</script>
<style scoped>
.editor-box > * {
  border-color: black;
  color: black;
  border-style: solid;
  border-width: 1px;
  padding: 4px, 4px;
  width: 100%;
  height: 300px;
  overflow-x: hidden;
  overflow-x: auto;
  font-size: 1em;
  font-family: Arial, Helvetica, sans-serif;
  line-height: 1.5;
}
.ProseMirror {
  background-color: black;
}
</style>
