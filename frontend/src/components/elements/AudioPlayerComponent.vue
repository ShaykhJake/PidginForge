<template>
  <v-card align="center">
    <v-card-text class="py-1">
      <v-btn
        outlined
        class="ma-1"
        @click="stepPosition(-2)"
        icon
        v-on:keyup.space="stepPosition(-2)"
      >
        <v-icon>mdi-undo</v-icon>
      </v-btn>

      <v-btn
        outlined
        icon
        class="ma-1"
        :color="color"
        @click.native="stop()"
        :disabled="!loaded"
      >
        <v-icon>mdi-stop</v-icon>
      </v-btn>

      <v-btn
        outlined
        icon
        class="ma-1"
        :color="color"
        @click.native="playing ? pause() : play()"
        :disabled="!loaded"
      >
        <v-icon v-if="paused || !loaded">mdi-play</v-icon>
        <v-icon v-else>mdi-pause</v-icon>
      </v-btn>

      <v-btn
        outlined
        icon
        class="ma-1"
        :color="color"
        @click.native="loaded ? download() : reload()"
        v-if="!loaded"
      >
        <v-icon>mdi-refresh</v-icon>
      </v-btn>
      <v-btn
        outlined
        icon
        class="ma-1"
        :color="color"
        @click.native="loaded ? download() : reload()"
        v-if="loaded && downloadable"
      >
        <v-icon>mdi-download</v-icon>
      </v-btn>

      <v-btn outlined class="ma-1" @click="stepPosition(2)" icon>
        <v-icon>mdi-redo</v-icon>
      </v-btn>
      <p class="title py-0 my-0">{{ currentTime }} / {{ duration }}</p>
      <v-slider
        :color="color"
        step="0.2"
        thumb-label
        v-model="slideTime"
        @click="setPosition"
        :min="min"
        :max="totalDuration"
        :disabled="!loaded"
        class="mb-0 pb-0"
        height="1"
        dense
      >
      </v-slider>
      <v-btn
        outlined
        icon
        class="ma-1"
        :color="color"
        @click.native="mute()"
        :disabled="!loaded"
        hidden
      >
        <v-icon v-if="!isMuted">mdi-volume-high</v-icon>
        <v-icon v-else>mdi-volume-mute</v-icon>
      </v-btn>
    </v-card-text>
    <audio
      id="player"
      ref="player"
      v-on:ended="ended"
      v-on:canplay="canPlay"
      :src="file"
      :key="playerKey"
      hidden
    ></audio>
  </v-card>
</template>
<script>
const formatTime = second =>
  new Date(second * 1000).toISOString().substr(11, 8);
