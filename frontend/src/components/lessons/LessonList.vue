<template>
  <div class="lessonlist">
    <v-card class="desertsand">
      <v-toolbar class="desertsand calligraphy--text" dense elevation="6">
        <v-toolbar-title
          >New Lessons
          <small v-if="totalCount > 0"
            >({{ lessons.length }} of {{ totalCount }} loaded)</small
          >
          <small v-else>(no results)</small>
        </v-toolbar-title>
        <v-spacer></v-spacer>

        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn
              v-on="on"
              icon
              :to="{
                name: 'Lesson-Builder'
              }"
            >
              <v-icon color="elements">library_add</v-icon>
            </v-btn>
          </template>
          <span>Add Lesson</span>
        </v-tooltip>

        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn
              v-on="on"
              icon
              @click="showLessons = !showLessons"
              class="garbage--text"
            >
              <v-icon v-if="!showLessons">mdi-eye</v-icon>
              <v-icon v-if="showLessons">mdi-eye-off</v-icon>
            </v-btn>
          </template>
          <span v-if="!showLessons">View Lessons</span>
          <span v-else>Hide Lessons</span>
        </v-tooltip>
      </v-toolbar>
      <v-card-text v-show="showLessons" class="content-box calligraphy pa-1">
        <v-row wrap dense v-if="lessons.length < 0 && !loadingLessons">
          <v-col cols="12">
            <v-card>
              <v-card-text class="desertsand calligraphy--text">
                There are no lessons which match your language preferences. You
                may need to update your profile to add learning languages...or
                maybe we just don't have enough content yet!
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        <v-row wrap dense v-if="lessons.length > 0">
          <v-col
            cols="12"
            sm="6"
            md="4"
            lg="3"
            v-for="lesson in lessons"
            :key="lesson.id"
          >
            <LessonMicro :lesson="lesson" />
          </v-col>
        </v-row>
        <v-btn
          v-show="next || loadingLessons"
          @click="getLessons"
          :loading="loadingLessons"
          class="elements desertsand--text"
          block
        >
          Load More Lessons <v-icon right>mdi-chevron-down</v-icon>
        </v-btn>
        <v-overlay :value="loadingLessons" absolute>
          <v-progress-circular indeterminate size="64"></v-progress-circular>
        </v-overlay>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import LessonMicro from "@/components/lessons/LessonMicro.vue";
export default {
  name: "LessonList",
  components: {
    LessonMicro
  },
  data() {
    return {
      showLessons: true,
      lessons: [],
      loadingLessons: false,
      next: null,
      totalCount: 0
    };
  },
  props: {
    preferenceFilter: {
      required: false,
      default: false
    }
  },
  computed: {},

  methods: {
    getLessons() {
      let endpoint = `/api/lessons/list/`;
      if (this.next) {
        endpoint = this.next;
      }
      this.loadingLessons = true;
      apiService(endpoint).then(data => {
        if (data) {
          this.totalCount = data.count;
          this.lessons.push(...data.results);
          this.loadingLessons = false;
          if (data.next) {
            this.next = data.next;
          } else {
            this.next = null;
            this.loadingLessons = false;
          }
        }
      });
    }
  },
  created() {
    this.getLessons();
  }
};
</script>
