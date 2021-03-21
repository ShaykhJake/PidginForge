<template>
  <v-dialog v-model="dialog" scrollable height="400">
    <v-card class="sandstone">
      <v-card-title>
        Add Vocab Pairs to Bank
      </v-card-title>
      <v-card-text class="px-2">
        <v-row wrap dense>
          <v-col cols="6">
            <v-card class="desertsand">
              <v-card-title>
                Source Term
              </v-card-title>
              <v-card-text>
                <v-autocomplete
                  v-model="l1Language"
                  name="l1language"
                  :items="allLanguages"
                  label="Source Language*"
                  placeholder="choose the L1 language"
                  :loading="loadingLanguages"
                  outlined
                  color="primary"
                  class="mt-2"
                  @change="loadL1WordList(l1Language)"
                >
                </v-autocomplete>

                <v-row
                  v-if="fetchingL1List"
                  align-content="center"
                  justify="center"
                  dense
                  no-gutters
                >
                  <v-col class="subtitle-1 text-center" cols="12">
                    ... retrieving word list for {{ l1Language }}...
                  </v-col>
                  <v-col cols="6">
                    <v-progress-linear
                      color="primary accent-4"
                      indeterminate
                      rounded
                      height="8"
                    ></v-progress-linear>
                  </v-col>
                </v-row>

                <v-row v-if="noL1Results && !showingL1WordList">
                  <v-col align="center">
                    <span class="overline"
                      >... no results (hint: add some) ...</span
                    >
                  </v-col>
                </v-row>

                <v-autocomplete
                  v-model="selectedL1Word"
                  v-if="showingL1WordList"
                  :items="l1WordList"
                  :loading="fetchingL1List"
                  outlined
                  :placeholder="
                    `${l1WordList.length} results for ${l1Language}`
                  "
                  color="primary"
                  :label="
                    `${l1Language} existing words in database (${l1WordList.length})`
                  "
                  item-text="word"
                  item-value="id"
                  @change="loadL1Details(selectedL1Word)"
                >
                  <template v-slot:item="data">
                    <template v-if="typeof data.item !== 'object'">
                      <v-list-item-content
                        v-text="data.item"
                      ></v-list-item-content>
                    </template>
                    <template v-else>
                      <v-list-item-content>
                        <v-list-item-title
                          v-html="data.item.word"
                        ></v-list-item-title>

                        <v-list-item-subtitle>
                          Language(s):
                          <v-chip small outlined class="languages">
                            {{ data.item.language }}
                          </v-chip>
                        </v-list-item-subtitle>

                        <v-list-item-subtitle
                          >Lexeme:
                          {{
                            data.item.lexeme ? data.item.lexeme.lemma : ""
                          }}</v-list-item-subtitle
                        >
                      </v-list-item-content>
                    </template>
                  </template>
                </v-autocomplete>

                <span v-if="showingL1WordList || noL1Results" class="overline"
                  >Don't like what you see?</span
                >
                <v-btn
                  small
                  v-if="showingL1WordList || noL1Results"
                  block
                  class="languages desertsand--text"
                  @click="newTerm1Dialog = true"
                  >Add New Term<v-icon right
                    >mdi-plus-box-outline</v-icon
                  ></v-btn
                >

                <AddNewTerm
                  v-if="newTerm1Dialog"
                  @closeDialog="newTerm1Dialog = false"
                  @pushNewTerm="selectNewTerm1"
                  :dialog="newTerm1Dialog"
                  :language="sourceLanguage"
                />
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="6">
            <v-card class="desertsand">
              <v-card-title>
                Target Term
              </v-card-title>
              <v-card-text>
                <v-row
                  v-if="loadingPairings"
                  align-content="center"
                  justify="center"
                  dense
                  no-gutters
                  class="my-5"
                >
                  <v-col class="subtitle-1 text-center" cols="12">
                    ... retrieving word pairings ...
                  </v-col>
                  <v-col cols="6">
                    <v-progress-linear
                      color="primary accent-4"
                      indeterminate
                      rounded
                      height="8"
                    ></v-progress-linear>
                  </v-col>
                </v-row>

                <v-autocomplete
                  v-if="
                    showingPairings && !loadingPairings && !loadingL1Details
                  "
                  v-model="selectedPairID"
                  name="currentpairings"
                  :items="currentPairings"
                  :label="`Current Pairings (${currentPairings.length})`"
                  placeholder="select a current pairing"
                  :loading="loadingPairings"
                  outlined
                  color="primary"
                  class="mt-4 mt-2"
                  item-text="word"
                  item-value="id"
                  @change="loadL2Details(selectedPairID)"
                >
                  <template v-slot:item="data">
                    <template v-if="typeof data.item !== 'object'">
                      <v-list-item-content
                        v-text="data.item"
                      ></v-list-item-content>
                    </template>
                    <template v-else>
                      <v-list-item-content>
                        <v-list-item-title
                          v-html="data.item.word"
                        ></v-list-item-title>

                        <v-list-item-subtitle>
                          Language(s):
                          <v-chip small outlined class="languages">
                            {{ data.item.language }}
                          </v-chip>
                        </v-list-item-subtitle>

                        <v-list-item-subtitle
                          >Lexeme:
                          {{
                            data.item.lexeme ? data.item.lexeme.lemma : ""
                          }}</v-list-item-subtitle
                        >

                        <v-list-item-subtitle>
                          Paired with your selected word
                          {{ data.item.count }} times...
                        </v-list-item-subtitle>
                      </v-list-item-content>
                    </template>
                  </template>
                </v-autocomplete>

                <v-btn
                  small
                  v-if="showingPairings"
                  block
                  class="topics desertsand--text mb-2"
                  @click="curateNewPairing"
                  >Add New Pairing
                  <v-icon right>mdi-plus-box-outline</v-icon></v-btn
                >

                <v-autocomplete
                  v-if="curatingNewPair"
                  v-model="l2Language"
                  name="l2language"
                  :items="allLanguages"
                  label="Target Language*"
                  placeholder="choose the L2 language"
                  :loading="loadingLanguages"
                  outlined
                  color="primary"
                  class="mt-4"
                  @change="loadL2WordList(l2Language)"
                >
                </v-autocomplete>

                <v-row
                  v-if="fetchingL2List"
                  align-content="center"
                  justify="center"
                  dense
                  no-gutters
                  class="mb-3"
                >
                  <v-col class="subtitle-1 text-center" cols="12">
                    ... retrieving word list for {{ l2Language }}...
                  </v-col>
                  <v-col cols="6">
                    <v-progress-linear
                      color="primary accent-4"
                      indeterminate
                      rounded
                      height="8"
                    ></v-progress-linear>
                  </v-col>
                </v-row>

                <v-row v-if="noL2Results && !showingL2WordList">
                  <v-col align="center">
                    <span class="overline"
                      >... no results (hint: add some) ...</span
                    >
                  </v-col>
                </v-row>

                <v-autocomplete
                  v-model="selectedL2Word"
                  v-if="showingL2WordList"
                  :items="l2WordList"
                  :loading="fetchingL2List"
                  outlined
                  :placeholder="
                    `${l2WordList.length} results for ${l2Language}`
                  "
                  color="primary"
                  :label="
                    `${l2Language} existing words in database (${l2WordList.length})`
                  "
                  item-text="word"
                  item-value="id"
                  @change="loadL2Details(selectedL2Word)"
                >
                  <template v-slot:item="data">
                    <template v-if="typeof data.item !== 'object'">
                      <v-list-item-content
                        v-text="data.item"
                      ></v-list-item-content>
                    </template>
                    <template v-else>
                      <v-list-item-content>
                        <v-list-item-title
                          v-html="data.item.word"
                        ></v-list-item-title>
                        <v-list-item-subtitle>
                          Language:
                          <v-chip small outlined class="languages">
                            {{ data.item.language }}
                          </v-chip>
                        </v-list-item-subtitle>

                        <v-list-item-subtitle
                          >Lexeme:
                          {{
                            data.item.lexeme ? data.item.lexeme.lemma : ""
                          }}</v-list-item-subtitle
                        >
                      </v-list-item-content>
                    </template>
                  </template>
                </v-autocomplete>
                <span v-if="showingL2WordList" class="overline"
                  >Don't like what you see?</span
                >
                <v-btn
                  small
                  v-if="showingL2WordList || noL2Results"
                  block
                  class="languages desertsand--text"
                  @click="newTerm2Dialog = true"
                  >Add New Term<v-icon right
                    >mdi-plus-box-outline</v-icon
                  ></v-btn
                >

                <AddNewTerm
                  v-if="newTerm2Dialog"
                  @closeDialog="newTerm2Dialog = false"
                  @pushNewTerm="selectNewTerm2"
                  :dialog="newTerm2Dialog"
                  :language="targetLanguage"
                />
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12">
            <v-card class="desertsand">
              <v-card-title>
                Selected Term Pair
              </v-card-title>

              <v-card-text>
                <v-row>
                  <v-col>
                    <v-row
                      v-if="loadingL1Details"
                      align-content="center"
                      justify="center"
                      dense
                      no-gutters
                      class="my-5"
                    >
                      <v-col cols="12" align="center">
                        <v-progress-circular
                          color="primary accent-4"
                          indeterminate
                          rounded
                          size="64"
                        ></v-progress-circular>
                      </v-col>
                    </v-row>

                    <v-card
                      class="sandstone mb-2"
                      v-if="l1Details.word && !loadingL1Details"
                    >
                      <v-card-title class="sandstone py-1">
                        Source
                      </v-card-title>
                      <v-card-text class="sandstone">
                        <h2>{{ l1Details.word }}</h2>
                        Curator: {{ l1Details.curator.username }}<br />
                        Date Created: {{ l1Details.curationdate }}<br />
                        Language(s):
                        <v-chip small outlined class="languages">
                          {{ l1Details.language }} </v-chip
                        ><br />
                        Lexeme:
                        {{ l1Details.lexeme ? l1Details.lexeme.lemma : ""
                        }}<br />
                        # of Definitions: {{ l1Details.definitions.length
                        }}<br />
                        # of Sentences: {{ l1Details.definitions.length }}<br />
                        # of Grammar Notes: {{ l1Details.grammars.length
                        }}<br />
                        # of Associated Pairs: {{ l1Details.word_pair_count
                        }}<br />
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col>
                    <v-row
                      v-if="loadingL2Details"
                      align-content="center"
                      justify="center"
                      dense
                      no-gutters
                      class="my-5"
                    >
                      <v-col cols="12" align="center">
                        <v-progress-circular
                          color="primary accent-4"
                          indeterminate
                          rounded
                          size="64"
                        ></v-progress-circular>
                      </v-col>
                    </v-row>

                    <v-card
                      class="sandstone mb-2"
                      v-if="
                        showingL2Details && l2Details.word && !loadingL2Details
                      "
                    >
                      <v-card-title class="sandstone py-1">
                        Target
                      </v-card-title>
                      <v-card-text class="sandstone">
                        <h2>{{ l2Details.word }}</h2>
                        Curator: {{ l2Details.curator.username }}<br />
                        Date Created: {{ l2Details.curationdate }}<br />
                        Language(s):
                        <v-chip small outlined class="languages">
                          {{ l2Details.language }} </v-chip
                        ><br />

                        Lexeme: {{ l2Details.lexeme.lemma }}<br />
                        # of Definitions: {{ l2Details.definitions.length
                        }}<br />
                        # of Sentences: {{ l2Details.definitions.length }}<br />
                        # of Grammar Notes: {{ l2Details.grammars.length
                        }}<br />
                        # of Associated Pairs: {{ l2Details.word_pair_count
                        }}<br />
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </v-card-text>
              <v-card-actions>
                <v-btn
                  small
                  :disabled="!showingL1Details || !showingL2Details"
                  block
                  class="primary desertsand--text"
                  @click="addPairToBank"
                  :loading="submittingNewPair"
                >
                  Add Pair to Bank <v-icon right>mdi-check</v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn class="garbage desertsand--text" @click="closeDialog">
          Close
        </v-btn>
        <v-spacer></v-spacer>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import AddNewTerm from "@/components/vocab/AddNewTerm.vue";
