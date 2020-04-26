<template>
  <v-card class="desertsand">
    <v-card-title class="calligraphy desertsand--text">
      Available Transcripts: {{ transcriptList.length }}
    </v-card-title>
    <v-list
      two-line
      dense
      subheader
      class="desertsand overflow-y-auto"
      max-height="300"
    >
      <v-list-item
        v-for="transcript in transcriptList"
        :key="transcript.id"
        @click="loadTranscript(transcript.id)"
      >
        <v-list-item-avatar>
          <v-avatar class="mr-2" size="42">
            <v-img
              class="elevation-6"
              :src="transcript.curator['user_profile'].avatar"
            ></v-img>
          </v-avatar>

          <v-icon v-text="transcript.curator['user_profile'].avatar"></v-icon>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title
            >{{ transcript.curator.username }} @
            {{ transcript.curationdate }}</v-list-item-title
          >
          <v-list-item-subtitle
            >Translations: {{ transcript.translations.length }}; Forks:
            {{ transcript.forks_count }} forks; last updated
            {{ transcript.curationdate }}.</v-list-item-subtitle
          >
          <v-list-item-subtitle>
            <v-icon :class="upClass(transcript.user_vote)">
              mdi-arrow-up-circle-outline
            </v-icon>
            <span class="green--text font-weight-bold">{{
              transcript.upvote_count
            }}</span>
            /
            <span class="red--text font-weight-bold">{{
              transcript.downvote_count
            }}</span>
            <v-icon :class="downClass(transcript.user_vote)">
              mdi-arrow-down-circle-outline
            </v-icon>
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>
    <v-card-actions class="calligraphy desertsand--text">
      <v-spacer></v-spacer>
      <v-btn @click="closeDialog" class="garbage desertsand--text"
        >Cancel<v-icon right>mdi-cancel</v-icon></v-btn
      >
      <v-spacer></v-spacer>
    </v-card-actions>
  </v-card>
</template>
<script>
export default {
  name: "TranscriptListModal",
  components: {},
  props: {
    transcriptList: {}
    // username: String
  },
  data: () => ({
    transcriptz: [
      {
        avatar: "folder",
        curator: "ShaykhJake",
        curationdate: "Jan 9, 2014",
        votebalance: "+1",
        translationcount: 1,
        id: 1
      },
      {
        avatar: "folder",
        curator: "ShaykhJake",
        curationdate: "Jan 9, 2014",
        votebalance: "-1",
        translationcount: 1,
        id: 2
      },
      {
        avatar: "folder",
        curator: "ShaykhJake",
        curationdate: "Jan 9, 2014",
        votebalance: "+5",
        translationcount: 1,
        id: 3
      },
      {
        avatar: "folder",
        curator: "ShaykhJake",
        curationdate: "Jan 9, 2014",
        votebalance: "-3",
        translationcount: 1,
        id: 4
      },
      {
        avatar: "folder",
        curator: "ShaykhJake",
        curationdate: "Jan 9, 2014",
        votebalance: "+6",
        translationcount: 1,
        id: 5
      }
    ]
  }),
  computed: {},
  methods: {
    upClass(userVote) {
      if (userVote === 1) {
        return "success--text";
      } else {
        return "";
      }
    },
    downClass(userVote) {
      if (userVote === -1) {
        return "error--text";
      } else {
        return "";
      }
    },
    closeDialog() {
      this.$emit("closeDialog");
    },
    loadTranscript(transcriptid) {
      this.$emit("loadTranscript", transcriptid);
      this.closeDialog();
      // this.$emit("loadTranscript", transcriptid);
    }
  },
  created() {}
};
</script>
<style lang="stylus"></style>
