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
      let endpoint=`api/lessons/vote/`
      this.voting = true;
      let payload = { 
        slug: this.slug,
        vote: votetype
      };
      try {
        apiService(endpoint, "POST", payload).then(data => {
          if (data) {
            this.$emit("updateVote", data);
            this.voting=false;
          } else {
            console.log("There was a major problem with the request.");
            // console.log(data.message);
            this.voting = false;
          }
        });
      } catch (err) {
        console.log(err);
        this.voting = false; 
      }
    }
  },
  created() {}
};
</script>
<style scoped></style>
