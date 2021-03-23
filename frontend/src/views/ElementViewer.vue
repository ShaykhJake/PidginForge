<template>
  <div class="mediaelement desertsand">
    <v-container fluid class="pa-2">
      <v-card class="desertsand">
        <v-card-title class="pb-1">
          <v-row wrap dense no-gutters class="pa-1">
            <v-col cols="12">
              {{ element.title }}
            </v-col>
            <v-col cols="12">
              <p class="overline mb-2">
                Curated by
                <v-btn
                  @click="profileDialog = true"
                  text
                  small
                  class="primary--text font-weight-bold px-0 py-0"
                >
                  {{ curatorName }}
                </v-btn>
                <ProfileSnippet
                  v-if="profileDialog"
                  :profileObject="element.curator"
                  :profileDialog="profileDialog"
                  @closeDialog="profileDialog = false"
                />

                on {{ element.curation_date }} <br />
              </p>
            </v-col>
          </v-row>
        </v-card-title>
        <v-card-text class="pt-1">
          <v-row dense no-gutters>
            <v-col cols="12" sm="7" class="pr-5">
              <div
                v-if="
                  element.sub_type == 'Audio' || element.sub_type == 'YouTube'
                "
              >
                <div v-if="element.sub_type == 'Audio'">
                  <AudioPlayerComponent
                    :key="element.id"
                    :file="element.element.audiofile"
                    color="calligraphy"
                    class="sandstone"
                    ref="player"
                    @recordTimeStamp="recordTimeStamp"
                  />
                </div>
                <div v-if="element.sub_type == 'YouTube'">
                  <YouTubePlayerComponent
                    :key="element.id"
                    :videoid="element.element.video_id"
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
              </div>
              <div v-if="element.sub_type == 'Text'">
                <SimpleTipTap
                  ref="textEditor"
                  :content="element.element.rich_text"
                />
              </div>
            </v-col>
            <v-col cols="12" sm="5" align="center">
              <p align="left">
                <span class="font-weight-bold">Description:</span>
                {{ element.description }}
              </p>
              <p align="left">
                <span class="font-weight-bold">Citation:</span>
                {{ element.citation }}
              </p>
              <ElementVoter
                @updateVote="updateVote"
                :up-vote-count="element.upvote_count"
                :down-vote-count="element.downvote_count"
                :user-vote="element.user_vote"
                :slug="slug"
                :object-type="'element'"
              />
              <hr />
              <div class="mt-1 mb-1">
                Target Language:
                <v-chip outlined small class="languages languages--text">{{
                  element.language
                }}</v-chip
                ><br />
                Tag(s):
                <v-chip
                  outlined
                  small
                  class="tags tags--text"
                  v-for="tag in element.tags"
                  :key="tag.id"
                  >{{ tag }}</v-chip
                >
              </div>
              <hr />
              <div class="mt-1">
                <v-btn
                  class="mr-1 mb-1 saves desertsand--text"
                  @click="toggleSave"
                  :loading="saving"
                  icon
                >
                  <v-badge
                    color="saves lighten-2"
                    :content="element.saved_count"
                  >
                    <v-icon v-if="!element.user_has_saved">mdi-heart</v-icon>
                    <v-icon v-else>mdi-heart-broken</v-icon>
                  </v-badge>
                </v-btn>
                <v-btn
                  class="mr-1 mb-1 garbage desertsand--text"
                  @click="toggleHide"
                  :loading="hiding"
                  icon
                >
                  <v-icon v-if="!element.user_has_hidden">mdi-eye-off</v-icon>
                  <v-icon v-else>mdi-eye</v-icon>
                </v-btn>
                <v-btn
                  @click="flaggerDialog = true"
                  :disabled="element.user_has_flagged"
                  class="mr-1 mb-1 error white--text"
                  icon
                >
                  <v-badge
                    color="error lighten-1 white--text"
                    :content="element.flag_count"
                  >
                    <v-icon>mdi-flag</v-icon>
                  </v-badge>
                </v-btn>
              </div>
              <hr />
              <div v-if="userIsCurator">
                <v-btn class="primary" @click="toggleEditor"
                  >Edit Element</v-btn
                >
              </div>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <ElementTranscripts
        v-if="element.id"
        :element_id="element.id"
        ref="scriptEditor"
        @triggerTimeStamp="triggerTimeStamp"
        @skipToTime="skipToTime"
      />
      <ElementComments v-if="element.id" :element_id="element.id" />

      <ContentFlagger
        :flagger-dialog="flaggerDialog"
        @closeDialog="flaggerDialog = false"
        content-type="'element'"
        :contentid="element.id"
      />
      <ElementEditor
        v-if="editorDialog"
        :editorDialog="editorDialog"
        :element="element"
        @updateViewer="updateElement"
        @closeDialog="editorDialog = false"
      />
    </v-container>
  </div>
</template>

