<template>
  <div>
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
          <v-btn color="calligraphy" icon @click="changeEditorFontSize('down')">
            <v-icon>mdi-magnify-minus</v-icon>
          </v-btn>
          Zoom
          <v-btn icon color="calligraphy" @click="changeEditorFontSize('up')">
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
    <v-btn
      small
      class="success mr-1"
      @click="submitAnswer"
      :loading="submittingAnswer"
    >
      Submit <v-icon right>mdi-reply</v-icon>
    </v-btn>
    <v-btn small class="garbage mr-1 desertsand--text" @click="cancelEdit">
      Cancel<v-icon right>mdi-cancel</v-icon>
    </v-btn>
  </div>
</template>

<script>
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
  name: "AnswerPost",
  props: {},
  data() {
    return {
      submitting: false,
      submittingAnswer: false,
      valid: false,

      newReply: {
        content: ""
      },
      rules: {
        contentMin: value =>
          (value || "").length > 4 || "You must type at least 5 characters!"
        // contentMax: value => (value || '').length < 241 || "No more than 240 characters!",
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
                              ...type your answer here...
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
  components: {
    EditorContent,
    EditorMenuBar
  },
  methods: {
    submitAnswer() {
      let details = this.editor.getJSON();
      this.$emit("submitAnswer", details);
    },
    cancelEdit() {
      this.$emit("cancelEdit");
    }
  },
  mounted() {},
  created() {},
  beforeDestroy() {
    this.editor.destroy();
  }
};
</script>
<style>
.ProseMirror {
  color: black;
  background-color: blue;
  padding: 10px 10px 10px 10px;
  height: 150px;
  font-size: 1.25em;
  line-height: 1.35em;
  overflow: auto;
  resize: vertical;
  border-color: blue;
  border-style: solid;
  border-width: 1px;
  border-radius: 5px;
}
</style>
