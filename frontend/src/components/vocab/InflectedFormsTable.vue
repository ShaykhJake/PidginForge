<template>
  <div>
    <v-row dense>
      <v-col class="pl-2" cols="6">
        <span class="body-1 font-weight-black">
          Inflected Forms ({{ words.length }})
        </span>
        <v-btn icon small @click="showList = !showList">
          <v-icon class="primary--text" v-if="showList">
            mdi-chevron-up
          </v-icon>
          <v-icon class="primary--text" v-else>
            mdi-chevron-down
          </v-icon>
        </v-btn>
      </v-col>
      <v-col cols="6" align="right">
        <v-btn
          small
          color="primary"
          dark
          class="mr-2"
          @click="itemEditorDialog = true"
          >Add Word/Term
        </v-btn>
      </v-col>
    </v-row>

    <div class="mx-1" v-show="showList">
      <v-row
        v-for="(item, index) in words"
        :key="index"
        flat
        class="mb-1 desertsand"
        dense
      >
        <v-col class="body-1">
          <a
            @click="
              expandedItemID === index
                ? (expandedItemID = null)
                : (expandedItemID = index)
            "
          >
            <div :style="`direction: ${item.direction}`" class="roundBox">
              <span class="title">{{ item.word }}</span>
            </div>
          </a>
          <div class="overline">
            Curated by
            <span class="primary--text font-weight-black">
              {{ item.curator.username }}
            </span>
            on {{ item.curationdate }}
          </div>
        </v-col>
        <v-col cols="2" align="center">
          <v-btn
            icon
            small
            @click="
              expandedItemID === index
                ? (expandedItemID = null)
                : (expandedItemID = index)
            "
          >
            <v-icon class="primary--text" v-if="index === expandedItemID">
              mdi-chevron-up
            </v-icon>
            <v-icon class="primary--text" v-else>
              mdi-chevron-down
            </v-icon>
          </v-btn>

          <v-icon
            small
            @click="editItem(item)"
            v-if="requestUser === item.curator.username"
          >
            mdi-eye-on
          </v-icon>
          <v-icon
            small
            @click="editItem(item)"
            v-if="requestUser === item.curator.username"
          >
            mdi-pencil
          </v-icon>
          <v-icon
            small
            @click="deleteItem(item)"
            :loading="deleting"
            v-if="requestUser === item.curator.username"
          >
            mdi-delete
          </v-icon>
        </v-col>
        <v-col cols="12" v-show="index === expandedItemID">
          <div class="listBox ml-5">
            <InflectedFormsTableItem :word="item" />
          </div>
        </v-col>
      </v-row>
      <v-overlay absolute :value="loadingWords">
        <v-progress-circular
          color="primary"
          indeterminate
          size="48"
        ></v-progress-circular>
      </v-overlay>
    </div>

    <v-dialog
      v-model="itemEditorDialog"
      v-if="itemEditorDialog"
      max-width="500px"
    >
      <v-card class="desertsand">
        <v-card-title class="sandstone">
          <span class="headline">{{ formTitle }}</span>
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-form v-model="valid">
              <div :style="termRTL ? 'direction:rtl;' : ''">
                <v-text-field
                  v-model="editedItem.word"
                  label="Word/Term Text"
                  outlined
                  :reverse="termRTL"
                  :rules="[rules.requiredWord]"
                  class="title"
                ></v-text-field>
              </div>

              <div>
                <v-textarea
                  v-model="editedItem.curator_note"
                  label="Curator Note*"
                  outlined
                  :rules="[rules.requiredCuratorNote]"
                ></v-textarea>
              </div>
            </v-form>
          </v-container>
        </v-card-text>

        <v-card-actions class="sandstone">
          <v-spacer></v-spacer>
          <v-btn color="garbage desertsand--text" @click="close">Cancel</v-btn>
          <v-btn color="primary" :disabled="!valid" @click="save">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import InflectedFormsTableItem from "@/components/vocab/InflectedFormsTableItem.vue";

