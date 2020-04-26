<template>
  <v-card class="desertsand">
    <v-card-title class="calligraphy desertsand--text">
      Available Translations: {{ translationList.length }}
    </v-card-title>
    <v-list
      two-line
      dense
      subheader
      class="desertsand overflow-y-auto"
      max-height="300"
    >
      <v-list-item
        v-for="translation in translationList"
        :key="translation.id"
        @click="loadTranslation(translation.id)"
      >
        <v-list-item-avatar>
          <v-avatar class="mr-2" size="42">
            <v-img
              class="elevation-6"
              :src="translation.curator['user_profile'].avatar"
            ></v-img>
          </v-avatar>

          <v-icon v-text="translation.curator['user_profile'].avatar"></v-icon>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title>
            {{ translation.curator.username }} @
            {{ translation.curationdate }}
            <v-chip small outlined class="languages languages--text">
              {{ translation.targetlanguage }}
            </v-chip>
          </v-list-item-title>
          <v-list-item-subtitle>
            <v-icon :class="upClass(translation.user_vote)">
              mdi-arrow-up-circle-outline
            </v-icon>
            <span class="green--text font-weight-bold">{{
              translation.upvote_count
            }}</span>
            /
            <span class="red--text font-weight-bold">{{
              translation.downvote_count
            }}</span>
            <v-icon :class="downClass(translation.user_vote)">
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
  name: "TranslationListModal",
  components: {},
  props: {
    translationList: {}
    // username: String
  },
  data: () => ({
    translationz: [
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
    loadTranslation(translationid) {
      this.$emit("loadTranslation", translationid);
      this.closeDialog();
      // this.$emit("loadTranslation", translationid);
    }
  },
  created() {}
};
</script>
<style lang="stylus"></style>
