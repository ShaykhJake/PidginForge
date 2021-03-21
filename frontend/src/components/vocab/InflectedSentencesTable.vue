<template>
  <div>
    <v-row dense>
      <v-col class="pl-2" cols="6">
        <span class="body-1 font-weight-black">
          Sentences ({{ sentences.length }})
        </span>
      </v-col>
      <v-col cols="6" align="right">
        <v-btn small color="primary" dark class="mr-2" @click="addItem"
          >Attach Sentence
        </v-btn>
      </v-col>
    </v-row>

    <div class="mx-1">
      <v-row
        v-for="(item, index) in sentences"
        :key="index"
        flat
        class="mb-1 desertsand"
        dense
      >
        <v-col class="body-1">
          <div
            :style="`direction: ${item.full_sentence.direction}`"
            class="roundBox"
          >
            {{ item.full_sentence.text }}
          </div>
          <v-row dense wrap>
            <v-col>
              <div class="overline">
                Translations: {{ item.full_sentence.translations.length }} ;
                Audio Samples: {{ item.full_sentence.audio.length }}
              </div>
              <div class="overline">
                Curated by
                <span class="primary--text font-weight-black">
                  {{ item.curator.username }}
                </span>
                on {{ item.curationdate }}
              </div>
            </v-col>
            <v-col align="right">
              <v-btn
                small
                class="primary--text"
                text
                @click="
                  viewingID = item.full_sentence.id;
                  viewerDialog = true;
                "
              >
                View Sentence Details
              </v-btn>
            </v-col>
          </v-row>
        </v-col>

        <v-col cols="1" align="right">
          <v-icon
            small
            @click="deleteItem(item)"
            :loading="deleting"
            v-if="requestUser === item.curator.username"
          >
            mdi-delete </v-icon
          ><br />
        </v-col>
      </v-row>
    </div>

    <SentenceViewer
      v-if="viewerDialog"
      :sentence-i-d="viewingID"
      :dialog="viewerDialog"
      @closeDialog="viewerDialog = false"
    />

    <v-dialog
      v-if="itemEditorDialog"
      v-model="itemEditorDialog"
      max-width="500px"
    >
      <v-card class="desertsand">
        <v-card-title class="sandstone">
          {{ formTitle }}
        </v-card-title>

        <v-card-text class="px-3 pt-2">
          <v-progress-linear
            v-if="searchingSentences"
            color="primary"
            height="25"
            indeterminate
          >
            <strong>Searching</strong>
          </v-progress-linear>

          <div v-if="!searchingSentences">
            <h2>Search Results ({{ searchResults.length }})</h2>
            <v-list
              two-line
              class="sandstone"
              outlined
              v-if="searchResults.length > 0"
            >
              <template v-for="(item, index) in searchResults">
                <v-subheader
                  v-if="item.header"
                  :key="item.header"
                  v-text="item.header"
                ></v-subheader>

                <v-divider
                  v-else-if="item.divider"
                  :key="index"
                  :inset="item.inset"
                ></v-divider>

                <v-list-item
                  v-else
                  :key="item.id"
                  @click="
                    selectedItem = item.id;
                    addNewSentence = false;
                  "
                  :class="item.id === selectedItem ? 'primary lighten-2' : ''"
                >
                  <v-list-item-content>
                    <v-list-item-title>
                      <div :style="`direction:${item.direction}`">
                        {{ item.text }}
                      </div>
                    </v-list-item-title>
                    <v-list-item-subtitle>
                      Curated by {{ item.curator.username }} on
                      {{ item.curationdate }}
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </template>
            </v-list>
            <span class="overline" v-if="searchResults.length < 1"
              >No additional sentences were found. Please add a new
              sentence.</span
            >
            <hr />

            <div style="text-align: center;" v-if="!addNewSentence">
              <span> Don't see what you like? </span><br />
              <v-btn
                small
                class="primary"
                @click="
                  addNewSentence = true;
                  selectedItem = null;
                "
                >Add New Sentence</v-btn
              >
            </div>

            <div v-if="addNewSentence" class="mt-3">
              <h2>Add New Sentence</h2>
              <span class="overline"
                >Your new sentence's language will automatically be set to the
                parent word/term's language:
                <v-chip class="languages languages--text" outlined small>
                  {{ language }}
                </v-chip>
              </span>
              <v-form v-model="valid" class="mt-3">
                <v-textarea
                  :style="`direction: ${direction}`"
                  v-model="newSentence.text"
                  label="Sentence Text*"
                  placeholder="i am a fun sentence"
                  outlined
                  :reverse="direction === 'RTL' ? true : false"
                  :rules="[rules.requiredSentence]"
                ></v-textarea>
                <v-text-field
                  v-model="newSentence.curator_note"
                  label="Curator Note*"
                  placeholder="curator note"
                  outlined
                  :rules="[rules.requiredCuratorNote]"
                ></v-text-field>
              </v-form>
              <span class="overline"
                >You must submit your new sentence before attaching it to the
                associated word/term.</span
              >
              <br />
              <v-btn
                :disabled="!valid"
                class="primary"
                @click="submitNewSentence"
              >
                Submit
              </v-btn>
            </div>
          </div>
        </v-card-text>

        <v-card-actions class="sandstone">
          <v-spacer></v-spacer>
          <v-btn color="garbage desertsand--text" @click="close">Cancel</v-btn>
          <v-btn
            color="primary"
            :disabled="!selectedItem"
            @click="submitAttach"
            :loading="attaching"
            >Attach</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog max-width="300" v-model="audioDialog" v-if="audioDialog">
      <v-card>
        <audio controls autoplay :src="selectedAudio"></audio>
        <v-card-actions class="justify-center">
          <v-btn @click="audioDialog = false" class="garbage desertsand--text"
            >Close</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import { apiFileService } from "@/common/api.fileservice.js";