export default {
  name: "InflectedFormsTable",
  components: {
    InflectedFormsTableItem
  },
  props: {
    lexemeslug: String,
    lexemelanguage: String
  },
  data: () => ({
    words: [],
    allLanguages: [],
    itemEditorDialog: false,
    loadingWords: false,
    deleting: false,
    saving: false,
    expandedItemID: null,
    valid: false,
    showList: true,

    returnCommand: function() {},
    headers: [
      {
        text: "Word/Term",
        align: "start",
        value: "word"
      },
      { text: "Curator", value: "curator.username" },
      { text: "Date Added", value: "curationdate" },

      { text: "# Definitions", value: "definitions.length" },
      { text: "# Sentences", value: "sentences.length" },
      { text: "# Pronunciations", value: "sentences.length" },
      { text: "# Word Pairs", value: "word_pair_count" },
      { text: "Actions", value: "actions", sortable: false }
    ],
    rules: {
      requiredWord: value =>
        (value || "").length > 0 ||
        "Word must be at least 1 character in length.",

      requiredCuratorNote: value =>
        (value || "").length > 2 ||
        "The curator note must be at least 3 characters in length."
    },

    editedIndex: -1,
    editedItem: {
      word: "",
      curator_note: "n/a"
    },
    defaultItem: {
      word: "",
      curator_note: "n/a"
    }
  }),

  computed: {
    requestUser() {
      return localStorage.getItem("username");
    },
    formTitle() {
      return this.editedIndex === -1
        ? "Add Inflected Word/Term"
        : "Edit Inflected Word/Term";
    },

    termRTL() {
      if (this.lexemelanguage) {
        for (var i = 0; i < this.allLanguages.length; i += 1) {
          if (this.allLanguages[i].name === this.lexemelanguage) {
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

  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  mounted() {
    this.loadWords(this.lexemeslug);
  },
  created() {
    this.getLanguages();
  },

  methods: {
    addWord(command, newLexeme) {
      this.dialog = true;
      this.returnCommand = command;
      this.editedItem = {
        lexeme: newLexeme.lexeme,
        translation: "",
        partofspeech: "",
        root: "",
        context: ""
      };
    },

    loadWords(lexemeslug) {
      this.loadingWords = true;

      let endpoint = `/api/vocab/lexemes/wordlist/${lexemeslug}/`;
      let method = "GET";
      try {
        apiService(endpoint, method).then(data => {
          if (data) {
            console.log(data);
            this.words = data;
            this.loadingWords = false;
          } else {
            console.log("There was a major problem with the request.");
            // console.log(data.message);
            this.loadingWords = false;
          }
        });
      } catch (err) {
        console.log(err);
        this.loadingWords = false;
      }
    },

    editItem(item) {
      this.editedIndex = this.words.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.itemEditorDialog = true;
    },

    deleteItem(item) {
      const index = this.words.indexOf(item);
      if (confirm("Are you sure you want to remove this word?")) {
        let endpoint = `/api/vocab/inflectedformz/${item.id}/`;
        let method = "DELETE";
        try {
          apiService(endpoint, method).then(() => {
            this.words.splice(index, 1);
            this.deleting = false;
          });
        } catch (err) {
          console.log(err);
          this.deleting = false;
        }
      }
      // Sent DELETE message to API to fully remove...
    },

    submitNew(item) {
      this.saving = true;
      let endpoint = `/api/vocab/inflectedformz/`;
      let method = "POST";
      let payload = {
        lexemeslug: this.lexemeslug,
        language: this.lexemelanguage,
        word: item.word,
        curator_note: item.curator_note
      };
      try {
        apiService(endpoint, method, payload).then(data => {
          if (data && data.id) {
            console.log(data);
            this.words.push(data);
            this.saving = false;
            this.close();
          } else {
            console.log("There was a major problem with the request.");
            // console.log(data.message);
            this.saving = false;
          }
        });
      } catch (err) {
        console.log(err);
        this.saving = false;
      }
    },
    submitSave(item) {
      this.saving = true;
      let endpoint = `/api/vocab/inflectedformz/${item.id}/`;
      let method = "PUT";
      let payload = {
        lexeme: this.lexemeslug,
        language: this.lexemelanguage,
        word: item.word,
        curator_note: item.curator_note
      };
      try {
        apiService(endpoint, method, payload).then(data => {
          if (data && data.id) {
            console.log(data);

            Object.assign(this.words[this.editedIndex], this.editedItem);

            this.saving = false;
            this.close();
          } else {
            console.log("There was a major problem with the request.");
            // console.log(data.message);
            this.saving = false;
          }
        });
      } catch (err) {
        console.log(err);
        this.saving = false;
      }
    },
    close() {
      this.itemEditorDialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    save() {
      if (this.editedIndex > -1) {
        this.submitSave(this.editedItem);
      } else {
        this.submitNew(this.editedItem);
      }
      if (this.returnCommand) {
        console.log(this.returnCommand);
        //   let lexemePackage = {
        //     editedItem: this.editedItem,
        //     returnCommand: this.returnCommand
        //   };
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
  }
};
</script>

<style scoped>
.dropbox {
  height: 150px;
  overflow: auto;
  resize: vertical;
}

.roundBox {
  color: black;
  background-color: antiquewhite;
  border-left-style: solid;
  border-right-style: solid;
  border-width: 1px;
  border-radius: 5px;
  border-color: grey;
  padding: 2px 2px 2px 2px;
}

.listBox {
  color: black;
  background-color: beige;
  border-style: solid;
  border-width: 1px;
  border-radius: 5px;
  border-color: grey;
  padding: 2px 2px 2px 2px;
}
</style>
