<template>
  <div>
    <v-card class="desertsand">
        <v-card-title class="justify-center">
          {{ stack.name }}
        </v-card-title>
        <v-card-text class="text-center">
          Curated by <span class="primary--text font-weight-bold"> {{ stack.curator.username }}</span> on {{stack.curationdate}}<br>
          Source Language: <v-chip small outlined class="languages languages--text">{{ stack.learning_language }}</v-chip><br>
          Target Language:  <v-chip small outlined class="languages languages--text">{{ stack.native_language }}</v-chip><br>
          Topic: <v-chip small outlined class="topics topics--text">{{ stack.topic }}</v-chip>
          <v-data-table
            :headers="headers"
            :items="stack.lexeme_pairs"
            :search="search"
            sort-by=""
            class="elevation-1 desertsand mt-2"
            @click:row="handleClick"
          >
            <template v-slot:top>
              <v-toolbar flat class="sandstone">
                <v-toolbar-title>Cards ({{ cards.length }})</v-toolbar-title>
                <v-divider
                  class="mx-4"
                  inset
                  vertical
                ></v-divider>
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search"
            single-line
            hide-details
          ></v-text-field>
                <v-spacer></v-spacer>
                <v-btn color="primary" dark class="mb-2" @click="dialog=true">Add Pair</v-btn>
                
                <v-dialog v-model="dialog" v-if="dialog" max-width="500px">
                  <v-card class="desertsand">
                    <v-card-title class="sandstone">
                      <span class="headline">{{ formTitle }}</span>
                    </v-card-title>

                    <v-card-text>
                      <v-container>
                          <span class="overline">Please note that languages are locked into the setting
                            for the overall card stack.</span><br>
                          

                        <v-form class="mt-3" dense>
                          <h3 class="mb-2">{{ stack.learning_language }} Lexemes</h3>
                          <v-autocomplete
                            v-model="lexeme1"
                            :disabled="fetchingLexeme1List"
                            :items="lexeme1List"
                            :label="`${l1Language} Lexemes (${lexeme1List.length})`"
                            :placeholder="`${lexeme1List.length} lexemes`"
                            outlined
                            color="blue-grey lighten-2"
                            item-text="lemma"
                            item-value="slug"
                            :loading="fetchingLexeme1List"
                            @change="loadPairings"
                            hide-details
                            class="mb-0 pb-0"
                          >
                            <template v-slot:item="data">
                              <template v-if="typeof data.item !== 'object'">
                                <v-list-item-content v-text="data.item"></v-list-item-content>
                              </template>
                              <template v-else>
                                <v-list-item-content>
                                  <v-list-item-title v-html="data.item.lemma"></v-list-item-title>
                                  <v-list-item-subtitle>Curated by {{data.item.curator.username}}</v-list-item-subtitle>
                                  <v-list-item-subtitle>0 Definitions; 0...; 0 Inflected Forms</v-list-item-subtitle>
                                </v-list-item-content>
                              </template>
                            </template>
                          </v-autocomplete>
                          <div style="text-align: center;" class="mb-5">
                            <span class="overline">Don't see what you want?</span><br>
                            <v-btn small class="primary" @click="addLexemeDialog=true">
                              Add New Lexeme
                            </v-btn>
                          </div>

                          <h3 class="mb-2">{{ stack.native_language }} Pairings</h3>
                          <v-autocomplete
                            v-model="lexemePair"
                            :disabled="loadingPairings"
                            :items="lexemePairList"
                            :label="`Existing Pairs (${lexemePairList.length})`"
                            :placeholder="`${lexemePairList.length} pairs`"
                            outlined
                            color="blue-grey lighten-2"
                            item-text="pairing.lemma"
                            :loading="loadingPairings"
                            item-value="id"
                            hide-details
                            class="mb-1 pb-1"
                          >
                            <template v-slot:item="data">
                              <template v-if="typeof data.item !== 'object'">
                                <v-list-item-content v-text="data.item"></v-list-item-content>
                              </template>
                              <template v-else>
                                <v-list-item-content>
                                  <v-list-item-title v-html="data.item.pairing.lemma"></v-list-item-title>
                                  <v-list-item-subtitle>Curated by {{data.item.pairing.curator.username}}</v-list-item-subtitle>
                                  <v-list-item-subtitle>{{ data.item.pairing.definitions.length }} definitions; {{ data.item.pairing.inflected_forms.length }} inflections</v-list-item-subtitle>
                                </v-list-item-content>
                              </template>
                            </template>
                          </v-autocomplete>
                          <div style="text-align: center;" class="mb-5">
                            <span class="overline">Don't see what you want?</span><br>
                            <v-btn small class="primary" @click="addPairDialog=true" :disabled="lexeme1.length < 1">
                              Add New Pairing
                            </v-btn>
                          </div>


                        </v-form>
                      </v-container>
                    </v-card-text>

                    <v-card-actions class="sandstone">
                      <v-spacer></v-spacer>
                      <v-btn color="garbage desertsand--text" @click="close">Cancel</v-btn>
                      <v-btn color="primary" :disabled="!lexemePair" @click="addPair">Save Pair</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-toolbar>
            </template>
            <template v-slot:item.lexeme_1_details.lemma="{ item }">
              <a @click.prevent="loadLexemeView(item.lexeme_1_details.slug)">
                <span class="subtitle-1">{{ item.lexeme_1_details.lemma }}</span>
              </a>
            </template>
            <template v-slot:item.lexeme_2_details.lemma="{ item }">
              <a @click.prevent="loadLexemeView(item.lexeme_2_details.slug)">
                <span class="subtitle-1">{{ item.lexeme_2_details.lemma }}</span>
              </a>
            </template>


            <template v-slot:item.actions="{ item }">
              <v-icon
                small
                v-if="requestUser===stack.curator.username"
                @click="deleteItem(item)"
              >
                mdi-delete
              </v-icon>
            </template>
            <template v-slot:no-data>
              ... stack is currently empty ...
            </template>
          </v-data-table>



        </v-card-text>
        <v-card-actions>
          <v-spacer />
            <v-btn 
              class="primary"
              @click="$router.push({name: 'Learn-Stack', params: { slug: slug}})"
            >
              Learn Stack
            </v-btn>
          <v-spacer />
        </v-card-actions>
          <v-overlay :value="loadingStack" absolute>
            <v-progress-circular indeterminate size="64"></v-progress-circular>
          </v-overlay>


    </v-card>
    <QuickAddLexeme 
      v-if="addLexemeDialog"
      :dialog="addLexemeDialog"
      :language="stack.learning_language"
      :direction="stack.l1direction"
      @closeDialog="addLexemeDialog=false"
      @selectNewLexeme="selectNewLexeme1"
    />
    <QuickAddPair
      v-if="addPairDialog"
      :dialog="addPairDialog"
      :lexeme_1="lexeme1Object"
      :language="stack.native_language"
      :direction="stack.l2direction"
      @closeDialog="addPairDialog=false"
      @selectNewPair="selectNewPair"
    />

    <v-dialog v-model="viewLexemeDetails" v-if="viewLexemeDetails" fullscreen hide-overlay transition="dialog-bottom-transition">
      <v-card class="sandstone">
        <v-toolbar class="sandstone">
          <v-btn icon @click="viewLexemeDetails=false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>
            Lexeme Viewer
          </v-toolbar-title>
        </v-toolbar>  
        <v-card-text>
              <LexemeCurator
                :lexemeslug="lexemeViewSlug"
              />
        </v-card-text>      
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import QuickAddLexeme from "@/components/vocab/stacks/QuickAddLexeme.vue";
import QuickAddPair from "@/components/vocab/stacks/QuickAddPair.vue";
import LexemeCurator from "@/components/vocab/LexemeCurator.vue";

