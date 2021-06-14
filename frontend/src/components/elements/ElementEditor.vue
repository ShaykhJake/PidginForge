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
        <span v-if="isNewElement">Curate New Element</span>
        <span v-else>Edit Element</span>
        <v-spacer></v-spacer>
      </v-card-title>
      <v-card-text class="pa-1 desertsand">
        <v-row wrap dense justify="center">
          <v-col cols="12" sm="10" md="8" lg="6">
            <p class="body-2 mx-2 black--text text-justify text-wrap">
              It is the responsibility of the uploader of this text element to
              ensure that copyright permissions have been properly secured with
              the content's creator. All imported material must have an
              appropriate source citation included. If it is the curator's own
              original work, or it is public domain, please cite that (i.e.
              'original work of the curator').
            </p>

            <v-row>
              <v-col>
                <v-form
                  ref="details"
                  v-model="valid"
                  @submit.prevent
                  v-if="loaded"
                >
                  <v-text-field
                    v-model="elementObject.title"
                    name="texttitle"
                    label="Element Title*"
                    placeholder="give this item a title"
                    :rules="[rules.requiredTitle]"
                    outlined
                    class="pb-0 mb-0"
                  ></v-text-field>

                  <v-select
                    v-model="elementObject.language"
                    name="textlanguage"
                    :items="allLanguages"
                    label="Target Language*"
                    placeholder="choose a target language"
                    :rules="[rules.requiredLanguage]"
                    required
                    :loading="loadingLanguages"
                    outlined
                  ></v-select>

                  <v-textarea
                    outlined
                    name="description"
                    label="Description*"
                    v-model="elementObject.description"
                    :rules="[rules.requiredDescription]"
                    counter
                    rows="3"
                    maxlength="300"
                  ></v-textarea>

                  <v-combobox
                    label="Topic Tags"
                    name="texttags"
                    v-model="elementObject.tags"
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

                  <v-textarea
                    outlined
                    name="sourcecitation"
                    label="Source Citation*"
                    v-model="elementObject.citation"
                    :rules="[rules.requiredCitation]"
                    counter
                    rows="3"
                    maxlength="300"
                  ></v-textarea>
                </v-form>
                <v-row wrap dense no-gutters>
                  <v-col cols="12">
                    <v-radio-group
                      v-if="isNewElement"
                      v-model="elementObject.sub_type"
                      @change="changeType"
                      row
                    >
                      <template v-slot:label>
                        <div>Language element type:</div>
                      </template>
                      <v-radio label="Text" value="Text"></v-radio>
                      <v-radio label="YouTube Video" value="YouTube"></v-radio>
                      <v-radio label="Audio" value="Audio"></v-radio>
                    </v-radio-group>
                  </v-col>
                </v-row>
                <div
                  v-if="elementObject.sub_type == 'Text' && loaded"
                  class="mb-3"
                >
                  <SimpleTipTap
                    :editMode="true"
                    ref="textEditor"
                    :content="elementObject.element.rich_text"
                  />
                </div>
                <div v-if="elementObject.sub_type == 'YouTube' && loaded" class="mb-3">
                  <v-row wrap dense v-if="isNewElement">
                    <v-col cols="9" md="10">
                      <v-form ref="linkform">
                        <v-text-field
                          v-model="videoURL"
                          @focus="clearWarnings"
                          label="YouTube Video ID or Link"
                          placeholder="paste id or link here"
                          outlined
                        ></v-text-field>
                      </v-form>
                    </v-col>
                    <v-col cols="3" md="2">
                      <v-btn
                        fab
                        @click="validateVideo"
                        color="primary"
                        :loading="validating"
                        ><v-icon>mdi-reload</v-icon></v-btn
                      >
                    </v-col>

                    <v-col cols="12">
                      <v-alert v-if="alertActive" :type="alertType" dense>
                        {{ alertMessage }}
                      </v-alert>
                      <v-alert
                        v-if="videoExists"
                        class="info"
                        type="info"
                        dense
                      >
                        <p class="font-weight-black white--text">
                          This video already exists in the PidginForge database
                          as "{{ existingTitle }}"
                        </p>
                        <v-btn
                          block
                          class="mb-2 orange lighten-2 black--text"
                          :to="{
                            name: 'Media-Viewer',
                            params: {
                              elementtype: 'YouTube',
                              elementslug: existingSlug
                            }
                          }"
                          >View Existing Video
                          <v-icon right class="black--text"
                            >mdi-play-circle</v-icon
                          ></v-btn
                        >
                      </v-alert>
                    </v-col>
                  </v-row>
                  <v-row v-if="videoLoaded || elementObject.element.video_id">
                    <v-col cols="12">
                      <v-card outlined>
                        <youtube
                          :key="youTubePlayerKey"
                          :video-id="elementObject.element.video_id"
                          :fit-parent="fitParent"
                          ref="youtube"
                        >
                        </youtube>
                      </v-card>
                    </v-col>
                  </v-row>
                </div>
                <div v-if="elementObject.sub_type == 'Audio'" class="mb-3">
                  <v-row dense no-gutters>
                    <v-col cols="12" v-if="audioLoaded">
                      Current Audio File:
                      <span class="font-weight-black black--text">
                        {{ elementObject.element.originalfilename }}</span
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
                    <v-col
                      cols="12"
                      align="center"
                      v-if="loaded && !loadNewFile"
                    >
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
                </div>
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
          @click="submitElement"
          :disabled="!valid || !loaded || loadNewFile"
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
  name: "ElementEditor",
  components: {
    SimpleTipTap: () =>
      import(
        /* webpackPrefetch: true */ "@/components/elements/SimpleTipTap.vue"
      ),
    AudioPlayerComponent: () =>
      import("@/components/elements/AudioPlayerComponent.vue")
  },
  props: {
    element: {
      type: Object,
      default: undefined
    },
    editorDialog: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    // userData: Object,
    elementObject: {
      sub_type: "Text",
      rich_text: ""
    },
    isNewElement: false,
    loaded: false,
    loadNewFile: false,
    videoLoaded: false,
    audioLoaded: false,
    newFileLoaded: false,
    video: {},
    newAudioID: "",
    audioFile: "",
    audioFileName: "",
    duration: "",
    videoID: "",
    videoURL: "",
    submitting: false,
    validating: false,
    videoExists: false,
    youTubePlayerKey: 0,
    valid: true,
    success: false,
    fitParent: true,
    alertType: "success",
    alertMessage: "It's all good!",
    alertActive: false,
    allLanguages: [],
    loadingLanguages: false,
    rules: {
      requiredTitle: value =>
        (value || "").length > 5 ||
        "You must provide a title of at least 6 characters.",
      requiredLanguage: languagevalue =>
        (languagevalue || "").length > 0 ||
        "You must choose at least 1 language.",
      requiredDescription: descriptionvalue =>
        !!descriptionvalue || "You must provied a description.",
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
      this.elementObject.tags.splice(this.elementObject.tags.indexOf(item), 1);
      this.elementObject.tags = [...this.elementObject.tags];
    },
    clearWarnings() {
      this.alertActive = false;
      this.videoExists = false;
      this.alertActive = false;
    },
    passDuration(duration) {
      this.duration = duration;
    },
    getLanguages() {
      var localLanguages = localStorage.getItem("languages");
      if (localLanguages.length > 1) {
        console.log("Shop local!");
        this.allLanguages = JSON.parse(localLanguages);
      } else {
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
      }
    },

    updateViewer(element) {
      this.$emit("updateViewer", element);
    },

    parseDuration(duration) {
      let matches = duration.match(/[0-9]+[HMS]/g);

      let seconds = 0;

      matches.forEach(function(part) {
        let unit = part.charAt(part.length - 1);
        let amount = parseInt(part.slice(0, -1));

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
    parseElementObject() {
      this.elementObject = this.element;
      if (this.elementObject.sub_type === "Text") {
        this.editMode = true;
        // this.$refs.textEditor.editor.setOptions({ editable: this.editMode });
      } else if (this.elementObject.sub_type === "YouTube") {
        console.log("hello");
      } else if (this.elementObject.sub_type === "Audio") {
        this.audioFile = this.elementObject.element.audiofile;
      } else {
        this.isNewElement === true;
      }
      this.loaded = true;
    },
    validateVideo() {
      this.alertActive = false;
      this.videoLoaded = false;
      if (this.videoURL.length < 1) {
        this.alertType = "error";
        this.alertMessage = "You have to enter something!";
        this.alertActive = true;
      } else {
        let urlSplit = this.videoURL.split("/");
        let checkID = urlSplit[urlSplit.length - 1];
        this.validating = true;
        let endpoint = `api/elements/youtube/check/`;
        try {
          apiService(endpoint, "POST", { videoid: checkID }).then(data => {
            if (data != null) {
              if (data.available == true) {
                this.available = true;
                // this.loaded = true;
                this.$gapi
                  .request({
                    path: "https://www.googleapis.com/youtube/v3/videos",
                    method: "GET",
                    params: {
                      part: "snippet,contentDetails,statistics",
                      id: checkID
                    }
                  })
                  .then(response => {
                    if (response.result.items.length > 0) {
                      let resultVideo = response.result.items[0];
                      this.videoid = checkID;
                      // this.playerVideoID = checkID;
                      this.elementObject.element.duration = this.parseDuration(
                        resultVideo.contentDetails.duration
                      );
                      this.elementObject.element.videoTitle =
                        resultVideo.snippet.title;
                      this.elementObject.element.video_id = resultVideo.id;
                      this.elementObject.element.thumb =
                        resultVideo.snippet.thumbnails.medium["url"];
                      this.videoLoaded = true;
                      this.validating = false;
                      this.loadNewFile = false;
                      // this.editing = false;
                    } else {
                      this.alertType = "error";
                      this.alertMessage =
                        "Error validating video from YouTube; it likely does not exist";
                      this.alertActive = true;
                      this.validating = false;
                    }
                  });
              } else {
                // IF THE VIDEO ALREADY EXISTS
                this.videoExists = true;
                this.existingSlug = data.slug;
                this.existingTitle = data.title;
                // this.alertMessage = `This video already exists in the ${} PidginForge database...${data.slug}`
                // this.alertType = 'warning'
                this.available = false;
                this.validating = false;
                this.loadNewFile = true;
              }
            } else {
              console.log("Something bad happened...");
              this.alertActive = true;
              this.alertMessage = "Something very bad happened...";
              this.alertType = "error";
              this.available = false;
              this.loadNewFile = true;
              return false;
            }
          });
        } catch (err) {
          console.log(err);
        }
      }
    },
    setAudio(newaudio) {
      if (newaudio) {
        const file = newaudio;
        if (file.type.indexOf("audio/") === -1) {
          alert("Please select an audio file");
          return;
        } else {
          this.elementObject.element.audiofile = newaudio;
          this.elementObject.element.originalfilename = newaudio.name;
          console.log(this.elementObject.originalfilename);
        }
        if (typeof FileReader === "function") {
          const reader = new FileReader();
          reader.onload = event => {
            // this.elementObject.element.audiofile = event.target.result;
            this.audioFile = event.target.result;
            console.log("Ready!");
            this.loadNewFile = false;
            this.newFileLoaded = true;
            this.audioLoaded = true;
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

    submitElement() {
      // Audio elements must be handled by a special form, hence a separate function call
      if (this.elementObject.sub_type === "Audio") {
        this.submitAudioElement();
      } else {
        this.submitting = true;
        let endpoint = new String();
        let method = new String();
        if (this.isNewElement) {
          endpoint = `/api/elements/elementz/`;
          method = "POST";
        } else {
          endpoint = `/api/elements/elementz/${this.elementObject.slug}/`;
          method = "PATCH";
        }
        let payload = {
          // id: this.elementObject.id,
          title: this.elementObject.title,
          description: this.elementObject.description,
          language: this.elementObject.language,
          sub_type: this.elementObject.sub_type,
          citation: this.elementObject.citation,
          tags: this.elementObject.tags
        };
        if (this.elementObject.sub_type === "Text") {
          payload.rich_text = this.$refs.textEditor.editor.getJSON();
          payload.plain_text = this.$refs.textEditor.editor.view.state.doc.textContent;
        } else if (this.elementObject.sub_type === "YouTube") {
          payload.duration = this.elementObject.element.duration;
          payload.video_id = this.elementObject.element.video_id;
          payload.thumb = this.elementObject.element.thumb;
        }
        console.log(payload);
        apiService(endpoint, method, payload).then(data => {
          if (data.slug) {
            if (this.isNewElement) {
              this.loaded = false
              this.closeDialog();
              this.$router.push({
                name: "Element-Viewer",
                params: { slug: data.slug }
              });
            } else {
              // this.alertActive = false;
              this.loaded = false
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
    submitAudioElement() {
      // The following grabs the blob, converts to a JPEG, wraps it, and sends it to the API
      this.submitting = true;
      let endpoint = `/api/elements/elementz/`;
      let method = "POST";
      if (this.elementObject.slug !== undefined) {
        endpoint += `${this.elementObject.slug}/`;
        method = "PATCH";
      }
      const formData = new FormData();
      if (this.newFileLoaded) {
        formData.append("audiofile", this.elementObject.element.audiofile);
        formData.append(
          "originalfilename",
          this.elementObject.element.originalfilename
        );
      }
      formData.append("title", this.elementObject.title);
      formData.append("language", this.elementObject.language);
      formData.append("description", this.elementObject.description);
      formData.append("duration", this.duration || 0);
      formData.append("citation", this.elementObject.citation);
      formData.append("tags", this.elementObject.tags);
      formData.append("sub_type", this.elementObject.sub_type);
      apiFileService(endpoint, method, formData).then(data => {
        if (data) {
          if (this.isNewElement) {
            this.closeDialog();
            this.$router.push({
              name: "Element-Viewer",
              params: { slug: data.slug }
            });
          } else {
            // this.alertActive = false;
            this.updateViewer(data);
            this.closeDialog();
          }
        } else {
          console.log("There was a major problem with the request.");
        }
        this.submitting = false;
      });
    },
    changeType(value) {
      if (value === "Text") {
        this.loadNewFile = false;
      } else if (this.newFileLoaded !== true) {
        {
          this.loadNewFile = true;
        }
      }
    }
  },
  mounted() {
    if (this.element) {
      this.parseElementObject();
    } else {
      this.isNewElement = true;
      this.loadNewFile = false;
      this.elementObject = {
        sub_type: "Text",
        element: {
          rich_text: {},
          plain_text: ""
        }
      };
      this.loaded = true;
    }
  },

  created() {
    this.getLanguages();
  }
};
</script>
<style></style>
