<template>
  <div>
    <v-card class="pa-0 ma-0 sandstone">
      <!-- COMMMENT CARD -->
      <v-card-title
        class="calligraphy desertsand--text subtitle-2 py-1 px-1 ma-0"
        v-if="transcript.id"
      >
        <v-avatar class="ma-0" size="30">
          <v-img
            class="elevation-6"
            :src="transcript.curator.user_profile.avatar"
          ></v-img>
        </v-avatar>
        <p class="ml-1 mr-1 pa-0 my-0">
          On {{ transcript.curation_date }},
          <v-dialog v-model="profileDialog" width="275">
            <template v-slot:activator="{ on }">
              <a
                v-on="on"
                text
                small
                class="primary--text font-weight-bold px-0 py-0"
              >
                {{ transcript.curator.username }}
              </a>
            </template>
            <ProfileSnippet
              v-if="profileDialog"
              :profileObject="transcript.curator"
              :profileDialog="profileDialog"
              @closeDialog="profileDialog = false"
            />
          </v-dialog>
          &nbsp;transcribed:
        </p>
        <v-spacer />
        <v-btn icon @click="changeEditorFontSize('up')">
          <v-icon color="primary">zoom_in</v-icon>
        </v-btn>
        <v-btn icon @click="changeEditorFontSize('down')" class="mr-2">
          <v-icon color="primary">zoom_out</v-icon>
        </v-btn>
        <div
          v-if="isTranscriptCurator && !editMode && !deleteConfirm"
          cols="12"
        >
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

        <div v-if="isTranscriptCurator && !editMode && deleteConfirm" cols="12">
          <v-btn
            small
            @click="submitTranscriptDelete"
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

        <div v-if="isTranscriptCurator && editMode">
          <v-btn
            small
            class="primary desertsand--text mr-1"
            @click="submitTranscriptEdit"
            :loading="submittingTranscript"
          >
            Submit Edit<v-icon right>mdi-reply</v-icon>
          </v-btn>
          <v-btn small class="garbage desertsand--text" @click="cancelEdit">
            Cancel <v-icon right>mdi-cancel</v-icon>
          </v-btn>
        </div>
      </v-card-title>
      <v-card-title
        class="calligraphy desertsand--text subtitle-2 py-1 px-1 ma-0"
        v-if="transcript.isNewTranscript"
      >
        New Transcript
        <v-spacer />
        <v-btn icon @click="changeEditorFontSize('up')">
          <v-icon color="primary">zoom_in</v-icon>
        </v-btn>
        <v-btn icon @click="changeEditorFontSize('down')" class="mr-2">
          <v-icon color="primary">zoom_out</v-icon>
        </v-btn>
        <v-btn
          small
          class="primary desertsand--text mr-1"
          @click="submitNewTranscript"
          :loading="submittingTranscript"
        >
          Submit Transcript<v-icon right>mdi-reply</v-icon>
        </v-btn>

        <v-btn
          small
          @click="cancelNewTranscript"
          class="mr-1 garbage desertsand--text"
        >
          Cancel<v-icon right>mdi-cancel</v-icon>
        </v-btn>
      </v-card-title>
      <!-- <v-card-title v-else>New Transcript</v-card-title> -->

      <v-card-text class="desertsand black--text pa-0 ma-0">
        <SimpleTipTap
          :editMode="editMode"
          :showZoom="false"
          @triggerTimeStamp="triggerTimeStamp"
          @skipToTime="skipToTime"
          :timingEnabled="true"
          ref="textEditor"
          :content="transcript.rich_text ? transcript.rich_text : null"
        />
      </v-card-text>

      <v-card-actions v-if="false" class="desertsand pb-0">
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
              :disabled="transcript.user_has_flagged"
              class="error desertsand--text mr-1"
            >
              <v-badge
                color="error lighten-1 white--text"
                :content="transcript.flag_count"
              >
                Flag<v-icon right>mdi-flag</v-icon>
              </v-badge>
            </v-btn>
            <!-- <ContentFlagger
              :flagger-dialog="flaggerDialog"
              @flagSuccess="flagSuccess"
              @closeDialog="flaggerDialog = false"
              content-type="answer"
              :contentid="transcript.id"
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

      <!-- <v-card-text class="desertsand" v-if="repliesExist">
        <v-row dense no-gutters>
          <v-col cols="12" v-for="reply in transcript.replies" :key="reply.id">
            <ReplyView :reply="reply" @delete-reply="deleteReply" />
          </v-col>
        </v-row>
      </v-card-text> -->
    </v-card>
  </div>
</template>

