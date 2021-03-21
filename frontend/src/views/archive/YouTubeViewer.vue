<template>
  <div class="youtubeviewer sandstone">
    <v-container fluid>
      <v-card class="desertsand">
        <v-card-title class="pb-1">
          <v-row wrap dense no-gutters class="pa-1">
            <v-col cols="12">
              {{ video.title }}
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
                    v-if="profileDialog"
                    :profileObject="video.curator"
                    :profileDialog="profileDialog"
                    @closeDialog="profileDialog = false"
                  />
                  <ProfileSnippet
                    :username="curatorName"
                    @closeDialog="closeProfileDialog"
                  />
                </v-dialog>

                on {{ video.curationdate }} <br />
              </p>
            </v-col>
          </v-row>
        </v-card-title>
        <v-card-text class="pt-1">
          <v-row dense no-gutters>
            <v-col cols="12" sm="7">
              <div ref="ytdiv">
                <youtube
                  :key="youTubePlayerKey"
                  :video-id="video.videoid"
                  :resize="true"
                  :height="YTheight"
                  :width="YTwidth"
                  ref="youtube"
                  @playing="playing"
                  @ready="loadingVideo = false"
                >
                </youtube>
              </div>
            </v-col>
            <v-overlay
              :value="loadingVideo"
              absolute
              color="calligraphy"
              opacity="0.75"
            >
              <v-progress-circular
                indeterminate
                size="64"
              ></v-progress-circular>
            </v-overlay>

            <v-col cols="12" sm="5" align="center">
              <p align="left">
                <span class="font-weight-bold">Learning Purpose:</span>
                {{ video.purpose }}
              </p>
              <YTUpDownVote
                @updateVote="updateVote"
                :up-vote-count="video.upvote_count"
                :down-vote-count="video.downvote_count"
                :user-vote="video.user_vote"
                :slug="slug"
              />
              <hr />
              Target Language:
              <v-chip outlined small class="languages languages--text">{{
                video.language
              }}</v-chip
              ><br />
              Primary Topic:
              <v-chip outlined small class="topics topics--text">{{
                video.topic
              }}</v-chip
              ><br />
              Tag(s):
              <v-chip
                outlined
                small
                class="tags tags--text"
                v-for="tag in video.tags"
                :key="tag.id"
                >{{ tag }}</v-chip
              >
              <hr />

              <v-btn
                class="mr-1 mb-1 saves desertsand--text"
                @click="toggleSave"
                :loading="saving"
              >
                <v-badge color="saves lighten-2" :content="video.saved_count">
                  <span :hidden="video.user_has_saved"
                    >Save<v-icon>mdi-heart</v-icon></span
                  >
                  <span :hidden="!video.user_has_saved"
                    >Unsave<v-icon>mdi-heart-broken</v-icon></span
                  >
                </v-badge>
              </v-btn>
              <v-btn
                class="mr-1 mb-1 garbage desertsand--text"
                @click="toggleHide"
                :loading="hiding"
              >
                <span :hidden="video.user_has_hidden"
                  >Hide<v-icon right>mdi-eye-off</v-icon></span
                >
                <span :hidden="!video.user_has_hidden"
                  >Un-Hide<v-icon right>mdi-eye</v-icon></span
                >
              </v-btn>

              <v-btn
                @click="loadYouTubeEditor"
                class="mr-1 mb-1 primary desertsand--text"
              >
                Edit
                <v-icon right>
                  mdi-pencil
                </v-icon>
              </v-btn>
              <YouTubeElementEditor
                v-if="youTubeEditorLoaded"
                :editor-dialog="showYouTubeEditor"
                :editing="true"
                :key="video.id"
                :video="video"
                @closeDialog="showYouTubeEditor = false"
                @rerenderYouTube="rerenderYouTube"
                @updateViewer="updateViewer"
              />
              <v-btn
                @click="flaggerDialog = true"
                :disabled="video.user_has_flagged"
                class="mr-1 mb-1 error white--text"
              >
                <v-badge
                  color="error lighten-1 white--text"
                  :content="video.flag_count"
                >
                  Flag<v-icon right>mdi-flag</v-icon>
                </v-badge>
              </v-btn>
            </v-col>
            <v-col cols="12">
              Transcripts and What-not Go Here
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
      <ContentFlagger
        :flagger-dialog="flaggerDialog"
        @closeDialog="flaggerDialog = false"
        content-type="youtube_element"
        :contentid="video.id"
      />
    </v-container>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import YTUpDownVote from "@/components/elements/YTUpDownVote.vue";
