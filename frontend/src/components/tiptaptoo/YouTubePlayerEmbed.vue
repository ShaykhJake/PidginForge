<template>
  <div>
    <v-card class="calligraphy desertsand--text" min-width="300">
      <v-card-title class="py-1" v-show="editing">
        <v-spacer />
        <v-icon color="elements">mdi-arrow-all</v-icon>
        <v-spacer />
      </v-card-title>
      <v-card-text class="pa-0">
        <div ref="ytdiv" class="responsive">
          <youtube
            :key="youTubePlayerKey"
            :video-id="videoid"
            :height="YTheight"
            :width="YTwidth"
            ref="youtube"
            @playing="playing"
            @ready="loadingVideo = false"
          >
          </youtube>
        </div>
      </v-card-text>
      <v-card-actions v-show="editing">
        <v-btn small icon @click="updateWrap('left')"
          ><v-icon :color="float === 'left' ? 'primary' : 'desertsand'"
            >mdi-arrow-collapse-left</v-icon
          ></v-btn
        >
        <v-spacer />
        <v-btn small icon @click="updateWrap('none')"
          ><v-icon :color="float === 'none' ? 'primary' : 'desertsand'"
            >mdi-format-wrap-top-bottom</v-icon
          ></v-btn
        >
        <v-spacer />
        <v-btn small icon @click="updateWrap('right')"
          ><v-icon :color="float === 'right' ? 'primary' : 'desertsand'"
            >mdi-arrow-collapse-right</v-icon
          ></v-btn
        >
      </v-card-actions>
    </v-card>
  </div>
</template>
<script>
// import VueYouTubeEmbed from 'vue-youtube-embed'
export default {
  name: "YouTubePlayerEmbed",
  props: {
    src: String,
    float: String,
    videoid: String,
    editing: {
      type: Boolean,
      default: true
    }
  },
  components: {},
  data() {
    return {
      player: {},
      heightText: "Start",
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
      loadingVideo: false,
      loadingAudio: false,
      fitParent: true,
      YTwidth: 275,
      YTheight: 200,
      userHidden: false,
      saving: false,
      hiding: false,
      voteScore: 0,
      youTubeHeight: 0
    };
  },
  methods: {
    // recordTimeStamp(time) {
    //   this.$refs.ttviewer.recordTimeStamp(time)
    // },
    // requestTimeStamp() {
    //   // Sends a trigger to the Players to Emit a Timestamp
    //   if(this.elementtype === "YouTube"){
    //     console.log("MediaViewer Says: YouTube, Please Emit Time")
    //   } else if (this.elementtype === "Audio"){
    //     // console.log("MediaViewer Says: Audio, Please Emit Time")
    //     this.$refs.audioPlayer.emitTimeStamp();
    //   }

    // },
    updateWrap(direction) {
      this.$emit("updateWrap", direction);
    },
    updateVideoSize(direction) {
      var newSize = this.minWidth;
      if (direction === "up") {
        if (newSize > 280) {
          newSize = 315;
        } else {
          newSize += 25;
        }
      } else {
        if (newSize < 150) {
          newSize = 125;
        } else {
          newSize -= 25;
        }
      }
      this.$emit("updateVideoSize", newSize);
    },
    setVideoSize() {
      let clientwidth = this.$refs.ytdiv.clientWidth;
      this.YTwidth = clientwidth - 10;
      this.YTheight = clientwidth * 0.65;
    },
    playVideo() {
      this.player.playVideo();
    },
    skipToTime(time) {
      this.player.seekTo(time, true);
    },
    skipSeek(delta) {
      this.player.getCurrentTime().then(currenttime => {
        let newtime = currenttime + delta;
        this.player.seekTo(newtime, true);
      });
    },
    togglePlay() {
      this.player.getPlayerState().then(state => {
        if (state === 1) {
          this.player.pauseVideo();
        } else {
          this.player.playVideo();
        }
      });
    },
    triggerTimeStamp() {
      this.player.getCurrentTime().then(currenttime => {
        console.log(currenttime);
        this.$emit("recordTimeStamp", currenttime);
      });
    },
    playing() {
      // Something here
    }
  },
  hide: function() {
    // now we can use the reference to Choices to perform clean up here
    // prior to removing the elements from the DOM
    this.player.destroy();
  },
  mounted() {
    this.player = this.$refs.youtube.player;
    // this.setVideoSize;
    // (this._keyListener = function(e) {
    //   // Rewind 1 Second
    //   if (e.key === "f" && (e.ctrlKey || e.metaKey)) {
    //     e.preventDefault();
    //     console.log("Rewind 1 second")
    //     this.skipSeek(-1);
    //     // this.audio.currentTime = this.audio.currentTime - 1;
    //   }
    //   // Advance 1 Second
    //   if (e.key === "j" && (e.ctrlKey || e.metaKey)) {
    //     e.preventDefault();
    //     console.log("Advance 1 second")
    //     this.skipSeek(1);
    //     // this.audio.currentTime = this.audio.currentTime + 1;
    //   }
    //   // Pause Audio
    //   if (e.key === "h" && (e.ctrlKey || e.metaKey)) {
    //     e.preventDefault();
    //     console.log("Pause/Play");
    //     this.togglePlay();
    //     // this.player.playVideo()
    //     // this.pause();
    //   }
    //   if (e.key === "g" && (e.ctrlKey || e.metaKey)) {
    //     e.preventDefault();
    //     this.player.getCurrentTime().then(currenttime => {
    //       console.log(currenttime);
    //       this.$emit("recordTimeStamp", currenttime);
    //     })
    //   }
    // }),
    //   document.addEventListener("keydown", this._keyListener.bind(this));
  },
  beforeDestroy() {
    document.removeEventListener("keydown", this._keyListener);
  }
};
</script>
<style type="text/css">
.responsive {
  width: 100%;
  padding-right: 10px;
  height: 0;
  padding-bottom: 56.25%;
  position: relative;
}
.responsive iframe {
  position: absolute;
  width: 100%;
  height: 100%;
}
</style>
