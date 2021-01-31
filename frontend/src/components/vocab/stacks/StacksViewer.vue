<template>
  <v-container>
     <h1>Vocabulary Card Stacks</h1>

<v-card>
    <v-card-text class="pa-0">
      <v-overlay :value="loadingStacks" absolute>
          <v-progress-circular indeterminate size="64"></v-progress-circular>
      </v-overlay>

      <v-data-table
        :headers="headers"
        :items="stacks"
        :search="search"
        sort-by="name"
        class="elevation-1 desertsand"
      >
        <template v-slot:top>
          <v-toolbar flat class="desertsand">
            <v-toolbar-title>Available Stacks</v-toolbar-title>
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
            <v-dialog v-model="dialog" max-width="500px">
              <template v-slot:activator="{ on }">
                <v-btn color="primary" dark class="mb-2" v-on="on">New Stack</v-btn>
              </template>
              <v-card class="desertsand">
                <v-card-title class="sandstone">
                  <span class="headline">{{ formTitle }}</span>
                </v-card-title>

                <v-card-text class="px-1">
                  <v-container>
                    <v-form v-model="valid">
                        <v-text-field 
                          v-model="editedItem.name" 
                          label="Stack Name"
                          outlined
                          placeholder="super cool stack"
                          counter="200"
                          :rules="[rules.requiredName, rules.maxName,]"
                        ></v-text-field>

                        <v-textarea 
                          v-model="editedItem.description" 
                          label="Stack Description"
                          placeholder="this is a longer description of my new stack..."
                          outlined
                          counter
                          :rules="[rules.requiredDescription, rules.maxDescription]"
                        ></v-textarea>

                      <v-autocomplete
                          v-model="editedItem.learning_language"
                          name="learninglanguage"
                          :items="allLanguages"
                          label="Learning Language*"
                          placeholder="choose the language that is being learned"
                          :loading="loadingLanguages"
                          outlined
                          color="primary"
                          class="mt-2"
                          item-text="name"
                          item-value="name"
                          :rules="[rules.requiredLanguage]"
                      >

                      </v-autocomplete>

                        <v-autocomplete
                            v-model="editedItem.native_language"
                            name="nativelanguage"
                            :items="allLanguages"
                            label="Native Language*"
                            placeholder="choose the native (familiar) language"
                            :loading="loadingLanguages"
                            outlined
                            color="primary"
                            class="mt-2"
                            item-text="name"
                            item-value="name"
                            :rules="[rules.requiredLanguage]"
                        >

                        </v-autocomplete>

                        <v-autocomplete
                            v-model="editedItem.topic"
                            name="topic"
                            :items="allTopics"
                            label="Primary Topic*"
                            placeholder="choose the primary topic area for this stack"
                            :loading="loadingTopics"
                            outlined
                            color="primary"
                            class="mt-2"
                            item-text="name"
                            item-value="name"
                            :rules="[rules.requiredTopic]"
                        >

                        </v-autocomplete>
                        <v-switch
                              v-model="editedItem.public"
                              label="Publicly Visible"
                        ></v-switch>
                    </v-form>
                  </v-container>
                </v-card-text>

                <v-card-actions class="sandstone">
                  <v-spacer></v-spacer>
                  <v-btn color="garbage desertsand--text" @click="close">Cancel</v-btn>
                  <v-btn 
                    color="primary" 
                    :disabled="!valid"
                    @click="submitSave(editedItem)"

                  >
                    Save
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-toolbar>
        </template>
        <template v-slot:item.name="{ item }">
          <a @click.prevent="loadStack(item.slug)">
            <div v-if="item.slug===selectedStack" class="selectedBox">
              {{ item.name }}>
            </div>
            <div v-else>
              {{ item.name }}
            </div>
          </a>
        </template>


        <template v-slot:item.actions="{ item }">
          <v-icon
            v-if="requestUser===item.curator.username"
            small
            class="mr-2"
            @click="editItem(item)"
          >
            mdi-pencil
          </v-icon>
          <v-icon
            small
            v-if="requestUser===item.curator.username"
            @click="deleteItem(item)"
          >
            mdi-delete
          </v-icon>
        </template>
        <template v-slot:no-data>
          <v-btn color="primary" @click="initialize">Reset</v-btn>
        </template>
      </v-data-table>

    </v-card-text>

</v-card>

<div v-if="selectedStack" class="mt-3">
    <StackCurator 
      :slug="selectedStack"
      :key="selectedStack"
    />
</div>
    
  </v-container>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import StackCurator from "@/components/vocab/stacks/StackCurator.vue"

