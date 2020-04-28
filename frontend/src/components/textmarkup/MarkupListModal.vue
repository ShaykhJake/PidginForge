<template>
  <v-card class="desertsand">
    <v-card-title class="calligraphy desertsand--text">
      Available Markups: {{ markupList.length }}
    </v-card-title>
    <v-list
      two-line
      dense
      subheader
      class="desertsand overflow-y-auto"
      max-height="300"
    >
      <v-list-item
        v-for="markup in markupList"
        :key="markup.id"
        @click="loadMarkup(markup.id)"
      >
        <v-list-item-avatar>
          <v-avatar class="mr-2" size="42">
            <v-img
              class="elevation-6"
              :src="markup.curator['user_profile'].avatar"
            ></v-img>
          </v-avatar>

          <v-icon v-text="markup.curator['user_profile'].avatar"></v-icon>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title>
            {{ markup.curator.username }} @
            {{ markup.curationdate }}
            <v-chip small outlined class="languages languages--text">
              {{ markup.targetlanguage }}
            </v-chip>
          </v-list-item-title>
          <v-list-item-subtitle>
            <v-icon :class="upClass(markup.user_vote)">
              mdi-arrow-up-circle-outline
            </v-icon>
            <span class="green--text font-weight-bold">{{
              markup.upvote_count
            }}</span>
            /
            <span class="red--text font-weight-bold">{{
              markup.downvote_count
            }}</span>
            <v-icon :class="downClass(markup.user_vote)">
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
  name: "MarkupListModal",
  components: {},
  props: {
    markupList: {}
    // username: String
  },
  data: () => ({
    markupz: [
      {
        avatar: "folder",
        curator: "ShaykhJake",
        curationdate: "Jan 9, 2014",
        votebalance: "+1",
        markupcount: 1,
        id: 1
      },
      {
        avatar: "folder",
        curator: "ShaykhJake",
        curationdate: "Jan 9, 2014",
        votebalance: "-1",
        markupcount: 1,
        id: 2
      },
      {
        avatar: "folder",
        curator: "ShaykhJake",
        curationdate: "Jan 9, 2014",
        votebalance: "+5",
        markupcount: 1,
        id: 3
      },
      {
        avatar: "folder",
        curator: "ShaykhJake",
        curationdate: "Jan 9, 2014",
        votebalance: "-3",
        markupcount: 1,
        id: 4
      },
      {
        avatar: "folder",
        curator: "ShaykhJake",
        curationdate: "Jan 9, 2014",
        votebalance: "+6",
        markupcount: 1,
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
    loadMarkup(markupid) {
      this.$emit("loadMarkup", markupid);
      this.closeDialog();
      // this.$emit("loadMarkup", markupid);
    }
  },
  created() {}
};
</script>
