<template>
   <v-dialog v-model="dialog" scrollable height=400>
      <v-card class="desertsand">
         <v-card-title class="sandstone">
            Add New Word/Term
         </v-card-title>
         <v-card-text class="px-2">
            <p class="overline">
            Add a new term/word (in its inflected form) to the database. This can
            be a single word or a phrase.  Start by choosing the languages in which
            this word/term has the same form:
            </p>
            <v-form v-model="valid">
              <v-autocomplete
                v-model="termLanguages"
                :items="allLanguages"
                dense
                outlined
                chips
                color="blue-grey lighten-2"
                label="Word/Term Language(s)"
                multiple
                item-text="name"
                item-value="name"
                :rules="[rules.requiredTermLanguage]"
              >
                <template v-slot:selection="data">
                  <v-chip
                    color="primary"
                    v-bind="data.attrs"
                    :input-value="data.selected"
                    close
                    @click="data.select"
                    @click:close="removeTermLanguage(data.item)"
                  >
                    {{ data.item.name }}
                  </v-chip>
                </template>
              </v-autocomplete>

               <div :style="termRTL ? 'direction:rtl;' : ''">
                  <v-text-field
                     v-model="newTerm"
                     label="New Word/Term"
                     outlined
                     :reverse="termRTL"
                     :rules="[rules.requiredTerm]"
                  ></v-text-field>
               </div>
               <v-text-field
                  v-model="curatorNote"
                  label="Curator Notes"
                  outlined
                  :rules="[rules.requiredNotes]"
               ></v-text-field>
               <p class="overline">
                  To add definitions, sentences, and other fun things, you
                  can use the full vocab editor once you've submitted this word. For
                  now we are focused on getting the word in the database so you
                  can finish your vocab bank.
               </p>
               <hr>

               <h3>Associated Lexeme:</h3>

               <p class="overline">
                  For multiple-word phrases like idioms, the lexeme may
                  be the same as the inflected/form.
               </p>

               <v-autocomplete
                  v-model="lexemeLanguage"
                  name="lexemelanguage"
                  :items="allLanguages"
                  label="Lexeme Language*"
                  placeholder="choose the lexeme language"
                  :loading="loadingLanguages"
                  outlined
                  color="primary"
                  class="mt-2"
                  item-text="name"
                  item-value="name"
                  @change="loadLexemeList(lexemeLanguage)"
                  :rules="[rules.requiredLexemeLanguage]"
               >

               </v-autocomplete>

               <v-row
                  v-if="fetchingLexemeList"
                  align-content="center"
                  justify="center"
                  dense
                  no-gutters
                  class="mb-5"
                  >
                  <v-col
                     class="subtitle-1 text-center"
                     cols="12"
                  >
                     ... retrieving lexeme list for {{ lexemeLanguage }}...
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
                  v-model="selectedLexeme"
                  v-if="lexemeLanguage && !fetchingLexemeList"
                  :items="lexemeList"
                  :loading="fetchingLexemeList"
                  outlined
                  :placeholder="`${lexemeList.length} results for ${lexemeLanguage}`"
                  color="primary"
                  :label="`${lexemeLanguage} existing lexemes in database (${lexemeList.length})`"
                  item-text="lemma"
                  item-value="id"
                  :rules="[rules.requiredLexeme]"
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
                              v-html="data.item.lemma"
                           ></v-list-item-title>
                           
                           <v-list-item-subtitle>
                              Language(s):
                              <v-chip small outlined class="languages" v-for="(language, index) in data.item.languages" :key="index">
                                 {{ language }}      
                              </v-chip>
                           </v-list-item-subtitle>

                        </v-list-item-content>
                     </template>
                  </template>
               </v-autocomplete>
            </v-form>
            Don't like your options?
            <v-btn small class="elements desertsand--text" @click="newLexemeDialog=true">
               Add a New Lexeme
            </v-btn>
            <AddNewLexeme 
               @closeDialog="newLexemeDialog=false"
               @selectNewLexeme="selectNewLexeme"
               :dialog="newLexemeDialog"
               :language="language"
            />
         </v-card-text>
         <v-card-actions class="sandstone">
            <v-spacer></v-spacer>
            <v-btn class="garbage desertsand--text" @click="closeDialog">
               Cancel
            </v-btn>
         
            <v-btn class="primary" :disabled="!valid" @click="submitTerm">
               Submit
            </v-btn>
            <v-spacer></v-spacer>
         </v-card-actions>
      </v-card>

   </v-dialog>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import AddNewLexeme from "@/components/vocab/AddNewLexeme.vue";
