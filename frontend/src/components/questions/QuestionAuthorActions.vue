<template>
  <div class="question-actions">
    <v-btn
      small
      @click="loadQuestionEditor"
      v-if="!deleteConfirm"
      class="primary desertsand--text mr-1"
      >Edit<v-icon right>mdi-pencil</v-icon></v-btn
    >
    <v-btn
      small
      class="garbage desertsand--text"
      v-if="!deleteConfirm"
      @click="deleteConfirm = true"
    >
      Delete<v-icon right>mdi-delete</v-icon>
    </v-btn>

    <v-btn
      small
      @click="deleteQuestion"
      v-if="deleteConfirm"
      class="success desertsand--text mr-1"
    >
      Confirm Delete <v-icon right>mdi-delete</v-icon>
    </v-btn>
    <v-btn
      small
      @click="deleteConfirm = false"
      v-if="deleteConfirm"
      class="mr-1 garbage desertsand--text"
    >
      Cancel Delete<v-icon right>mdi-cancel</v-icon>
    </v-btn>

    <QuestionEditor
      v-if="questionEditorLoaded"
      :editor-dialog="showQuestionEditor"
      :slug="slug"
      :question="question"
      :editing="true"
      @closeDialog="showQuestionEditor = false"
      @updateQuestion="updateQuestion"
    />
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "QuestionAuthorActions",
  props: {
    // question: Object,
    question: {
      type: Object,
      required: true
    },
    slug: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      deleteConfirm: false,
      askQuestionDialog: false,
      questionEditorLoaded: false,
      showQuestionEditor: false
    };
  },
  components: {
    QuestionEditor: () =>
      import(
        /* webpackPrefetch: true */ "@/components/questions/QuestionEditor.vue"
      )
  },

  methods: {
    loadQuestionEditor() {
      this.questionEditorLoaded = true;
      this.showQuestionEditor = !this.showQuestionEditor;
    },
    updateQuestion(data) {
      this.$emit("updateQuestion", data);
    },
    async deleteQuestion() {
      this.deleteConfirm = false;
      let endpoint = `/api/questions/${this.slug}/`;
      try {
        await apiService(endpoint, "DELETE");
        this.$router.push("/");
      } catch (err) {
        // console.log(err);
      }
    }
  }
};
</script>
