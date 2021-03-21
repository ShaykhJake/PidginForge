<template>
  <div>
    <v-card class="mt-2" pa-0>
      <v-card-title class="py-1 px-2 desertsand">
        Learner Replys
        <small v-if="replies.length > 0"
          >&nbsp;({{ replies.length }} of {{ totalCount }} loaded)</small
        >
        <small v-else>(no replies yet)</small>
        <v-spacer></v-spacer>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn icon v-on="on" class="primary--text" @click="addReply">
              <v-icon>library_add</v-icon>
            </v-btn>
          </template>
          <span>Add Learner Reply</span>
        </v-tooltip>
      </v-card-title>
      <v-card-text class="pa-0 ma-0 desertsand">
        <ReplyComponent
          v-for="(reply, index) in replies"
          :reply="reply"
          :key="index"
          :comment_id="comment_id"
          :reply_index="index"
          :isNewReply="reply.isNewReply"
          @cancelNew="deleteReply(reply)"
          @updateReply="submitReplyEdit"
          @submitReply="submitNewReply"
        />
      </v-card-text>
      <v-card-actions class="desertsand ma-0 pa-0">
        <v-btn
          v-show="next || loading"
          @click="getReplies"
          :loading="loading"
          class="primary desertsand--text"
          block
        >
          Load More Replys <v-icon right>mdi-chevron-down</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
// import ReplyView from "@/components/questions/ReplyView.vue";
import ReplyComponent from "@/components/elements/ReplyComponent.vue";
export default {
  name: "ElementReplys",
  props: {
    comment_id: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      replies: [],
      next: null,
      loading: false,
      totalCount: 0,
      addingReply: false,
      flaggerDialog: false,
      deleteConfirm: false,
      profileDialog: false,
      submitting: false,
      editing: false,
      editMode: false,
      editValid: false,
      submittingReply: false,
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
  computed: {},
  components: {
    ReplyComponent
  },
  methods: {
    toggleEdit() {
      this.editMode = !this.editMode;
      this.editor.setOptions({
        editable: this.editMode
      });
    },
    getReplies() {
      this.loading = true;
      let endpoint = `/api/elements/commentreplies/list/?comment=${this.comment_id}`;
      if (this.next) {
        endpoint = this.next;
      }
      apiService(endpoint).then(data => {
        console.log(data);
        this.totalCount = data.count;
        this.replies.push(...data.results);
        this.loading = false;
        if (data.next) {
          this.next = data.next;
        } else {
          this.next = null;
        }
      });
    },
    addReply() {
      const newReply = {
        rich_text: "new comment",
        comment_id: this.comment_id,
        isNewReply: true
      };
      this.replies.unshift(newReply);
      this.addingReply = true;
      console.log("new reply");
    },
    deleteReply(comment) {
      this.replies.splice(this.replies.indexOf(comment), 1);
    },
    submitReplyEdit(comment_index, comment) {
      this.submitting = true;
      let endpoint = `/api/elements/elementcommentz/${comment.id}/`;
      apiService(endpoint, "PATCH", {
        plain_text: comment.plain_text,
        rich_text: comment.rich_text,
        element: this.comment_id
      }).then(data => {
        if (data) {
          this.$set(this.replies, comment_index, data);
          this.editMode = false;
          this.submittingReply = false;
        }
      });
    },
    submitNewReply(comment_index, comment) {
      this.submitting = true;
      let endpoint = `/api/elements/elementcommentz/`;
      let method = "POST";
      let payload = {
        rich_text: comment.rich_text,
        plain_text: comment.plain_text,
        element: this.comment_id
      };
      apiService(endpoint, method, payload).then(data => {
        if (data) {
          this.$set(this.replies, comment_index, data);
          // this.replies.unshift(data)
        }
        this.submitting = false;
      });
      console.log("submitting");
      this.submitting = false;
    },

    updateReply(comment_index, data) {
      // console.log(data)
      // this.replies[comment_index] = data;
      // console.log(this.replies)
      this.$set(this.replies, comment_index, data);
      console.log(this.replies);
      // this.replies.splice(this.replies.indexOf(comment), 1);
    },
    submitNew() {
      console.log("submitting");
      this.addingReply = false;
    }
  },
  mounted() {
    this.getReplies();
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
