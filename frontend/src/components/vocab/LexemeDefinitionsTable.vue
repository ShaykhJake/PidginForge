<template>
  <div>
    <v-row dense>
      <v-col class="pl-2" cols="6">
        <span class="body-1 font-weight-black">
          Definitions ({{ definitions.length }})
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
          >Add Definition
        </v-btn>
      </v-col>
    </v-row>

    <div class="mx-1" v-show="showList">
      <v-row
        v-for="(item, index) in definitions"
        :key="index"
        flat
        class="mb-1 desertsand"
        dense
        align="center"
      >
        <v-col class="body-1">
          <div :style="`direction: ${item.direction}`" class="overline mt-1">
            {{ item.part_of_speech }}
          </div>
          <div :style="`direction: ${item.direction}`" class="roundBox">
            {{ item.content }}
          </div>
          <div class="overline mt-1">
            <v-chip x-small class="languages languages--text mr-1" outlined>
              {{ item.language }}
            </v-chip>
            Curated by
            <span class="primary--text font-weight-black">
              {{ item.curator.username }}
            </span>
            on {{ item.curationdate }}<br />
            <span class="overline font-italic"
              >Source: {{ item.source_name }}, {{ item.source_citation }}</span
            >
          </div>
        </v-col>
        <v-col cols="1" align="right">
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
      </v-row>
      <v-overlay absolute :value="loadingDefinitions">
        <v-progress-circular
          color="primary"
          indeterminate
          size="48"
        ></v-progress-circular>
      </v-overlay>
    </div>

    <v-dialog v-model="itemEditorDialog" max-width="500px">
      <v-card class="desertsand">
        <v-card-title class="sandstone">
          <span class="headline">{{ formTitle }}</span>
        </v-card-title>

        <v-card-text>
          <v-container>
            <p class="overline">
              Choose the language for the <strong>definition text</strong>.
            </p>
            <v-form v-model="valid">
              <v-autocomplete
                v-model="editedItem.language"
                :items="allLanguages"
                dense
                outlined
                color="primary"
                label="Word/Term Language(s)"
                item-text="name"
                item-value="name"
                :rules="[rules.requiredLanguage]"
              >
              </v-autocomplete>

              <div :style="termRTL ? 'direction:rtl;' : ''">
                <v-text-field
                  v-model="editedItem.part_of_speech"
                  label="Part of Speech"
                  outlined
                  :reverse="termRTL"
                  :rules="[rules.requiredPOS]"
                ></v-text-field>
              </div>

              <div :style="termRTL ? 'direction:rtl;' : ''">
                <v-textarea
                  v-model="editedItem.content"
                  label="Definition Text"
                  outlined
                  :reverse="termRTL"
                  :rules="[rules.requiredDefinition]"
                ></v-textarea>
              </div>

              <h3>Source Citation (optional)</h3>
              <v-text-field
                v-model="editedItem.source_name"
                label="Source Short Name"
                outlined
                hint="e.g. 'Hans Wehr', 'Websters', etc"
                persistent-hint
              ></v-text-field>

              <v-textarea
                v-model="editedItem.source_citation"
                label="Source Full Citation"
                outlined
                hint="e.g. 'Hans Wehr Dictionary of Modern Written Arabic, 4th Edition'"
                persistent-hint
              ></v-textarea>
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

