<template>
  <div>
    <v-card class="pa-1 sandstone">
      <!-- COMMMENT CARD -->
      <v-card-title
        class="calligraphy desertsand--text subtitle-2 py-1 px-1 ma-0"
        v-if="comment.id"
      >
        <!-- <CommentUpDownVote
          @updateVote="updateVote"
          :up-vote-count="comment.upvote_count"
          :down-vote-count="comment.downvote_count"
          :user-vote="comment.user_vote"
          :disabled="isCommentCurator"
          :comment_id="comment.id"
        /> -->

        <v-avatar class="ma-0" size="30">
          <v-img
            class="elevation-6"
            :src="comment.curator.user_profile.avatar"
          ></v-img>
        </v-avatar>
        <p class="ml-1 mr-1 pa-0 my-0">
          On {{ comment.curation_date }},
          <v-dialog v-model="profileDialog" width="275">
            <template v-slot:activator="{ on }">
              <a
                v-on="on"
                text
                small
                class="primary--text font-weight-bold px-0 py-0"
              >
                {{ comment.curator.username }}
              </a>
            </template>
            <ProfileSnippet
              v-if="profileDialog"
              :profileObject="comment.curator"
              :profileDialog="profileDialog"
              @closeDialog="profileDialog = false"
            />
          </v-dialog>
          &nbsp;commented:
        </p>
        <v-spacer />
        <div v-if="isCommentCurator && !editMode && !deleteConfirm" cols="12">
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

        <div v-if="isCommentCurator && !editMode && deleteConfirm" cols="12">
          <v-btn
            small
            @click="submitCommentDelete"
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

        <div v-if="isCommentCurator && editMode">
          <v-btn
            small
            class="primary desertsand--text mr-1"
            @click="submitCommentEdit"
            :loading="submittingComment"
          >
            Submit Edit<v-icon right>mdi-reply</v-icon>
          </v-btn>
          <v-btn small class="garbage desertsand--text" @click="cancelEdit">
            Cancel <v-icon right>mdi-cancel</v-icon>
          </v-btn>
        </div>
      </v-card-title>
      <!-- <v-card-title v-else>New Comment</v-card-title> -->

      <v-card-text class="desertsand black--text pa-0 ma-0">
        <SimpleTipTap
          :editMode="editMode"
          ref="textEditor"
          :content="comment.rich_text ? comment.rich_text : 'new comment'"
        />
      </v-card-text>

      <v-card-actions v-if="comment.isNewComment">
        <div>
          <v-btn
            small
            class="primary desertsand--text mr-1"
            @click="submitNewComment"
            :loading="submittingComment"
          >
            Submit Comment<v-icon right>mdi-reply</v-icon>
          </v-btn>

          <v-btn
            small
            @click="cancelNewComment"
            class="mr-1 garbage desertsand--text"
          >
            Cancel<v-icon right>mdi-cancel</v-icon>
          </v-btn>
        </div>
      </v-card-actions>

      <v-card-actions v-else class="desertsand pb-0">
        <v-row dense wrap no-gutters>
          <v-col v-if="!replying && !editMode && false" cols="12">
            <v-btn
              small
              class="primary desertsand--text mr-1"
              @click="replying = true"
            >
              Reply <v-icon right>mdi-reply</v-icon>
            </v-btn>

            <v-btn
              small
              @click="flaggerDialog = true"
              :disabled="comment.user_has_flagged"
              class="error desertsand--text mr-1"
            >
              <v-badge
                color="error lighten-1 white--text"
                :content="comment.flag_count"
              >
                Flag<v-icon right>mdi-flag</v-icon>
              </v-badge>
            </v-btn>
            <!-- <ContentFlagger
              :flagger-dialog="flaggerDialog"
              @flagSuccess="flagSuccess"
              @closeDialog="flaggerDialog = false"
              content-type="answer"
              :contentid="comment.id"
            /> -->
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

      <v-card-text class="desertsand" v-if="repliesExist">
        <v-row dense no-gutters>
          <v-col cols="12" v-for="reply in comment.replies" :key="reply.id">
            <ReplyView :reply="reply" @delete-reply="deleteReply" />
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
// import ReplyView from "@/components/questions/ReplyView.vue";
// import CommentUpDownVote from "@/components/questions/CommentUpDownVote.vue";
// import ContentFlagger from "@/components/ContentFlagger.vue";
import SimpleTipTap from "@/components/elements/SimpleTipTap.vue";
export default {
  name: "ReplyComponent",
  props: {
    isNewComment: {
      type: Boolean,
      default: false
    },
    comment_index: {
      type: Number,
      required: true
    },
    comment_id: {
      type: Number,
      required: true
    },
    comment: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      comments: [],
      addingComment: false,
      flaggerDialog: false,
      deleteConfirm: false,
      profileDialog: false,
      submitting: false,
      editing: false,
      editMode: false,
      editValid: false,
      submittingComment: false,
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
      }
    };
  },
  computed: {
    isCommentCurator() {
      return (
        this.comment.curator.username ===
        window.localStorage.getItem("username")
      );
    },
    repliesExist() {
      if (this.comment.replies) {
        return true;
      } else {
        return false;
      }
    }
  },
  components: {
    ReplyView,
    SimpleTipTap
    // CommentUpDownVote,
    // ContentFlagger,
    // ProfileSnippet: () =>
    //   import(
    //     /* webpackPrefetch: true */ "@/components/profile/ProfileSnippet.vue"
    //   ),
  },
  methods: {
    toggleEdit() {
      this.editMode = true;
      this.$refs.textEditor.editor.setOptions({ editable: this.editMode });
    },
    cancelEdit() {
      this.editMode = false;
      this.$refs.textEditor.editor.setOptions({ editable: this.editMode });
      this.$refs.textEditor.editor.setContent(this.comment.rich_text);
    },
    submitCommentEdit() {
      this.editMode = false;
      this.$refs.textEditor.editor.setOptions({ editable: this.editMode });
      this.comment.rich_text = this.$refs.textEditor.editor.getJSON();
      this.comment.plain_text = this.$refs.textEditor.editor.view.state.doc.textContent;
      this.$emit("updateComment", this.comment_index, this.comment);
    },
    submitCommentDelete() {
      this.deleteConfirm = false;
      this.$emit("delete-comment", this.comment_index, this.comment);
    },
    cancelNewComment() {
      this.$emit("cancelNew");
    },
    submitNewComment() {
      this.editMode = false;
      this.$refs.textEditor.editor.setOptions({ editable: this.editMode });
      this.comment.rich_text = this.$refs.textEditor.editor.getJSON();
      this.comment.plain_text = this.$refs.textEditor.editor.view.state.doc.textContent;
      this.$emit("submitComment", this.comment_index, this.comment);
    },
    flagSuccess() {
      this.flaggerDialog = false;
      this.comment.user_has_flagged = true;
      this.comment.flag_count += 1;
    },
    setEditor() {
      this.editor.setContent(this.comment.details);
    }
  },
  mounted() {
    if (this.comment.isNewComment) {
      this.editMode = true;
      this.$refs.textEditor.editor.setOptions({ editable: this.editMode });
    }
  },
  created() {}
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
  border-style: none;
  border-width: 0px;
  border-radius: 5px;
}
>>> .ProseMirror:focus {
  outline: none;
}
</style>