export default {
  name: "BankItemEditor",
  components: {
    AddNewTerm
  },
  props: {
    dialog: {
      type: Boolean,
      default: false
    },
    l1Word: {
      type: String,
      required: false
    },
    sourceLanguage: {
      type: String,
      required: false
    },
    targetLanguage: {
      type: String,
      required: false
    },
    vocabBankID: {
      type: Number
    }
  },
  data: () => ({
    fetchingL1List: false,
    fetchingL2List: false,
    selectedL1Word: null,
    selectedL2Word: null,
    l1WordList: [],
    l2WordList: [],
    l1Details: {},
    l2Details: {},
    addingPairing: false,
    hidingDetails: false,
    hidingL2Details: false,
    hidingPairs: false,

    newTerm1Dialog: false,
    newTerm2Dialog: false,

    curatingNewPair: false,
    showingTargetWord: false,
    submittingNewPair: false,
    selectedPairID: null,

    loadingPairings: false,
    showingPairings: false,
    currentPairings: [],

    loadingLanguages: false,
    allLanguages: [],
    l1Language: "",
    l2Language: "",
    noL1Results: false,
    noL2Results: false,
    loadingL1WordList: false,
    loadingL1Details: false,

    showingWordDetails: false,
    wordDetails: {},

    showingL1WordList: false,
    showingL1Details: false,

    loadingL2WordList: false,
    loadingL2Details: false,

    showingL2WordList: false,
    showingL2Details: false
  }),

  methods: {
    closeDialog() {
      this.$emit("closeDialog");
    },

    loadL1WordList(language) {
      this.selectedPairID = null;
      this.showingL1Details = false;
      this.l1Details = {};
      this.fetchingL1List = true;
      this.showingL1WordList = false;
      this.noL1Results = false;
      let endpoint = `/api/vocab/words/wordlist/?language=${language}`;
      let method = "GET";
      try {
        apiService(endpoint, method).then(data => {
          if (data) {
            console.log(data);
            this.l1WordList = data;
            if (this.l1WordList.length < 1) {
              this.noL1Results = true;
            } else {
              this.showingL1WordList = true;
            }
            this.fetchingL1List = false;
          } else {
            console.log("There was a major problem with the request.");
            // console.log(data.message);
            this.fetchingL1List = false;
          }
        });
      } catch (err) {
        console.log(err);
        this.fetchingL1List = false;
      }
    },
    selectNewTerm1(newTerm) {
      this.l1WordList.push(newTerm);
      this.selectedL1Word = newTerm.id;
      this.loadL1Details(newTerm.id);
    },
    selectNewTerm2(newTerm) {
      this.l2WordList.push(newTerm);
      this.selectedL2Word = newTerm.id;
      this.loadL2Details(newTerm.id);
    },
    curateNewPairing() {
      this.selectedPairID = null;
      this.l2details = null;
      this.curatingNewPair = true;
      console.log(this.selectedPairID);
      this.showingL2Details = false;
      this.l2Language = this.targetLanguage;
      this.loadL2WordList(this.targetLanguage);
    },
    loadL2WordList(language) {
      this.l2Details = {};
      this.fetchingL2List = true;
      this.showingL2WordList = false;
      this.showingL2Details = false;
      this.noL2Results = false;
      let endpoint = `/api/vocab/words/wordlist/?language=${language}`;
      let method = "GET";
      try {
        apiService(endpoint, method).then(data => {
          if (data) {
            console.log(data);
            this.l2WordList = data;
            if (this.l2WordList.length < 1) {
              this.noL2Results = true;
            } else {
              this.showingL2WordList = true;
            }
            this.fetchingL2List = false;
          } else {
            console.log("There was a major problem with the request.");
            // console.log(data.message);
            this.fetchingL2List = false;
          }
        });
      } catch (err) {
        console.log(err);
        this.fetchingL2List = false;
      }
    },
    loadL1Details(word) {
      this.showingL1Details = false;
      this.loadingL1Details = true;

      let endpoint = `/api/vocab/inflectedformz/${word}/`;
      let method = "GET";
      try {
        apiService(endpoint, method).then(data => {
          if (data) {
            console.log(data);
            this.l1Details = data;
            this.loadingL1Details = false;
            this.showingL1Details = true;
            this.loadPairings(word);
          } else {
            console.log("There was a major problem with the request.");
            // console.log(data.message);
            this.loadingL1Details = false;
          }
        });
      } catch (err) {
        console.log(err);
        this.loadingL1Details = false;
      }
    },
    loadPairings(word) {
      this.showingPairings = false;
      this.loadingPairings = true;
      this.showingL2Details = false;
      let endpoint = `/api/vocab/words/pairings/${word}/`;
      let method = "GET";
      try {
        apiService(endpoint, method).then(data => {
          if (data) {
            console.log(data);
            this.currentPairings = data;
            this.loadingPairings = false;
            this.showingPairings = true;
          } else {
            console.log("There was a major problem with the request.");
            // console.log(data.message);
            this.loadingPairings = false;
          }
        });
      } catch (err) {
        console.log(err);
        this.loadingPairings = false;
      }
    },

    loadL2Details(word) {
      this.showingL2Details = false;
      this.loadingL2Details = true;

      let endpoint = `/api/vocab/inflectedformz/${word}/`;
      let method = "GET";
      try {
        apiService(endpoint, method).then(data => {
          if (data) {
            console.log(data);
            this.l2Details = data;
            this.loadingL2Details = false;
            this.showingL2Details = true;
          } else {
            console.log("There was a major problem with the request.");
            // console.log(data.message);
            this.loadingL2Details = false;
            this.showingL2Details = false;
          }
        });
      } catch (err) {
        console.log(err);
        this.loadingL2Details = false;
        this.showingL2Details = false;
      }
    },

    getLanguages() {
      var localLanguages = localStorage.getItem("languages");
      if (localLanguages.length > 1) {
        console.log("Shop local!");
        this.allLanguages = JSON.parse(localLanguages);
        this.allLanguages.unshift("all");
      } else {
        this.loadingLanguages = true;
        let endpoint = `/api/categories/languages/`;
        try {
          apiService(endpoint).then(data => {
            if (data != null) {
              this.allLanguages = data;
              this.allLanguages.unshift("all");
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
    addNewPairing() {
      this.addingPairing = true;
      this.hidingDetails = true;
      this.hidingPairs = true;
      this.selectedPairID = null;
    },
    addPairToBank() {
      // First, send post data; create new pair if i doesn't exist already for user...
      // Then, add that pairing to the Vocab List for the exercise...
      this.submittingNewPair = true;

      let endpoint = `/api/vocab/addpair/`;
      let method = "POST";
      let payload = {
        vocab_bank: this.vocabBankID,
        inflected_form_1: this.l1Details.id,
        inflected_form_2: this.l2Details.id,
        curator_note: ""
      };
      try {
        apiService(endpoint, method, payload).then(data => {
          if (data) {
            console.log(data);
            this.$emit("addPair", data);
            this.submittingNewPair = false;
            // Emit the new Language Pair up to The Vocab Bank
            // Reset the Modal down to source language
            // Post a snack to say that the word was added...
          } else {
            console.log("There was a major problem with the request.");
            // console.log(data.message);
            this.submittingNewPair = false;
          }
        });
      } catch (err) {
        console.log(err);
        this.submittingNewPair = false;
      }
    },
    selectPair(pairID) {
      console.log(pairID);
    }
  },
  created() {
    this.getLanguages();
  },
  mounted() {
    if (this.sourceLanguage) {
      this.l1Language = this.sourceLanguage;
      this.loadL1WordList(this.sourceLanguage);
      this.l2Language = this.targetlanguage;
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