export default {
  name: "LexemeDefinitionsTable",
  components: {},
  props: {
    lexemeslug: String
  },
  data: () => ({
    definitions: [],
    allLanguages: [],

    showList: true,
    itemEditorDialog: false,

    loadingDefinitions: false,
    deleting: false,
    saving: false,

    valid: false,

    returnCommand: function() {},
    headers: [
      {
        text: "Definition Language",
        align: "start",
        value: "language"
      },
      { text: "Curator", value: "curator.username" },
      { text: "Date Added", value: "curationdate" },
      { text: "P.O.S.", value: "part_of_speech" },
      { text: "Source", value: "source_name" },
      { text: "Actions", value: "actions", sortable: false }
    ],
    rules: {
      requiredLanguage: value => !!value || "Must select a language.",

      requiredDefinition: value =>
        (value || "").length > 4 ||
        "The definition must be at least 5 characters in length.",

      requiredPOS: value =>
        (value || "").length > 1 ||
        "The part of speech must be at least 2 characters in length."
    },

    editedIndex: -1,
    editedItem: {
      language: "English",
      content: "",
      part_of_speech: "",
      source_name: "n/a",
      source_citation: "n/a"
    },
    defaultItem: {
      language: "English",
      content: "",
      part_of_speech: "",
      source_name: "n/a",
      source_citation: "n/a"
    }
  }),

  computed: {
    requestUser() {
      return localStorage.getItem("username");
    },
    formTitle() {
      return this.editedIndex === -1 ? "Add Definition" : "Edit Definition";
    },
    termRTL() {
      if (this.editedItem.language) {
        for (var i = 0; i < this.allLanguages.length; i += 1) {
          if (this.allLanguages[i].name === this.editedItem.language) {
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

  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  mounted() {
    this.loadDefinitions(this.lexemeslug);
  },
  created() {
    this.getLanguages();
  },

  methods: {
    addDefinition(command, newLexeme) {
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

    loadDefinitions(lexemeslug) {
      this.loadingDefinitions = true;

      let endpoint = `/api/vocab/lexemes/definitionlist/${lexemeslug}/`;
      let method = "GET";
      try {
        apiService(endpoint, method).then(data => {
          if (data) {
            console.log(data);
            this.definitions = data;
            this.loadingDefinitions = false;
          } else {
            console.log("There was a major problem with the request.");
            // console.log(data.message);
            this.loadingDefinitions = false;
          }
        });
      } catch (err) {
        console.log(err);
        this.loadingDefinitions = false;
      }
    },

    editItem(item) {
      this.editedIndex = this.definitions.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.itemEditorDialog = true;
    },

    deleteItem(item) {
      const index = this.definitions.indexOf(item);
      if (confirm("Are you sure you want to remove this definition?")) {
        let endpoint = `/api/vocab/lexemedefinitionz/${item.id}/`;
        let method = "DELETE";
        try {
          apiService(endpoint, method).then(() => {
            this.definitions.splice(index, 1);
            this.deleting = false;
          });
        } catch (err) {
          console.log(err);
          this.deleting = false;
        }
      }
      // Sent DELETE message to API to fully remove...
    },
    //  deletePair(pairID){
    //      let endpoint = `/api/vocab/inflectedpairz/${pairID}`;
    //      let method = "DELETE";
    //      try {
    //        apiService(endpoint, method).then(data => {
    //            if (data){
    //              console.log(data);
    //            } else {
    //              console.log("There was a major problem with the request.");
    //            }
    //        });
    //      } catch (err) {
    //        console.log(err);
    //      }

    //  },
    submitNew(item) {
      this.saving = true;
      let endpoint = `/api/vocab/lexemedefinitionz/`;
      let method = "POST";
      let payload = {
        lexeme: this.lexemeslug,
        language: item.language,
        content: item.content,
        part_of_speech: item.part_of_speech,
        source_name: item.source_name,
        source_citation: item.source_citation
      };
      try {
        apiService(endpoint, method, payload).then(data => {
          if (data && data.id) {
            console.log(data);
            this.definitions.push(data);
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
      let endpoint = `/api/vocab/lexemedefinitionz/${item.id}/`;
      let method = "PUT";
      let payload = {
        lexeme: this.lexemeslug,
        language: item.language,
        content: item.content,
        part_of_speech: item.part_of_speech,
        source_name: item.source_name,
        source_citation: item.source_citation
      };
      try {
        apiService(endpoint, method, payload).then(data => {
          if (data && data.id) {
            console.log(data);

            Object.assign(this.definitions[this.editedIndex], this.editedItem);

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
</style>
