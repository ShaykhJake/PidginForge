<template>
   <v-dialog v-model="dialog" scrollable height=400>
      <v-card class="desertsand">
         <v-card-title class="sandstone">
            Add New Word/Term
         </v-card-title>
         <v-card-text class="px-2">
            <p class="overline">
            Add a new term/word (<a @click="inflectedFormInfo=true">in its inflected form</a>) to the database. This can
            be a single word or a phrase.  Start by choosing the languages in which
            this word/term has the same form:
            </p>
            <v-dialog
               v-model="inflectedFormInfo"
               max-width="450"
               scrollable
            >
               <v-card class="desertsand">
                  <v-card-title
                     class="headline sandstone calligraphy--text"
                     primary-title
                  >
                     Why Inflected Form?
                  </v-card-title>

                  <v-card-text>
                     <p>
                     Although admittedly inconvenient for curators when
                     adding words to our PidginForge dictionary, there is a reason
                     for distinguishing between the inflected form and the lexeme.
                     </p>

                     <blockquote class="blockquote">
                     <em>inflection:</em>
                     a change in the form of a word (typically the ending) to 
                     express a grammatical function or attribute such as tense, 
                     mood, person, number, case, and gender.
                     </blockquote>

                     <blockquote class="blockquote">
                     <em>lexeme:</em>
                     a basic lexical unit of a language, consisting of one word or several words, 
                     considered as an abstract unit, 
                     and applied to a family of words related by form or meaning
                     </blockquote>

                     <p>
                     While it's important to memorize inflected forms, it's even
                     more important for the linguist to be able to reduce these forms
                     to their shared lexeme. PidginForge groups these words together
                     by lexeme as a way to expand the linguist's vocabulary when
                     doing exercises. 
                     
                     </p>
                     <p>
                     For example, if we create a vocab card for the lexeme 
                     "go", it will automatically link to (and test the user with) any
                     inflected forms that have been declared and linked in the database. The user
                     may be quizzed on the following pairs: "go", "to go", "he goes", "they went", 
                     etc. 
                     </p>
                     <p>
                     Let's do some math. Assume that each Arabic verb has more than 10 inflected
                     (conjugated in this case) forms. You could maintain 1 vocabulary card
                     for the lexeme, or 10 vocabulary cards for those inflected forms. That might
                     be okay if you're learning just a few words, but if you have 100 verbs
                     that you want to learn, a stack of 1000 may be cumbersome.
                     </p>
                     <p>
                     For compound words and idioms, we also follow this rule, but mostly just
                     to maintain the system PidginForge uses for storing these words. Yet some
                     idioms and phrases do get conjugated. For example: 
                     </p>
                     <p>
                     "Ball is in your court": this is form is for 2nd person singular, with
                     the 2nd person possessive pronoun being the variable here. It would be
                     ineffective if we had separate vocabulary cards in our stacks for 
                     each and everyone one of those, because it would be hard for a user
                     to easily maintain those stacks. Instead, we would create a lexeme like
                     "ball is in (s.o.'s) court" (curators have some artistic license here).
                     </p>
                     <p>
                     Additionally, it is very important that, when doing vocabublary exercises,
                     that we link to real context; for that real context, we must maintain
                     the inflected forms.
                     </p>
                     <p>
                     It must be emphasized that we frequently encounter inflected forms
                     which look exactly like their lexeme. This is okay, but we still need
                     to create separate entries (one for inflected form, one for lexeme). We 
                     see this very often with simple nouns: "dog". This is both an inflected form
                     (singular) and the lexeme into which we also group the plural form "dogs".
                     </p>
                     <p>
                     I'll close by noting: You can add BOTH lexeme cards and inflected form
                     cards to your vocab card stack; your choice. However, I feel that most people, in
                     the end, will prefer to group those cards by lexeme, just as a dictionary does.
                     </p>
                  </v-card-text>

                  <v-divider></v-divider>

                  <v-card-actions class="sandstone">
                     <v-spacer></v-spacer>
                     <v-btn
                        color="primary"
                        text
                        @click="inflectedFormInfo = false"
                     >
                        Got It
                     </v-btn>
                  </v-card-actions>
               </v-card>
            </v-dialog>
            <v-form v-model="valid">
              <v-autocomplete
                v-model="termLanguage"
                :items="allLanguages"
                dense
                outlined
                color="primary"
                label="Word/Term Language(s)"
                item-text="name"
                item-value="name"
                :rules="[rules.requiredTermLanguage]"
              >
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
                              <v-chip small outlined class="languages">
                                 {{ data.item.language }}      
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
      termLanguage: null,
      valid: false,
      curatorNote: null,
      newTerm: null,
      inflectedFormInfo: false,
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
         if(this.termLanguage){
            for(var i = 0; i < this.allLanguages.length; i += 1 ){
               if(this.allLanguages[i].name === this.termLanguage){
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
      selectNewLexeme(lexeme){
         this.lexemeList.push(lexeme)
         this.selectedLexeme=lexeme.id;
         this.lexemeLanguage=lexeme.language
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
            language: this.termLanguage,
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
         this.termLanguage = this.language;
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