export default {
   name: "StacksViewer",
   components: {
     StackCurator
   },
   props: {},
   data: () => ({
      communityStacks: [],
      search: '',
      selectedStack: null,
      loadingStacks: false,
      loadingLanguages: false,
      loadingTopics: false,
      allLanguages: [],
      allTopics: [],
      valid: false,
      rules: {
        requiredLanguage: value =>
          (value || "").length > 0 ||
          "You must choose a language",

        requiredDescription: value =>
          (value || "").length > 3 ||
          "Description must be at least 4 characters long.",

        maxName: value =>
          (value || "").length <= 200 ||
          'Must be less than 120 characters',

        maxDescription: value =>
          (value || "").length <= 200 ||
          'Must be less than 200 characters',


        requiredName: value =>
          (value || "").length > 3 ||
          "Name must be at least 4 characters long.",


        requiredTopic: typevalue =>
          (typevalue || "").length > 0 || "You must choose a topic.",
      },
      dialog: false,
        headers: [
          {
            text: 'Stack Name',
            align: 'start',
            sortable: true,
            value: 'name',
          },
          { text: 'Learning Language', value: 'learning_language' },
          { text: 'Native Language', value: 'native_language' },
          { text: '# of Cards', value: 'lexeme_pairs.length' },
          { text: 'Curator', value: 'curator.username' },
          { text: 'Actions', value: 'actions', sortable: false },
        ],
        stacks: [],
        userStacks: [],
        editedIndex: -1,
        editedItem: {
          name: '',
          description: '',
          learning_language: '',
          native_language: '',
          topic: '',
          public: true,
        },
        defaultItem: {
          name: '',
          description: '',
          learning_language: '',
          native_language: '',
          topic: '',
          public: true,
        },


   }),
   computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'New Stack' : 'Edit Stack'
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
      this.getTopics();

    },
   methods: {
      loadStacks(){
        this.loadingStacks = true;
        let endpoint = `/api/vocab/cardstackz/`;
        let method = "GET";      
        try {
          apiService(endpoint, method).then(data => {
              if (data){
                console.log(data);
                this.stacks = data;
                this.loadingStacks = false;
              } else {
                console.log("There was a major problem with the request.");
                // console.log(data.message);
                this.loadingStacks = false;
              }
          });
        } catch (err) {
        console.log(err);
          this.loadingStacks = false;
        }
      },

      initialize () {
        this.userStacks = [
          {
            name: 'Simple Adventures - Episode 1',
            curationdate: 'Jun 5, 2020',
            curator: 'ShaykhJake',
            description: 'Some simple vocabulary about learning Arabic',
            topic: 'Sports',
            learning_language: 'Arabic-MSA',
            native_language: 'English',
            card_count: '10',
            id: '2',
            slug: 'blah-blah',
          },
          {
            name: 'Bonjour Monsieur',
            curationdate: 'Jun 5, 2020',
            curator: 'Jake',
            description: 'Some simple vocabulary about learning French',
            topic: 'Sports',
            learning_language: 'French',
            native_language: 'English',
            card_count: '10',
            id: '3',
            slug: 'dah-blah',
          },
          {
            name: 'Unit 1',
            curationdate: 'Jun 2, 2020',
            curator: 'Bob',
            description: 'Some simple vocabulary about learning Russian',
            topic: 'Sports',
            learning_language: 'Russian',
            native_language: 'English',
            card_count: '10',
            id: '4',
            slug: 'mah-blah',
          }, 
        ]
      },

      editItem (item) {
        this.editedIndex = this.stacks.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },
      deleteItem(item){
        confirm('Are you sure you want to delete this item?') && this.submitDelete(item);
      }, 
      submitDelete (item) {
        const index = this.stacks.indexOf(item)
        this.deleting = true;
        let endpoint = `/api/vocab/cardstackz/${item.slug}/`;
        let method = "DELETE";

        try {
          apiService(endpoint, method).then(() => {
            this.stacks.splice(index, 1)
            this.deleting = false;
          });
        } catch (err) {
        console.log(err);
          this.deleting = false;
        }
      },
      handleClick(value) {
        this.selectedStack = null;
        this.selectedStack = value.id;
        console.log(this.selectedStack)
        console.log(value)
      },
      close () {
        this.dialog = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },

      save () {
        if (this.editedIndex > -1) {
          Object.assign(this.stacks[this.editedIndex], this.editedItem)
        } else {
          this.stacks.push(this.editedItem)
        }
        this.close()
      },
      loadStack(slug){
        this.selectedStack=slug;
        console.log(slug)
      },
      submitSave(item){
        this.saving = true;
        let endpoint = `/api/vocab/cardstackz/`;
        let method = "POST";
        if(item.slug){
          endpoint = endpoint + `${item.slug}/`;
          method = "PATCH";
        }
        let payload = {
          name: item.name,
          description: item.description,
          learning_language: item.learning_language,
          native_language: item.native_language,
          topic: item.topic,
          public: item.public,
        }
        try {
          apiService(endpoint, method, payload).then(data => {
            if (data && data.slug){
              if (this.editedIndex > -1) {
                Object.assign(this.stacks[this.editedIndex], data)
              } else {
                this.stacks.push(data)
              }
              this.close()
              this.saving = false;
              this.selectedStack=null;
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
      getTopics() {
        var localTopics = localStorage.getItem("topics");
        if (localTopics.length > 1) {
          console.log("Shop local!");
          this.allTopics = JSON.parse(localTopics);
        } else {
          this.loadingTopics = true;
          let endpoint = `/api/categories/topics/`;
          try {
            apiService(endpoint).then(data => {
              if (data != null) {
                this.allTopics = data;
                this.error = false;
              } else {
                console.log("Something bad happened...");
                this.error = true;
              }
              this.loadingTopics = false;
            });
          } catch (err) {
            console.log(err);
          }
        }
      },

   },
   mounted(){
     this.loadStacks();
   }


}
</script>

<style scoped>
.selectedBox {
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