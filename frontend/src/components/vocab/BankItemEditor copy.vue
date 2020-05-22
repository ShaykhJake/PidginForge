<template>
   <v-dialog v-model="dialog" scrollable height=400>
      <v-card>
         <v-card-title>
            Quick Add Vocab Pairs
         </v-card-title>
         <v-card-text>


            <v-row>
               <v-col cols="12" sm="6">
                  <v-card>
                     <v-card-title>
                        Source Word
                     </v-card-title>
                     <v-card-text>

                     </v-card-text>
                  </v-card>





               </v-col>
               <v-col cols="12" sm="6">
                  <v-card>
                     <v-card-title>
                        Target Word
                     </v-card-title>
                     <v-card-text>

                     </v-card-text>
                  </v-card>

                  
               </v-col>
            </v-row>






            <v-card>
               <v-card-title>
            
               </v-card-title>
               <v-card-text>

               </v-card-text>
            </v-card>



         </v-card-text>
         <v-card-action>
            <v-btn>
               Close
            </v-btn>
            <v-btn>
               Submit
            </v-btn>
         </v-card-action>
      </v-card>


        <v-card class="desertsand">
           <v-card-title class="sandstone calligraphy--text">
              Add Word Pair to Vocab Bank
           </v-card-title>
            <v-card-text>
               Start by choosing the first language:

               <v-autocomplete
                  v-model="l1Language"
                  name="l1language"
                  :items="allLanguages"
                  label="L1 Language*"
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
                  <v-col
                     class="subtitle-1 text-center"
                     cols="12"
                  >
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

               <v-autocomplete
                  v-model="selectedL1Word"
                  v-if="showingL1WordList"
                  :items="l1WordList"
                  :loading="fetchingL1List"
                  outlined
                  :placeholder="`${l1WordList.length} results for ${l1Language}`"
                  color="primary"
                  :label="`${l1Language} Word List (${l1WordList.length})`"
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
                           <v-list-item-subtitle>Language(s): {{
                              data.item.languages
                           }}</v-list-item-subtitle>
                           <v-list-item-subtitle>Lexeme: {{
                              data.item.lexeme.lemma
                           }}</v-list-item-subtitle>
                        </v-list-item-content>
                     </template>
                  </template>
               </v-autocomplete>

               <v-row
                  v-if="loadingL1Details"
                  align-content="center"
                  justify="center"
                  dense
                  no-gutters
                  >
                  <v-col
                     class="subtitle-1 text-center"
                     cols="12"
                  >
                     ... retrieving word details ...
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
               <div align="center" class="my-2" v-if="noL1Results">
                  Sorry, but there were no results for {{l1Language}}
               </div>
               <div align="center" class="my-2" v-if="showingL1WordList || noL1Results">
                  Don't see what you're looking for?
                  <v-btn small class="primary">
                     Add New Word
                  </v-btn>
               </div>

               <v-card 
                  v-if="showingL1Details && !loadingL1Details" 
                  class="desertsand mb-2"
               >
                  <v-card-title class="sandstone calligraphy--text py-1">
                     Details for <span class="font-weight-black primary--text"> {{ l1Details.word }} </span>
                     <v-spacer></v-spacer>

                     <v-btn small @click="hidingDetails=!hidingDetails" class="garbage desertsand--text">
                        <span v-if="!hidingDetails">Hide</span>
                        <span v-else>Show</span>
                     </v-btn>

                  </v-card-title>
                  <v-card-text v-show="!hidingDetails">
                        <div>
                           Curated by <strong>{{ l1Details.curator.username }}</strong> on {{ l1Details.curationdate }}<br>
                        </div>
                     <strong>Associated Lexeme:</strong><br>
                        <div class="ml-5 mr-">
                           {{ l1Details.lexeme.lemma}}
                        </div>
                     <strong>Languages:</strong><br>
                        <v-chip 
                           small
                           outlined
                           v-for="(language, langIndex) in l1Details.languages" 
                           :key="`language-${langIndex}`">
                           {{ language }}
                        </v-chip><br>
                     <strong>Definitions ({{l1Details.definitions.length}}):</strong><br>
                        <v-list 
                           two-line 
                           class="pa-0 overflow-y-auto"
                           style="border-style: solid; border-width: 1px; border-color: black;"
                           dense
                           max-height="125"            
                        >
                           <v-list-item
                              v-for="(definition, defIndex) in l1Details.definitions" 
                              :key="`definition-${defIndex}`"
                              class="px-3"
                           >
                              <v-list-item-content>
                                 <v-list-item-title 
                                    :style="`direction:${definition.language.direction}`"
                                    
                                 >
                                 {{ definition.definition}}
                                 <v-chip 
                                       small
                                       outlined
                                    >
                                     {{ definition.language.name }}
                                    </v-chip>
                                 </v-list-item-title>
                                 <v-list-item-subtitle>
                                 </v-list-item-subtitle>
                              </v-list-item-content>
                           </v-list-item>
                        </v-list>   
                     <strong>Grammar Notes ({{l1Details.grammars.length}}):</strong><br>
                        <v-list 
                           two-line 
                           class="pa-0 overflow-y-auto"
                           style="border-style: solid; border-width: 1px; border-color: black;"
                           dense
                           max-height="125"            
                        >
                           <v-list-item
                              v-for="(grammar, gramIndex) in l1Details.grammars" 
                              :key="`grammar-${gramIndex}`"
                              class="px-3"
                           >
                              <v-list-item-content>
                                 <v-list-item-title 
                                    :style="`direction:${grammar.language.direction}`"
                                    
                                 >
                                 {{ grammar.content}}
                                 <v-chip 
                                       small
                                       outlined
                                    >
                                     {{ grammar.language.name }}
                                    </v-chip>
                                 </v-list-item-title>
                                 <v-list-item-subtitle>
                                 </v-list-item-subtitle>
                              </v-list-item-content>
                           </v-list-item>
                        </v-list>   

                     <strong>Context Sentences ({{l1Details.sentences.length}}):</strong><br>
                        <v-list 
                           two-line 
                           class="pa-0 overflow-y-auto"
                           style="border-style: solid; border-width: 1px; border-color: black;"
                           dense
                           max-height="125"            
                        >
                           <v-list-item
                              v-for="(sentence, sentIndex) in l1Details.sentences" 
                              :key="`sentence-${sentIndex}`"
                              class="px-3"
                           >
                              <v-list-item-content>
                                 <v-list-item-title 
                                    :style="`direction:${sentence.language.direction}`"
                                    
                                 >
                                 {{ sentence.text}}
                                 <v-chip 
                                       small
                                       outlined
                                    >
                                     {{ sentence.language.name }}
                                    </v-chip>
                                 </v-list-item-title>
                                 <v-list-item-subtitle>
                                 </v-list-item-subtitle>
                              </v-list-item-content>
                           </v-list-item>
                        </v-list>   
               </v-card-text>
            </v-card>
            <v-card v-if="showingL1Details && !loadingL1Details && l1Details.word_pairs" class="desertsand">
               <v-card-title class="sandstone py-1 calligraphy--text">
                  Word Pairs for <span class="font-weight-black primary--text"> {{l1Details.word }} </span> ({{l1Details.word_pairs.length}}):
                  <v-spacer></v-spacer>
                     <v-btn small @click="hidingPairs=!hidingPairs" class="garbage desertsand--text mr-2">
                        <span v-if="!hidingPairs">Hide</span>
                        <span v-else>Show</span>
                     </v-btn>

               </v-card-title>
               <v-card-text 
                  v-if="l1Details.word_pairs.length > 0" 
                  class="pa-0"
                  v-show="!hidingPairs"
               >
                     <v-list 
                        three-line 
                        class="pa-0 overflow-y-auto"
                        style="border-style: solid; border-width: 1px; border-color: black;"
                        dense
                        max-height="125"            
                     >
                        <v-list-item
                           v-for="wordPair in l1Details.word_pairs"
                           :key="wordPair.id"
                           @click="wordPair.id === selectedPairID ? selectedPairID = null : selectedPairID = wordPair.id"
                           class="px-0"
                        >
                           <v-list-item-content 
                              v-if="wordPair.inflected_form_1.id === l1Details.id"
                              :class="wordPair.id === selectedPairID ? 'primary lighten-2 px-2' : 'white px-2'"
                           >
                              <v-list-item-title v-text="wordPair.inflected_form_2.word"></v-list-item-title>
                              <v-list-item-subtitle>
                                 Language(s):  
                                 <v-chip 
                                    small
                                    outlined
                                    v-for="language in wordPair.inflected_form_2.languages" 
                                    :key="language"
                                 >
                                    {{ language }}
                                 </v-chip>
                              </v-list-item-subtitle>
                              <v-list-item-subtitle>
                                 Lexeme: "{{ wordPair.inflected_form_2.lexeme.lemma }}"
                              </v-list-item-subtitle>

                           </v-list-item-content>

                           <v-list-item-content 
                              v-else 
                              :class="wordPair.id === selectedPairID ? 'primary lighten-2 px-2' : 'white px-2'"
                           >
                              <v-list-item-title v-text="wordPair.inflected_form_1.word"></v-list-item-title>
                              <v-list-item-subtitle>
                                 Language(s):  
                                 <v-chip 
                                    small
                                    outlined
                                    v-for="language in wordPair.inflected_form_1.languages" 
                                    :key="language"
                                 >
                                    {{ language }}
                                 </v-chip>
                              </v-list-item-subtitle>
                              <v-list-item-subtitle>
                                 Lexeme: "{{ wordPair.inflected_form_1.lexeme.lemma }}"
                              </v-list-item-subtitle>
                           </v-list-item-content>

                        </v-list-item>
                     </v-list>

               </v-card-text>
               <v-card-text v-else>
                  <p>
                     This word currently has no pairings in the database. Please add a new pairing.
                  </p>
               </v-card-text>
               <v-card-actions class="sandstone" v-if="!addingPairing">
                  <v-spacer></v-spacer>
                     Don't see the pair you're looking for?
                     <v-btn small class="primary" @click="addNewPairing">
                        Add New Pairing
                     </v-btn>
                  <v-spacer></v-spacer>
               </v-card-actions>

            </v-card>


            <v-card v-if="addingPairing" class="mt-2 desertsand">
               <v-card-title class="sandstone calligraphy--text py-1">
                  Add New Pairing for <span class="font-weight-black primary--text"> {{ l1Details.word }} </span>
               </v-card-title>
               <v-card-text>

                  Select the target language (L2):
                  <v-autocomplete
                     v-model="l2Language"
                     name="l2language"
                     :items="allLanguages"
                     label="L2 Language*"
                     placeholder="choose the L2 language"
                     :loading="loadingLanguages"
                     outlined
                     color="primary"
                     class="mt-2"
                     @change="loadL2WordList(l2Language)"
                  >
                  </v-autocomplete>

                  <v-row
                     v-if="fetchingL2List"
                     align-content="center"
                     justify="center"
                     dense
                     no-gutters
                     >
                     <v-col
                        class="subtitle-1 text-center"
                        cols="12"
                     >
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

                  <v-autocomplete
                     v-model="selectedL2Word"
                     v-if="showingL2WordList"
                     :items="l2WordList"
                     :loading="fetchingL2List"
                     outlined
                     :placeholder="`${l2WordList.length} results for ${l2Language}`"
                     color="primary"
                     :label="`${l2Language} Word List (${l2WordList.length})`"
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
                              <v-list-item-subtitle>Language(s): {{
                                 data.item.languages
                              }}</v-list-item-subtitle>
                              <v-list-item-subtitle>Lexeme: {{
                                 data.item.lexeme.lemma
                              }}</v-list-item-subtitle>
                           </v-list-item-content>
                        </template>
                     </template>
                  </v-autocomplete>

                  <div align="center" class="my-2" v-if="noL2Results">
                     Sorry, but there were no results for {{l2Language}}
                  </div>
                  <div align="center" class="my-2" v-if="showingL2WordList || noL2Results">
                     Don't see what you're looking for?
                     <v-btn small class="primary">
                        Add New Word
                     </v-btn>
                  </div>
                  <v-row
                     v-if="loadingL2Details"
                     align-content="center"
                     justify="center"
                     dense
                     no-gutters
                     >
                     <v-col
                        class="subtitle-1 text-center"
                        cols="12"
                     >
                        ... retrieving word details ...
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


                  <v-card 
                     v-if="showingL2Details && !loadingL2Details" 
                     class="desertsand mb-2"
                  >
                     <v-card-title class="sandstone calligraphy--text py-1">
                        Details for <span class="font-weight-black primary--text"> {{ l2Details.word }} </span>
                        <v-spacer></v-spacer>

                        <v-btn small @click="hidingL2Details=!hidingL2Details" class="garbage desertsand--text">
                           <span v-if="!hidingL2Details">Hide</span>
                           <span v-else>Show</span>
                        </v-btn>

                     </v-card-title>
                     <v-card-text v-show="!hidingL2Details">
                           <div>
                              Curated by <strong>{{ l2Details.curator.username }}</strong> on {{ l2Details.curationdate }}<br>
                           </div>
                        <strong>Associated Lexeme:</strong><br>
                           <div class="ml-5 mr-">
                              {{ l2Details.lexeme.lemma}}
                           </div>
                        <strong>Languages:</strong><br>
                           <v-chip 
                              small
                              outlined
                              v-for="(language, langIndex) in l2Details.languages" 
                              :key="`language-${langIndex}`">
                              {{ language }}
                           </v-chip><br>
                        <strong>Definitions ({{l2Details.definitions.length}}):</strong><br>
                           <v-list 
                              two-line 
                              class="pa-0 overflow-y-auto"
                              style="border-style: solid; border-width: 1px; border-color: black;"
                              dense
                              max-height="125"            
                           >
                              <v-list-item
                                 v-for="(definition, defIndex) in l2Details.definitions" 
                                 :key="`definition-${defIndex}`"
                                 class="px-3"
                              >
                                 <v-list-item-content>
                                    <v-list-item-title 
                                       :style="`direction:${definition.language.direction}`"
                                       
                                    >
                                    {{ definition.definition}}
                                    <v-chip 
                                          small
                                          outlined
                                       >
                                       {{ definition.language.name }}
                                       </v-chip>
                                    </v-list-item-title>
                                    <v-list-item-subtitle>
                                    </v-list-item-subtitle>
                                 </v-list-item-content>
                              </v-list-item>
                           </v-list>   
                        <strong>Grammar Notes ({{l2Details.grammars.length}}):</strong><br>
                           <v-list 
                              two-line 
                              class="pa-0 overflow-y-auto"
                              style="border-style: solid; border-width: 1px; border-color: black;"
                              dense
                              max-height="125"            
                           >
                              <v-list-item
                                 v-for="(grammar, gramIndex) in l2Details.grammars" 
                                 :key="`grammar-${gramIndex}`"
                                 class="px-3"
                              >
                                 <v-list-item-content>
                                    <v-list-item-title 
                                       :style="`direction:${grammar.language.direction}`"
                                       
                                    >
                                    {{ grammar.content}}
                                    <v-chip 
                                          small
                                          outlined
                                       >
                                       {{ grammar.language.name }}
                                       </v-chip>
                                    </v-list-item-title>
                                    <v-list-item-subtitle>
                                    </v-list-item-subtitle>
                                 </v-list-item-content>
                              </v-list-item>
                           </v-list>   

                        <strong>Context Sentences ({{l2Details.sentences.length}}):</strong><br>
                           <v-list 
                              two-line 
                              class="pa-0 overflow-y-auto"
                              style="border-style: solid; border-width: 1px; border-color: black;"
                              dense
                              max-height="125"            
                           >
                              <v-list-item
                                 v-for="(sentence, sentIndex) in l2Details.sentences" 
                                 :key="`sentence-${sentIndex}`"
                                 class="px-3"
                              >
                                 <v-list-item-content>
                                    <v-list-item-title 
                                       :style="`direction:${sentence.language.direction}`"
                                       
                                    >
                                    {{ sentence.text}}
                                    <v-chip 
                                          small
                                          outlined
                                       >
                                       {{ sentence.language.name }}
                                       </v-chip>
                                    </v-list-item-title>
                                    <v-list-item-subtitle>
                                    </v-list-item-subtitle>
                                 </v-list-item-content>
                              </v-list-item>
                           </v-list>   
                  </v-card-text>
               </v-card>


               </v-card-text>
               <v-card-actions class="sandstone">
                  <v-spacer></v-spacer>
                  <v-btn class="primary" :disabled="!l2Details.word">
                     Submit New Pair
                  </v-btn>
                  <v-spacer></v-spacer>
               </v-card-actions>
            </v-card>
            </v-card-text>
            <v-row dense no-gutters justify="center">
               <v-col cols="6" align="center">
                  Word 1
               </v-col>
               <v-col cols="6" align="center">
                  Word 2
               </v-col>
            </v-row>
            <v-row dense no-gutters>
               <v-col cols="6" align="center">
                  {{ l1Details.word }}
               </v-col>
               <v-col cols="6" align="center">
                  {{ l2Details.word }}
               </v-col>
            </v-row>
            <v-card-actions class="sandstone calligraphy--text">
               <v-spacer></v-spacer>
               <v-btn @click="closeDialog" class="garbage desertsand--text">
                  Cancel
               </v-btn>
               <v-btn :disabled="selectedPairID === null" class="primary desertsand--text">
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
   name: "BankItemEditor",
   props: {
      dialog: {
         type: Boolean,
         default: false,
      },
      l1Word: {
         type: String,
         required: false,
      }
   },
   data: () => ({
      fetchingL1List: false,
      fetchingL2List: false,
      selectedL1Word: '',
      selectedL2Word: '',
      l1WordList: [],
      l2WordList: [],
      l1Details: {},
      l2Details: {},
      addingPairing: false,
      hidingDetails: false,
      hidingL2Details: false,
      hidingPairs: false,
      selectedPairID: null,
      loadingLanguages: false,
      allLanguages: [],
      l1Language: "",
      l2Language: "",
      noL1Results: false,
      noL2Results: false,
      loadingL1WordList: false,
      loadingL1Details: false,

      showingL1WordList: false,
      showingL1Details: false,

      loadingL2WordList: false,
      loadingL2Details: false,

      showingL2WordList: false,
      showingL2Details: false,
   }),

   components: {

   },
   methods: {
      closeDialog(){
         this.$emit("closeDialog")
      },

      loadL1WordList(language){
         this.selectedPairID=null;
         this.showingL1Details = false;
         this.l1Details = {}
         this.fetchingL1List = true;
         this.showingL1WordList = false;
         this.noL1Results = false;
         let endpoint = `/api/vocab/words/wordlist/?language=${language}`;
         let method = "GET";
         try {
         apiService(endpoint, method).then(data => {
            if (data){
               console.log(data);
               this.l1WordList = data;
               if(this.l1WordList.length < 1){
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

      loadL2WordList(language){
         this.l2Details = {}
         this.fetchingL2List = true;
         this.showingL2WordList = false;
         this.showingL2Details = false;
         this.noL2Results = false;
         let endpoint = `/api/vocab/words/wordlist/?language=${language}`;
         let method = "GET";
         try {
         apiService(endpoint, method).then(data => {
            if (data){
               console.log(data);
               this.l2WordList = data;
               if(this.l2WordList.length < 1){
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
      loadL1Details(word){
         this.selectedPairID=null;
         this.addingPairing=false;
         this.loadingL1Details = true;
         this.showingL1Details = false;
         let endpoint = `/api/vocab/inflectedformz/${word}/`;
         let method = "GET";
         try {
         apiService(endpoint, method).then(data => {
            if (data){
               console.log(data);
               this.l1Details=data;
               this.loadingL1Details = false;
               this.showingL1Details = true;
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
      loadL2Details(word){
         this.l2Details = {}
         this.showingL2Details = false;
         this.loadingL2Details = true;
         let endpoint = `/api/vocab/inflectedformz/${word}/`;
         let method = "GET";
         try {
         apiService(endpoint, method).then(data => {
            if (data){
               console.log(data);
               this.l2Details=data;
               this.loadingL2Details = false;
               this.showingL2Details = true;
            } else {
               console.log("There was a major problem with the request.");
               // console.log(data.message);
               this.loadingL2Details = false;
            }
         });
         } catch (err) {
         console.log(err);
            this.loadingL2Details = false;
         }
      }, 
      submitNewPair(){
         console.log("Hello")
      },

      getLanguages() {
         var localLanguages = localStorage.getItem("languages");
         if (localLanguages.length > 1) {
            console.log("Shop local!");
            this.allLanguages = JSON.parse(localLanguages);
            this.allLanguages.unshift("all")
         } else {
            this.loadingLanguages = true;
            let endpoint = `/api/categories/languages/`;
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
      addNewPairing(){
         this.addingPairing=true; 
         this.hidingDetails=true; 
         this.hidingPairs=true;
         this.selectedPairID=null;
      },
      selectPair(pairID){
         console.log(pairID);
      },
   },
   created(){
      this.getLanguages();
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