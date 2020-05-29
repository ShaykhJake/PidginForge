<template>
  <div>

  <v-data-table
    :headers="headers"
    :items="words"
    multi-sort
    :sort-by="['language', 'curationdate']"
    :sort-desc="[false, true]"
    class="desertsand"
    show-expand
    :loading="loadingWords"
    loading-text="...fetching lexeme defintions..."
  >
    <template v-slot:top>
      <v-toolbar flat color="desertsand">
        <v-toolbar-title>Inflected Word Forms</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
        <v-btn small color="primary" dark class="mb-2" @click="itemEditorDialog=true"
            >Add Word/Term</v-btn
        >
      </v-toolbar>
    </template>

    <template v-slot:expanded-item="{ headers, item }">
      <td :colspan="headers.length" :style="`direction: ${item.direction}`">
        <InflectedFormsTableItem
          :word="item"
        />
      </td>
    </template>


    <template v-slot:item.actions="{ item }">
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
         :loading="deletingWord"
         v-if="requestUser === item.curator.username"
      >
        mdi-delete
      </v-icon>
    </template>
    <template v-slot:no-data>
      ... this bank is currently empty ...
      
    </template>
  </v-data-table>

       <v-dialog v-model="itemEditorDialog" max-width="500px">
          <v-card>
            <v-card-title>
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

            <v-card-actions>
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
import InflectedFormsTableItem from "@/components/vocab/InflectedFormsTableItem.vue"

export default {
  name: "InflectedFormsTable",
  components: {
    InflectedFormsTableItem
  },
  props: {
    lexemeslug: String,
    lexemelanguage: String,
  },
  data: () => ({
    words: [],
    allLanguages: [],
    itemEditorDialog: false,
    loadingWords: false,
    deletingWord: false,
    saving: false,

    valid: false,

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
         ( value || "").length > 0 ||
         "Word must be at least 1 character in length.",

         requiredCuratorNote: value =>
         (value || "").length > 2 ||
         "The curator note must be at least 3 characters in length.",

      },

    editedIndex: -1,
    editedItem: {
      word: "",
      curator_note: "n/a",
    },
    defaultItem: {
      word: "",
      curator_note: "n/a",
    }

  }),

  computed: {
    requestUser(){
       return localStorage.getItem("username");
    }, 
    formTitle() {
      return this.editedIndex === -1 ? "Add Word/Term" : "Edit Word/Term";
    },

   termRTL(){
      if(this.lexemelanguage){
         for(var i = 0; i < this.allLanguages.length; i += 1 ){
            if(this.allLanguages[i].name === this.lexemelanguage){

               if(this.allLanguages[i].direction === "RTL"){
                  return true
               } else {
                  return false
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

    loadWords(lexemeslug){
      this.loadingWords = true;
      
      let endpoint = `/api/vocab/lexemes/wordlist/${lexemeslug}/`;
      let method = "GET";
      try {
        apiService(endpoint, method).then(data => {
            if (data){
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
      if(confirm("Are you sure you want to remove this word?")){
        let endpoint = `/api/vocab/inflectedformz/${item.id}/`;
        let method = "DELETE";
        try {
          apiService(endpoint, method).then(() => {
                this.words.splice(index, 1);
                this.deletingWord = false;
          });
        } catch (err) {
        console.log(err);
          this.deletingWord = false;
        }
      }
      // Sent DELETE message to API to fully remove...
    },
  
     submitNew(item){
      this.saving = true;
      let endpoint = `/api/vocab/inflectedformz/`;
      let method = "POST";
      let payload = {
         lexemeslug: this.lexemeslug,
         language: this.lexemelanguage,
         word: item.word,
         curator_note: item.curator_note,
      }
      try {
        apiService(endpoint, method, payload).then(data => {
            if (data && data.id){
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
     submitSave(item){
      this.saving = true;
      let endpoint = `/api/vocab/inflectedformz/${item.id}/`;
      let method = "PUT";
      let payload = {
         lexeme: this.lexemeslug,
         language: this.lexemelanguage,
         word: item.word,
         curator_note: item.curator_note,
      }
      try {
        apiService(endpoint, method, payload).then(data => {
            if (data && data.id){
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
      },
   },

  
};
</script>

<style></style>
