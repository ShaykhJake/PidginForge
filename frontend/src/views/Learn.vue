<template>
    <div>
    <v-container class="pa-2 pt-2 mx-auto" fill-height fluid>
      <h1>Learner Dashboard</h1>
        <v-row wrap dense v-if="false">
          <v-col cols="12">
            <v-card>
              <v-card-title>
                Your Stats
              </v-card-title>
              <v-card-text>
                Total Points: Followers:
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        <v-row wrap dense>
          <v-col cols="12" sm="6" md="4" lg="4">
            <SavedStackList />
          </v-col>

          <v-col cols="12" sm="6" md="4" lg="4">
            <SavedElementList />
          </v-col>

          <v-col cols="12" sm="6" md="4" lg="4">
            <SavedQuestionList />
          </v-col>
        </v-row>
    </v-container>
  </div>
</template>
<script>
import SavedStackList from "@/components/vocab/SavedStackList.vue";
import SavedQuestionList from "@/components/questions/SavedQuestionList.vue";
import SavedElementList from "@/components/elements/SavedElementList.vue";

export default {
  name: "Learn",
  data() {
    return {
      thinking: false,
      loadingQuestions: false
    };
  },
  components: {
    SavedStackList,
    // SavedLessonList,
    SavedElementList,
    SavedQuestionList
    // SavedAudioList,
    // SavedVideoList,
    // SavedTextList
  },
  props: {},
  methods: {},
  created() {}
};
</script>
<style scoped>
.content-box > * {
  width: 100%;
  max-height: 650px;
  overflow-x: hidden;
  overflow-x: auto;
  /* overflow-y: hidden; */
  /* overflow-x: auto; */

  position: relative;
  /* position: absolute; */
  /* width: 100%; */
}
</style>
