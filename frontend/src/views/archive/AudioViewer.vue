<template>
  <div class="audioviewer sandstone">
    <v-container fluid>
      <v-card class="desertsand">
        <v-card-title class="pb-1">
          <v-row wrap dense no-gutters class="pa-1">
            <v-col cols="12">
              {{ audio.title }}
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

                on {{ audio.curationdate }} <br />
              </p>
              <p align="left" class="caption">
                <span class="font-weight-bold">Learning Purpose:</span>
                {{ audio.purpose }}
              </p>
            </v-col>
          </v-row>
        </v-card-title>
        <v-card-text class="pt-1">
          <v-row dense wrap>
            <v-col cols="12">
              <v-row>
                <v-col cols="12" align="center">
                  <AudioPlayerComponent
                    :file="audio.audiofile"
                    color="calligraphy"
                    class="sandstone"
                    :key="audioPlayerKey"
                    @timeStamp="recordTimeStamp"
                  />
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" align="center">
                  <AudioUpDownVote
                    @updateVote="updateVote"
                    :up-vote-count="audio.upvote_count"
                    :down-vote-count="audio.downvote_count"
                    :user-vote="audio.user_vote"
                    :slug="slug"
                  />
                  <hr />
                  Target Language:
                  <v-chip outlined small class="languages languages--text">{{
                    audio.language
                  }}</v-chip
                  ><br />
                  Primary Topic:
                  <v-chip outlined small class="topics topics--text">{{
                    audio.topic
                  }}</v-chip
                  ><br />
                  Tag(s):
                  <v-chip
                    outlined
                    small
                    class="tags tags--text"
                    v-for="tag in audio.tags"
                    :key="tag.id"
                    >{{ tag }}</v-chip
                  >
                  <hr />

                  <v-btn
                    class="mr-1 mb-1 saves desertsand--text"
                    @click="toggleSave"
                    :loading="saving"
                  >
                    <v-badge
                      color="saves lighten-2"
                      :content="audio.saved_count"
                    >
                      <span :hidden="audio.user_has_saved"
                        >Save<v-icon>mdi-heart</v-icon></span
                      >
                      <span :hidden="!audio.user_has_saved"
                        >Unsave<v-icon>mdi-heart-broken</v-icon></span
                      >
                    </v-badge>
                  </v-btn>
                  <v-btn
                    class="mr-1 mb-1 garbage desertsand--text"
                    @click="toggleHide"
                    :loading="hiding"
                  >
                    <span :hidden="audio.user_has_hidden"
                      >Hide<v-icon right>mdi-eye-off</v-icon></span
                    >
                    <span :hidden="!audio.user_has_hidden"
                      >Un-Hide<v-icon right>mdi-eye</v-icon></span
                    >
                  </v-btn>

                  <v-btn
                    @click="loadAudioEditor"
                    class="mr-1 mb-1 primary desertsand--text"
                  >
                    Edit
                    <v-icon right>
                      mdi-pencil
                    </v-icon>
                  </v-btn>
                  <AudioElementEditor
                    v-if="audioEditorLoaded"
                    :editor-dialog="showAudioEditor"
                    :editing="true"
                    :key="audio.id"
                    :audio="audio"
                    @closeDialog="showAudioEditor = false"
                    @rerenderAudio="rerenderAudio"
                    @updateViewer="updateViewer"
                  />
                  <v-btn
                    @click="flaggerDialog = true"
                    :disabled="audio.user_has_flagged"
                    class="mr-1 mb-1 error white--text"
                  >
                    <v-badge
                      color="error lighten-1 white--text"
                      :content="audio.flag_count"
                    >
                      Flag<v-icon right>mdi-flag</v-icon>
                    </v-badge>
                  </v-btn>
                </v-col>
              </v-row>
            </v-col>
            <v-overlay
              :value="loadingAudio"
              absolute
              color="calligraphy"
              opacity="0.75"
            >
              <v-progress-circular
                indeterminate
                size="64"
              ></v-progress-circular>
            </v-overlay>

            <v-col cols="12">
              Transcripts and What-not Go Here
            </v-col>
            <v-col>
              <TranscriptEditor ref="transcript" v-model="scriptcontent" />
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
      <ContentFlagger
        :flagger-dialog="flaggerDialog"
        @closeDialog="flaggerDialog = false"
        content-type="audio_element"
        :contentid="audio.id"
      />
    </v-container>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import AudioUpDownVote from "@/components/elements/AudioUpDownVote.vue";