<script>
  import { apiService } from "@/common/api.service.js";
  // import ReplyView from "@/components/questions/ReplyView.vue";
  // import TranscriptUpDownVote from "@/components/questions/TranscriptUpDownVote.vue";
  // import ContentFlagger from "@/components/ContentFlagger.vue";
  import SimpleTipTap from "@/components/elements/SimpleTipTap.vue";
  // import TranscriptReplies from "@/components/elements/TranscriptReplies.vue";
  export default {
    name: "TranscriptComponents",
    props: {
      isNewTranscript: {
        type: Boolean,
        default: false,
      },
      transcript_index: {
        type: Number,
        required: true,
      },
      element_id: {
        type: Number,
        required: true,
      },
      transcript: {
        type: Object,
        required: true,
      },
    },
    data() {
      return {
        addingTranscript: false,
        flaggerDialog: false,
        deleteConfirm: false,
        profileDialog: false,
        submitting: false,
        editing: false,
        editMode: false,
        editValid: false,
        submittingTranscript: false,
        submittingReply: false,
        replying: false,
        userHasReplied: false,
        valid: false,

        newReply: {
          content: "",
        },
        rules: {
          contentMin: (value) =>
            (value || "").length > 4 || "You must type at least 5 characters!",
          // contentMax: value => (value || '').length < 241 || "No more than 240 characters!",
        },
      };
    },
    computed: {
      isTranscriptCurator() {
        return (
          this.transcript.curator.username ===
          window.localStorage.getItem("username")
        );
      },
      repliesExist() {
        if (this.transcript.replies) {
          return true;
        } else {
          return false;
        }
      },
    },
    components: {
      // ReplyView,
      SimpleTipTap,
      // TranscriptReplies,
      // TranscriptUpDownVote,
      // ContentFlagger,
      // ProfileSnippet: () =>
      //   import(
      //     /* webpackPrefetch: true */ "@/components/profile/ProfileSnippet.vue"
      //   ),
    },
    methods: {
      skipToTime(time) {
        this.$emit("skipToTime", time);
      },
      triggerTimeStamp() {
        // console.log("triggering2")
        console.log(this.transcript_index);
        this.$emit("triggerTimeStamp", this.transcript_index);
      },
      recordTimeStamp(time) {
        this.$refs.textEditor.recordTimeStamp(time);
      },
      toggleEdit() {
        this.editMode = true;
        this.$refs.textEditor.editor.setOptions({ editable: this.editMode });
      },
      cancelEdit() {
        this.editMode = false;
        this.$refs.textEditor.editor.setOptions({ editable: this.editMode });
        this.$refs.textEditor.editor.setContent(this.transcript.rich_text);
      },
      submitReply() {
        // console.log("submitted");
        this.submittingReply = true;
        let endpoint = `/api/questions/reply/post/`;
        apiService(endpoint, "POST", {
          content: this.newReply.content,
          answerpk: this.transcript.id,
        }).then((data) => {
          this.transcript.replies.unshift(data.data);
          // this.userHasReplied = true;
          this.submittingReply = false;
          this.replying = false;
          // console.log(data);
        });
      },
      submitTranscriptEdit() {
        this.editMode = false;
        this.$refs.textEditor.editor.setOptions({ editable: this.editMode });
        this.transcript.rich_text = this.$refs.textEditor.editor.getJSON();
        this.transcript.plain_text = this.$refs.textEditor.editor.view.state.doc.textContent;
        this.$emit("updateTranscript", this.transcript_index, this.transcript);
      },
      cancelNewTranscript() {
        this.$emit("cancelNew");
      },
      submitNewTranscript() {
        this.editMode = false;
        this.$refs.textEditor.editor.setOptions({ editable: this.editMode });
        this.transcript.rich_text = this.$refs.textEditor.editor.getJSON();
        this.transcript.plain_text = this.$refs.textEditor.editor.view.state.doc.textContent;
        this.$emit("submitTranscript", this.transcript_index, this.transcript);
      },
      updateVote(data) {
        this.transcript.user_vote = data.newuservote;
        this.transcript.downvote_count = data.newdowncount;
        this.transcript.upvote_count = data.newupcount;
      },
      flagSuccess() {
        this.flaggerDialog = false;
        this.transcript.user_has_flagged = true;
        this.transcript.flag_count += 1;
      },
      changeEditorFontSize(direction) {
        if (direction === "up") {
          this.$refs.textEditor.changeEditorFontSize("up");
        } else {
          this.$refs.textEditor.changeEditorFontSize("down");
        }
      },
    },
    mounted() {
      if (this.transcript.isNewTranscript) {
        this.editMode = true;
        this.$refs.textEditor.editor.setOptions({ editable: this.editMode });
      }
    },
    created() {},
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
