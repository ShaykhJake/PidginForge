<template>
  <v-dialog v-model="dialog" max-width="375" persistent>
    <v-card class="desertsand">
      <v-card-title class="sandstone">
        {{ audioRecord ? "Edit Audio" : "Attach Audio" }}
      </v-card-title>
      <v-card-text class="px-2">
        <div
          class="sentenceBox title"
          :style="`direction:${sentence.direction}`"
        >
          {{ sentence.text }}
        </div>

        <div
          v-if="audio && !newRecording"
          class="my-4"
          style="text-align:center;"
        >
          Current Recording:
          <audio :src="audio.audioFile" controls></audio>
          <v-btn
            small
            class="primary"
            @click="
              newRecording = true;
              audio = null;
            "
            >New Recording</v-btn
          >
        </div>
        <div v-if="!audio || newRecording">
          <AudioRecorder @selectAudio="selectAudio" />
        </div>
        <v-form v-model="valid" class="mt-2 mb-0 pb-0">
          <v-textarea
            class="mb-0 pb-0"
            v-model="curator_note"
            outlined
            placeholder="curator note"
            label="Curator Note*"
            :rules="[rules.requiredCuratorNote]"
          >
          </v-textarea>
        </v-form>
      </v-card-text>
      <v-card-actions class="sandstone">
        <v-btn @click="closeDialog" class="garbage desertsand--text">
          Cancel
        </v-btn>
        <v-btn
          class="primary"
          :disabled="!valid || !audio"
          @click="submitAudio"
          :loading="saving"
        >
          Submit
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import AudioRecorder from "@/components/recorder/AudioRecorder.vue";
import { apiFileService } from "@/common/api.fileservice.js";

export default {
  name: "AttachAudio",
  props: {
    sentence: Object,
    audioRecord: Object,
    dialog: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    audio: {},
    valid: false,
    saving: false,
    curator_note: "",
    newRecording: false,
    rules: {
      requiredCuratorNote: value =>
        (value || "").length > 2 ||
        "The curator note must be at least 3 characters in length."
    }
  }),
  components: {
    AudioRecorder
  },
  methods: {
    selectAudio(audio) {
      this.audio = audio;
    },
    closeDialog() {
      this.$emit("closeDialog");
    },
    submitAudio() {
      // The following grabs the blob and sends it to the API
      this.saving = true;
      var endpoint = "";
      var method = "";
      const formData = new FormData();

      if (this.audioRecord.id && !this.newRecording) {
        // Item exists and needs patching
        endpoint = `/api/vocab/sentenceaudioz/${this.audioRecord.id}/`;
        method = "PATCH";
        formData.append("curator_note", this.curator_note);
      } else if (this.audioRecord.id && this.newRecording) {
        endpoint = `/api/vocab/sentenceaudioz/${this.audioRecord.id}/`;
        method = "PATCH";
        formData.append("curator_note", this.curator_note);
        formData.append("audio_file", this.audio.audioFile);
        formData.append("originalfilename", this.audio.originalfilename);
      } else {
        // Item is new and needs posting
        endpoint = `/api/vocab/sentenceaudioz/`;
        method = "POST";
        formData.append("curator_note", this.curator_note);
        formData.append("audio_file", this.audio.audioFile);
        formData.append("originalfilename", this.audio.originalfilename);
        formData.append("sentence", this.sentence.id);
      }

      try {
        apiFileService(endpoint, method, formData).then(data => {
          if (data && data.id) {
            if (this.audioRecord.id) {
              this.$emit("updateAudio", data);
              this.saving = false;
              this.closeDialog();
            } else {
              this.$emit("pushAudio", data);
              this.saving = false;
              this.closeDialog();
            }
          } else {
            console.log(data || "no data");
            console.log("Something bad happened");
            this.saving = false;
          }
          this.saving = false;
        });
      } catch (err) {
        console.log(err);
        this.saving = false;
      }
    }
  },
  mounted() {
    if (this.audioRecord) {
      this.audio.audioFile = this.audioRecord.audio_file;
      this.curator_note = this.audioRecord.curator_note;
    }
  }
};
</script>

<style scoped>
.sentenceBox {
  color: black;
  background-color: antiquewhite;
  border-left-style: solid;
  border-right-style: solid;
  border-width: 1px;
  border-radius: 5px;
  border-color: grey;
  padding: 2px 2px 2px 2px;
  margin: 2px 2px 2px 2px;
}
audio {
  /* filter: sepia(20%) saturate(70%) grayscale(1) contrast(99%) invert(12%) drop-shadow(3px 3px 3px orange); */
  /* filter: drop-shadow(2px 2px 2px orange); */
  width: 100%;
  height: 50px;
}
/* https://chromium.googlesource.com/chromium/blink/+/72fef91ac1ef679207f51def8133b336a6f6588f/Source/core/css/mediaControls.css?autodive=0%2F%2F%2F */
audio::-webkit-media-controls-panel {
  display: flex;
  flex-direction: row;
  align-items: center;
  /* We use flex-start here to ensure that the play button is visible even
     * if we are too small to show all controls.
     */
  justify-content: flex-start;
  -webkit-user-select: none;
  position: relative;
  z-index: 5;
  height: 50px;
  /* background-color: #DBD4C4; */
  background-color: rgba(219, 212, 196, 1);
  /* border-radius: 5px; */
  /* The duration is also specified in MediaControlElements.cpp and LayoutTests/media/media-controls.js */
  transition: opacity 0.3s;
}
</style>