export default {
  name: "InflectedSentencesTable",
  components: {
    // AudioRecorder: () => import("@/components/recorder/AudioRecorder.vue"),
    SentenceViewer: () =>
      import("@/components/vocab/sentences/SentenceViewer.vue")
  },
  props: {
    inflectedid: [String, Number],
    sentences: Array,
    direction: String,
    language: String
  },
  data: () => ({
    audioSource: "file",
    // sentences: [],
    allLanguages: [],

    audio: {},
    searchResults: [],
    audioAttachment: null,
    audioFile: null,
    newFileLoaded: false,
    selectedItem: null,
    useAudio: false,

    itemEditorDialog: false,
    audioDialog: false,
    selectedAudio: null,
    searchingSentences: false,
    loadingSentences: false,
    viewerDialog: false,
    attaching: false,
    deleting: false,
    saving: false,
    viewingID: null,

    addNewSentence: false,
    newSentence: {
      curator_note: "none"
    },
    defaultNew: {
      curator_note: "none"
    },

    valid: false,

    // returnCommand: function() {},
    headers: [
      {
        text: "Curator",
        align: "start",
        value: "curator.username"
      },
      { text: "Date Added", value: "curationdate" },
      { text: "Sentence", value: "text" },
      { text: "Audio", value: "audio_file" },
      { text: "Actions", value: "actions", sortable: false }
    ],
    rules: {
      requiredSentence: value =>
        (value || "").length > 4 ||
        "The sentence must be at least 5 characters in length.",

      requiredCuratorNote: value =>
        (value || "").length > 2 ||
        "The curator note must be at least 3 characters in length."
    },

    editedIndex: -1,
    editedItem: {
      id: null,
      audio_file: null,
      text: ""
    },
    defaultItem: {
      id: null,
      audio_file: null,
      text: ""
    }
  }),

  computed: {
    requestUser() {
      return localStorage.getItem("username");
    },
    formTitle() {
      return this.editedIndex === -1 ? "Attach Sentence" : "Edit Sentence";
    }
  },
  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  mounted() {
    // this.loadSentences(this.lexemeslug);
  },
  created() {},

  methods: {
    addItem() {
      // this.editedItem = this.defaultItem;
      // this.editedItem.text = "";
      // this.useAudio = false;
      this.itemEditorDialog = true;
      this.searchSentences(this.inflectedid);
      // this.returnCommand = command;
    },

    selectAudio(audio) {
      this.newFileLoaded = true;
      this.audioAttachment = audio;

      // console.log(this.audioAttachment)
      // console.log(this.audioAttachment.audioBits)
    },

    editItem(item) {
      this.editedIndex = this.sentences.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.editedItem.audio_file
        ? (this.useAudio = true)
        : (this.useAudio = false);
      this.itemEditorDialog = true;
    },

    deleteItem(item) {
      const index = this.sentences.indexOf(item);
      if (confirm("Are you sure you want to detach this sentence?")) {
        let endpoint = `/api/vocab/inflectedsentencez/${item.id}/`;
        let method = "DELETE";
        try {
          apiService(endpoint, method).then(() => {
            this.sentences.splice(index, 1);
            this.deleting = false;
          });
        } catch (err) {
          console.log(err);
          this.deleting = false;
        }
      }
      // Sent DELETE message to API to fully remove...
    },

    close() {
      this.itemEditorDialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign(this.editedItem, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    searchSentences(wordID) {
      this.searchingSentences = true;

      let endpoint = `/api/vocab/sentences/searchwords/${wordID}/`;
      let method = "GET";
      try {
        apiService(endpoint, method).then(data => {
          if (data) {
            console.log(data);
            if (data.length > 0 && this.sentences.length > 0) {
              for (let i = 0; i < this.sentences.length; i++) {
                for (let x = 0; x < data.length; x++) {
                  if (this.sentences[i].id === data[x].id) {
                    data.splice(x, 1);
                    break;
                  }
                }
              }
            }
            this.searchResults = data;
            this.searchingSentences = false;
          } else {
            console.log("There was a major problem with the request.");
            // console.log(data.message);
            this.searchingSentences = false;
          }
        });
      } catch (err) {
        console.log(err);
        this.searchingSentences = false;
      }
    },

    submitNewSentence() {
      this.saving = true;

      const endpoint = `/api/vocab/sentencez/`;
      const method = "POST";
      const payload = {
        text: this.newSentence.text,
        language: this.language,
        curator_note: this.newSentence.curator_note
      };

      try {
        apiService(endpoint, method, payload).then(data => {
          if (data && data.id) {
            console.log(data);
            this.selectedItem = data.id;
            this.searchResults.push(data);
            this.saving = false;
            this.addNewSentence = false;
            this.newSentence = this.defaultNew;
          } else {
            console.log("Something bad happended!");
            this.saving = false;
          }
        });
      } catch (err) {
        console.log(err);
        this.saving = false;
      }
    },

    submitAttach() {
      this.attaching = true;

      const endpoint = `/api/vocab/inflectedsentencez/`;
      const method = "POST";
      const payload = {
        sentence: this.selectedItem,
        inflected_form: this.inflectedid
      };

      try {
        apiService(endpoint, method, payload).then(data => {
          if (data && data.id) {
            console.log(data);
            this.attaching = false;
            this.sentences.push(data);
            this.itemEditorDialog = false;
          } else {
            console.log("Something bad happended!");
            this.attaching = false;
          }
        });
      } catch (err) {
        console.log(err);
        this.attaching = false;
      }
    },

    submitSave(item) {
      // The following grabs the blob and sends it to the API
      this.saving = true;
      var endpoint = "";
      var method = "";
      if (item.id) {
        // Item exists and needs patching
        endpoint = `/api/vocab/inflectedsentencez/${item.id}`;
        method = "PATCH";
      } else {
        // Item is new and needs posting
        endpoint = `/api/vocab/inflectedsentencez/`;
        method = "POST";
      }
      const formData = new FormData();
      // Check for whether or not audio is being attached
      if (this.useAudio && this.newFileLoaded && this.audioAttachment) {
        formData.append("audio_file", this.audioAttachment.audioFile);
        formData.append(
          "originalfilename",
          this.audioAttachment.originalfilename
        );
      }
      formData.append("text", this.editedItem.text);
      formData.append("inflected_form", this.inflectedid);

      try {
        apiFileService(endpoint, method, formData).then(data => {
          if (data && data.id) {
            if (item.id) {
              Object.assign(this.sentences[this.editedIndex], this.editedItem);
              this.saving = false;
              this.close();
            } else {
              this.sentences.push(data);
              this.saving = false;
              this.close();
            }
          } else {
            console.log(data || "no data");
            console.log("Something bad happened");
            this.saving = false;
          }
          this.submitting = false;
        });
      } catch (err) {
        console.log(err);
        this.saving = false;
      }
    },
    playAudio(audio) {
      this.selectedAudio = audio;
      this.audioDialog = true;
    }
  }
};
</script>

<style scoped>
.roundBox {
  color: black;
  background-color: antiquewhite;
  border-left-style: solid;
  border-right-style: solid;
  border-width: 1px;
  border-radius: 5px;
  border-color: grey;
  padding: 2px 2px 2px 2px;
}
.listBox {
  color: black;
  background-color: antiquewhite;
  border-style: solid;
  border-width: 1px;
  border-radius: 10px;
  border-color: grey;
  padding: 2px 2px 2px 2px;
}
</style>
