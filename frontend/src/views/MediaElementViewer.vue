<template>
  <div class="mediaelement sandstone">
    <v-container fluid>
      <v-card class="desertsand">
        <v-card-title class="pb-1">
          <v-row wrap dense no-gutters class="pa-1">
            <v-col cols="12">
              {{ elementObject.title }}
            </v-col>
            <v-col cols="12">
              <p class="overline mb-2">
                Curated by

                <v-dialog v-model="profileDialog" width="275">
                  <template v-slot:activator="{ on }">
                    <v-btn
                      v-on="on"
                      text
                      small
                      class="primary--text font-weight-bold px-0 py-0"
                    >
                      {{ curatorName }}
                    </v-btn>
                  </template>
                  <ProfileSnippet
                    :username="curatorName"
                    @closeDialog="closeProfileDialog"
                  />
                </v-dialog>

                on {{ elementObject.curationdate }} <br />
              </p>
            </v-col>
          </v-row>
        </v-card-title>
        <v-card-text class="pt-1">
          <v-row dense no-gutters>
            <v-col cols="12" sm="7" class="pr-5">
              <div v-if="typeAudio">
                <AudioPlayerComponent
                  :key="elementObject.id"
                  :file="elementObject.audiofile"
                  color="calligraphy"
                  class="sandstone"
                  ref="player"
                  @recordTimeStamp="recordTimeStamp"
                />
              </div>
              <div v-if="typeVideo">
                <YouTubePlayerComponent
                  :key="elementObject.id"
                  :videoid="elementObject.videoid"
                  @recordTimeStamp="recordTimeStamp"
                  ref="player"
                />
              </div>
              <v-btn
                block
                class="primary desertsand--text"
                @click="toggleHotKeys"
                v-if="hotKeysActive"
                >Disable Hot Keys<v-icon right>mdi-lock</v-icon></v-btn
              >
              <div
                style="text-align: center"
                class="overline pt-1"
                v-if="hotKeysActive"
              >
                <span>Cmd/Ctrl+F - Skip Back 1 Second</span><br />
                <span>Cmd/Ctrl+G - Insert Timestamp</span><br />
                <span>Cmd/Ctrl+H - Play/Pause</span><br />
                <span>Cmd/Ctrl+J - Skip Forward 1 Second</span><br />
                <span class="languages--text"
                  >(Works well in Chrome, use only the <i>Ctrl</i> key in
                  Safari)</span
                >
              </div>
              <v-btn
                block
                class="d-none d-sm-flex primary desertsand--text"
                @click="toggleHotKeys"
                v-if="!hotKeysActive"
                >Enable Hot Keys<v-icon right
                  >mdi-lock-open-variant</v-icon
                ></v-btn
              >
              <div hidden>
                <b>Hotkeys:</b><br />
                Rewind 1 Second: Cmd/Ctrl+F; Advance 1 Second: Cmd/Ctrl+J;
                Play/Pause: Cmd/Ctrl+H; Insert Time: Cmd/Ctrl+G
              </div>
            </v-col>
            <v-col cols="12" sm="5" align="center">
              <p align="left">
                <span class="font-weight-bold">Learning Purpose:</span>
                {{ elementObject.purpose }}
              </p>
              <ElementVoter
                @updateVote="updateVote"
                :up-vote-count="elementObject.upvote_count"
                :down-vote-count="elementObject.downvote_count"
                :user-vote="elementObject.user_vote"
                :slug="elementslug"
                :element-type="elementtype"
              />
              <hr />
              Target Language:
              <v-chip outlined small class="languages languages--text">{{
                elementObject.language
              }}</v-chip
              ><br />
              Primary Topic:
              <v-chip outlined small class="topics topics--text">{{
                elementObject.topic
              }}</v-chip
              ><br />
              Tag(s):
              <v-chip
                outlined
                small
                class="tags tags--text"
                v-for="tag in elementObject.tags"
                :key="tag.id"
                >{{ tag }}</v-chip
              >
              <hr />

              <v-btn
                class="mr-1 mb-1 saves desertsand--text"
                @click="toggleSave"
                :loading="saving"
                icon
              >
                <v-badge
                  color="saves lighten-2"
                  :content="elementObject.saved_count"
                >
                  <v-icon v-if="!elementObject.user_has_saved">mdi-heart</v-icon>
                  <v-icon v-else>mdi-heart-broken</v-icon>
                </v-badge>
              </v-btn>
              <v-btn
                class="mr-1 mb-1 garbage desertsand--text"
                @click="toggleHide"
                :loading="hiding"
                icon
              >
                <v-icon v-if="!elementObject.user_has_hidden">mdi-eye-off</v-icon>
                <v-icon v-else>mdi-eye</v-icon>
              </v-btn>

              <v-btn
                v-if="typeVideo"
                @click="loadYouTubeEditor"
                class="mr-1 mb-1 primary desertsand--text"
                icon
              >
                <v-icon>
                  mdi-pencil
                </v-icon>
              </v-btn>
              <YouTubeElementEditor
                v-if="youTubeEditorLoaded"
                :editor-dialog="showYouTubeEditor"
                :editing="true"
                :video="elementObject"
                @closeDialog="showYouTubeEditor = false"
                @rerenderYouTube="rerenderYouTube"
                @updateViewer="updateViewer"
              />

              <v-btn
                v-if="typeAudio"
                @click="loadAudioEditor"
                class="mr-1 mb-1 primary desertsand--text"
                icon
              >
                <v-icon>
                  mdi-pencil
                </v-icon>
              </v-btn>

              <AudioElementEditor
                v-if="audioEditorLoaded"
                :editor-dialog="showAudioEditor"
                :editing="true"
                :audio="elementObject"
                @closeDialog="showAudioEditor = false"
                @rerenderAudio="rerenderAudio"
                @updateViewer="updateViewer"
              />
              <v-btn
                @click="flaggerDialog = true"
                :disabled="elementObject.user_has_flagged"
                class="mr-1 mb-1 error white--text"
                icon
              >
                <v-badge
                  color="error lighten-1 white--text"
                  :content="elementObject.flag_count"
                >
                  <v-icon>mdi-flag</v-icon>
                </v-badge>
              </v-btn>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <v-row dense no-gutters wrap class="d-none d-sm-flex">
        <v-col cols="12">
          <TranscriptEditor
            v-if="ready"
            ref="scripteditor"
            :element-type="elementtype"
            :element-slug="elementslug"
            :passed-object="elementObject"
            @triggerTimeStamp="triggerTimeStamp"
            @skipToTime="skipToTime"
          />
        </v-col>
      </v-row>
      <ContentFlagger
        :flagger-dialog="flaggerDialog"
        @closeDialog="flaggerDialog = false"
        :content-type="elementtype"
        :contentid="elementObject.id"
      />
    </v-container>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";