import ContentFlagger from "@/components/ContentFlagger.vue";
export default {
  name: "YouTubeList",
  components: {
    YTUpDownVote,
    ContentFlagger,
    ProfileSnippet: () =>
      import(
        /* webpackPrefetch: true */ "@/components/profile/ProfileSnippet.vue"
      ),
    YouTubeElementEditor: () =>
      import(
        /* webpackPrefetch: true */ "@/components/elements/YouTubeElementEditor.vue"
      )
  },
  data() {
    return {
      youTubeKey: 0,
      youTubeEditorLoaded: false,
      showYouTubeEditor: false,
      editorDialog: false,
      profileDialog: false,
      video: {
        curator: {}
      },
      max: 100,
      youTubePlayerKey: 0,
      next: null,
      flaggerDialog: false,
      loadEditor: false,
      loadingVideo: false,
      fitParent: true,
      YTwidth: 200,
      YTheight: 135,
      userHidden: false,
      saving: false,
      hiding: false,
      requestUser: "",
      userSaved: false,
      voteScore: 0,
      isProfileSnippetVisible: false,
      voteColor: "text--black font-weight-bold"
    };
  },
  props: {
    slug: {
      type: String,
      required: true
    }
  },
  computed: {
    player() {
      return this.$refs.youtube.player;
    },
    curatorName() {
      return this.video.curator.username;
    },
    userIsCurator() {
      return this.curatorName() === this.requestUser;
      // return false;
    },
    length() {
      let totalseconds = this.video.duration;
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
    closeEditorDialog() {
      this.editorDialog = false;
    },
    updateVote(data) {
      this.video.user_vote = data.newuservote;
      this.video.downvote_count = data.newdowncount;
      this.video.upvote_count = data.newupcount;
    },
    closeProfileDialog() {
      this.profileDialog = false;
    },
    updateViewer(video) {
      this.video = video;
    },
    loadYouTubeEditor() {
      this.youTubeEditorLoaded = true;
      this.showYouTubeEditor = !this.showYouTubeEditor;
    },

    setRequestUser() {
      return (this.requestUser = window.localStorage.getItem("username"));
    },
    rerenderYouTube() {
      this.youTubeKey += 1;
    },
    getVideo() {
      this.loadingVideo = true;
      let endpoint = `/api/elements/youtubez/${this.slug}/`;
      apiService(endpoint).then(data => {
        if (data) {
          this.video = data;
          //  this.loadingVideo = false;
        } else {
          this.video = null;
          this.setPageTitle("404 - Page Note Found");
          this.loadingVideo = false;
        }
      });
    },
    setVideoSize() {
      let clientwidth = this.$refs.ytdiv.clientWidth;
      this.YTwidth = clientwidth - 10;
      this.YTheight = clientwidth * 0.65;
    },
    playVideo() {
      this.player.playVideo();
    },
    playing() {
      // Something here
    },
    toggleSave() {
      this.saving = true;
      let endpoint = `api/elements/youtube/saved/`;
      try {
        apiService(endpoint, "POST", { pk: this.video.id }).then(data => {
          if (data != null) {
            if (data.success == true) {
              // this.$emit("hideElement")
              this.video.user_has_saved = !this.video.user_has_saved;
              if (this.video.user_has_saved) {
                this.video.saved_count += 1;
              } else {
                this.video.saved_count -= 1;
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
    openEditor() {
      this.loadEditor = true;
      this.youTubeEditorDialog = true;
    },
    toggleHide() {
      this.hiding = true;
      let endpoint = `api/elements/youtube/hidden/`;
      try {
        apiService(endpoint, "POST", { pk: this.video.id }).then(data => {
          if (data != null) {
            if (data.success == true) {
              this.video.user_has_hidden = !this.video.user_has_hidden;
              console.log("This item has been hidden");
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
    } // Hide from List
    //
    //
  },
  updated() {
    this.setVideoSize();
  },
  created() {
    this.getVideo();
    this.setRequestUser();
    // Get comments?? (this can probably just be part of the larger package)
  }
};
</script>
<style scoped></style>
