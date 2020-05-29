<template>
  <div>

  <v-data-table
    :headers="headers"
    :items="definitions"
    multi-sort
    :sort-by="['language', 'curationdate']"
    :sort-desc="[false, true]"
    class="desertsand"
    show-expand
    :loading="loadingDefinitions"
    loading-text="...fetching inflected forms defintions..."
  >
    <template v-slot:top>
      <v-toolbar flat color="desertsand">
        <v-toolbar-title>Inflected Form Definitions</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
        <v-btn small color="primary" dark class="mb-2" @click="itemEditorDialog=true"
            >Add Inflected Form Definition</v-btn
        >
      </v-toolbar>
    </template>

    <template v-slot:expanded-item="{ headers, item }">
      <td :colspan="headers.length" :style="`direction: ${item.direction}`">{{ item.definition }}</td>
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
         :loading="deletingDefinition"
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
                     <v-textarea
                        v-model="editedItem.definition"
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

export default {
  name: "InflectedDefinitionsTable",
  components: {
    
  },
  props: {
    inflectedid: Number,
    definitions: Array,
  },
  data: () => ({
    // definitions: [],
    allLanguages: [],


    itemEditorDialog: false,

    loadingDefinitions: false,
    deletingDefinition: false,
    saving: false,

    valid: false,

    returnCommand: function() {},
    headers: [
      {
        text: "Definition",
        align: "start",
        value: "definition"
      },
      { text: "Curator", value: "curator.username" },
      { text: "Language", value: "language" },
      { text: "Date Added", value: "curationdate" },
      { text: "Actions", value: "actions", sortable: false }
    ],
      rules: {
         requiredLanguage: value =>
         !!value ||
         "Must select a language.",

         requiredDefinition: value =>
         (value || "").length > 4 ||
         "The definition must be at least 5 characters in length.",

         requiredPOS: value =>
         (value || "").length > 1 ||
         "The part of speech must be at least 2 characters in length.",

      },

    editedIndex: -1,
    editedItem: {
      language: "English",
      definition: "",
      source_name: "n/a",
      source_citation: "n/a",
    },
    defaultItem: {
      language: "English",
      definition: "",
      source_name: "n/a",
      source_citation: "n/a",
    }

  }),

  computed: {
    requestUser(){
       return localStorage.getItem("username");
    }, 
    formTitle() {
      return this.editedIndex === -1 ? "Add Definition" : "Edit Definition";
    },
   termRTL(){
      if(this.editedItem.language){
         for(var i = 0; i < this.allLanguages.length; i += 1 ){
            if(this.allLanguages[i].name === this.editedItem.language){
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

  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  mounted() {
    // this.loadDefinitions(this.lexemeslug);
  },
  created() {
    this.getLanguages();
  },

  methods: {

    // addDefinition(command, newLexeme) {
    //   this.dialog = true;
    //   this.returnCommand = command;
    //   this.editedItem = {
    //     inflected_form: this.inflectedid,
    //     language: "",
    //     definition: "",
    //   };
    // },

    // loadDefinitions(lexemeslug){
    //   this.loadingDefinitions = true;
      
    //   let endpoint = `/api/vocab/lexemes/definitionlist/${lexemeslug}/`;
    //   let method = "GET";
    //   try {
    //     apiService(endpoint, method).then(data => {
    //         if (data){
    //           console.log(data);
    //           this.definitions = data;
    //           this.loadingDefinitions = false;
    //         } else {
    //           console.log("There was a major problem with the request.");
    //           // console.log(data.message);
    //           this.loadingDefinitions = false;
    //         }
    //     });
    //   } catch (err) {
    //   console.log(err);
    //     this.loadingDefinitions = false;
    //   }
    // },

    editItem(item) {
      this.editedIndex = this.definitions.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.itemEditorDialog = true;
    },

    deleteItem(item) {
      const index = this.definitions.indexOf(item);
      if(confirm("Are you sure you want to remove this definition?")){
        let endpoint = `/api/vocab/inflecteddefinitionz/${item.id}/`;
        let method = "DELETE";
        try {
          apiService(endpoint, method).then(() => {
                this.definitions.splice(index, 1);
                this.deletingDefinition = false;
          });
        } catch (err) {
        console.log(err);
          this.deletingDefinition = false;
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
     submitNew(item){
      this.saving = true;
      let endpoint = `/api/vocab/inflecteddefinitionz/`;
      let method = "POST";
      let payload = {
         inflected_form: this.inflectedid,
         language: item.language,
         definition: item.definition,
         source_citation: item.source_citation,
         source_name: item.source_name,
      }
      try {
        apiService(endpoint, method, payload).then(data => {
            if (data && data.id){
              console.log(data);
              this.definitions.push(data);
              this.saving = false;
              this.close();
            } else {
              console.log((data || "nothing"))
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
      let endpoint = `/api/vocab/inflecteddefinitionz/${item.id}/`;
      let method = "PUT";
      let payload = {
         inflected_form: this.inflectedid,
         language: item.language,
         definition: item.definition,
         source_citation: item.source_citation,
         source_name: item.source_name,
      }
      try {
        apiService(endpoint, method, payload).then(data => {
            if (data && data.id){
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
      },
   },

  
};
</script>

<style></style>
