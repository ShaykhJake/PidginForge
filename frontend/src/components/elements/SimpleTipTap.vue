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
              'is-active': isActive.heading({ level: 1 }),
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
              'is-active': isActive.heading({ level: 2 }),
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
              'is-active': isActive.heading({ level: 3 }),
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
                orientation: 'left',
              }),
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
                orientation: 'center',
              }),
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
                orientation: 'right',
              }),
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
                direction: 'ltr',
              }),
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
                direction: 'rtl',
              }),
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
          <div v-if="timingEnabled">
          <v-divider class="mx-1" inset vertical></v-divider>

          <v-btn
            icon
            @click="triggerTimeStamp"
            color="primary"

          >
            <v-icon>timer</v-icon>
          </v-btn>
          <v-divider class="mx-1" inset vertical></v-divider>
          </div>
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
    <v-btn icon @click="changeEditorFontSize('up')" v-if="showZoom">
      <v-icon color="primary">zoom_in</v-icon>
    </v-btn>
    <v-btn icon @click="changeEditorFontSize('down')" v-if="showZoom">
      <v-icon color="primary">zoom_out</v-icon>
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
    Underline,
    History,
  } from "tiptap-extensions";
  import { default as Alignment } from "@/components/tiptaptoo/Alignment.js";
  import { default as TextDirection } from "@/components/tiptaptoo/TextDirection.js";
  import { default as Highlighter } from "@/components/tiptaptoo/Highlighter.js";
  import { default as TimeStamp } from "@/components/tiptaptoo/TimeStamp.js";

  export default {
    name: "SimpleTipTap",

    components: {
      EditorContent,
      EditorMenuBar,
    },
    props: {
      content: {
        type: Object,
        required: false,
      },
      editMode: {
        type: Boolean,
        default: false,
      },
      timingEnabled: {
        type: Boolean,
        default: false,
      },
      showZoom: {
        type: Boolean,
        default: true,
      }
    },
    data() {
      return {
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
          new Highlighter(),
          new TimeStamp(),
        ],
        editorProps: {
          handleClickOn: (view, pos, node, nodePos, event) => {
            if (node.type.name === "timestamp") {
              // console.log(`Skip to ${node.attrs.timehack}`);
              this.$emit("skipToTime", node.attrs.timehack);
            } else {
              return view, pos, node, nodePos, event;
            }
          },
        },
        content: "...type here...",
                onUpdate: () => {
          this.unsavedChanges = true;
          // console.log("Unsaved changes");
        },
        handleDOMEvents: {}

      }),
      }
    },
    computed: {
      editorFontClass() {
        return `font-size:${this.editorFontSize}em`;
      },
      characterCount() {
        return this.editor.view.state.doc.textContent.length;
      },
    },
    methods: {
      triggerTimeStamp() {
        // console.log("triggering1")
        this.$emit("triggerTimeStamp");
      },

      recordTimeStamp(currenttime) {
        // console.log("sending1")
        if (this.editMode) {
          var newstamp = parseInt(currenttime);
          this.editor.commands.timestamp({ timehack: newstamp });
        } else {
          // console.log("Transcript is locked");
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
      toggleEditMode() {
        this.editMode = !this.editMode;
        this.editor.setOptions({ editable: this.editMode });
      },
    },
    mounted() {
      if(this.content){
        this.editor.setContent(this.content);
      }
      if (this.editMode) {
        this.editor.setOptions({ editable: this.editMode });
      }
      this.loaded = true;
    },
    created() {},
  };
</script>

<style>
</style>
