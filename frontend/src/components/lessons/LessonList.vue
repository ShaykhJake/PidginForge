<template>
  <div class="lessonlist">
    <v-row wrap dense v-if="!filteredCount && !loadingLessons">
      <v-col cols="12">
        <v-card>
          <v-card-text class="desertsand calligraphy--text">
            There are no lessons which match your language/topic
            preferences. You may need to update your profile to add learning
            languages and topics...or maybe we just don't have enough content
            yet!
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row wrap dense v-if="filteredCount">
      <v-col cols="12" v-for="lesson in filteredLessons" :key="lesson.id">
        <LessonMicro
          :lesson="lesson"
          :hidden="lesson.user_has_hidden"
          @hideLesson="lesson.user_has_hidden = !lesson.user_has_hidden"
        />
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
      lessons: [],
      loadingLessons: false,
      next: null
    };
  },
  props: {
    preferenceFilter: {
      required: false,
      default: false
    }
  },
  computed: {
    filteredLessons() {
      if (this.preferenceFilter) {
        return this.lessons.filter(lesson => {
          return !lesson.filtered;
        });
      } else {
        return this.lessons;
      }
    },
    filteredCount() {
      return this.filteredLessons.length;
    }
  },

  methods: {
    getLessons() {
      let endpoint = `/api/lessons/lessonz/`;
      if (this.next) {
        endpoint = this.next;
      }
      this.loadingLessons = true;
      apiService(endpoint).then(data => {
        if (data) {
          console.log(data)
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