import ElementVoter from "@/components/elements/ElementVoter.vue";
import ContentFlagger from "@/components/ContentFlagger.vue";
export default {
  name: "MediaElementViewer",
  components: {
    // YTUpDownVote,
    ElementVoter,
    ContentFlagger,
    ProfileSnippet: () =>
      import(
        /* webpackPrefetch: true */ "@/components/profile/ProfileSnippet.vue"
      ),
    YouTubeElementEditor: () =>
      import(
        /* webpackPrefetch: true */ "@/components/elements/YouTubeElementEditor.vue"
      ),
    AudioPlayerComponent: () =>
      import(
        /* webpackPrefetch: true */ "@/components/elements/AudioPlayerComponent.vue"
      ),

    YouTubePlayerComponent: () =>
      import(
        /* webpackPrefetch: true */ "@/components/elements/YouTubePlayerComponent.vue"
      ),

    AudioElementEditor: () =>
      import(
        /* webpackPrefetch: true */ "@/components/elements/AudioElementEditor.vue"
      ),

    TranscriptEditor: () =>
      import(
        /* webpackPrefetch: true */ "@/components/transcript/TranscriptEditor.vue"
      )
  },
  data() {
    return {
      mediaType: "",
      hotKeysActive: false,
      audioPlayerKey: 0,
      heightText: "Start",
      youTubeKey: 0,
      audioKey: 0,
      youTubeEditorLoaded: false,
      showYouTubeEditor: false,
      showAudioEditor: false,
      audioEditorLoaded: false,
      editorDialog: false,
      profileDialog: false,
      elementObject: {
        curator: {},
        transcripts: {}
      },
      video: {
        curator: {}
      },
      max: 100,
      youTubePlayerKey: 0,
      next: null,
      flaggerDialog: false,
      loadEditor: false,
      ready: false,
      loadingVideo: false,
      loadingAudio: false,
      fitParent: true,
      YTwidth: 275,
      YTheight: 200,
      userHidden: false,
      saving: false,
      hiding: false,
      requestUser: "",
      userSaved: false,
      voteScore: 0,
      youTubeHeight: 0,
      isProfileSnippetVisible: false,
      voteColor: "text--black font-weight-bold"
    };
  },
  props: {
    elementtype: {
      type: String,
      required: true
    },
    elementslug: {
      type: String,
      required: true
    }
  },
  computed: {
    typeAudio() {
      return this.mediaType === "Audio";
    },
    typeVideo() {
      return this.mediaType === "YouTube";
    },
    player() {
      return this.$refs.player;
    },
    curatorName() {
      return this.elementObject.curator.username;
    },
    userIsCurator() {
      return this.curatorName() === this.requestUser;
      // return false;
    },
    length() {
      let totalseconds = this.elementObject.duration;
      var hours = totalseconds / 3600,
        minutes = (hours % 1) * 60,
        seconds = (minutes % 1) * 60;
      if (hours < 1) {
        return Math.floor(minutes) + ":" + Math.round(seconds);
      } else {
        return (
          Math.floor(hours) +
          ":" +
          Math.floor(minutes) +
          ":" +
          Math.round(seconds)
        );
      }
    }
  },

  methods: {
    // Get Current User
    // Save / Unsave Item
    destroyPlayer() {
      // this.$destory()
      console.log("hello");
    },
    closeEditorDialog() {
      this.editorDialog = false;
    },
    recordTimeStamp(time) {
      // this.$refs.ttviewer.recordTimeStamp(time)
      this.$refs.scripteditor.recordTimeStamp(time);
    },
    triggerTimeStamp() {
      // Sends a trigger to the Players to Emit a Timestamp
      this.$refs.player.triggerTimeStamp();
    },
    updateVote(data) {
      this.elementObject.user_vote = data.newuservote;
      this.elementObject.downvote_count = data.newdowncount;
      this.elementObject.upvote_count = data.newupcount;
    },
    closeProfileDialog() {
      this.profileDialog = false;
    },
    updateViewer(elementObject) {
      this.elementObject = elementObject;
    },
    loadYouTubeEditor() {
      this.youTubeEditorLoaded = true;
      this.showYouTubeEditor = !this.showYouTubeEditor;
    },
    loadAudioEditor() {
      this.audioEditorLoaded = true;
      this.showAudioEditor = !this.showAudioEditor;
    },
    setRequestUser() {
      return (this.requestUser = window.localStorage.getItem("username"));
    },
    rerenderYouTube() {
      this.youTubeKey += 1;
    },
    getVideo() {
      this.loadingVideo = true;
      let endpoint = `/api/elements/youtubez/${this.elementslug}/`;
      apiService(endpoint).then(data => {
        if (data) {
          console.log("Get Video:");
          console.log(data);
          this.elementObject = data;
          // this.setVideoSize;
          this.loadingVideo = false;
          this.ready = true;
        } else {
          this.elementObject = null;
          this.setPageTitle("404 - Page Note Found");
          this.loadingVideo = false;
        }
      });
    },

    getAudio() {
      this.loadingAudio = true;
      let endpoint = `/api/elements/audioz/${this.elementslug}/`;
      apiService(endpoint).then(data => {
        if (data) {
          console.log("Get Audio:");
          console.log(data);
          this.elementObject = data;
          //  this.loadingAudio = false;
          this.ready = true;
        } else {
          this.elementObject = null;
          this.setPageTitle("404 - Page Note Found");
        }
        this.loadingAudio = false;
      });
    },

    toggleSave() {
      this.saving = true;
      let endpoint = "";
      if (this.elementtype === "YouTube") {
        endpoint = `api/elements/youtube/save/`;
      } else if (this.elementtype === "Audio") {
        endpoint = `api/elements/audio/save/`;
      }

      try {
        apiService(endpoint, "POST", { pk: this.elementObject.id }).then(
          data => {
            if (data != null) {
              if (data.success == true) {
                // this.$emit("hideElement")
                this.elementObject.user_has_saved = !this.elementObject
                  .user_has_saved;
                if (this.elementObject.user_has_saved) {
                  this.elementObject.saved_count += 1;
                } else {
                  this.elementObject.saved_count -= 1;
                }
                // console.log(data.message)
              } else {
                // this.alertType = 'error';
              }
            } else {
              // this.alertType = 'error';
            }
            this.saving = false;
          }
        );
      } catch (err) {
        console.log(err);
      }
    },
    openEditor() {
      this.loadEditor = true;
      this.youTubeEditorDialog = true;
    },
    toggleHide() {
      this.hiding = true;
      let endpoint = "";
      if (this.elementtype === "YouTube") {
        endpoint = `api/elements/youtube/hide/`;
      } else if (this.elementtype === "Audio") {
        endpoint = `api/elements/audio/hide/`;
      }
      try {
        apiService(endpoint, "POST", { pk: this.elementObject.id }).then(
          data => {
            if (data != null) {
              if (data.success == true) {
                this.elementObject.user_has_hidden = !this.elementObject
                  .user_has_hidden;
              } else {
                this.alertType = "error";
              }
            } else {
              this.alertType = "error";
            }
            this.hiding = false;
          }
        );
      } catch (err) {
        console.log(err);
      }
    },
    skipToTime(time) {
      this.player.skipToTime(time);
    },
    skipSeek(delta) {
      this.player.skipSeek(delta);
    },
    togglePlay() {
      this.player.togglePlay();
    },
    toggleHotKeys() {
      if (!this.hotKeysActive) {
        window.addEventListener("keydown", this.playerHotKey);
        // document.addEventListener("keydown", this.playerHotKey);
        this.hotKeysActive = true;
        // console.log("Hot keys enabled")
      } else {
        // document.removeEventListener("keydown", this.playerHotKey);
        window.removeEventListener("keydown", this.playerHotKey);
        this.hotKeysActive = false;
        // console.log("Hot keys disabled");
      }
    },

    playerHotKey(e) {
      if (e.key === "f" && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        // console.log("Rewind 1 second")
        this.skipSeek(-1);
      }
      // Advance 1 Second
      if (e.key === "j" && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        // console.log("Advance 1 second")
        this.skipSeek(1);
      }
      // Pause Audio
      if (e.key === "h" && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        // console.log("Pause/Play");
        this.togglePlay();
      }
      if (e.key === "g" && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        console.log("This is media viewer, requesting a time stamp...");
        this.triggerTimeStamp();
      }
    }
  },
  // updated() {
  //   if(this.elementtype === "YouTube"){
  //     this.setVideoSize();
  //   }
  // },
  created() {
    this.setRequestUser();
    if (this.elementtype === "YouTube") {
      this.getVideo();
      // this.setVideoSize();
    } else {
      this.getAudio();
    }
  },

  watch: {
    $route() {
      console.log("Watched: Change Route");
      if (this.hotKeysActive) {
        window.removeEventListener("keydown", this.playerHotKey);
        this.hotKeysActive = false;
        console.log("Hot keys disabled");
      }
    }
  },
  mounted() {
    this.mediaType = this.$route.params.elementtype;
  },
  beforeDestroy() {
    console.log("Before destroy?");
    // document.removeEventListener("keydown", this.playerHotKey);
    if (this.hotKeysActive) {
      window.removeEventListener("keydown", this.playerHotKey);
      this.hotKeysActive = false;
      console.log("Hot keys disabled");
    }
  }
  // Get comments?? (this can probably just be part of the larger package
};
</script>
<style  type="text/css">
.v-card__text,
.v-card__title {
  word-break: keep-all; /* maybe !important  */
  word-wrap: normal;
}
</style>