export default {
   name: "AddNewTerm",
   props: {
      dialog: {
         type: Boolean,
         default: false
      },
      language: {
         type: String,
         required: false,   
      }
   },
   data: () => ({
      newLexemeDialog: false,
      termLanguages: [],
      valid: false,
      curatorNote: null,
      newTerm: null,
      lexemeLanguage: null,
      fetchingLexemeList: false,
      selectedLexeme: null,
      lexemeList: [],
      loadingLanguages: false,
      allLanguages: [],
      rules: {
         requiredTermLanguage: value =>
         (value || "").length > 0 ||
         "Must select at least one term language.",

         requiredTerm: value =>
         (value || "").length > 0 ||
         "Your term must have at least one letter!",

         requiredNotes: value =>
         (value || "").length > 0 ||
         "Your must enter something, even it it's just 'n/a'!",

         requiredLexemeLanguage: value =>
         !!value ||
         "You must choose an associated lexeme language...",

         requiredLexeme: value =>
         !!value ||
         "You must choose an associated lexeme.",
      },


   }),

   components: {
      AddNewLexeme
   },
   computed: {
      termRTL(){
         if(this.termLanguages && this.termLanguages.length > 0){
            for(var i = 0; i < this.allLanguages.length; i += 1 ){
               if(this.allLanguages[i].name === this.termLanguages[0]){
                  console.log("found it")
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
   methods: {
      closeDialog(){
         this.$emit("closeDialog")
      },
      removeTermLanguage(item) {
         const index = this.termLanguages.indexOf(item);
         if (index >= 0) this.termLanguages.splice(index, 1);
      },
      selectNewLexeme(lexeme){
         this.lexemeList.push(lexeme)
         this.selectedLexeme=lexeme.id;
         this.lexemeLanguage=lexeme.languages[0]
         console.log(lexeme)
      },
      loadLexemeList(language){
         this.showingLexemeList = false;
         this.fetchingLexemeList = true;

         let endpoint = `/api/vocab/lexemes/lexemelist/?language=${language}`;
         let method = "GET";
         try {
         apiService(endpoint, method).then(data => {
            if (data){
               console.log(data);
               this.lexemeList = data;

               this.fetchingLexemeList = false;
            } else {
               console.log("There was a major problem with the request.");
               // console.log(data.message);
               this.fetchingLexemeList = false;
            }
         });
         } catch (err) {
         console.log(err);
            this.fetchingLexemeList = false; 
         }

      },

      submitTerm(){
         this.submittingTerm = true;
         let endpoint = `/api/vocab/inflectedformz/`;
         let method = "POST";
         let payload = {
            languages: this.termLanguages,
            word: this.newTerm,
            curator_note: this.curatorNote,
            lexeme_id: this.selectedLexeme,
         }
         try {
         apiService(endpoint, method, payload).then(data => {
            if (data && data.id){
               console.log(data);
               this.$emit("pushNewTerm", data)
               this.closeDialog()
               this.submittingTerm = false
            } else {
               console.log("There was a major problem with the request.");
               // console.log(data.message);
               this.submittingTerm = false;
            }
         });
         } catch (err) {
         console.log(err);
            this.submittingTerm = false; 
         }

      },
      getLanguages() {
         var localLanguagesFull = localStorage.getItem("languages_full");
         if (localLanguagesFull) {
            console.log("Shop local!");
            this.allLanguages = JSON.parse(localLanguagesFull);
            this.allLanguages.unshift("all")
         } else {
            this.loadingLanguages = true;
            let endpoint = `/api/categories/languages_full/`;
            try {
               apiService(endpoint).then(data => {
               if (data != null) {
                  this.allLanguages = data;
                  this.allLanguages.unshift("all")
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
   created(){
      this.getLanguages();
   },
   mounted(){
      if(this.language){
         this.termLanguages.push(this.language);
         this.lexemeLanguage = this.language;
         this.loadLexemeList(this.language);
      }
   }
}
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