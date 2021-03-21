<template>
  <div>
    <v-container fluid dense>
      <v-card v-if="stack.id">
        <v-card-title class="sandstone">
          Learn Stack: {{ stack.name }} ({{
            stack.lexeme_pairs ? stack.lexeme_pairs.length : 0
          }}
          Pairs)
        </v-card-title>
        <v-card-text class="desertsand">
          Stack Details:<br />
          Curator: {{ stack.curator ? stack.curator.username : "" }}<br />
          Created on: {{ stack.curationdate }}<br />
          Language Pair: {{ stack.learning_language }} ->
          {{ stack.native_language }}<br />
          # of Lexeme Pairs: {{ stack.lexeme_pairs.length }}<br />
          <br />
          <v-data-table
            :headers="headers"
            :items="stack.lexeme_pairs"
            class="elevation-1"
          >
            <template v-slot:item.lexeme_1_details.lemma="{ item }">
              <a @click.prevent="loadLexemeView(item.lexeme_1_details.slug)">
                <span class="subtitle-1">{{
                  item.lexeme_1_details.lemma
                }}</span>
              </a>
            </template>

            <template v-slot:item.lexeme_2_details.lemma="{ item }">
              <a @click.prevent="loadLexemeView(item.lexeme_2_details.slug)">
                <span class="subtitle-1">{{
                  item.lexeme_2_details.lemma
                }}</span>
              </a>
            </template>
          </v-data-table>
        </v-card-text>

        <v-card-actions class="sandstone">
          <v-spacer />
          <v-btn class="mr-2 desertsand" @click="simpleFlipDialog = true">
            Simple Flip
          </v-btn>
          <v-btn class="mr-2 desertsand" @click="multipleChoiceDialog = true">
            Multiple Choice
          </v-btn>
          <v-btn disabled class="mr-2 desertsand"> Mix & Match </v-btn><br />
          <v-btn disabled class="mr-2 desertsand"> Cloze </v-btn><br />
          <v-btn disabled class="mr-2 desertsand"> Speech </v-btn><br />
          <v-spacer />
        </v-card-actions>
      </v-card>
      <v-overlay :value="loadingStack" absolute>
        <v-progress-circular indeterminate size="64"></v-progress-circular>
      </v-overlay>
    </v-container>

    <SimpleFlip
      v-if="simpleFlipDialog"
      :dialog="simpleFlipDialog"
      :pairs="stack.lexeme_pairs"
      @closeDialog="simpleFlipDialog = false"
    />
    <MultipleChoice
      v-if="multipleChoiceDialog"
      :dialog="multipleChoiceDialog"
      :pairs="stack.lexeme_pairs"
      @closeDialog="multipleChoiceDialog = false"
      @correctAnswer="recordCorrectAnswer"
      @incorrectAnswer="recordIncorrectAnswer"
    />
    <!-- <MixAndMatch
        v-if="mixAndMatchDialog"
        :dialog="mixAndMatchDialog"
        :pairs="stack.lexeme_pairs"
        @closeDialog="mixAndMatchDialog = false"
        @correctAnswer="recordCorrectAnswer"
        @incorrectAnswer="recordIncorrectAnswer"
      /> -->

    <v-dialog
      v-model="viewLexemeDetails"
      v-if="viewLexemeDetails"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card class="sandstone">
        <v-toolbar class="sandstone">
          <v-btn icon @click="viewLexemeDetails = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title> Lexeme Viewer </v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <LexemeCurator :lexemeslug="lexemeViewSlug" />
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import SimpleFlip from "@/components/vocab/stacks/SimpleFlip.vue";
import MultipleChoice from "@/components/vocab/stacks/MultipleChoice.vue";
// import MixAndMatch from "@/components/vocab/stacks/MixAndMatch.vue";
import LexemeCurator from "@/components/vocab/LexemeCurator.vue";

export default {
  name: "LearnStack",
  components: {
    SimpleFlip,
    MultipleChoice,
    // MixAndMatch,
    LexemeCurator
  },
  props: {
    slug: String
  },
  data: () => ({
    simpleFlipDialog: false,
    loadingStack: true,
    multipleChoiceDialog: false,
    mixAndMatchDialog: false,
    viewLexemeDetails: false,
    lexemeViewSlug: null,
    headers: [
      {
        text: "Lexeme 1",
        align: "start",
        sortable: false,
        value: "lexeme_1_details.lemma"
      },
      { text: "Lexeme 2", value: "lexeme_2_details.lemma" },
      { text: "Attempts Correct", value: "pair_learning.number_correct" },
      { text: "Total Attempts", value: "pair_learning.attempts" },
      { text: "Last Attempt", value: "pair_learning.last_attempted" }
    ],
    search: "",
    selectedCard: null,
    cards: [],
    stack: {
      id: null
    }
  }),
  methods: {
    loadStack(slug) {
      this.loadingStack = true;
      let endpoint = `/api/vocab/learnstack/${slug}/`;
      let method = "GET";
      try {
        apiService(endpoint, method).then(data => {
          if (data) {
            // console.log(data);
            console.log(data);
            this.stack = data;
            this.loadingStack = false;
          } else {
            console.log("There was a major problem with the request.");
            // console.log(data.message);
            this.loadingStack = false;
          }
        });
      } catch (err) {
        console.log(err);
        this.loadingStack = false;
      }
    },
    recordCorrectAnswer(pair) {
      for (let x = 0; x < this.stack.lexeme_pairs.length; x++) {
        if (this.stack.lexeme_pairs[x].id == pair.id) {
          this.stack.lexeme_pairs[x].pair_learning.number_correct++;
          this.stack.lexeme_pairs[x].pair_learning.attempts++;
          break;
        }
      }
      console.log(this.stack.lexeme_pairs.indexOf(pair));
      let endpoint = `/api/vocab/lexemes/learning/correct/`;
      let method = "POST";

      let payload = {
        learning_pair_id: pair.pair_learning.id
      };

      try {
        apiService(endpoint, method, payload).then(data => {
          if (data) {
            // console.log(data);
            console.log(data.message);
          } else {
            console.log("Update Completed");
          }
        });
      } catch (err) {
        console.log(err);
      }

      //
    },
    loadLexemeView(slug) {
      console.log(slug);
      this.lexemeViewSlug = slug;
      this.viewLexemeDetails = true;
    },
    recordIncorrectAnswer(pair) {
      for (let x = 0; x < this.stack.lexeme_pairs.length; x++) {
        if (this.stack.lexeme_pairs[x].id == pair.id) {
          this.stack.lexeme_pairs[x].pair_learning.attempts++;
          break;
        }
      }
      let endpoint = `/api/vocab/lexemes/learning/incorrect/`;
      let method = "POST";
      let payload = {
        learning_pair_id: pair.pair_learning.id
      };

      try {
        apiService(endpoint, method, payload).then(data => {
          if (data) {
            // console.log(data);
            console.log(data.message);
          } else {
            console.log("Update Completed");
          }
        });
      } catch (err) {
        console.log(err);
      }

      //
    }
  },
  mounted() {
    this.loadStack(this.slug);
  }
};
</script>

<style></style>
