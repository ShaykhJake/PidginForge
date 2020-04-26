<template>
  <v-dialog
    v-model="editorDialog"
    scrollable
    persistent
    fullscreen
    hide-overlay
    transition="dialog-bottom-transition"
  >
    <v-card class="ma-0 desertsand" max-width="500">
      <v-card-title class="pb-1 calligraphy desertsand--text">
        <v-spacer></v-spacer>
        <span v-if="!editing">Import Audio Element</span>
        <span v-else>Edit Audio Element</span>
        <v-spacer></v-spacer>
      </v-card-title>
      <v-card-text class="pa-1 desertsand">
        <v-row wrap dense justify="center">
          <v-col cols="12" sm="10" md="8" lg="6">
            <p class="body-2 mx-2 black--text text-justify text-wrap">
              It is the responsibility of the uploader of this audio element to
              ensure that copyright permissions have been properly secured with
              the content's creator. All imported material must have an
              appropriate source citation included.
            </p>

            <v-row wrap dense no-gutters>
              <v-col cols="12">
                <v-row dense no-gutters>
                  <v-col cols="12" v-if="loaded">
                    Current Audio File:
                    <span class="font-weight-black black--text">
                      {{ audio.originalfilename }}</span
                    >
                  </v-col>
                  <v-col cols="12" class="mt-3">
                    <v-file-input
                      v-if="loadNewFile"
                      show-size
                      :rules="[rules.maxAudioSize]"
                      @change="setAudio"
                      accept="audio/mpeg"
                      placeholder="Pick a valid mp3 audio file"
                      prepend-icon="mdi-volume-high"
                      label="Audio File"
                      outlined
                      ref="input"
                    >
                    </v-file-input>
                  </v-col>
                  <v-col cols="12" align="center" v-if="loaded && !loadNewFile">
                    <AudioPlayerComponent
                      :file="audioFile"
                      color="calligraphy"
                      class="sandstone"
                      @passDuration="passDuration"
                    />
                    <v-btn
                      block
                      small
                      class="elements desertsand--text mt-2"
                      @click="loadNewFile = true"
                      >Choose New File<v-icon right>mdi-volume-high</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
              </v-col>
              <v-col cols="12">
                <v-alert :hidden="!alertActive" :type="alertType" dense>
                  {{ alertMessage }}
                </v-alert>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-form
                  ref="details"
                  v-model="valid"
                  @submit.prevent
                  v-if="loaded"
                  :hidden="success || (!loaded && !editing)"
                >
                  <v-text-field
                    v-model="audio.title"
                    name="audiotitle"
                    label="Element Title*"
                    placeholder="give this item a title"
                    :rules="[rules.requiredTitle]"
                    outlined
                  ></v-text-field>

                  <v-select
                    v-model="audio.language"
                    name="audiolanguage"
                    :items="allLanguages"
                    label="Target Language*"
                    placeholder="choose a target language"
                    :rules="[rules.requiredLanguage]"
                    required
                    :loading="loadingLanguages"
                    outlined
                  ></v-select>

                  <v-select
                    v-model="audio.topic"
                    name="audiotopic"
                    :items="allTopics"
                    label="Primary Topic*"
                    placeholder="choose the primary topic"
                    :rules="[rules.requiredTopic]"
                    required
                    :loading="loadingTopics"
                    outlined
                  ></v-select>

                  <v-textarea
                    outlined
                    name="learningpurpose"
                    label="Language Learning Purpose*"
                    v-model="audio.purpose"
                    :rules="[rules.requiredPurpose]"
                    counter
                    rows="3"
                    maxlength="300"
                  ></v-textarea>

                  <v-textarea
                    outlined
                    name="sourcecitation"
                    label="Source Citation*"
                    v-model="audio.citation"
                    :rules="[rules.requiredCitation]"
                    counter
                    rows="3"
                    maxlength="300"
                  ></v-textarea>

                  <v-textarea
                    outlined
                    name="audionotes"
                    label="Curator Notes"
                    v-model="audio.notes"
                    value=""
                    rows="3"
                    counter
                    maxlength="300"
                  ></v-textarea>
                  <v-combobox
                    label="Additional Topic Tags"
                    name="audiotags"
                    v-model="audio.tags"
                    chips
                    clearable
                    hint="Hit <enter> or <tab> after each entry (max of 5 tags allowed)"
                    persistent-hint
                    multiple
                    :rules="[rules.maxTags]"
                    outlined
                    counter
                  >
                    <template
                      v-slot:selection="{ attrs, item, select, selected }"
                    >
                      <v-chip
                        v-bind="attrs"
                        :input-value="selected"
                        close
                        class="calligraphy desertsand--text"
                        @click="select"
                        @click:close="removeTag(item)"
                      >
                        <strong>{{ item }}</strong
                        >&nbsp;
                      </v-chip>
                    </template>
                  </v-combobox>
                </v-form>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions class="calligraphy">
        <v-spacer></v-spacer>
        <v-btn color="garbage desertsand--text" @click="closeDialog"
          >Cancel<v-icon right>mdi-close</v-icon></v-btn
        >
        <v-btn
          color="success"
          @click="submitAudioElement"
          :disabled="!valid || !loaded"
          :loading="submitting"
          >Submit<v-icon right>mdi-thumb-up</v-icon></v-btn
        >
        <v-spacer></v-spacer>
        <!-- TODO: need to ensure that the user information is reloaded after saving -->
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import { apiService } from "@/common/api.service.js";
import { apiFileService } from "@/common/api.fileservice.js";
export default {
  name: "audioElementEditor",
  components: {
    AudioPlayerComponent: () =>
      import("@/components/elements/AudioPlayerComponent.vue")
  },
  props: {
    editorDialog: Boolean,
    editing: {
      type: Boolean,
      default: false
    },
    audio: {
      type: Object
    }
  },
  data: () => ({
    // userData: Object,
    loadNewFile: false,
    audioPlayerKey: 0,
    loaded: false,
    newFileLoaded: false,
    existingSlug: "",
    existingTitle: "",
    newAudioID: "",
    audioFile: "",
    audioFileName: "",
    duration: "",
    // items: ['Streaming', 'Eating'],

    // use this audio as a sample of a audio that exists: -YJSDJGyIaU, this does not: KmOAznOQX-g
    available: false,
    submitting: false,
    valid: true,
    success: false,
    fitParent: true,
    alertType: "success",
    alertMessage: "It's all good!",
    alertActive: false,
    allLanguages: [],
    loadingLanguages: false,
    loadingTopics: false,
    allTopics: [],
    rules: {
      requiredTitle: value =>
        (value || "").length > 5 ||
        "You must provide a title of at least 6 characters.",
      requiredLanguage: languagevalue =>
        (languagevalue || "").length > 0 ||
        "You must choose at least 1 language.",
      requiredTopic: topicvalue =>
        (topicvalue || "").length > 0 || "You must choose a primary topic.",
      requiredPurpose: purposevalue =>
        !!purposevalue || "You must provied a learning purpose.",
      requiredCitation: citationvalue =>
        !!citationvalue || "You must provied a source citation.",
      maxTags: tagsvalue =>
        (tagsvalue || "").length < 6 || "Maximum of 5 tags allowed!",
      maxAudioSize: value =>
        !value || value.size < 5000000 || "Audio file should be under 5MB!"
    }
  }),
  computed: {},
  methods: {
    closeDialog() {
      this.$emit("closeDialog");
    },
    chooseNewFile() {
      this.loadNewFile = true;
    },
    removeTag(item) {
      this.audio.tags.splice(this.audio.tags.indexOf(item), 1);
      this.audio.tags = [...this.audio.tags];
    },

    clearWarnings() {
      this.alertActive = false;
    },
    passDuration(duration) {
      this.duration = duration;
    },
    setAudio(newaudio) {
      if (newaudio) {
        const file = newaudio;
        if (file.type.indexOf("audio/") === -1) {
          alert("Please select an audio file");
          return;
        } else {
          this.audio.audiofile = newaudio;
          this.audio.originalfilename = newaudio.name;
        }
        if (typeof FileReader === "function") {
          const reader = new FileReader();
          reader.onload = event => {
            this.audioFile = event.target.result;
            console.log("Ready!");
            this.loadNewFile = false;
            this.newFileLoaded = true;
            this.loaded = true;
          };
          reader.readAsDataURL(file);
        } else {
          alert("Sorry, FileReader API not supported");
        }
      } else {
        this.loaded = false;
        this.audioFile = "";
      }
    },
    getLanguages() {
      this.loadingLanguages = true;
      let endpoint = `/api/categories/languages/`;
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
    },

    getTopics() {
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
    },
    parseDuration(duration) {
      var matches = duration.match(/[0-9]+[HMS]/g);

      var seconds = 0;

      matches.forEach(function(part) {
        var unit = part.charAt(part.length - 1);
        var amount = parseInt(part.slice(0, -1));

        switch (unit) {
          case "H":
            seconds += amount * 60 * 60;
            break;
          case "M":
            seconds += amount * 60;
            break;
          case "S":
            seconds += amount;
            break;
          default:
          // noop
        }
      });

      return seconds;
    },

    setEditingAudioData() {
      if (this.editing) {
        // LOAD AUDIO ELEMENT FROM SERVER
        this.audioFile = this.audio.audiofile;
        this.loaded = true;
      } else {
        this.loadNewFile = true;
        this.loaded = false;
      }
    },
    updateViewer(audio) {
      this.$emit("updateViewer", audio);
    },

    submitAudioElement() {
      // The following grabs the blob, converts to a JPEG, wraps it, and sends it to the API
      this.submitting = true;
      let endpoint = `/api/elements/audioz/`;
      let method = "POST";
      if (this.audio.slug !== undefined) {
        endpoint += `${this.audio.slug}/`;
        method = "PATCH";
      }
      const formData = new FormData();
      if (this.newFileLoaded) {
        formData.append("audiofile", this.audio.audiofile);
        formData.append("originalfilename", this.audio.originalfilename);
      }
      formData.append("title", this.audio.title);
      formData.append("language", this.audio.language);
      formData.append("topic", this.audio.topic);
      formData.append("purpose", this.audio.purpose);
      formData.append("duration", this.duration || 0);
      formData.append("citation", this.audio.citation);
      formData.append("notes", this.audio.notes);
      formData.append("tags", this.audio.tags);

      apiFileService(endpoint, method, formData).then(data => {
        if (data) {
          if (this.editing === false) {
            this.$router.push({
              name: "Media-Viewer",
              params: { elementtype: "Audio", elementslug: data.slug }
            });
          } else {
            // this.alertActive = false;
            this.updateViewer(data);
            this.closeDialog();
          }
        } else {
          console.log("There was a major problem with the request.");
          // console.log(data.message);
        }
        this.submitting = false;
      });
    }
  },
  created() {
    this.getLanguages();
    this.getTopics();
    this.setEditingAudioData();
  }
};
</script>
<style scoped>
audio {
  width: 100%;
  background-image: none !important;
}
.mejs-container {
  background-image: none !important;
}
button.v-btn[disabled] {
  opacity: 1;
  color: green;
}
@media screen and (max-width: 450px) {
  iframe {
    width: 100%;
    height: 180px;
  }
}
@media screen and (max-width: 768px) {
  iframe {
    width: 100%;
    height: 180px;
  }
}
</style>
