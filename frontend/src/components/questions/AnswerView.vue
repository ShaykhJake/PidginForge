<template>
  <div>
    <v-card class="ml-6">
      <v-card-title class="calligraphy desertsand--text subtitle-2 pa-1">
        <AnswerUpDownVote
          @updateVote="updateVote"
          :up-vote-count="answer.upvote_count"
          :down-vote-count="answer.downvote_count"
          :user-vote="answer.user_vote"
          :disabled="isAnswerAuthor"
          :answer_id="answer.id"
        />
        <v-avatar class="mr-2" size="35">
          <v-img
            class="elevation-6"
            :src="answer.author.user_profile.avatar"
          ></v-img>
        </v-avatar>
        <p>
          On {{ answer.created_at }},
          <v-dialog v-model="profileDialog" width="275">
            <template v-slot:activator="{ on }">
              <a
                v-on="on"
                text
                small
                class="primary--text font-weight-bold px-0 py-0"
              >
                {{ answer.author.username }}
              </a>
            </template>
            <ProfileSnippet
              v-if="profileDialog"
              :profileObject="answer.author"
              :profileDialog="profileDialog"
              @closeDialog="profileDialog = false"
            />
          </v-dialog>

          answered:
        </p>
        <v-spacer />
        <div v-if="isAnswerAuthor && !editMode && !deleteConfirm" cols="12">
          <v-btn
            small
            class="primary desertsand--text mr-1"
            @click="toggleEdit"
          >
            Edit <v-icon right>mdi-pencil</v-icon>
          </v-btn>
          <v-btn
            small
            class="garbage desertsand--text"
            @click="deleteConfirm = true"
          >
            Delete <v-icon right>mdi-delete</v-icon>
          </v-btn>
        </div>

        <div v-if="isAnswerAuthor && !editMode && deleteConfirm" cols="12">
          <v-btn
            small
            @click="submitAnswerDelete"
            v-if="deleteConfirm"
            class="success desertsand--text mr-1"
          >
            Confirm Delete <v-icon right>mdi-delete</v-icon>
          </v-btn>
          <v-btn
            small
            @click="deleteConfirm = false"
            v-if="deleteConfirm"
            class="mr-1 garbage desertsand--text"
          >
            Cancel<v-icon right>mdi-cancel</v-icon>
          </v-btn>
        </div>

        <div v-if="isAnswerAuthor && editMode">
          <v-btn
            small
            class="primary desertsand--text mr-1"
            @click="submitAnswerEdit"
            :loading="submittingAnswer"
          >
            Submit Edit<v-icon right>mdi-reply</v-icon>
          </v-btn>
          <v-btn
            small
            class="garbage desertsand--text"
            @click="editMode = false"
          >
            Cancel <v-icon right>mdi-cancel</v-icon>
          </v-btn>
        </div>
      </v-card-title>
      <v-card-text class="desertsand black--text pa-0 pb-0">
        <editor-menu-bar
          :editor="editor"
          v-if="editMode"
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
      </v-card-text>

      <v-card-actions class="pb-0 desertsand">
        <v-row dense wrap no-gutters>
          <v-col v-if="!replying && !editMode" cols="12">
            <v-btn
              small
              class="primary desertsand--text mr-1"
              @click="replying = true"
            >
              Reply <v-icon right>mdi-reply</v-icon>
            </v-btn>

            <v-btn
              small
              v-if="!isAnswerAuthor"
              @click="flaggerDialog = true"
              :disabled="answer.user_has_flagged"
              class="error desertsand--text mr-1"
            >
              <v-badge
                color="error lighten-1 white--text"
                :content="answer.flag_count"
              >
                Flag<v-icon right>mdi-flag</v-icon>
              </v-badge>
            </v-btn>
            <ContentFlagger
              :flagger-dialog="flaggerDialog"
              @flagSuccess="flagSuccess"
              @closeDialog="flaggerDialog = false"
              content-type="answer"
              :contentid="answer.id"
            />
          </v-col>

          <v-col v-if="replying" cols="12">
            <v-form ref="newReply" v-model="valid" class="mt-2">
              <v-textarea
                v-model="newReply.content"
                block
                outlined
                label="Reply Content*"
                :rules="[rules.contentMin]"
                counter
                rows="3"
                maxlength="240"
              ></v-textarea>
            </v-form>
            <v-btn
              small
              class="success desertsand--text mr-1"
              @click="submitReply"
              :disabled="!valid"
              :loading="submittingReply"
            >
              Submit <v-icon right>mdi-reply</v-icon>
            </v-btn>
            <v-btn
              small
              class="garbage desertsand--text mr-1"
              @click="replying = false"
            >
              Cancel <v-icon right>mdi-cancel</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-card-actions>

      <v-card-text class="desertsand pl-4" v-if="repliesExist">
        <v-row dense no-gutters>
          <v-col cols="12" v-for="reply in answer.replies" :key="reply.id">
            <ReplyView :reply="reply" @delete-reply="deleteReply" />
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import ReplyView from "@/components/questions/ReplyView.vue";
import AnswerUpDownVote from "@/components/questions/AnswerUpDownVote.vue";
import ContentFlagger from "@/components/ContentFlagger.vue";
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
  name: "AnswerView",
  props: {
    answer: {
      type: Object,
      required: true
    },
    slug: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      flaggerDialog: false,
      deleteConfirm: false,
      profileDialog: false,
      submitting: false,
      editing: false,
      editMode: false,
      editValid: false,
      submittingAnswer: false,
      submittingReply: false,
      replying: false,
      userHasReplied: false,
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
        editable: false,
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
    },
    isAnswerAuthor() {
      return (
        this.answer.author.username === window.localStorage.getItem("username")
      );
    },
    repliesExist() {
      if (this.answer.replies) {
        return true;
      } else {
        return false;
      }
    }
  },
  components: {
    EditorContent,
    EditorMenuBar,
    ReplyView,
    AnswerUpDownVote,
    ContentFlagger,
    ProfileSnippet: () =>
      import(
        /* webpackPrefetch: true */ "@/components/profile/ProfileSnippet.vue"
      )
  },
  methods: {
    submitReply() {
      // console.log("submitted");
      this.submittingReply = true;
      let endpoint = `/api/questions/reply/post/`;
      apiService(endpoint, "POST", {
        content: this.newReply.content,
        answerpk: this.answer.id
      }).then(data => {
        this.answer.replies.unshift(data.data);
        // this.userHasReplied = true;
        this.submittingReply = false;
        this.replying = false;
        // console.log(data);
      });
    },
    toggleEdit() {
      this.editMode = !this.editMode;
      this.editor.setOptions({
        editable: this.editMode
      });
    },
    submitAnswerEdit() {
      this.submittingAnswer = true;
      let endpoint = `/api/questions/answers/${this.answer.id}/`;
      apiService(endpoint, "PATCH", {
        content: "placeholder",
        details: this.editor.getJSON()
      }).then(() => {
        this.editMode = false;
        this.submittingAnswer = false;
      });
    },
    submitAnswerDelete() {
      this.deleteConfirm = false;
      this.$emit("delete-answer", this.answer);
    },
    async deleteReply(reply) {
      let endpoint = `/api/questions/reply/delete/${reply.id}/`;
      console.log("deleting");
      try {
        await apiService(endpoint, "DELETE");
        this.$delete(this.answer.replies, this.answer.replies.indexOf(reply));
        this.userHasReplied = false;
      } catch (err) {
        // console.log(err)
      }
    },
    updateVote(data) {
      this.answer.user_vote = data.newuservote;
      this.answer.downvote_count = data.newdowncount;
      this.answer.upvote_count = data.newupcount;
    },
    flagSuccess() {
      this.flaggerDialog = false;
      this.answer.user_has_flagged = true;
      this.answer.flag_count += 1;
    },
    setEditor() {
      this.editor.setContent(this.answer.details);
    }
  },
  mounted() {},
  created() {
    // this.setRequestUser();
    this.setEditor();
  },
  beforeDestroy() {
    this.editor.destroy();
  }
};
</script>
<style scoped>
>>> .ProseMirror {
  color: black;
  background-color: none;
  padding: 10px 10px 10px 10px;
  height: auto;
  font-size: 1em;
  line-height: 1.35em;
  overflow: auto;
  resize: vertical;
  border-color: black;
  border-style: dotted;
  border-width: 1px;
  border-radius: 5px;
}
>>> .ProseMirror:focus {
  outline: none;
}
</style>