export default {
  name: "AudioPlayerComponent",
  props: {
    file: {
      type: [String, File],
      default: null
    },
    autoPlay: {
      type: Boolean,
      default: false
    },
    ended: {
      type: Function,
      default: () => {}
    },
    canPlay: {
      type: Function,
      default: () => {}
    },
    color: {
      type: String,
      default: null
    },
    downloadable: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    duration: function() {
      return this.audio ? formatTime(this.totalDuration) : "";
    }
  },
  data() {
    return {
      alive: true,
      audioKey: 0,
      playerKey: 0,
      firstPlay: true,
      isMuted: false,
      loaded: false,
      playing: false,
      paused: true,
      percentage: 0,
      currentTime: "00:00:00",
      audio: {},
      totalDuration: 0,
      min: 0,
      max: 100,
      slideTime: 0
    };
  },
  methods: {
    resumePlay() {
      this.setPosition();
      this.play();
    },
    slidePosition() {
      this.audio.currentTime = parseInt(this.slideTime);
      this.play();
    },
    stepPosition(step) {
      this.audio.currentTime = this.audio.currentTime + step;
    },
    setPosition() {
      //  this.audio.currentTime = parseInt(this.audio.duration / 100 * this.percentage);
      this.audio.currentTime = parseInt(this.slideTime);
    },
    stop() {
      this.audio.pause();
      this.paused = true;
      this.playing = false;
      this.audio.currentTime = 0;
    },
    togglePlay() {
      if (this.playing) {
        this.pause();
        this.playing = false;
      } else {
        this.play();
      }
    },
    skipToTime(time) {
      this.audio.currentTime = time;
    },
    skipSeek(delta) {
      this.audio.currentTime = this.audio.currentTime + delta;
      // this.player.getCurrentTime().then(currenttime => {
      //     let newtime = currenttime + delta;
      //     this.player.seekTo(newtime, true);
      // })
    },

    triggerTimeStamp() {
      this.$emit("recordTimeStamp", this.audio.currentTime);
      // this.player.getCurrentTime().then(currenttime => {
      //   console.log(currenttime);
      //   this.$emit("recordTimeStamp", currenttime);
      // })
    },

    play() {
      if (this.playing) return;
      this.audio.play().then(() => {
        this.playing = true;
      });
      this.paused = false;
    },
    pause() {
      this.paused = !this.paused;
      this.paused ? this.audio.pause() : this.audio.play();
    },
    download() {
      this.audio.pause();
      window.open(this.file, "download");
    },
    mute() {
      this.isMuted = !this.isMuted;
      this.audio.muted = this.isMuted;
      this.volumeValue = this.isMuted ? 0 : 75;
    },
    reload() {
      this.audio.load();
    },
    _handleLoaded: function() {
      if (this.audio.readyState >= 2) {
        if (this.audio.duration === Infinity) {
          // Fix duration for streamed audio source or blob based
          // https://stackoverflow.com/questions/38443084/how-can-i-add-predefined-length-to-audio-recorded-from-mediarecorder-in-chrome/39971175#39971175
          this.audio.currentTime = 1e101;
          this.audio.ontimeupdate = () => {
            this.audio.ontimeupdate = () => {};
            this.audio.currentTime = 0;
            this.totalDuration = parseInt(this.audio.duration);
            this.loaded = true;
          };
        } else {
          this.totalDuration = parseInt(this.audio.duration);
          this.$emit("passDuration", this.totalDuration);
          this.loaded = true;
        }
        if (this.autoPlay) this.audio.play();
      } else {
        throw new Error("Failed to load sound file");
      }
    },
    _handlePlayingUI: function() {
      this.percentage = (this.audio.currentTime / this.audio.duration) * 100;
      this.slideTime = this.audio.currentTime;
      this.currentTime = formatTime(this.audio.currentTime);
      this.playing = true;
    },
    _handlePlayPause: function(e) {
      if (e.type === "play" && this.firstPlay) {
        // in some situations, audio.currentTime is the end one on chrome
        this.audio.currentTime = 0;
        if (this.firstPlay) {
          this.firstPlay = false;
        }
      }
      if (
        e.type === "pause" &&
        this.paused === false &&
        this.playing === false
      ) {
        this.currentTime = "00:00:00";
      }
    },
    _handleEnded() {
      this.paused = this.playing = false;
    },
    init: function() {
      this.audio.addEventListener("timeupdate", this._handlePlayingUI);
      this.audio.addEventListener("loadeddata", this._handleLoaded);
      //  this.audio.addEventListener('pause', this._handlePlayPause);
      //  this.audio.addEventListener('play', this._handlePlayPause);
      //  this.audio.addEventListener('ended', this._handleEnded);
    },
    emitTimeStamp() {
      // console.log(`This is the audio player, emitting ${this.audio.currentTime}!`)
      this.$emit("recordTimeStamp", this.audio.currentTime);
    }
  },

  mounted() {
    this.audio = this.$refs.player;
    this.init();

    //   (this._keyListener = function(e) {
    //     // Rewind 1 Second
    //     if (e.key === "f" && (e.ctrlKey || e.metaKey)) {
    //       e.preventDefault();
    //       this.audio.currentTime = this.audio.currentTime - 1;
    //     }
    //     // Advance 1 Second
    //     if (e.key === "j" && (e.ctrlKey || e.metaKey)) {
    //       e.preventDefault();
    //       this.audio.currentTime = this.audio.currentTime + 1;
    //     }
    //     // Pause Audio
    //     if (e.key === "h" && (e.ctrlKey || e.metaKey)) {
    //       e.preventDefault();
    //       this.togglePlay();
    //     }
    //     if (e.key === "g" && (e.ctrlKey || e.metaKey)) {
    //       e.preventDefault();
    //       this.emitTimeStamp();
    //     }
    //   }),
    //     document.addEventListener("keydown", this._keyListener.bind(this));
  },
  beforeDestroy() {
    this.audio.removeEventListener("timeupdate", this._handlePlayingUI);
    this.audio.removeEventListener("loadeddata", this._handleLoaded);
    this.audio.removeEventListener("pause", this._handlePlayPause);
    this.audio.removeEventListener("play", this._handlePlayPause);
    this.audio.removeEventListener("ended", this._handleEnded);
    // document.removeEventListener("keydown", this._keyListener);
  }
};
</script>
