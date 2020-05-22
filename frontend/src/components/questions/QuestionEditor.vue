<template>
  <v-row justify="center" class="ma-0">
    <v-dialog
      v-model="editorDialog"
      scrollable
      persistent
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card
        :loading="loadingLanguages || loadingQuestion || loadingTopics"
        class="desertsand"
      >
        <v-card-title v-if="editing">Edit Your Language Question</v-card-title>
        <v-card-title v-else>Ask a Language Question</v-card-title>
        <v-card-text>
          <v-form ref="questioncontent" v-model="valid" class="mt-2">
            <v-textarea
              v-model="content"
              outlined
              label="Question Content*"
              :rules="[rules.contentMin]"
              counter
              rows="4"
              maxlength="240"
            ></v-textarea>

            <v-select
              v-model="nativelanguage"
              :items="allLanguages"
              label="Native Language*"
              placeholder="choose the native language"
              :rules="[rules.requiredLanguage]"
              required
              outlined
            ></v-select>

            <v-select
              v-model="learninglanguage"
              :items="allLanguages"
              :loading="loadingLanguages"
              label="Learning Language*"
              placeholder="choose the learning language"
              :rules="[rules.requiredLanguage]"
              required
              outlined
            ></v-select>

            <v-select
              v-model="topic"
              :items="allTopics"
              label="Primary Topic*"
              :loading="loadingTopics"
              placeholder="choose a topic"
              :rules="[rules.requiredTopic]"
              required
              outlined
            ></v-select>

            <v-combobox
              label="Additional Topic Tags"
              v-model="tags"
              chips
              clearable
              hint="Hit <enter> or <tab> after each entry (max of 5 tags allowed)"
              persistent-hint
              multiple
              :rules="[rules.maxTags]"
              outlined
              counter
            >
              <template v-slot:selection="{ attrs, item, select, selected }">
                <v-chip
                  v-bind="attrs"
                  :input-value="selected"
                  close
                  @click="select"
                  @click:close="removeTag(item)"
                  class="calligraphy desertsand--text"
                >
                  <strong>{{ item }}</strong
                  >&nbsp;
                </v-chip>
              </template>
            </v-combobox>
          </v-form>
          <p v-if="error" class="muted mt-2">{{ error }}</p>
        </v-card-text>
        <v-card-actions class="calligraphy desertsand--text" justify="center">
          <v-spacer></v-spacer>
          <v-btn class="garbage desertsand--text" @click="closeDialog"
            >Cancel<v-icon right>mdi-close</v-icon></v-btn
          >
          <v-btn
            @click="onSubmit"
            class="green desertsand--text"
            :disabled="!valid"
            :loading="submitting"
            :hidden="submitted"
            >Submit<v-icon right>mdi-send</v-icon></v-btn
          >
          <v-btn class="success desertsand--text" :hidden="!submitted"
            >Success<v-icon right>mdi-thumb-up</v-icon></v-btn
          >
          <!-- TODO: need to ensure that the user information is reloaded after saving -->
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "QuestionEditor",
  props: {
    editing: {
      type: Boolean,
      default: false
    },
    slug: {
      type: String,
      required: false
    },
    question: {
      type: Object,
      required: false
    },
    editorDialog: {
      default: false
    }
  },
  data() {
    return {
      submitting: false,
      submitted: false,
      valid: false,
      loadingQuestion: false,
      loadingLanguages: false,
      loadingTopics: false,
      error: null,
      author: "",
      content: "",
      nativelanguage: "",
      learninglanguage: "",
      topic: "",
      allLanguages: [],
      allTopics: [],
      tags: [],
      rules: {
        contentMin: value =>
          (value || "").length > 15 || "You must type at least 16 characters!",
        // contentMax: value => (value || '').length < 241 || "No more than 240 characters!",
        requiredLanguage: value =>
          !!value || "You must choose at least 1 language.",
        requiredTopic: value => !!value || "You must choose a primary topic.",
        maxTags: value =>
          (value || "").length < 6 || "Maximum of 5 tags allowed!"
      }
    };
  },
  methods: {
    closeDialog() {
      this.$emit("closeDialog");
    },
    onSubmit() {
      this.submitting = true;
      let endpoint = "/api/questions/";
      let method = "POST";
      if (this.slug !== undefined) {
        endpoint += `${this.slug}/`;
        method = "PATCH";
      }
      let payload = {
        content: this.content,
        nativelanguage: this.nativelanguage,
        learninglanguage: this.learninglanguage,
        topic: this.topic,
        tags: []
      };
      console.log(payload);
      apiService(endpoint, method, payload).then(data => {
        if (this.editing === true) {
          this.$emit("updateQuestion", payload);
          this.$emit("closeDialog");
          this.submitting = false;
        } else {
          this.submitted = true;
          this.$router.push({
            name: "Question-Viewer",
            params: { slug: data.slug }
          });
        }
      });
    },
    removeTag(item) {
      this.tags.splice(this.tags.indexOf(item), 1);
      this.tags = [...this.tags];
    },
    getLanguages() {
      var localLanguages = localStorage.getItem("languages");
      if (localLanguages.length > 1) {
        console.log("Shop local!");
        this.allLanguages = JSON.parse(localLanguages);
      } else {
        this.loadingLanguages = true;
        let endpoint = `/api/categories/languages/`;
        try {
          apiService(endpoint).then(data => {
            if (data != null) {
              this.allLanguages = data;
              this.error = false;
            } else {
              console.log("Something bad happened...");
              this.error = true;
            }
            this.loadingLanguages = false;
          });
        } catch (err) {
          console.log(err);
        }
      }
    },

    getTopics() {
      var localTopics = localStorage.getItem("topics");
      if (localTopics.length > 1) {
        console.log("Shop local!");
        this.allTopics = JSON.parse(localTopics);
      } else {
        this.loadingTopics = true;
        let endpoint = `/api/categories/topics/`;
        try {
          apiService(endpoint).then(data => {
            if (data != null) {
              this.allTopics = data;
              this.error = false;
            } else {
              console.log("Something bad happened...");
              this.error = true;
            }
            this.loadingTopics = false;
          });
        } catch (err) {
          console.log(err);
        }
      }
    },
    getQuestionData() {
      if (this.editing) {
        (this.author = this.question.author),
          (this.content = this.question.content),
          (this.nativelanguage = this.question.nativelanguage),
          (this.learninglanguage = this.question.learninglanguage),
          (this.topic = this.question.topic),
          (this.tags = this.question.tags);
        this.loadingQuestion = false;
      }
    },
    getQuestionData2() {
      if (this.editing) {
        this.loadingQuestion = true;
        let endpoint = `/api/questions/${this.slug}/`;
        apiService(endpoint).then(data => {
          if (data) {
            (this.author = data.author),
              (this.content = data.content),
              (this.nativelanguage = data.nativelanguage),
              (this.learninglanguage = data.learninglanguage),
              (this.topic = data.topic),
              (this.tags = data.tags);
            this.loadingQuestion = false;
          } else {
            this.question = null;
            this.setPageTitle("404 - Page Note Found");
            this.loadingQuestion = false;
          }
        });
      }
    }
  },
  created() {
    this.getQuestionData();
    this.getLanguages();
    this.getTopics();
  }
};
</script>
<style scoped></style>
