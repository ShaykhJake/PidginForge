<template>
  <div>

  <v-data-table
    :headers="headers"
    :items="vocabBank.word_pairs"
    sort-by="L1 Word"
    class="elevation-5 desertsand"
    :loading="loadingBank"
    loading-text="...fetching word pairs..."
  >
    <template v-slot:top>
      <v-toolbar flat color="desertsand">
        <v-toolbar-title>Vocab Bank</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
        <v-btn 
          small 
          color="primary" 
          dark class="mb-2" 
          @click="itemEditorDialog=true"
          v-if="vocabBank.curator && requestUser===vocabBank.curator.username"
        >
        Add Word Pair(s)</v-btn
        >
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon 
        small 
        v-if="vocabBank.curator && requestUser===vocabBank.curator.username"
        @click="deleteItem(item)" 
        :loading="deletingPair"
      >
        mdi-delete
      </v-icon>
    </template>
    <template v-slot:no-data>
      ... this bank is currently empty ...
      
    </template>
  </v-data-table>
  <BankItemEditor
    v-if="itemEditorDialog"
    :dialog="itemEditorDialog"
    :vocab-bank-i-d="vocabBankID"
    :source-language="sourceLanguage"
    :target-language="targetLanguage"
    @addPair="addPair"
    @closeDialog="itemEditorDialog=false"
  />
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import BankItemEditor from "@/components/vocab/BankItemEditor.vue";
export default {
  name: "VocabBank",
  components: {
    BankItemEditor,
  },
  props: {
    vocabBankID: Number,
    sourceLanguage: String,
    targetLanguage: String,
  },
  data: () => ({
    dialog: false,
    itemEditorDialog: false,
    vocabBank: {},
    loadingBank: false,
    deletingPair: false,
    returnCommand: function() {},
    headers: [
      {
        text: "Source Word",
        align: "start",
        value: "inflected_form_1.word"
      },
      { text: "Source Lexeme", value: "inflected_form_1.lexeme.lemma" },
      { text: "Target Word", value: "inflected_form_2.word" },
      { text: "Target Lexeme", value: "inflected_form_2.lexeme.lemma" },
      { text: "Actions", value: "actions", sortable: false }
    ],
    inflectedForms: [],

    wordPairs: [
      {
          "id": 1,
          "curator": {
              "id": 1,
              "username": "ShaykhJake",
              "user_profile": {
                  "avatar": "https://jakesdesk-media.s3.amazonaws.com/media/public/avatars/2020/04/29/auto-mechanic-2829141_1280_wWHTNbf.jpg",
                  "image": "https://jakesdesk-media.s3.amazonaws.com/media/public/profile_pics/2020/04/29/auto-mechanic-2829141_1280_C9M1Lll.jpg"
              }
          },
          "curationdate": "May 17, 2020",
          "updated": "May 17, 2020",
          "inflected_form_1": {
              "id": 1,
              "curator": {
                  "id": 1,
                  "username": "ShaykhJake",
                  "user_profile": {
                      "avatar": "https://jakesdesk-media.s3.amazonaws.com/media/public/avatars/2020/04/29/auto-mechanic-2829141_1280_wWHTNbf.jpg",
                      "image": "https://jakesdesk-media.s3.amazonaws.com/media/public/profile_pics/2020/04/29/auto-mechanic-2829141_1280_C9M1Lll.jpg"
                  }
              },
              "curationdate": "May 17, 2020",
              "updated": "May 17, 2020",
              "grammars": [
                  {
                      "id": 1,
                      "curator": {
                          "id": 41,
                          "username": "Jake",
                          "user_profile": {
                              "avatar": "https://jakesdesk-media.s3.amazonaws.com/media/public/avatars/2020/04/29/J_logo_EDENL6I.jpg",
                              "image": "https://jakesdesk-media.s3.amazonaws.com/media/public/profile_pics/2020/04/29/J_logo_mOg6SmT.jpg"
                          }
                      },
                      "curationdate": "May 17, 2020",
                      "updated": "May 17, 2020",
                      "language": "English",
                      "content": "This particular form is the 1st person past tense.",
                      "rich_content": null,
                      "inflected_form": 1
                  }
              ],
              "definitions": [],
              "pronunciations": [],
              "images": [],
              "lexeme": {
                  "id": 1,
                  "lemma": "استخرج"
              },
              "sentences": [],
              "word": "استخرجت"
          },
          "inflected_form_2": {
              "id": 3,
              "curator": {
                  "id": 1,
                  "username": "ShaykhJake",
                  "user_profile": {
                      "avatar": "https://jakesdesk-media.s3.amazonaws.com/media/public/avatars/2020/04/29/auto-mechanic-2829141_1280_wWHTNbf.jpg",
                      "image": "https://jakesdesk-media.s3.amazonaws.com/media/public/profile_pics/2020/04/29/auto-mechanic-2829141_1280_C9M1Lll.jpg"
                  }
              },
              "curationdate": "May 17, 2020",
              "updated": "May 17, 2020",
              "grammars": [],
              "definitions": [],
              "pronunciations": [],
              "images": [],
              "lexeme": {
                  "id": 2,
                  "lemma": "extract"
              },
              "sentences": [],
              "word": "I extracted"
          },
          "curator_note": "n/a"
      }
    ],


    lexemes: [],
    editedIndex: -1,
    editedItem: {
      lexeme: "",
      translation: "",
      partofspeech: "",
      root: "",
      context: ""
    },
    defaultItem: {
      lexeme: "",
      translation: "",
      partofspeech: "",
      root: "",
      context: ""
    }
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "Add Lexeme" : "Edit Lexeme";
    },
    requestUser(){
        return localStorage.getItem("username");
    }, 
  },

  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  mounted() {
    // console.log(this.vocabBankID)
    this.loadVocabBank(this.vocabBankID);
    console.log(this.vocabBankID);
  },
  created() {
    // this.initialize();
  },

  methods: {
    addPair(pair){
      if(this.vocabBank.word_pairs.some(word_pair => word_pair.id === pair.id)){
        console.log("That pair is already in the bank")
      } else {
        this.vocabBank.word_pairs.push(pair);
      }
    },
    initialize() {
      // this.lexemes = [
      //   {
      //     lexeme: "اشترك في",
      //     translation: "to participate in",
      //     partofspeech: "verb",
      //     root: "شرك",
      //     context: "اشتركتُ في بناء الموقع"
      //   },
      //   {
      //     lexeme: "شخص",
      //     translation: "person",
      //     partofspeech: "noun",
      //     root: "شخص",
      //     context: "رأيت شخص مشتبه به"
      //   },
      //   {
      //     lexeme: "طائرة",
      //     translation: "airplane",
      //     partofspeech: "noun",
      //     root: "طار يطير",
      //     context: "افادت نشرة الاخبار بأن طائرة فرنسية اصتدمت ببرج ايفل"
      //   }
      // ];
    },

    addLexeme(command, newLexeme) {
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
    editItem(lexeme) {
      this.editedIndex = this.lexemes.indexOf(lexeme);
      this.editedItem = Object.assign({}, lexeme);
      this.dialog = true;
    },
    loadVocabBank(bank){
      this.loadingBank = true;
      let endpoint = `/api/vocab/bank/${bank}/`;
      let method = "GET";
      try {
        apiService(endpoint, method).then(data => {
            if (data){
              // console.log(data);
              this.vocabBank = data;
              this.loadingBank = false;
            } else {
              console.log("There was a major problem with the request.");
              // console.log(data.message);
              this.loadingBank = false;
            }
        });
      } catch (err) {
      console.log(err);
        this.loadingL1Details = false;
      }
    },

    createVocabBank(){
      this.creatingBank = true;
      
      let endpoint = `/api/lessons/createvocab/`;
      let method = "POST";
      let payload = {
        lesson: this.lesson.id,
      }
      try {
        apiService(endpoint, method, payload).then(data => {
            if (data){
              // console.log(data);
              this.vocabBankID = data.vocab_bank_id;
              this.loadVocabBank(this.vocabBankID);
              this.creatingBank = false;
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
    deleteItem(item) {
      const index = this.vocabBank.word_pairs.indexOf(item);
      if(confirm("Are you sure you want to remove this word pair?")){
        this.vocabBank.word_pairs.splice(index, 1);

        let endpoint = `/api/vocab/removepair/`;
        let method = "POST";
        let payload = {
          vocab_bank: this.vocabBankID,
          word_pair: item.id
        }
        try {
          apiService(endpoint, method, payload).then(data => {
              if (data){
                // console.log(data);
                
                
                this.deletingPair = false;
              } else {
                console.log("There was a major problem with the request.");
                // console.log(data.message);
                this.deletingPair = false;
              }
          });
        } catch (err) {
        console.log(err);
          this.deletingPair = false;
        }
      }
      // Sent DELETE message to API to fully remove...
    },
    deletePair(pairID){
        let endpoint = `/api/vocab/inflectedpairz/${pairID}`;
        let method = "DELETE";
        try {
          apiService(endpoint, method).then(data => {
              if (data){
                // console.log(data);
              } else {
                console.log("There was a major problem with the request.");
              }
          });
        } catch (err) {
          console.log(err);
        }

    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.lexemes[this.editedIndex], this.editedItem);
      } else {
        this.lexemes.push(this.editedItem);
      }
      if (this.returnCommand) {
        // console.log(this.returnCommand);
        let lexemePackage = {
          editedItem: this.editedItem,
          returnCommand: this.returnCommand
        };
        this.$emit("setLexemeDefinition", lexemePackage);
      }
      this.close();
    }
  }
};
</script>

<style></style>