import ContentFlagger from "@/components/ContentFlagger.vue";
import TranscriptEditor from "@/components/transcript/TranscriptEditor.vue";
export default {
  name: "AudioViewer",
  components: {
    AudioUpDownVote,
    ContentFlagger,
    TranscriptEditor,
    ProfileSnippet: () =>
      import(
        /* webpackPrefetch: true */ "@/components/profile/ProfileSnippet.vue"
      ),
    AudioPlayerComponent: () =>
      import("@/components/elements/AudioPlayerComponent.vue"),
    AudioElementEditor: () =>
      import(
        /* webpackPrefetch: true */ "@/components/elements/AudioElementEditor.vue"
      )
  },
  data() {
    return {
      audioKey: 0,
      scriptcontent: "",
      audioEditorLoaded: false,
      showAudioEditor: false,
      editorDialog: false,
      profileDialog: false,
      audio: {
        curator: {}
      },
      max: 100,
      audioPlayerKey: 0,
      next: null,
      flaggerDialog: false,
      loadEditor: false,
      loadingAudio: false,
      fitParent: true,
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
    curatorName() {
      return this.audio.curator.username;
    },
    userIsCurator() {
      return this.curatorName() === this.requestUser;
      // return false;
    },
    length() {
      let totalseconds = this.audio.duration;
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
    recordTimeStamp(time) {
      this.$refs.transcript.recordTimeStamp(time);
      // console.log(time);
    },
    closeEditorDialog() {
      this.editorDialog = false;
    },
    updateVote(data) {
      this.audio.user_vote = data.newuservote;
      this.audio.downvote_count = data.newdowncount;
      this.audio.upvote_count = data.newupcount;
    },
    closeProfileDialog() {
      this.profileDialog = false;
    },
    updateViewer(audio) {
      this.audio = audio;
    },
    loadAudioEditor() {
      this.audioEditorLoaded = true;
      this.showAudioEditor = !this.showAudioEditor;
    },

    setRequestUser() {
      return (this.requestUser = window.localStorage.getItem("username"));
    },
    rerenderAudio() {
      this.audioKey += 1;
    },
    getAudio() {
      this.loadingAudio = true;
      let endpoint = `/api/elements/audioz/${this.slug}/`;
      apiService(endpoint).then(data => {
        if (data) {
          this.audio = data;
          //  this.loadingAudio = false;
        } else {
          this.audio = null;
          this.setPageTitle("404 - Page Note Found");
        }
        this.loadingAudio = false;
      });
    },
    toggleSave() {
      this.saving = true;
      let endpoint = `api/elements/audio/save/`;
      try {
        apiService(endpoint, "POST", { pk: this.audio.id }).then(data => {
          if (data != null) {
            if (data.success == true) {
              // this.$emit("hideElement")
              this.audio.user_has_saved = !this.audio.user_has_saved;
              if (this.audio.user_has_saved) {
                this.audio.saved_count += 1;
              } else {
                this.audio.saved_count -= 1;
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
      this.audioEditorDialog = true;
    },
    toggleHide() {
      this.hiding = true;
      let endpoint = `api/elements/audio/hide/`;
      try {
        apiService(endpoint, "POST", { pk: this.audio.id }).then(data => {
          if (data != null) {
            if (data.success == true) {
              this.audio.user_has_hidden = !this.audio.user_has_hidden;
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
  created() {
    this.getAudio();
    this.setRequestUser();
    // Get comments?? (this can probably just be part of the larger package)
  }
};
</script>
<style scoped></style>
