<template>
  <v-dialog v-model="dialog" scrollable height="400" max-width="425">
    <v-card class="desertsand">
      <v-card-title class="sandstone">
        Add {{ language }} Pairing for {{ lexeme_1.lemma }}
      </v-card-title>
      <v-card-text class="px-2">
        <v-form v-model="valid" class="mt-2">
          <h3 class="mb-2">Available {{ language }} Lexemes</h3>
          <v-autocomplete
            v-model="lexeme2"
            :disabled="fetchingLexeme2List"
            :items="lexeme2List"
            :label="`${language} Lexemes (${lexeme2List.length})`"
            :placeholder="`${lexeme2List.length} lexemes`"
            outlined
            color="blue-grey lighten-2"
            item-text="lemma"
            item-value="id"
            :loading="fetchingLexeme2List"
            hide-details
            class="mb-0 pb-0"
          >
            <template v-slot:item="data">
              <template v-if="typeof data.item !== 'object'">
                <v-list-item-content v-text="data.item"></v-list-item-content>
              </template>
              <template v-else>
                <v-list-item-content>
                  <v-list-item-title
                    v-html="data.item.lemma"
                  ></v-list-item-title>
                  <v-list-item-subtitle
                    >Curated by
                    {{ data.item.curator.username }}</v-list-item-subtitle
                  >
                  <v-list-item-subtitle
                    >0 Definitions; 0...; 0 Inflected
                    Forms</v-list-item-subtitle
                  >
                </v-list-item-content>
              </template>
            </template>
          </v-autocomplete>
          <div style="text-align: center;" class="mb-5">
            <span class="overline">Don't see what you want?</span><br />
            <v-btn small class="primary" @click="addLexemeDialog = true">
              Add New Lexeme
            </v-btn>
          </div>

          <v-textarea
            v-model="curator_note"
            label="Curator Note"
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
          :disabled="!lexeme2"
          @click="submitPair"
          :loading="submittingPair"
        >
          Submit Pair
        </v-btn>
        <v-spacer></v-spacer>
      </v-card-actions>
    </v-card>

    <QuickAddLexeme
      v-if="addLexemeDialog"
      :dialog="addLexemeDialog"
      :language="language"
      :direction="direction"
      @closeDialog="addLexemeDialog = false"
      @selectNewLexeme="selectNewLexeme2"
    />
  </v-dialog>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import QuickAddLexeme from "@/components/vocab/stacks/QuickAddLexeme.vue";

export default {
  name: "QuickAddPair",
  components: {
    QuickAddLexeme
  },
  props: {
    dialog: {
      type: Boolean,
      default: false
    },
    lexeme_1: Object,
    language: String,
    direction: String
  },
  data: () => ({
    valid: false,
    lemma: null,
    curator_note: null,
    lexeme2List: [],
    fetchingLexeme2List: false,
    lexeme2: null,
    submittingPair: false,
    addLexemeDialog: false,

    rules: {
      requiredLexeme: value =>
        (value || "").length > 0 || "You must choose a lexeme!",

      requiredNotes: value =>
        (value || "").length > 0 ||
        "Your must enter something, even it it's just 'n/a'!",

      maxNote: value =>
        (value || "").length < 201 ||
        "Your note must be shorter than 200 characters"
    }
  }),

  methods: {
    closeDialog() {
      this.$emit("closeDialog");
    },
    submitPair() {
      // console.log(this.lexeme_1.id, this.lexeme2)

      this.submittingLexeme = true;
      let endpoint = `/api/vocab/lexemepairz/`;
      let method = "POST";
      let payload = {
        curator_note: this.curator_note,
        lexeme_1: this.lexeme_1.id,
        lexeme_2: this.lexeme2
      };
      try {
        apiService(endpoint, method, payload).then(data => {
          if (data && data.id) {
            console.log(data);
            this.$emit("selectNewPair", data);
            this.closeDialog();
            this.submittingPair = false;
          } else {
            console.log("There was a major problem with the request.");
            // console.log(data.message);
            this.submittingPair = false;
          }
        });
      } catch (err) {
        console.log(err);
        this.submittingPair = false;
      }
    },

    selectNewLexeme2(lexeme) {
      this.lexeme2List.push(lexeme);
      console.log(lexeme);
      this.lexeme2 = lexeme.id;
    },

    loadLexeme2List(language) {
      //  this.showingLexemeList = false;
      this.fetchingLexeme2List = true;
      this.lexeme2 = "";
      this.lexeme2List = [];

      let endpoint = `/api/vocab/lexemes/lexemelist/?language=${language}`;
      let method = "GET";
      try {
        apiService(endpoint, method).then(data => {
          if (data) {
            console.log(data);
            this.lexeme2List = data;
            this.fetchingLexeme2List = false;
          } else {
            console.log("There was a major problem with the request.");
            // console.log(data.message);
            this.fetchingLexeme2List = false;
          }
        });
      } catch (err) {
        console.log(err);
        this.fetchingLexeme2List = false;
      }
    }
  },
  mounted() {
    if (this.language) {
      this.loadLexeme2List(this.language);
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
