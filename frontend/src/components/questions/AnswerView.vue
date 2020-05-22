<template>
  <div>
    <v-card class="ml-6">
      <v-card-title class="calligraphy desertsand--text subtitle-2 pa-1">
        <v-avatar class="mr-2" size="42">
          <v-img
            class="elevation-6"
            :src="answer.author.user_profile.avatar"
          ></v-img>
        </v-avatar>
        On {{ answer.created_at }},
        <v-dialog v-model="profileDialog" width="275">
          <template v-slot:activator="{ on }">
            <a
              v-on="on"
              text
              small
              class="primary--text font-weight-bold px-1 py-0"
            >
              {{ answer.author.username }}
            </a>
          </template>
          <ProfileSnippet
            :username="answer.author.username"
            @closeDialog="profileDialog = false"
          />
        </v-dialog>
        answered...

        <AnswerUpDownVote
          @updateVote="updateVote"
          :up-vote-count="answer.upvote_count"
          :down-vote-count="answer.downvote_count"
          :user-vote="answer.user_vote"
          :answerid="answer.id"
        />
      </v-card-title>
      <v-card-text class="desertsand black--text pt-2 pb-0">
        <div v-if="!editing">
          {{ answer.content }}
        </div>
        <div v-if="editing">
          <v-form ref="editAnswer" v-model="editValid" class="mt-2">
            <v-textarea
              v-model="answer.content"
              block
              outlined
              label="Answer Content*"
              :rules="[rules.contentMin]"
              counter
              rows="3"
              maxlength="240"
            ></v-textarea>
          </v-form>
        </div>
      </v-card-text>

      <v-card-actions class="desertsand pb-0">
        <v-row dense wrap no-gutters>
          <v-col v-if="isAnswerAuthor && !editing && !deleteConfirm" cols="12">
            <v-btn
              small
              class="primary desertsand--text mr-1"
              @click="editing = true"
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
          </v-col>
          <v-col v-if="isAnswerAuthor && !editing && deleteConfirm" cols="12">
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
          </v-col>

          <v-col v-if="isAnswerAuthor && editing">
            <v-btn
              small
              class="primary desertsand--text mr-1"
              @click="submitAnswerEdit"
              :loading="submittingAnswer"
            >
              Submit <v-icon right>mdi-reply</v-icon>
            </v-btn>
            <v-btn
              small
              class="garbage desertsand--text"
              @click="editing = false"
            >
              Cancel <v-icon right>mdi-cancel</v-icon>
            </v-btn>
          </v-col>
          <v-col v-if="!isAnswerAuthor && !replying" cols="12">
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

      <v-card-text class="desertsand" v-if="repliesExist">
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
          (value || "").length > 15 || "You must type at least 16 characters!"
        // contentMax: value => (value || '').length < 241 || "No more than 240 characters!",
      }
    };
  },
  computed: {
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
      console.log("submitted");
      this.submittingReply = true;
      let endpoint = `/api/reply/post/`;
      apiService(endpoint, "POST", {
        content: this.newReply.content,
        answerpk: this.answer.id
      }).then(data => {
        this.answer.replies.unshift(data.data);
        // this.userHasReplied = true;
        this.submittingReply = false;
        this.replying = false;
        console.log(data);
      });
    },
    submitAnswerEdit() {
      if (this.answer.content) {
        this.submittingAnswer = true;
        console.log(this.answer);
        let endpoint = `/api/answers/${this.answer.id}/`;
        apiService(endpoint, "PATCH", { content: this.answer.content }).then(
          () => {
            this.editing = false;
            this.submittingAnswer = false;
          }
        );
      } else {
        this.error = "You can't submit an empty asnwer!";
      }
    },
    submitAnswerDelete() {
      this.deleteConfirm = false;
      this.$emit("delete-answer", this.answer);
    },
    async deleteReply(reply) {
      let endpoint = `/api/reply/delete/${reply.id}/`;
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
    }
  }
};
</script>
