<template>
  <span>
    <v-btn icon @click="castVote('up')" :loading="voting">
      <v-icon :class="upClass">
        mdi-arrow-up-circle-outline
      </v-icon>
    </v-btn>
    <span :class="upTextClass">{{ upVoteCount }}</span> /
    <span :class="downTextClass">{{ downVoteCount }}</span>
    <v-btn icon @click="castVote('down')" :loading="voting">
      <v-icon :class="downClass">
        mdi-arrow-down-circle-outline
      </v-icon>
    </v-btn>
  </span>
</template>
<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "UpDownVote",

  data() {
    return {
      voting: false
    };
  },
  props: {
    upVoteCount: Number,
    downVoteCount: Number,
    userVote: Number,
    slug: {
      type: String,
      required: false
    },
    elementType: {
      type: String,
      required: true
    },
    elementid: {
      type: Number,
      required: false
    },
    textTypography: {
      type: String,
      default: "",
      required: false
    }
  },
  computed: {
    upTextClass() {
      return this.textTypography + " green--text font-weight-bold";
    },
    downTextClass() {
      return this.textTypography + " red--text font-weight-bold";
    },
    upClass() {
      if (this.userVote === 1) {
        return "success--text";
      } else {
        return "";
      }
    },
    downClass() {
      if (this.userVote === -1) {
        return "error--text";
      } else {
        return "";
      }
    }
  },

  methods: {
    castVote(votetype) {
      if (votetype == "up" && this.userVote === 1) {
        return false;
      } else if (votetype == "down" && this.userVote === -1) {
        return false;
      }
      this.voting = true;
      let payload = {};
      let endpoint = "";
      if (this.elementType === "YouTube") {
        endpoint = `/api/elements/youtube/vote/`;
        payload.slug = this.slug;
        payload.vote = votetype;
      } else if (this.elementType === "Audio") {
        endpoint = `/api/elements/audio/vote/`;
        payload.slug = this.slug;
        payload.vote = votetype;
      } else if (this.elementType === "Transcript") {
        endpoint = `/api/elements/transcript/vote/`;
        payload.id = this.elementid; // Note that this will actually be the pk
        payload.vote = votetype;
      } else if (this.elementType === "Translation") {
        endpoint = `/api/elements/translation/vote/`;
        payload.id = this.elementid; // Note that this will actually be the pk
        payload.vote = votetype;
      }

      if (endpoint) {
        apiService(endpoint, "POST", payload).then(data => {
          if (data) {
            this.$emit("updateVote", data);
            // message = data.message;
            // success = data.success;
          } else {
            // message = "There was an error submitting your vote";
            // success = false
          }
          this.voting = false;
        });
      } else {
        this.voting = false;
      }
    }
  },
  created() {}
};
</script>
<style scoped></style>
