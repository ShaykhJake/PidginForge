<template>
  <div>
    <v-btn icon @click="castVote('up')" :loading="voting">
      <v-icon :class="upClass">
        mdi-arrow-up-bold
      </v-icon>
    </v-btn>
    <span class="green--text font-weight-bold">{{ upVoteCount }}</span> /
    <span class="red--text font-weight-bold">{{ downVoteCount }}</span>
    <v-btn icon @click="castVote('down')" :loading="voting">
      <v-icon :class="downClass">
        mdi-arrow-down-bold
      </v-icon>
    </v-btn>
  </div>
</template>
<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "AnswerUpDownVote",

  data() {
    return {
      voting: false
    };
  },
  props: {
    upVoteCount: Number,
    downVoteCount: Number,
    userVote: Number,
    answerid: {
      type: Number,
      required: true
    }
  },
  computed: {
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
      let endpoint = `/api/answer/vote/`;
      let payload = {
        pk: this.answerid,
        vote: votetype
      };
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
    }
  },
  created() {}
};
</script>
<style scoped></style>
