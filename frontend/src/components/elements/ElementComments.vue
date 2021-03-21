<template>
  <div>
    <v-card class="mt-2" pa-0>
      <v-card-title class="py-1 px-2 desertsand">
        Learner Comments
        <v-spacer></v-spacer>
        <small v-if="comments.length > 0"
          >&nbsp;({{ comments.length }} of {{ totalCount }} loaded)</small
        >
        <small v-else>(no comments yet)</small>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn icon v-on="on" class="primary--text" @click="addComment">
              <v-icon>library_add</v-icon>
            </v-btn>
          </template>
          <span>Add Learner Comment</span>
        </v-tooltip>
      </v-card-title>
      <v-card-text class="pa-0 ma-0 desertsand">
        <CommentComponent
          v-for="(comment, index) in comments"
          :comment="comment"
          :key="index"
          :element_id="element_id"
          :comment_index="index"
          :isNewComment="comment.isNewComment"
          @cancelNew="deleteComment(comment)"
          @updateComment="submitCommentEdit"
          @submitComment="submitNewComment"
        />
      </v-card-text>
      <v-card-actions class="desertsand ma-0 pa-0">
        <v-btn
          v-show="next || loading"
          @click="getComments"
          :loading="loading"
          class="primary desertsand--text"
          block
        >
          Load More Comments <v-icon right>mdi-chevron-down</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
// import ReplyView from "@/components/questions/ReplyView.vue";
import CommentComponent from "@/components/elements/CommentComponent.vue";
export default {
  name: "ElementComments",
  props: {
    element_id: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      comments: [],
      next: null,
      loading: false,
      totalCount: 0,
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
    CommentComponent
  },
  methods: {
    submitReply() {
      // console.log("submitted");
      this.submittingReply = true;
      let endpoint = `/api/questions/reply/post/`;
      apiService(endpoint, "POST", {
        content: this.newReply.content,
        answerpk: this.comment.id
      }).then(data => {
        this.comment.replies.unshift(data.data);
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
    getComments() {
      this.loading = true;
      let endpoint = `/api/elements/comments/list/?element=${this.element_id}`;
      if (this.next) {
        endpoint = this.next;
      }
      apiService(endpoint).then(data => {
        console.log(data);
        this.totalCount = data.count;
        this.comments.push(...data.results);
        this.loading = false;
        if (data.next) {
          this.next = data.next;
        } else {
          this.next = null;
        }
      });
    },
    submitCommentDelete() {
      this.deleteConfirm = false;
      this.$emit("delete-comment", this.comment);
    },
    addComment() {
      const newComment = {
        rich_text: "new comment",
        element_id: this.element_id,
        isNewComment: true
      };
      this.comments.unshift(newComment);
      this.addingComment = true;
      console.log("new comment");
    },
    deleteComment(comment) {
      this.comments.splice(this.comments.indexOf(comment), 1);
    },
    submitCommentEdit(comment_index, comment) {
      this.submitting = true;
      let endpoint = `/api/elements/elementcommentz/${comment.id}/`;
      apiService(endpoint, "PATCH", {
        plain_text: comment.plain_text,
        rich_text: comment.rich_text,
        element: this.element_id
      }).then(data => {
        if (data) {
          this.$set(this.comments, comment_index, data);
          this.editMode = false;
          this.submittingComment = false;
        }
      });
    },
    submitNewComment(comment_index, comment) {
      this.submitting = true;
      let endpoint = `/api/elements/elementcommentz/`;
      let method = "POST";
      let payload = {
        rich_text: comment.rich_text,
        plain_text: comment.plain_text,
        element: this.element_id
      };
      apiService(endpoint, method, payload).then(data => {
        if (data) {
          this.$set(this.comments, comment_index, data);
          // this.comments.unshift(data)
        }
        this.submitting = false;
      });
      console.log("submitting");
      this.submitting = false;
    },

    updateComment(comment_index, data) {
      // console.log(data)
      // this.comments[comment_index] = data;
      // console.log(this.comments)
      this.$set(this.comments, comment_index, data);
      console.log(this.comments);
      // this.comments.splice(this.comments.indexOf(comment), 1);
    },
    submitNew() {
      console.log("submitting");
      this.addingComment = false;
    },
    async deleteReply(reply) {
      let endpoint = `/api/elements/comments/reply/delete/${reply.id}/`;
      console.log("deleting");
      try {
        await apiService(endpoint, "DELETE");
        this.$delete(this.comment.replies, this.comment.replies.indexOf(reply));
        this.userHasReplied = false;
      } catch (err) {
        // console.log(err)
      }
    },
    updateVote(data) {
      this.comment.user_vote = data.newuservote;
      this.comment.downvote_count = data.newdowncount;
      this.comment.upvote_count = data.newupcount;
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
    this.getComments();
  },
  created() {}
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
