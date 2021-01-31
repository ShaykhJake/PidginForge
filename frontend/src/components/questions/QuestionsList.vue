<template>
  <div class="questionlist">
    <v-row wrap dense v-if="!filteredCount && !loadingQuestions">
      <v-col cols="12">
        <v-card>
          <v-card-text class="desertsand calligraphy--text">
            There are no questions which match your language/topic preferences.
            You may need to update your profile to add learning languages and
            topics...or maybe we just don't have enough content yet!
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row dense wrap v-if="filteredQuestions">
      <v-col cols="12"  sm="6" md="4" lg="3" v-for="question in filteredQuestions" :key="question.id">
        <QuestionMicro :question="question" />
      </v-col>
    </v-row>
    <v-btn
      v-show="next || loadingQuestions"
      @click="getQuestions"
      :loading="loadingQuestions"
      class="primary desertsand--text"
      block
    >
      Load More Questions <v-icon right>mdi-chevron-down</v-icon>
    </v-btn>
    <v-overlay :value="loadingQuestions" absolute>
      <v-progress-circular indeterminate size="64"></v-progress-circular>
    </v-overlay>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import QuestionMicro from "@/components/questions/QuestionMicro.vue";
export default {
  name: "QuestionsList",
  data() {
    return {
      questions: [],
      next: null,
      loadingQuestions: false
    };
  },
  components: {
    QuestionMicro
  },
  props: {
    preferenceFilter: {
      required: false,
      default: false
    }
  },
  computed: {
    filteredQuestions() {
      if (this.preferenceFilter) {
        return this.questions.filter(question => {
          return !question.filtered;
        });
      } else {
        return this.questions;
      }
    },
    filteredCount() {
      return this.filteredQuestions.length;
    }
  },

  methods: {
    getQuestions() {
      let endpoint = "/api/questions/";
      if (this.next) {
        endpoint = this.next;
      }
      this.loadingQuestions = true;
      apiService(endpoint).then(data => {
        this.questions.push(...data.results);
        this.loadingQuestions = false;
        if (data.next) {
          this.next = data.next;
        } else {
          this.next = null;
        }
      });
    }
  },
  created() {
    this.getQuestions();
  }
};
</script>
<style scoped>
.question-author {
  font-weight: bold;
  color: maroon;
}
.question-link {
  font-weight: bold;
  color: black;
}
.question-link:hover {
  font-weight: bold;
  color: gray;
  text-decoration: none;
}
</style>
