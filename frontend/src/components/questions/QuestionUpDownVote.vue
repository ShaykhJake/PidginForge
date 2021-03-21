<template>
  <div>
    <v-row no-gutters dense>
      <v-col cols="auto" class="ma-0 pa-0">
        <v-col cols="12" class="ma-0 pa-0">
          <v-btn
            fab
            x-small
            color="sandstone"
            @click="castVote('up')"
            :loading="voting"
            :disabled="disabled"
            class="ma-0 pa-0"
          >
            <v-icon :class="upClass"> mdi-arrow-up-bold </v-icon>
          </v-btn>
        </v-col>
        <v-col class="ma-0 pa-0">
          <span class="green--text font-weight-bold ma-0 pa-0">{{
            upVoteCount
          }}</span>
          /
          <span class="red--text font-weight-bold ma-0 pa-0">{{
            downVoteCount
          }}</span>
        </v-col>
        <v-col class="ma-0 pa-0">
          <v-btn
            x-small
            fab
            color="sandstone"
            @click="castVote('down')"
            :loading="voting"
            :disabled="disabled"
          >
            <v-icon :class="downClass"> mdi-arrow-down-bold </v-icon>
          </v-btn>
        </v-col>
      </v-col>
    </v-row>
  </div>
</template>
<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "QuestionUpDownVote",
  data() {
    return {
      voting: false
    };
  },
  props: {
    upVoteCount: Number,
    downVoteCount: Number,
    userVote: Number,
    disabled: {
      type: Boolean,
      default: false
    },
    question_id: {
      type: Number,
      required: true
    }
  },
  computed: {
    upClass() {
      if (this.userVote === 1) {
        return "success--text";
      } else {
        return "black--text";
      }
    },
    downClass() {
      if (this.userVote === -1) {
        return "error--text";
      } else {
        return "black--text";
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
      let endpoint = `/api/questions/question/vote/`;
      let payload = {
        question_id: this.question_id,
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
  created() {
    console.log(this.userVote);
  }
};
</script>
<style scoped></style>
