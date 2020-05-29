<template>
  <v-container>
      <v-card v-if="lexeme.lemma" class="desertsand mb-2">
         <v-card-title class="display-1 justify-center desertsand" :style="`text-align: center; direction: ${lexeme.direction}`">
            {{ lexeme.lemma }}<br>


         </v-card-title>
         <v-card-text class="text-center">
            Curated by 
               <span class="primary--text font-weight-black">
                  {{ lexeme.curator.username }}
               </span>
               on {{ lexeme.curationdate }}
            <br>
            Language:
            <v-chip small outlined class="languages languages--text">
               {{ lexeme.language }}
            </v-chip>
         </v-card-text>
      </v-card>

      <v-card class="desertsand mb-2">
         <v-card-text pa-0>
               <LexemeDefinitionsTable 
                  :lexemeslug="lexemeslug"
               />
         </v-card-text>
      </v-card>
      <v-card class="desertsand mb-2">
         <v-card-text pa-0>
               <LexemePronunciationsTable 
                  :lexemeslug="lexemeslug"
               />
         </v-card-text>
      </v-card>
      <v-card class="desertsand mb-2">
         <v-card-text pa-0>
               <InflectedFormsTable 
                  :lexemeslug="lexemeslug"
                  :lexemelanguage="lexeme.language"
               />
         </v-card-text>
      </v-card>

               
               Inflected Forms (v-for components)
               
               Comments


  </v-container>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import LexemeDefinitionsTable from "@/components/vocab/LexemeDefinitionsTable.vue";
import LexemePronunciationsTable from "@/components/vocab/LexemePronunciationsTable.vue";
import InflectedFormsTable from "@/components/vocab/InflectedFormsTable.vue";
export default {
  name: "VocabCurator",
  components: {
     LexemeDefinitionsTable,
     LexemePronunciationsTable,
     InflectedFormsTable,
  },
  props: {
    lexemeslug: {
       type: String,
       required: false
    }
    
  },
  data: () => ({
    lexeme: {},
    

    sentenceEditorDialog: false,
    definitionEditorDialog: false,
    grammarNoteDialog: false,
    pronunciationDialog: false,
    inflectedFormDialog: false,
    lexemePairDialog: false,
    inflectedPairDialog: false,

    

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
    }
  },

  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  mounted() {
    if(this.lexemeslug){
      this.loadLexeme(this.lexemeslug);
    }
  },
  created() {
    // this.initialize();
  },

  methods: {
     loadLexeme(slug){
        this.loadingLexeme = true;
         let endpoint = `/api/vocab/lexemez/${slug}/`;
         let method = "GET";
         try {
         apiService(endpoint, method).then(data => {
               if (data && data.lemma){
                  // console.log(data);
                  this.lexeme = data;
                  this.loadingLexeme = false;
               } else {
                  console.log("There was a major problem with the request.");
                  // console.log(data.message);
                  this.loadingLexeme = false;
               }
         });
         } catch (err) {
            console.log(err);
            this.loadingLexeme = false;
         }
     },


    deletePair(pairID){
        let endpoint = `/api/vocab/inflectedpairz/${pairID}`;
        let method = "DELETE";
        try {
          apiService(endpoint, method).then(data => {
              if (data){
                console.log(data);
              } else {
                console.log("There was a major problem with the request.");
              }
          });
        } catch (err) {
          console.log(err);
        }

    },

  }
};
</script>

<style></style>
