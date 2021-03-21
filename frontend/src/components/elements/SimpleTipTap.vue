<template>
  <div>
    <editor-menu-bar
      v-if="loaded && editMode"
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
            :class="{
              'is-active': isActive.heading({ level: 1 })
            }"
            @click="commands.heading({ level: 1 })"
          >
            <v-icon> mdi-format-header-1 </v-icon>
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
            <v-icon> mdi-format-header-2 </v-icon>
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
            <v-icon> mdi-format-header-3 </v-icon>
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
          Text Size
          <v-btn icon color="calligraphy" @click="changeEditorFontSize('up')">
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
  Underline,
  History
} from "tiptap-extensions";
import { default as Alignment } from "@/components/tiptaptoo/Alignment.js";
import { default as TextDirection } from "@/components/tiptaptoo/TextDirection.js";
import { default as Highlighter } from "@/components/tiptaptoo/Highlighter.js";

export default {
  name: "SimpleTipTap",

  components: {
    EditorContent,
    EditorMenuBar
  },
  props: {
    content: {
      type: Object,
      required: false
    },
    editMode: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    loaded: false,
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
      content: "...loading..."
    })
  }),
  computed: {
    editorFontClass() {
      return `font-size:${this.editorFontSize}em`;
    },
    characterCount() {
      return this.editor.view.state.doc.textContent.length;
    }
  },
  methods: {
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
    toggleEditMode() {
      this.editMode = !this.editMode;
      this.editor.setOptions({ editable: this.editMode });
    }
  },
  mounted() {
    this.editor.setContent(this.content);
    this.loaded = true;
    // if (this.forEdit) {
    //   this.editMode = true;
    //   this.editor.setOptions({ editable: this.editMode });
    // }
  },
  created() {}
};
</script>

<style></style>