export default {
   name: "StackCurator",
   components: {
     QuickAddLexeme,
     QuickAddPair,
     LexemeCurator
   },
   props: {
     slug: String,
   },
   data: () => ({
      search: '',
      selectedCard: null,
      cards: [],
      stack: {
        name: 'Fun Stack',
        slug: 'dirka-dirka',
        curator: 'ShaykhJake',
        curationdate: 'May 5, 2020',

      },
      allLanguages: [],
      loadingLanguages: [],
      lexeme1Object: {},
      l1Language: '',
      lexemeViewSlug: null,
      lexeme1: '',
      lexeme2: '',
      lexemePair: null,
      addLexemeDialog: false,
      addPairDialog: false,
      viewLexemeDetails: false,
      l2Language: '',
      lexeme1List: [],
      fetchingLexeme1List: false,
      lexemePairList: [],
      loadingPairings: false,
      lexeme2List: [],
      loadingStack: false,
      rules: {
        requiredLanguage: value =>
          (value || "").length > 0 ||
          "You must choose a language",

        requiredDescription: value =>
          (value || "").length > 3 ||
          "Description must be at least 4 characters long.",

      },


      dialog: false,
        headers: [
          {
            text: 'Pair ID',
            align: 'start',
            sortable: true,
            value: 'id',
          },
          { text: 'Lexeme 1', value: 'lexeme_1_details.lemma' },
          { text: 'L1 Language', value: 'lexeme_1_language.name' },
          { text: 'Lexeme 2', value: 'lexeme_2_details.lemma' },
          { text: 'L2 Language', value: 'lexeme_2_language.name' },
          { text: 'Actions', value: 'actions', sortable: false },
        ],
        editedIndex: -1,
        editedItem: {
          lexeme_1: '',
          lexeme_1_language: {
            name: '',
            direction: '',
          },
          lexeme_2: '',
          lexeme_2_language: {
            name: '',
            direction: '',
          },
        },
        defaultItem: {
          lexeme_1: '',
          lexeme_1_language: {
            name: '',
            direction: '',
          },
          lexeme_2: '',
          lexeme_2_language: {
            name: '',
            direction: '',
          },
        },
   }),
   computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'Add Pairing to Stack' : 'Edit Pair'
      },
      requestUser(){
        return localStorage.getItem("username");
      }, 
   },
   watch: {
      dialog (val) {
        val || this.close()
      },
    },

    created () {
      this.getLanguages();
    },
   methods: {
      loadStack(slug){
        this.loadingStack = true;
        let endpoint = `/api/vocab/cardstackz/${slug}/`;
        let method = "GET";      
        try {
          apiService(endpoint, method).then(data => {
              if (data){
                // console.log(data);
                this.stack = data;
                this.cards = data.lexeme_pairs;
                this.l1Language = data.learning_language
                this.l2Language = data.native_language
                this.loadLexeme1List(this.l1Language);
                this.loadingStack = false;
              } else {
                console.log("There was a major problem with the request.");
                // console.log(data.message);
                this.loadingStack = false;
              }
          });
        } catch (err) {
        console.log(err);
          this.loadingStack = false;
        }
      },
      loadLexemeView(slug){
        console.log(slug)
        this.lexemeViewSlug = slug;
        this.viewLexemeDetails = true;
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
      selectNewLexeme1(lexeme){
        this.lexeme1List.push(lexeme);
        this.lexeme1Object = lexeme;
        this.lexeme1 = lexeme.slug;

      },
      selectNewPair(pair){
        this.loadPairings()
        // this.lexemePairList.push(pair);
        this.lexemePair = pair.id;
      },
      createNewPair(){
        let lexeme1 = this.lexeme1
        var filteredArray = this.lexeme1List.filter(function (element) { 
          return element.slug === lexeme1;
        });
        this.lexeme1Object = filteredArray[0];
        // console.log(this.lexeme1Object)
      },
      initialize () {
        this.cards = [
          {
            lexeme_1: {
              lexeme: 'اشتراك',
              language: 'Arabic-MSA',
              direction: 'RTL',
              slug: 'blah-blah-blah'
            },
            lexeme_2:{
              lexeme: 'participation',
              language: 'English',
              direction: 'LTR',
              slug: 'blah-blag-blah'
            },
            id: '2',
            curator_note: 'blah blah',
          },
          {
            lexeme_1: {
              lexeme: 'tableau',
              language: 'French',
              direction: 'LTR',
              slug: 'blah-slah-blah'
            },
            lexeme_2:{
              lexeme: 'table',
              language: 'English',
              direction: 'LTR',
              slug: 'blah-tlah-blah'
            },
            id: '3',
            curator_note: 'blah blah',
          },
          {
            lexeme_1: {
              lexeme: 'taco',
              language: 'Spanish',
              direction: 'LTR',
              slug: 'blah-blap-blah'
            },
            lexeme_2:{
              lexeme: 'taco',
              language: 'English',
              direction: 'LTR',
              slug: 'blah-blar-blah'
            },
            id: '4',
            curator_note: 'blah blah',
          },
        ]
      },
      loadPairings(){
         this.loadingPairings = true;
         let lexeme1 = this.lexeme1
         var filteredArray = this.lexeme1List.filter(function (element) { 
           return element.slug === lexeme1;
         });
         this.lexeme1Object = filteredArray[0];
        //  console.log(this.lexeme1Object)

         let endpoint = `/api/vocab/lexemes/pairlist/${this.lexeme1}/${this.stack.native_language}/`;
         let method = "GET";
         try {
          apiService(endpoint, method).then(data => {
              if (data){
                // console.log(data);
                this.lexemePairList = data;
                this.loadingPairings = false;
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



      loadLexeme1List(language){
        //  this.showingLexemeList = false;
         this.fetchingLexeme1List = true;
         this.lexeme1 = '';
         this.lexeme1List = [];

         let endpoint = `/api/vocab/lexemes/lexemelist/?language=${language}`;
         let method = "GET";
         try {
         apiService(endpoint, method).then(data => {
            if (data){
              //  console.log(data);
               this.lexeme1List = data;
               this.fetchingLexeme1List = false;
            } else {
               console.log("There was a major problem with the request.");
               // console.log(data.message);
               this.fetchingLexeme1List = false;
            }
         });
         } catch (err) {
         console.log(err);
            this.fetchingLexeme1List = false; 
         }
      },

      loadLexeme2List(language){
         this.showingLexemeList = false;
         this.fetchingLexemeList = true;

         let endpoint = `/api/vocab/lexemes/lexemelist/?language=${language}`;
         let method = "GET";
         try {
         apiService(endpoint, method).then(data => {
            if (data){
              //  console.log(data);
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


      deleteItem (item) {
        const index = this.cards.indexOf(item)
        confirm('Are you sure you want to delete this item?') && this.cards.splice(index, 1)
        // console.log(item.id)
        let endpoint = `/api/vocab/deletestackpair/`;
        let method = "POST";
        let payload = {
          stack: this.stack.slug,
          pair: item.id,
        }
        try {
          apiService(endpoint, method, payload).then(data => {
            if (data){
              // console.log(data)
            } else {
              console.log("There was a major problem with the request.");
              // console.log(data.message);
            }
          });
        } catch (err) {
        console.log(err);
        }



      },
      handleClick(value) {
        this.selectedStack = value.id;
        // console.log(this.selectedStack)
        // console.log(value)
      },
      close() {
        this.dialog = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },

      addPair() {
        this.saving = true;
        let endpoint = `/api/vocab/addstackpair/`;
        let method = "POST";
        let payload = {
          stack: this.stack.slug,
          pair: this.lexemePair,
        }
        try {
          apiService(endpoint, method, payload).then(data => {
            if (data && data.id){
              this.stack.lexeme_pairs.push(data)
              // console.log(data)
              this.close()
              this.saving = false;
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

        this.close()
      },

      // submitSave(item){
      //   this.saving = true;
      //   let endpoint = `/api/vocab/cardstackz/`;
      //   let method = "POST";
      //   if(item.slug){
      //     endpoint = endpoint + `${item.slug}/`;
      //     method = "PATCH";
      //   }
      //   let payload = {
      //     name: item.name,
      //     description: item.description,
      //     learning_language: item.learning_language,
      //     native_language: item.native_language,
      //     topic: item.topic,
      //     public: item.public,
      //   }
      //   try {
      //     apiService(endpoint, method, payload).then(data => {
      //       if (data && data.slug){
      //         if (this.editedIndex > -1) {
      //           Object.assign(this.stacks[this.editedIndex], data)
      //         } else {
      //           this.stacks.push(data)
      //         }
      //         this.close()
      //         this.saving = false;
      //       } else {
      //         console.log("There was a major problem with the request.");
      //         // console.log(data.message);
      //         this.saving = false;
      //       }
      //     });
      //   } catch (err) {
      //   console.log(err);
      //     this.saving = false;
      //   }
      // },

   },
   mounted(){
    //  console.log("mount");
    //  this.initialize();
      this.loadStack(this.slug);
     


    //  this.loadStack(this.slug)
   }
};
</script>

<style>

</style>