<script>
  import { apiService } from "@/common/api.service.js";
  import ElementComments from "@/components/elements/ElementComments.vue";
  import ElementTranscripts from "@/components/elements/ElementTranscripts.vue";
  import ElementVoter from "@/components/elements/ElementVoter.vue";
  import ElementEditor from "@/components/elements/ElementEditor.vue";
  import ContentFlagger from "@/components/ContentFlagger.vue";
  import SimpleTipTap from "@/components/elements/SimpleTipTap.vue";
  export default {
    name: "ElementViewer",
    components: {
      // YTUpDownVote,
      SimpleTipTap,
      ElementVoter,
      ElementEditor,
      ElementComments,
      ElementTranscripts,
      ContentFlagger,
      ProfileSnippet: () =>
        import(
          /* webpackPrefetch: true */ "@/components/profile/ProfileSnippet.vue"
        ),
      // YouTubeElementEditor: () =>
      //   import(
      //     /* webpackPrefetch: true */ "@/components/elements/YouTubeElementEditor.vue"
      //   ),
      AudioPlayerComponent: () =>
        import(
          /* webpackPrefetch: true */ "@/components/elements/AudioPlayerComponent.vue"
        ),

      YouTubePlayerComponent: () =>
        import(
          /* webpackPrefetch: true */ "@/components/elements/YouTubePlayerComponent.vue"
        ),

      // AudioElementEditor: () =>
      //   import(
      //     /* webpackPrefetch: true */ "@/components/elements/AudioElementEditor.vue"
      //   ),

      // TranscriptEditor: () =>
      //   import(
      //     /* webpackPrefetch: true */ "@/components/transcript/TranscriptEditor.vue"
      //   )
    },
    data() {
      return {
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
        element: {
          curator: {},
          transcripts: {},
        },
        video: {
          curator: {},
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

        voteColor: "text--black font-weight-bold",
      };
    },
    props: {
      slug: {
        type: String,
        required: true,
      },
    },
    computed: {
      player() {
        return this.$refs.player;
      },
      curatorName() {
        return this.element.curator.username;
      },
      userIsCurator() {
        return this.element.curator.username === this.requestUser;
        // return false;
      },
      length() {
        if (this.element.element.duration) {
          let totalseconds = this.element.duration;
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
        } else {
          return undefined;
        }
      },
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
      toggleEditMode() {
        this.$refs.textEditor.toggleEditMode();
        console.log(
          this.$refs.textEditor.editor.view.state.doc.textContent.length
        );
        console.log(this.$refs.textEditor.editor.getJSON());
        console.log(this.$refs.textEditor.editor.view.state.doc.textContent);
      },
      recordTimeStamp(time) {
        // this.$refs.ttviewer.recordTimeStamp(time)
        this.$refs.scriptEditor.recordTimeStamp(time);
        console.log("sending4");
      },
      triggerTimeStamp(index) {
        // Sends a trigger to the Players to Emit a Timestamp
        // console.log("triggering4");
        this.$refs.player.triggerTimeStamp(index);
      },
      updateVote(data) {
        this.element.user_vote = data.newuservote;
        this.element.downvote_count = data.newdowncount;
        this.element.upvote_count = data.newupcount;
      },
      closeProfileDialog() {
        this.profileDialog = false;
      },
      updateElement(element) {
        this.element = element;
        this.$refs.textEditor.editor.setContent(this.element.element.rich_text);
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
      loadElement(slug) {
        this.loadingElement = true;
        let endpoint = `/api/elements/element/${slug}/`;
        apiService(endpoint).then((data) => {
          if (data) {
            console.log(data);
            this.element = data;
            // this.setVideoSize;
            this.loadingElement = false;
            this.ready = true;
          } else {
            this.element = null;
            this.setPageTitle("404 - Page Note Found");
            this.loadingElement = false;
          }
        });
      },

      getAudio() {
        this.loadingAudio = true;
        let endpoint = `/api/elements/audioz/${this.slug}/`;
        apiService(endpoint).then((data) => {
          if (data) {
            console.log("Get Audio:");
            console.log(data);
            this.element = data;
            //  this.loadingAudio = false;
            this.ready = true;
          } else {
            this.element = null;
            this.setPageTitle("404 - Page Note Found");
          }
          this.loadingAudio = false;
        });
      },

      toggleSave() {
        this.saving = true;
        let endpoint = "";
        endpoint = `api/elements/save/element/`;
        try {
          apiService(endpoint, "POST", { pk: this.element.id }).then((data) => {
            if (data != null) {
              if (data.success == true) {
                // this.$emit("hideElement")
                this.element.user_has_saved = !this.element.user_has_saved;
                if (this.element.user_has_saved) {
                  this.element.saved_count += 1;
                } else {
                  this.element.saved_count -= 1;
                }
                // console.log(data.message)
              } else {
                // this.alertType = 'error';
              }
            } else {
              // this.alertType = 'error';
            }
            this.saving = false;
          });
        } catch (err) {
          console.log(err);
        }
      },
      toggleHide() {
        this.hiding = true;
        let endpoint = "api/elements/hide/element/";
        try {
          apiService(endpoint, "POST", { pk: this.element.id }).then((data) => {
            if (data != null) {
              if (data.success == true) {
                this.element.user_has_hidden = data.hidden;
              } else {
                this.alertType = "error";
              }
            } else {
              this.alertType = "error";
            }
            this.hiding = false;
          });
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
      toggleEditor() {
        if (this.element.sub_type === "Audio" && this.$refs.player) {
          this.$refs.player.stop();
        }
        this.editorDialog = !this.editorDialog;
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
      },
    },

    created() {
      this.setRequestUser();
      this.loadElement(this.slug);
    },

    watch: {
      $route() {
        console.log("Watched: Change Route");
        if (this.hotKeysActive) {
          window.removeEventListener("keydown", this.playerHotKey);
          this.hotKeysActive = false;
          console.log("Hot keys disabled");
        }
      },
    },
    mounted() {},
    beforeDestroy() {
      console.log("Before destroy?");
      // document.removeEventListener("keydown", this.playerHotKey);
      if (this.hotKeysActive) {
        window.removeEventListener("keydown", this.playerHotKey);
        this.hotKeysActive = false;
        console.log("Hot keys disabled");
      }
    },
    // Get comments?? (this can probably just be part of the larger package
  };
</script>
<style type="text/css">
  .v-card__text,
  .v-card__title {
    word-break: keep-all; /* maybe !important  */
    word-wrap: normal;
  }
</style>
