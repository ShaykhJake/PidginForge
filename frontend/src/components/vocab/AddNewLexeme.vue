<template>
   <v-dialog v-model="dialog" scrollable height=400>
      <v-card class="desertsand">
         <v-card-title class="sandstone">
            Add New Lexeme
         </v-card-title>
         <v-card-text class="px-2">
            <p class="overline">
            A lexeme is "a basic lexical unit of a language, consisting of one
            word or several words, considered as an abstract unit, and applied to a
            family of words related by form or meaning." In english, to go, he goes,
            and I went all can be grouped with the lexeme "go", which is how they
            are found in a dictionary. Lexeme and lemma are often used interchangeably,
            but lemma is the actual word representation of the lexeme.
            </p>
            <v-form v-model="valid">
              <v-autocomplete
                v-model="lexemeLanguage"
                :items="allLanguages"
                dense
                outlined
                color="primary"
                label="Lexeme Language(s)"
                item-text="name"
                item-value="name"
                :rules="[rules.requiredLexemeLanguage]"
              >

              </v-autocomplete>

               <div :style="termRTL ? 'direction:rtl;' : ''">
                  <v-text-field
                     label="New Lexeme's Lemma"
                     v-model="lemma"
                     outlined
                     :reverse="termRTL"
                     :rules="[rules.requiredLemma]"
                  ></v-text-field>
               </div>
               <v-text-field
                  v-model="curator_note"
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

            </v-form>
         </v-card-text>
         <v-card-actions class="sandstone">
            <v-spacer></v-spacer>
            <v-btn class="garbage desertsand--text" @click="closeDialog">
               Cancel
            </v-btn>
         
            <v-btn class="primary" :disabled="!valid" @click="submitLexeme" :loading="submittingLexeme">
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
   name: "AddNewLexeme",
   props: {
      dialog: {
         type: Boolean,
         default: false
      },
      language: {
         language: {
            type: String,
            required: false,
         }
      }

   },
   data: () => ({
      valid: false,
      lexemeLanguage: null,
      lemma: null,
      curator_note: null,
      submittingLexeme: false,
      fetchingLexemeList: false,
      selectedLexeme: null,
      lexemeList: [],
      loadingLanguages: false,
      allLanguages: [],
      rules: {
         requiredLexemeLanguage: value =>
         (value || "").length > 0 ||
         "Must select at least one term language.",

         requiredLemma: value =>
         (value || "").length > 0 ||
         "Your term must have at least one letter!",

         requiredNotes: value =>
         (value || "").length > 0 ||
         "Your must enter something, even it it's just 'n/a'!",
      },


   }),

   components: {

   },
   computed: {
      termRTL(){
         if(this.lexemeLanguage){
            for(var i = 0; i < this.allLanguages.length; i += 1 ){
               if(this.allLanguages[i].name === this.lexemeLanguage){
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
      removeLexemeLanguage(item) {
         const index = this.lexemeLanguage.indexOf(item);
         if (index >= 0) this.lexemeLanguage.splice(index, 1);
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
      submitLexeme(){
         this.submittingLexeme = true;
         let endpoint = `/api/vocab/lexemez/`;
         let method = "POST";
         let payload = {
            language: this.lexemeLanguage,
            lemma: this.lemma,
            curator_note: this.curator_note,
         }
         try {
         apiService(endpoint, method, payload).then(data => {
            if (data && data.id){
               console.log(data);
               this.$emit("selectNewLexeme", data)
               this.closeDialog()
               this.submittingLexeme = false
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
         this.lexemeLanguage = this.language;
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