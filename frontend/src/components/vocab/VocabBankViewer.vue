<template>
  <v-data-table
    :headers="headers"
    :items="lexemes"
    sort-by="lexeme"
    class="elevation-5 desertsand"
  >
    <template v-slot:top>
      <v-toolbar flat color="desertsand">
        <v-toolbar-title>My Vocab</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
        <v-btn small>
          Play Game
        </v-btn>
        <v-btn small>
          Import Selected
        </v-btn>
        
        <v-dialog v-model="dialog" max-width="500px">
          <template v-slot:activator="{ on }">
            <v-btn small color="primary" v-on="on"
              >New Lexeme</v-btn
            >
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedItem.lexeme"
                      label="Lexeme"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedItem.translation"
                      label="Translation"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedItem.partofspeech"
                      label="Part of Speech"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedItem.root"
                      label="Root"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedItem.context"
                      label="Context"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click="save">Save</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon small class="mr-2" @click="editItem(item)">
        mdi-pencil
      </v-icon>
      <v-icon small @click="deleteItem(item)">
        mdi-delete
      </v-icon>
    </template>
    <template v-slot:no-data>
      <v-btn color="primary" @click="initialize">Reset</v-btn>
    </template>
  </v-data-table>
</template>

<script>
export default {
  name: "VocabBankViewer",
  data: () => ({
    dialog: false,
    returnCommand: function() {},
    headers: [
      {
        text: "Lexeme",
        align: "start",
        value: "lexeme"
      },
      { text: "Translation", value: "translation" },
      { text: "Part of Speech", value: "partofspeech" },
      { text: "Root", value: "root" },
      { text: "Context", value: "context" },
      { text: "Actions", value: "actions", sortable: false }
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
      return this.editedIndex === -1 ? "New Lexeme" : "Edit Lexeme";
    }
  },

  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      this.lexemes = [
        {
          lexeme: "اشترك في",
          translation: "to participate in",
          partofspeech: "verb",
          root: "شرك",
          context: "اشتركتُ في بناء الموقع"
        },
        {
          lexeme: "شخص",
          translation: "person",
          partofspeech: "noun",
          root: "شخص",
          context: "رأيت شخص مشتبه به"
        },
        {
          lexeme: "طائرة",
          translation: "airplane",
          partofspeech: "noun",
          root: "طار يطير",
          context: "افادت نشرة الاخبار بأن طائرة فرنسية اصتدمت ببرج ايفل"
        }
      ];
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

    deleteItem(lexeme) {
      const index = this.lexemes.indexOf(lexeme);
      confirm("Are you sure you want to delete this lexeme?") &&
        this.lexemes.splice(index, 1);
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
        console.log(this.returnCommand);
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
