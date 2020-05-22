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
        <span v-if="!editing">Import YouTube Element</span>
        <span v-else>Edit YouTube Element</span>
        <v-spacer></v-spacer>
      </v-card-title>
      <v-card-text class="pa-1 desertsand">
        <v-row wrap dense justify="center">
          <v-col cols="12" sm="10" md="8" lg="6">
            <p class="body-2 mx-2 black--text text-justify text-wrap">
              To avoid copyright infringement, an imported YouTube element is
              merely a link to the original content, along with a few extra bits
              of information which are relevant for language learning. Please
              choose videos of quality with a clear purpose for language
              learning.
            </p>

            <v-row wrap dense>
              <v-col cols="9" md="10">
                <v-form ref="linkform">
                  <v-text-field
                    v-model="newVideoID"
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
                <v-alert v-if="videoExists" class="info" type="info" dense>
                  <p class="font-weight-black white--text">
                    This video already exists in the PidginForge database as "{{
                      existingTitle
                    }}"
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
            <v-row v-if="loaded">
              <v-col cols="12">
                <v-card outlined>
                  <youtube
                    :key="youTubePlayerKey"
                    :video-id="video.videoid"
                    :fit-parent="fitParent"
                    ref="youtube"
                    @playing="playing"
                  >
                  </youtube>
                </v-card>
              </v-col>
            </v-row>

            <v-form
              ref="details"
              v-model="valid"
              @submit.prevent
              :v-if="!validating && loaded"
              :hidden="success || validating || !loaded"
            >
              <v-text-field
                v-model="video.title"
                name="videotitle"
                label="Element Title*"
                placeholder="give this item a title"
                :rules="[rules.requiredTitle]"
                outlined
              ></v-text-field>

              <v-select
                v-model="video.language"
                name="videolanguage"
                :items="allLanguages"
                label="Target Language*"
                placeholder="choose a target language"
                :rules="[rules.requiredLanguage]"
                required
                :loading="loadingLanguages"
                outlined
              ></v-select>

              <v-select
                v-model="video.topic"
                name="videotopic"
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
                v-model="video.purpose"
                :rules="[rules.requiredPurpose]"
                counter
                rows="3"
                maxlength="300"
              ></v-textarea>

              <v-textarea
                outlined
                name="videonotes"
                label="Curator Notes"
                v-model="video.notes"
                value=""
                rows="3"
                counter
                maxlength="300"
              ></v-textarea>
              <v-combobox
                label="Additional Topic Tags"
                name="videotags"
                v-model="video.tags"
                chips
                clearable
                hint="Hit <enter> or <tab> after each entry (max of 5 tags allowed)"
                persistent-hint
                multiple
                :rules="[rules.maxTags]"
                outlined
                counter
              >
                <template v-slot:selection="{ attrs, item, select, selected }">
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
      </v-card-text>
      <v-card-actions class="calligraphy">
        <v-spacer></v-spacer>
        <v-btn color="garbage desertsand--text" @click="closeDialog"
          >Cancel<v-icon right>mdi-close</v-icon></v-btn
        >
        <v-btn
          color="success"
          @click="submitElement"
          :disabled="!valid || (!available && !editing)"
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
export default {
  name: "youTubeElementEditor",
  components: {},
  props: {
    editorDialog: Boolean,
    editing: {
      type: Boolean,
      default: false
    },
    video: {
      type: Object
    }
  },
  data: () => ({
    // userData: Object,
    validating: false,
    youTubePlayerKey: 0,
    loaded: false,
    videoExists: false,
    existingSlug: "",
    existingTitle: "",
    // items: ['Streaming', 'Eating'],
    newVideoID: "KOfWzrQYqxY",
    // use this video as a sample of a video that exists: -YJSDJGyIaU, this does not: KmOAznOQX-g
    available: false,
    submitting: false,
    valid: false,
    success: false,
    fitParent: true,
    alertType: "success",
    alertMessage: "",
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
      requiredPurpose: purposevalue =>
        !!purposevalue || "You must provied a learning purpose.",
      requiredTopic: topicvalue =>
        (topicvalue || "").length > 0 || "You must choose a primary topic.",
      maxTags: tagsvalue =>
        (tagsvalue || "").length < 6 || "Maximum of 5 tags allowed!"
    }
  }),
  computed: {
    player() {
      return this.$refs.youtube.player;
    }
  },
  methods: {
    closeDialog() {
      this.$emit("closeDialog");
    },

    removeTag(item) {
      this.video.tags.splice(this.video.tags.indexOf(item), 1);
      this.video.tags = [...this.video.tags];
    },
    clearWarnings() {
      this.videoExists = false;
      this.alertActive = false;
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

    validateVideo() {
      this.alertActive = false;
      this.loaded = false;
      if (this.newVideoID.length < 1) {
        this.alertType = "error";
        this.alertMessage = "You have to enter something!";
        this.alertActive = true;
      } else {
        var urlSplit = this.newVideoID.split("/");
        var checkID = urlSplit[urlSplit.length - 1];

        this.validating = true;
        let endpoint = `api/elements/youtube/check/`;
        try {
          apiService(endpoint, "POST", { videoid: checkID }).then(data => {
            if (data != null) {
              if (data.available == true) {
                this.available = true;
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
                      // this.playerVideoID = checkID;
                      console.log(resultVideo);
                      this.video.duration = this.parseDuration(
                        resultVideo.contentDetails.duration
                      );
                      this.video.title = resultVideo.snippet.title;
                      this.video.videoid = resultVideo.id;
                      this.video.thumbURL =
                        resultVideo.snippet.thumbnails.medium["url"];
                      this.loaded = true;
                      this.validating = false;
                      this.editing = false;
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
              }
            } else {
              console.log("Something bad happened...");
              this.alertActive = true;
              this.alertMessage = "Something very bad happened...";
              this.alertType = "error";
              this.available = false;
              return false;
            }
          });
        } catch (err) {
          console.log(err);
        }
      }
    },
    setEditVideoData() {
      if (this.editing) {
        this.newVideoID = this.video.videoid;
        this.validating = false;
        this.loaded = true;
      } else {
        this.loaded = false;
        this.validating = false;
      }
    },
    updateViewer(video) {
      this.$emit("updateViewer", video);
    },
    playVideo() {
      this.player.playVideo();
    },
    playing() {
      console.log("We are watching!!!");
    },
    cancelDialog() {
      this.$emit("closeDialog");
    },
    submitElement() {
      if (this.valid) {
        this.submitting = true;
        let endpoint = `api/elements/youtubez/`;
        let method = "POST";
        if (this.video.slug !== undefined) {
          endpoint += `${this.video.slug}/`;
          method = "PATCH";
        }
        var payload = {
          duration: this.video.duration,
          title: this.video.title,
          videoid: this.video.videoid,
          thumbURL: this.video.thumbURL,
          language: this.video.language,
          topic: this.video.topic,
          purpose: this.video.purpose,
          notes: this.video.notes,
          tags: this.video.tags
        };
        console.log(payload);
        try {
          apiService(endpoint, method, payload).then(data => {
            if (data != null) {
              console.log(data);
              if (data.slug != null) {
                // console.log(data);
                this.error = false;
                // this.$emit("rerenderYouTube");
                if (!this.editing) {
                  this.$router.push({
                    name: "Media-Viewer",
                    params: { elementtype: "YouTube", elementslug: data.slug }
                  });
                  this.submitting = false;
                } else {
                  this.alertActive = false;
                  this.updateViewer(data);
                  this.closeDialog();
                }
              } else {
                this.alertType = "error";
                this.alertMessage = "There was an error with your submission!";
                this.alertActive = true;
              }
            } else {
              this.alertType = "error";
              this.alertMessage = "Something really bad happened...";
              this.alertActive = true;
            }
            this.submitting = false;
          });
        } catch (err) {
          console.log(err);
        }
      }
    }
  },
  created() {
    this.getLanguages();
    this.getTopics();
    this.setEditVideoData();
  }
};
</script>
<style scoped>
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
