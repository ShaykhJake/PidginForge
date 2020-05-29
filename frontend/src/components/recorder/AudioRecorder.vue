<template>
<div>
   <v-card class="desertsand">
      <v-card-text class="text-center">

         <h3>Attach Audio</h3>
         <v-radio-group v-model="audioSource" @change="audio.audioURL=null">
            <v-radio label="Upload File" value="file"></v-radio>
            <v-radio label="Record New" value="microphone"></v-radio>
         </v-radio-group>

         <v-file-input
            v-if="audioSource==='file'"
            v-model="userFile"
            show-size
            :rules="[rules.maxAudioSize]"
            @change="setAudio"
            accept="['audio/mp3','audio/aac','audio/m4a'"
            placeholder="Pick a valid audio file"
            prepend-icon="mdi-volume-high"
            label="Audio File"
            capture
            outlined
            ref="input"
         >
         </v-file-input>

         <div v-if="audioSource==='microphone'">
            <hr>
            <span class="overline" v-if="!recording && !processing">Click to Record</span>
            <span class="overline" v-if="recording">Click to Stop</span>
            <br>

               <v-btn fab icon class="green mb-5" @click="toggleRecorder" v-if="!isRecording && !processing">
                  <v-icon>mdi-microphone</v-icon>
               </v-btn>

               <v-btn class="recordingButton mb-5" fab icon @click="stopRecorder" v-if="isRecording && !processing">
                  <v-icon>mdi-microphone</v-icon>
               </v-btn>
               <div v-if="isRecording" class="mb-5">
                  <meter min="0" low="25" optimum="75" high="100" max="150" :value="volume"></meter><br>
                  {{ recordedTime }}
               </div>

            <br>
         </div>

         <audio 
            class="audioPlayer" 
            v-if="audioSelected && !isRecording && !processing && audioSource==='microphone'" 
            controls 
            autoplay 
            :src="recorder.recording.url" 
            block>
         </audio>
         <v-progress-linear
               color="orange"
               v-if="recorder.processing"
               v-model="processPercent"
               height="35"
            >
               <strong>Processing: {{ Math.ceil(processPercent) }}%</strong>
         </v-progress-linear>

         <audio 
            class="audioPlayer" 
            v-if="fileLoaded && !loading && audioSource==='file'" 
            controls 
            autoplay 
            :src="audio.audioURL" 
            block>
         </audio>
         <v-progress-linear
               color="orange"
               v-if="loading && audioSource==='file'"
               indeterminate
               height="35"
            >
               <strong>Loading File</strong>
         </v-progress-linear>
         

         <canvas v-if="false" id="c"></canvas>
         <div class="overline" style="text-align:left;" v-if="audioSource==='microphone'">
            <v-switch v-model="postProcess" label="Post Process Audio"></v-switch>
            <span>
               All audio is encoded as MP3, which is an intensive operation; if you
               experience any trouble with quality, please select the post process
               option.
            </span>
         </div>

      </v-card-text>
   </v-card>
 
</div>
</template>
<script>

// import Encoder from './encoder'
import Recorder from './lameworker/recorder';
// import Worker from "./lameworker/lame.worker.js"
// import LameWorker from './lameworker'
import { convertTimeMMSS }  from './utils';

// const worker = new Worker();


