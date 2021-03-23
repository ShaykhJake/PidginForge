<template>
  <div>
    <v-card class="mt-2" pa-0>
      <v-card-title class="py-1 px-2 desertsand">
        Transcripts
        <v-spacer></v-spacer>
        <small v-if="transcripts.length > 0"
          >&nbsp;({{ transcripts.length }} of {{ totalCount }} loaded)</small
        >
        <small v-else>(no transcripts yet)</small>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn icon v-on="on" class="primary--text" @click="addTranscript">
              <v-icon>library_add</v-icon>
            </v-btn>
          </template>
          <span>Add Transcript</span>
        </v-tooltip>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn
              v-on="on"
              icon
              @click="showTranscripts = !showTranscripts"
              class="garbage--text"
            >
              <v-icon v-if="!showTranscripts">mdi-eye</v-icon>
              <v-icon v-if="showTranscripts">mdi-eye-off</v-icon>
            </v-btn>
          </template>
          <span v-if="!showTranscripts">View Transcripts</span>
          <span v-else>Hide Transcripts</span>
        </v-tooltip>
      </v-card-title>
      
      <v-card-text class="pa-1 ma-0 desertsand" v-show="showTranscripts">
        <TranscriptComponent
          class="mb-1"
          ref="scriptEditor"
          v-for="(transcript, index) in transcripts"
          :transcript="transcript"
          :key="transcript.id"
          :element_id="element_id"
          :transcript_index="index"
          :isNewTranscript="transcript.isNewTranscript"
          @triggerTimeStamp="triggerTimeStamp"
          @skipToTime="skipToTime"
          @cancelNew="deleteTranscript(transcript)"
          @updateTranscript="submitTranscriptEdit"
          @submitTranscript="submitNewTranscript"
        />
      </v-card-text>
      <v-card-actions class="desertsand ma-0 pa-0">
        <v-btn
          v-show="next || loading"
          @click="getTranscripts"
          :loading="loading"
          class="primary desertsand--text"
          block
        >
          Load More Transcripts <v-icon right>mdi-chevron-down</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
  import { apiService } from "@/common/api.service.js";
  // import ReplyView from "@/components/questions/ReplyView.vue";
  import TranscriptComponent from "@/components/elements/TranscriptComponent.vue";
  export default {
    name: "ElementTranscripts",
    props: {
      element_id: {
        type: Number,
        required: true,
      },
    },
    data() {
      return {
        transcripts: [],
        next: null,
        loading: false,
        totalCount: 0,
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
        showTranscripts: true,
        valid: false,
        activeTranscriptIndex: 0,
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
    },
    components: {
      TranscriptComponent,
    },
    methods: {
      skipToTime(time) {
        this.$emit("skipToTime", time);
      },
      triggerTimeStamp(index) {
        console.log(index)
        this.activeTranscriptIndex = index;
        // console.log("triggering3")
        this.$emit("triggerTimeStamp");
      },
      recordTimeStamp(time) {
        // this.$refs.ttviewer.recordTimeStamp(time)
        // console.log("sending3")
        console.log(this.activeTranscriptIndex)
        if(this.activeTranscriptIndex != null){
          this.$refs.scriptEditor[this.activeTranscriptIndex].recordTimeStamp(time);
        } else {
          console.log("no active transcript")
        }
      },
      toggleEdit() {
        this.editMode = !this.editMode;
        this.editor.setOptions({
          editable: this.editMode,
        });
      },
      getTranscripts() {
        this.loading = true;
        let endpoint = `/api/elements/transcripts/list/?element=${this.element_id}`;
        if (this.next) {
          endpoint = this.next;
        }
        apiService(endpoint).then((data) => {
          // console.log(data);
          this.totalCount = data.count;
          this.transcripts.push(...data.results);
          this.loading = false;
          if (data.next) {
            this.next = data.next;
          } else {
            this.next = null;
          }
        });
      },
      submitTranscriptDelete() {
        this.deleteConfirm = false;
        this.$emit("delete-transcript", this.transcript);
      },
      addTranscript() {
        const newTranscript = {
          // rich_text: "new transcript",
          element_id: this.element_id,
          isNewTranscript: true,
        };
        this.activeTranscriptIndex = 0;
        this.transcripts.push(newTranscript);
        this.addingTranscript = true;
        console.log(this.transcripts)
      },
      deleteTranscript(transcript) {
        this.transcripts.splice(this.transcripts.indexOf(transcript), 1);
      },
      submitTranscriptEdit(transcript_index, transcript) {
        this.submitting = true;
        console.log("submitting)")
        console.log(transcript)
        let endpoint = `/api/elements/transcriptz/${transcript.id}/`;
        apiService(endpoint, "PATCH", {
          plain_text: transcript.plain_text,
          rich_text: transcript.rich_text,
          element: this.element_id,
          published: true,
        }).then((data) => {
          if (data) {
            console.log(data);
            this.$set(this.transcripts, transcript_index, data);
            this.editMode = false;
            this.submittingTranscript = false;
          }
        });
      },
      submitNewTranscript(transcript_index, transcript) {
        this.submitting = true;
        let endpoint = `/api/elements/transcriptz/`;
        let method = "POST";
        let payload = {
          rich_text: transcript.rich_text,
          plain_text: transcript.plain_text,
          element: this.element_id,
          published: true,
        };
        apiService(endpoint, method, payload).then((data) => {
          if (data) {
            this.$set(this.transcripts, transcript_index, data);
            this.totalCount++;
            // this.transcripts.unshift(data)
          }
          this.submitting = false;
        });
        console.log("submitting");
        this.submitting = false;
      },

      updateTranscript(transcript_index, data) {
        // console.log(data)
        // this.transcripts[transcript_index] = data;
        // console.log(this.transcripts)
        this.$set(this.transcripts, transcript_index, data);
        console.log(this.transcripts);
        // this.transcripts.splice(this.transcripts.indexOf(transcript), 1);
      },
      submitNew() {
        console.log("submitting");
        this.addingTranscript = false;
      },
    },
    mounted() {
      this.getTranscripts();
    },
    created() {},
  };
</script>
<style>
</style>
