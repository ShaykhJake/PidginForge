// import Encoder from './encoder'
import { convertTimeMMSS } from './utils'
import Worker from "./lame.worker.js"
const lameEncoder = new Worker()

export default class {
  constructor (options = {}) {
    this.beforeRecording = options.beforeRecording
    this.pauseRecording  = options.pauseRecording
    this.afterRecording  = options.afterRecording
    this.micFailed       = options.micFailed

    this.bufferSize = 4096
    this.records    = []
    this.soundChunks = []
    this.processPercent = 0
    this.recording = {}
    
    this.isPause     = false
    this.isRecording = false
    this.processing = false

    this.duration = 0
    this.volume   = 0
    this.returnBuffer = []
    this.volArray = []
    this._duration = 0
  }

  start (postProcess) {
    this.soundChunks = []
    this.recording = {}
    this.postProcess = postProcess
    const constraints = {
      video: false,
      audio: {
        channelCount: 1,
        echoCancellation: false
      }
    }

    lameEncoder.onmessage = (data) => {
      //   this.mp3Blob = data.result
        if(data.data.restype==='finished'){

          this.recording = data.data.result
          // console.log(this.recording)
          this.processing = false;
        } else if (data.data.restype==='progress'){
          // console.log(data.data.processPercent)
          this.processPercent = data.data.processPercent
        } else {
          console.log(`Unexpected data: ${data}`)
        }
    };

    this.volArray = []
    this.returnBuffer = []
    
    this.beforeRecording && this.beforeRecording('start recording')

    navigator.mediaDevices
             .getUserMedia(constraints)
             .then(this._micCaptured.bind(this))
             .catch(this._micError.bind(this))
    this.isPause = false
  }

  stop () {
    this.isRecording = false
    this.isPause     = false
    this.stream.getTracks().forEach((track) => track.stop())
    this.input.disconnect()
    this.processor.disconnect()
    this.context.close()


    if(this.postProcess){
      this.processPercent = 0
      this.processing = true;
      lameEncoder.postMessage({calltype: "postProcess", rawData: this.soundChunks});
    } else {
      lameEncoder.postMessage({calltype: "finishLive"});
    }
    
    this.recording.duration = convertTimeMMSS(this.duration)
    
    // this.records.push(record)
    // this.recording = record
    const record = ""
    
    this._duration = 0
    this.duration  = 0
    this.afterRecording && this.afterRecording(record)
    return this.returnBuffer
  }

  pause () {
    this.stream.getTracks().forEach((track) => track.stop())
    this.input.disconnect()
    this.processor.disconnect()
    this.context.close()

    this._duration = this.duration
    this.isPause = true

    this.pauseRecording && this.pauseRecording('pause recording')
  }

  recordList () {
    return this.records
  }

  lastRecord () {
    return this.records.slice(-1)
  }

  _micCaptured (stream) {
    this.context    = new(window.AudioContext || window.webkitAudioContext)({ sampleRate: 48000})
    this.duration   = this._duration
    this.input      = this.context.createMediaStreamSource(stream)
    this.processor  = this.context.createScriptProcessor(this.bufferSize, 1, 1)
    this.stream     = stream
    this.analyzer   = this.context.createAnalyser();
    
    this.isRecording = true
    this.processor.onaudioprocess = (ev) => {
      const sample = ev.inputBuffer.getChannelData(0)
      let sum = 0.0

      const sampleArray = new Float32Array(sample)
      if(this.postProcess){
        this.soundChunks.push(sampleArray)
      } else {
        lameEncoder.postMessage({calltype: "liveProcess", rawData: sampleArray});
      }
      
      for (let i = 0; i < sample.length; ++i) {
        sum += sample[i] * sample[i]
      }

      this.duration = parseFloat(this._duration) + parseFloat(this.context.currentTime.toFixed(2))
      // this.volume = Math.sqrt(sum / sample.length).toFixed(2)
      this.volume = Math.sqrt(sum / sample.length).toFixed(2)
      this.volArray.push(this.volume * 500)
    }

    this.input.connect(this.processor)
    this.processor.connect(this.context.destination)
  }

  _micError (error) {
    this.micFailed && this.micFailed(error)
  }
}