export default {
   name: "AudioRecorder",
   props: {
      currentAudio: {
         required: false,
         type: String,
      }
   },
   data(){
      return {
         audioSource: "file",
         record: null,
         recording: false,
         selectedRecord: null,
         mediaRecorder: {},
         userFile: null,
         recordedAudio: {},
         mp3Audio: {},
         mp3Recording: [],
         recordingList: [],
         recordedAudios: [],
         audioURL: null,
         rawAudio: null,
         loading: false,
         fileLoaded: false,
         postProcess: false,
         processProgress: 0,
         audio: {
            audioFile: null,
            originalFileName: null,
            audioURL: null,
         },
         vueCanvas: null,
         canvasWidth: null,
         canvasHeight: null,
         attempts: 3,
         time: 3,
         isUploading   : false,
         recorder      : this._initRecorder(),
         // encoder       : this._initEncoder(),
         recordList    : [],
         selected      : {},
         uploadStatus  : null,
         
         mp3Blob: null,
         // encoder: new Encoder({}),

         rules: {
           maxAudioSize: value =>
           !value || value.size < 500000 || "Audio file must be under 500kb!"
         },
         // lamejs: new lamejs(),
      }
   },
   components: {
      // LameWorker
   },
    computed: {
      attemptsLeft () {
        return this.attempts - this.recordList.length
      },
      // isPause () {
      //   return this.recorder.isPause
      // },
      isRecording () {
        return this.recorder.isRecording
      },
      processing(){
         return this.recorder.processing;
      },
      processPercent(){
         return this.recorder.processPercent;
      },
      recordedTime () {
        if (this.time && this.recorder.duration >= this.time * 60) {
          this.stopRecorder()
        }
        return convertTimeMMSS(this.recorder.duration)
      },
      volume () {
        let volIn = parseFloat(this.recorder.volume)
        
      //   let volOut = Math.log((volIn + 1));
         // let volOut = Math.log(volIn + 1)
      //   console.log(volIn *150)
      //   this.drawWave(volIn * 100)
        return (volIn*750)
      },
      audioSelected(){
         if(this.recorder.recording.url){
            const audio = {
               audioFile: new File([this.recorder.recording.blob], "pronunciation.mp3"),
               audioURL: this.recorder.recording.url,
               originalFileName: "pronunciation.mp3",
            }
            this.$emit("selectAudio", audio)
            return true
         } else {
            this.$emit("selectAudio", null)
            return false
         }
      }
    },

   methods: {
      toggleRecorder () {
        if (!this.isRecording || (this.isRecording && this.isPause)) {
          this.recorder.start(this.postProcess)
        } else {
          this.recorder.pause()
        }
      },

      stopRecorder () {
        if (!this.isRecording) {
          return
        }
        this.recorder.stop()
      //   this.drawWave(this.recorder.volArray)
      },

      _initRecorder () {
        return new Recorder({
          beforeRecording : this.beforeRecording,
          afterRecording  : this.afterRecording,
          pauseRecording  : this.pauseRecording,
          micFailed       : this.micFailed
        })
      },

   
      drawWave(volumeArray) {
         const ctx = this.vueCanvas
         const width = this.canvasWidth;
         const height = this.canvasHeight;
         const midPoint = height/2;

         ctx.clearRect(0, 0, width, height);

         console.log("midpoint:", midPoint)
         const stepSize = width / volumeArray.length;
         ctx.beginPath();
         console.log("hello")
         ctx.moveTo(0,midPoint);
         ctx.lineWidth=2;
         for(let i = 0; i < volumeArray.length; i++){
            const vol = volumeArray[i]
            // ctx.lineTo((i*stepSize), vol + midPoint);
            // console.log(volumeArray[i])
            ctx.quadraticCurveTo((i*stepSize) - (stepSize/2), vol+midPoint, (i*stepSize), midPoint);
            ctx.stroke();
            ctx.quadraticCurveTo(i*stepSize, (-1*vol)+midPoint, (i*stepSize) + (stepSize/2), midPoint);
            ctx.stroke();
               // ctx.lineTo((i*stepSize) + (stepSize/2), (-1 * vol) + midPoint);
               // ctx.stroke();
         }
         // var midPoint = ctx.height / 2
      },

      // processAudio(){
      //    this.processing = true;
      //    // reconstitute Data:
      //    this.processProgress = 0;

      // },

      callback (data) {
        console.debug(data)
      },

      setAudio(newaudio) {
         this.loading = true;
         if (newaudio) {
            const file = newaudio;
            if (file.type.indexOf("audio/") === -1) {
               alert("Please select an audio file");
               this.userFile = null;
               return;
            } else {
               // console.log(newaudio)
               this.audio.audioFile = newaudio;
               this.audio.originalFileName = newaudio.name;
            }
            if (typeof FileReader === "function") {
               const reader = new FileReader();
               reader.onload = event => {
                  this.audio.audioURL = event.target.result;
                  this.loading = false;
                  this.fileLoaded = true;
               };
               reader.readAsDataURL(file);
            } else {
               alert("Sorry, FileReader API not supported");
            }
         } else {
            this.loading = false;
            this.audio = {};
         }
      },
      sayHello(){
         return "hello"
      }


   },
   mounted() {
      if(this.currentAudio){
         this.audio.audioBits = this.currentAudio;
      }
      // var c = document.getElementById("c");
      // this.canvasWidth = c.width;
      // this.canvasHeight = c.height;
      // var ctx = c.getContext("2d");    
      // this.vueCanvas = ctx;
      
   },
   beforeDestroy () {
      this.stopRecorder()
    },
};

</script>
<style lang="scss" scoped>

$primary: #FF3D7F;
$secondary: #3FB8AF;
$size: 75px;

audio {
    /* filter: sepia(20%) saturate(70%) grayscale(1) contrast(99%) invert(12%) drop-shadow(3px 3px 3px orange); */
    /* filter: drop-shadow(2px 2px 2px orange); */
    width: 100%;
    height: 50px;
}
/* https://chromium.googlesource.com/chromium/blink/+/72fef91ac1ef679207f51def8133b336a6f6588f/Source/core/css/mediaControls.css?autodive=0%2F%2F%2F */
audio::-webkit-media-controls-panel {
    display: flex;
    flex-direction: row;
    align-items: center;
    /* We use flex-start here to ensure that the play button is visible even
     * if we are too small to show all controls.
     */
    justify-content: flex-start;
    -webkit-user-select: none;
    position: relative;
    z-index: 5;
    height: 50px;
    /* background-color: #DBD4C4; */
    background-color: rgba(219, 212, 196, 1.0);
    /* border-radius: 5px; */
    /* The duration is also specified in MediaControlElements.cpp and LayoutTests/media/media-controls.js */
    transition: opacity 0.3s;
}

#speech.btn {
  border: none;
  padding: 0;
  border-radius: 100%;
  width: $size;
  height: $size;
  font-size: 1.5em;
  color: #fff;
  padding: 0;
  margin: 0;
  background: $primary;
	position: relative;
  display: inline-block;
    line-height: 50px;
    text-align: center;
    white-space: nowrap;
    vertical-align: middle;
    -ms-touch-action: manipulation;
    touch-action: manipulation;
    cursor: pointer;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    background-image: none;
}

.recordingButton {
	background: red;
	border-radius: 50%;
	// margin: 10px;
	// height: 20px;
	// width: 20px;

	// box-shadow: 0 0 0 0 rgba(0, 0, 0, 1);
	// transform: scale(1);
	animation: pulse 0.75s infinite;
}

@keyframes pulse {
	0% {
		// transform: scale(1);
		box-shadow: 0 0 0 0px rgba(255, 0, 0, 0.3);
	}

   100% {
		// transform: scale(0.85);
		box-shadow: 0 0 0 25px rgba(255, 0, 0, 0);
	}
}

</style>
