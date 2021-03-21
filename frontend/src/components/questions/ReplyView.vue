<template>
  <v-card class="sandstone mb-1" outlined>
    <v-card-title class="sandstone">
      <v-avatar class="mr-2" size="42">
        <v-img
          class="elevation-6"
          :src="reply.author.user_profile.avatar"
        ></v-img>
      </v-avatar>

      <span class="overline"
        >On {{ reply.created_at }},
        <v-dialog v-model="profileDialog" width="275">
          <template v-slot:activator="{ on }">
            <a
              v-on="on"
              text
              small
              class="primary--text font-weight-bold px-1 py-0"
            >
              {{ reply.author.username }}
            </a>
          </template>
          <ProfileSnippet
            v-if="profileDialog"
            :profileObject="reply.author"
            :profileDialog="profileDialog"
            @closeDialog="profileDialog = false"
          />
        </v-dialog>

        replied:</span
      ><br />
    </v-card-title>
    <v-card-text class="py-1 sandstone black--text">
      <v-row wrap no-gutters dense>
        <v-col cols="12" v-if="!replying">
          <p class="body-2">{{ reply.content }}</p>
        </v-col>
        <v-col v-if="replying" cols="12">
          <v-form ref="editreply" v-model="valid" class="mt-2">
            <v-textarea
              v-model="reply.content"
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
            class="primary desertsand--text mr-1"
            @click="submitReplyEdit"
            :loading="submitting"
            :disabled="!valid"
          >
            Submit <v-icon right>mdi-reply</v-icon>
          </v-btn>
          <v-btn
            small
            class="garbage desertsand--text mr-1"
            @click="cancelEdit"
          >
            Cancel<v-icon right>mdi-cancel</v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </v-card-text>

    <v-card-actions class="py-1">
      <v-btn
        x-small
        class="mr-1 primary desertsand--text"
        v-if="isReplyAuthor && !replying && !deleteConfirm"
        @click="replying = true"
      >
        Edit <v-icon right>mdi-pencil</v-icon>
      </v-btn>
      <v-btn
        x-small
        class="mr-1 garbage desertsand--text"
        v-if="isReplyAuthor && !replying && !deleteConfirm"
        @click="deleteConfirm = true"
      >
        Delete <v-icon right>mdi-delete</v-icon>
      </v-btn>
      <v-btn
        small
        @click="submitReplyDelete"
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
        Cancel Delete<v-icon right>mdi-cancel</v-icon>
      </v-btn>
      <v-btn
        x-small
        :hidden="deleteConfirm"
        @click="flaggerDialog = true"
        v-if="!isReplyAuthor"
        :disabled="reply.user_has_flagged"
        class="error desertsand--text mr-1"
      >
        <v-badge
          color="error lighten-1 white--text"
          :content="reply.flag_count"
        >
          Flag<v-icon right>mdi-flag</v-icon>
        </v-badge>
      </v-btn>
      <ContentFlagger
        :flagger-dialog="flaggerDialog"
        @flagSuccess="flagSuccess"
        @closeDialog="flaggerDialog = false"
        content-type="answer_reply"
        :contentid="reply.id"
      />
    </v-card-actions>
  </v-card>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import ContentFlagger from "@/components/ContentFlagger.vue";
export default {
  name: "Reply",
  props: {
    reply: {
      type: Object,
      required: false
    }
  },
  data() {
    return {
      oldContent: "",
      flaggerDialog: false,
      deleteConfirm: false,
      profileDialog: false,
      replying: false,
      valid: false,
      submitting: false,
      rules: {
        contentMin: value =>
          (value || "").length > 15 || "You must type at least 16 characters!"
        // contentMax: value => (value || '').length < 241 || "No more than 240 characters!",
      }
    };
  },
  components: {
    ContentFlagger,
    ProfileSnippet: () =>
      import(
        /* webpackPrefetch: true */ "@/components/profile/ProfileSnippet.vue"
      )
  },
  computed: {
    isReplyAuthor() {
      return (
        this.reply.author.username === window.localStorage.getItem("username")
      );
    }
  },
  methods: {
    cancelEdit() {
      this.replying = false;
      this.reply.content = this.oldContent;
    },
    submitReplyEdit() {
      if (this.reply.content) {
        this.submitting = true;
        let endpoint = `/api/questions/reply/edit/`;
        apiService(endpoint, "PATCH", {
          pk: this.reply.id,
          content: this.reply.content
        }).then(() => {
          this.replying = false;
          this.submitting = false;
        });
      } else {
        this.error = "You can't submit an empty reply!";
      }
    },
    submitReplyDelete() {
      this.deleteConfirm = false;
      this.$emit("delete-reply", this.reply);
    },
    flagSuccess() {
      this.flaggerDialog = false;
      this.reply.user_has_flagged = true;
      this.reply.flag_count += 1;
    }
  },
  mounted() {
    this.oldContent = this.reply.content;
  }
};
</script>
