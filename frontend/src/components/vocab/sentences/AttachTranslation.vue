<template>
  <v-dialog v-model="dialog" max-width="315" persistent>
    <v-card class="desertsand">
      <v-card-title class="sandstone">
        Attach Translation
      </v-card-title>
      <v-card-text class="px-2">
        <div
          class="sentenceBox title mb-2"
          :style="`direction:${sentence.direction}`"
        >
          {{ sentence.text }}
        </div>

        <v-form v-model="valid">
          <v-autocomplete
            v-model="language"
            :items="allLanguages"
            dense
            outlined
            color="primary"
            label="Translation Language(s)"
            item-text="name"
            item-value="name"
            :rules="[rules.requiredLanguage]"
          >
          </v-autocomplete>

          <div :style="translationRTL ? 'direction:rtl;' : ''">
            <v-textarea
              v-model="text"
              label="Translation Text"
              outlined
              :reverse="translationRTL"
              :rules="[rules.requiredTranslation]"
            ></v-textarea>
          </div>

          <div :style="translationRTL ? 'direction:rtl;' : ''">
            <v-textarea
              v-model="curator_note"
              label="Curator Note"
              outlined
              :reverse="translationRTL"
              :rules="[rules.requiredCuratorNote]"
            ></v-textarea>
          </div>
        </v-form>
      </v-card-text>
      <v-card-actions class="sandstone">
        <v-btn @click="closeDialog" class="garbage desertsand--text">
          Cancel
        </v-btn>
        <v-btn
          class="primary"
          :disabled="!valid"
          :loading="saving"
          @click="submit"
        >
          Submit
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "AttachTranslation",
  props: {
    sentence: Object,
    translation: Object,
    dialog: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    allLanguages: [],
    loadingLanguages: false,
    language: "",
    text: "",
    curator_note: "",
    valid: false,
    saving: false,
    rules: {
      requiredLanguage: value =>
        (value || "").length > 2 ||
        "The translation must be at least 3 characters in length.",

      requiredTranslation: value =>
        (value || "").length > 2 ||
        "The translation must be at least 3 characters in length.",

      requiredCuratorNote: value =>
        (value || "").length > 2 ||
        "The curator note must be at least 3 characters in length."
    }
  }),
  computed: {
    translationRTL() {
      if (this.language) {
        for (var i = 0; i < this.allLanguages.length; i += 1) {
          if (this.allLanguages[i].name === this.language) {
            console.log("found it");
            if (this.allLanguages[i].direction === "RTL") {
              return true;
            } else {
              return false;
            }
          }
        }
        return false;
      } else {
        return false;
      }
    }
  },
  components: {},
  methods: {
    closeDialog() {
      this.$emit("closeDialog");
    },
    submit() {
      this.saving = true;
      var endpoint = "";
      var method = "";
      if (this.translation.id) {
        endpoint = `/api/vocab/sentencetranslationz/${this.translation.id}/`;
        method = "PUT";
      } else {
        endpoint = `/api/vocab/sentencetranslationz/`;
        method = "POST";
      }
      const payload = {
        text: this.text,
        curator_note: this.curator_note,
        language: this.language,
        sentence: this.sentence.id
      };
      try {
        apiService(endpoint, method, payload).then(data => {
          if (data && data.id) {
            if (this.translation.id) {
              this.$emit("updateTranslation", data);
            } else {
              this.$emit("pushTranslation", data);
            }
            this.saving = false;
            this.closeDialog();
          } else {
            console.log(data || "no data");
            console.log("Something bad happened");
            this.saving = false;
          }
          this.saving = false;
        });
      } catch (err) {
        console.log(err);
        this.saving = false;
      }
    },
    getLanguages() {
      var localLanguagesFull = localStorage.getItem("languages_full");
      if (localLanguagesFull) {
        console.log("Shop local!");
        this.allLanguages = JSON.parse(localLanguagesFull);
      } else {
        this.loadingLanguages = true;
        let endpoint = `/api/categories/languages_full/`;
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
    }
  },
  mounted() {
    if (this.translation && this.translation.id) {
      this.language = this.translation.language;
      this.text = this.translation.text;
      this.curator_note = this.translation.curator_note;
    }
  },
  created() {
    this.getLanguages();
  }
};
</script>

<style scoped>
.sentenceBox {
  color: black;
  /* background-color: antiquewhite; */
  border-left-style: solid;
  border-right-style: solid;
  border-width: 1px;
  border-radius: 5px;
  border-color: grey;
  padding: 2px 2px 2px 2px;
  margin: 2px 2px 2px 2px;
}
</style>
