<template>
  <v-dialog v-model="dialog" scrollable height="400" max-width="425">
    <v-card class="desertsand">
      <v-card-title class="sandstone">
        Add New {{ language }} Lexeme
      </v-card-title>
      <v-card-text class="px-2">
        <v-form v-model="valid" class="mt-2">
          <div :style="`direction:${direction}`">
            <v-text-field
              label="New Lexeme"
              v-model="lemma"
              outlined
              :reverse="direction === 'RTL' ? true : false"
              :rules="[rules.requiredLemma]"
            ></v-text-field>
          </div>
          <v-textarea
            v-model="curator_note"
            label="Curator Notes"
            outlined
            :rules="[rules.requiredNotes, rules.maxNote]"
            counter
          ></v-textarea>
        </v-form>
      </v-card-text>
      <v-card-actions class="sandstone">
        <v-spacer></v-spacer>
        <v-btn class="garbage desertsand--text" @click="closeDialog">
          Cancel
        </v-btn>

        <v-btn
          class="primary"
          :disabled="!valid"
          @click="submitLexeme"
          :loading="submittingLexeme"
        >
          Submit
        </v-btn>
        <v-spacer></v-spacer>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { apiService } from "@/common/api.service.js";
export default {
  name: "QuickAddLexeme",
  props: {
    dialog: {
      type: Boolean,
      default: false
    },
    language: String,
    direction: String
  },
  data: () => ({
    valid: false,
    lemma: null,
    curator_note: "n/a",

    submittingLexeme: false,

    rules: {
      requiredLemma: value =>
        (value || "").length > 0 || "Your term must have at least one letter!",

      requiredNotes: value =>
        (value || "").length > 0 ||
        "Your must enter something, even it it's just 'n/a'!",

      maxNote: value =>
        (value || "").length < 201 ||
        "Your note must be shorter than 200 characters"
    }
  }),
  components: {},
  methods: {
    closeDialog() {
      this.$emit("closeDialog");
    },
    submitLexeme() {
      this.submittingLexeme = true;
      let endpoint = `/api/vocab/lexemez/`;
      let method = "POST";
      let payload = {
        language: this.language,
        lemma: this.lemma,
        curator_note: this.curator_note
      };
      try {
        apiService(endpoint, method, payload).then(data => {
          if (data && data.id) {
            // console.log(data);
            this.$emit("selectNewLexeme", data);
            this.closeDialog();
            this.submittingLexeme = false;
          } else {
            console.log("There was a major problem with the request.");
            // console.log(data.message);
            this.submittingLexeme = false;
          }
        });
      } catch (err) {
        console.log(err);
        this.submittingLexeme = false;
      }
    }
  }
};
</script>

<style>
.multilingual {
  border-style: solid;
  border-width: 1px;
  border-color: black;
  padding: 2px 2px 2px 2px;
  border-radius: 10px;
}
</style>
