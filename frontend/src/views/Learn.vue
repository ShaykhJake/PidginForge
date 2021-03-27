<template>
    <div>
    <v-container class="pa-2 pt-2 mx-auto" fill-height fluid>
      <h1>Browse Learning Material</h1>
        <v-row wrap dense>
          <v-col cols="12">
            [Insert Checkboxes Here]
            - Media type
            - Languages 
            - Tags
            <v-btn>Full Text Search</v-btn>
          </v-col>
        </v-row>

        <v-row wrap dense>
          <v-col cols="12">
            <v-card>
              <v-card-title>
                Language Elements (Audio, Video, Text)
              </v-card-title>
              <v-card-text>
                Total Points: Followers:
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12">
            <v-card>
              <v-card-title>
                Vocabulary
              </v-card-title>
              <v-card-text>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
    </v-container>
  </div>
</template>
<script>

export default {
  name: "Learn",
  data() {
    return {
      thinking: false,
      loadingQuestions: false
    };
  },
  components: {

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
