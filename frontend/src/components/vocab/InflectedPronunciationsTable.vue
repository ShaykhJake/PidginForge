<template>
  <div>
    <v-row dense>
      <v-col class="pl-2" cols="6">
        <span class="body-1 font-weight-black">
          Pronunciations ({{ pronunciations.length }})
        </span>
      </v-col>
      <v-col cols="6" align="right">
        <v-btn small color="primary" dark class="mr-2" @click="addItem"
          >Add Pronunciation
        </v-btn>
      </v-col>
    </v-row>

    <div  class="mx-1">
      <v-row 
        v-for="(item, index) in pronunciations" 
        :key="index"
        flat
        class="mb-1 desertsand"
        dense
      >
        <v-col class="body-1">
          <div  class="roundBox">
            {{ item.text }}
            <v-btn small v-if="item.audio_file" icon @click="playAudio(item.audio_file)"><v-icon>mdi-volume-high</v-icon></v-btn>
          </div>
          <div class="overline">
            Curated by 
            <span class="primary--text font-weight-black">
                {{ item.curator.username }}
            </span> 
             on {{ item.curationdate }}
          </div>
        </v-col>
        <v-col cols="1" align="right">
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
            :loading="deletingPronunciation"
            v-if="requestUser === item.curator.username"
          >
            mdi-delete
          </v-icon>
        </v-col>
      </v-row>
    </div>


    <v-dialog v-if="itemEditorDialog" v-model="itemEditorDialog" max-width="500px">
      <v-card class="desertsand">
        <v-card-title class="sandstone">
          <span class="headline">{{ formTitle }}</span>
        </v-card-title>

        <v-card-text>

              <v-form v-model="valid" class="mt-2">

                <v-text-field
                  v-model="editedItem.text"
                  label="Pronunciation Text*"
                  placeholder="prŏ-nun-si-ay-shŏn"
                  outlined
                  :rules="[rules.requiredPronunciation]"
                ></v-text-field>

                <v-switch v-model="useAudio" label="Attach Audio" class="py-0 my-0"></v-switch>
                
                <AudioRecorder 
                  v-if="useAudio"
                  :currentAudio="editedItem.audio_file"
                  @selectAudio="selectAudio"
                />
                
              </v-form>

        </v-card-text>

        <v-card-actions class="sandstone">
          <v-spacer></v-spacer>
          <v-btn color="garbage desertsand--text" @click="close">Cancel</v-btn>
          <v-btn color="primary" :disabled="!valid || (useAudio && !audioAttachment)" @click="submitSave" :loading="saving">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog max-width=300 v-model="audioDialog" v-if="audioDialog">
      <v-card>
        <audio controls autoplay :src="selectedAudio"
        >
        </audio>
        <v-card-actions class="justify-center">
          <v-btn @click="audioDialog=false" class="garbage desertsand--text">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import { apiFileService } from "@/common/api.fileservice.js";

export default {
  name: "InflectedPronunciationsTable",
  components: {
      AudioRecorder: () => import("@/components/recorder/AudioRecorder.vue"),
  },
  props: {
    inflectedid: [String, Number],
    pronunciations: Array,
  },
  data: () => ({
    audioSource: "file",
    // pronunciations: [],
    allLanguages: [],

    audio: {},
    
    audioAttachment: null,
    audioFile: null,
    newFileLoaded: false,

    useAudio: false,

    itemEditorDialog: false,
    audioDialog:false,
    selectedAudio: null,
    loadingPronunciations: false,
    deletingPronunciation: false,
    saving: false,

    valid: false,

    // returnCommand: function() {},
    headers: [
      {
        text: "Curator",
        align: "start",
        value: "curator.username"
      },
      { text: "Date Added", value: "curationdate" },
      { text: "Pronunciation", value: "text" },
      { text: "Audio", value: "audio_file" },
      { text: "Actions", value: "actions", sortable: false }
    ],
      rules: {
         requiredPronunciation: value =>
         (value || "").length > 1 ||
         "The definition must be at least 2 characters in length.",

        maxAudioSize: value =>
        !value || value.size < 500000 || "Audio files for pronunciations must be under 500kb!"

      },

    editedIndex: -1,
    editedItem: {
      id: null,
      audio_file: null,
      text: "",
    },
    defaultItem: {
      id: null,
      audio_file: null,
      text: "",
    }

  }),

  computed: {
    requestUser(){
       return localStorage.getItem("username");
    }, 
    formTitle() {
      return this.editedIndex === -1 ? "Add Pronunciation" : "Edit Pronunciation";
    },
  },
  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  mounted() {
    // this.loadPronunciations(this.lexemeslug);
  },
  created() {

  },

  methods: {

    addItem() {
      // this.editedItem = this.defaultItem;
      // this.editedItem.text = "";
      this.useAudio = false;
      this.itemEditorDialog = true;
      // this.returnCommand = command;
    },

    selectAudio(audio){
      this.newFileLoaded = true;
      this.audioAttachment = audio;

      // console.log(this.audioAttachment)
      // console.log(this.audioAttachment.audioBits)
    },


    editItem(item) {
      this.editedIndex = this.pronunciations.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.editedItem.audio_file ? this.useAudio = true : this.useAudio = false;
      this.itemEditorDialog = true;
    },

    deleteItem(item) {
      const index = this.pronunciations.indexOf(item);
      if(confirm("Are you sure you want to remove this definition?")){
        let endpoint = `/api/vocab/inflectedpronunciationz/${item.id}/`;
        let method = "DELETE";
        try {
          apiService(endpoint, method).then(() => {
                this.pronunciations.splice(index, 1);
                this.deletingPronunciation = false;
          });
        } catch (err) {
        console.log(err);
          this.deletingPronunciation = false;
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

  
    submitSave(item) {
      // The following grabs the blob and sends it to the API
      this.saving = true;
      var endpoint = "";
      var method = "";
      if(item.id){
        // Item exists and needs patching
        endpoint = `/api/vocab/inflectedpronunciationz/${item.id}`;
        method = "PATCH";
      } else {
        // Item is new and needs posting
        endpoint = `/api/vocab/inflectedpronunciationz/`;
        method = "POST";
      }
      const formData = new FormData();
      // Check for whether or not audio is being attached
      if (this.useAudio && this.newFileLoaded && this.audioAttachment) {
        formData.append("audio_file", this.audioAttachment.audioFile);
        formData.append("originalfilename", this.audioAttachment.originalfilename);
      }
      formData.append("text", this.editedItem.text);
      formData.append("inflected_form", this.inflectedid);
    
      try {
        apiFileService(endpoint, method, formData).then(data => {
          if (data && data.id) {
              if(item.id){
                Object.assign(this.pronunciations[this.editedIndex], this.editedItem);
                this.saving = false;
                this.close();
              } else {
                this.pronunciations.push(data);
                this.saving = false;
                this.close();
              }
            } else {
              console.log((data || "no data"))
              console.log("Something bad happened")
              this.saving=false;
            }
            this.submitting = false;
        });
      } catch (err) {
        console.log(err);
        this.saving = false;
      } 
    },
    playAudio(audio){
      this.selectedAudio = audio;
      this.audioDialog = true;
    }


   },

  
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
</style>
