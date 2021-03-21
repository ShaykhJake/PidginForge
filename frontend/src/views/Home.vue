<template>
  <div class="sandstone">
    <v-container class="pa-2 pt-2 mx-auto" fill-height fluid>
      <v-row justify-center dense wrap>
        <v-col cols="12">
          <v-row justify-center dense wrap>
            <v-col cols="12"> </v-col>
            <!-- This is the new section for the new elements list -->
            <v-col cols="12"><QuestionsList /></v-col>
            <v-col cols="12"><ElementList /></v-col>
            <v-col cols="12"><StackList /></v-col>
            <!-- <v-col cols="12"><LessonList /></v-col> -->
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import ElementList from "@/components/elements/ElementList.vue";
// import LessonList from "@/components/lessons/LessonList.vue";
import QuestionsList from "@/components/questions/QuestionsList.vue";
import StackList from "@/components/vocab/StackList.vue";
export default {
  name: "Home",
  data() {
    return {};
  },
  components: {
    ElementList,
    // LessonList,
    QuestionsList,
    StackList
  },
  methods: {
    loadLearning() {},
    loadNewStuff() {},
    loadForum() {}
  },
  created() {
    document.title = "PidginForge: Home";
  }
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
