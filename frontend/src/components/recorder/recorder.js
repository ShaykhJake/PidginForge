// import Encoder from './encoder'
import { convertTimeMMSS } from "./utils";
// import Worker from "./lameworker/lame.worker.js"
// const worker = new Worker()

export default class {
  constructor(options = {}) {
    this.beforeRecording = options.beforeRecording;
    this.pauseRecording = options.pauseRecording;
    this.afterRecording = options.afterRecording;
    this.micFailed = options.micFailed;

    this.bufferSize = 1024;
    this.records = [];
    this.soundChunks = [];
    this.recording = {};

    this.postProcess = false;
    this.processsing = false;

    this.isPause = false;
    this.isRecording = false;

    this.duration = 0;
    this.volume = 0;
    this.returnBuffer = [];
    this.waveArray = [];
    this._duration = 0;
  }

  start(postProcess) {
    const constraints = {
      video: false,
      audio: {
        channelCount: 1,
        echoCancellation: false
      }
    };

    this.waveArray = [];
    this.postProcess = postProcess;
    this.returnBuffer = [];
    // this.lameEncoder = new Encoder({postProcess: this.postProcess})

    this.beforeRecording && this.beforeRecording("start recording");

    navigator.mediaDevices
      .getUserMedia(constraints)
      .then(this._micCaptured.bind(this))
      .catch(this._micError.bind(this));
    this.isPause = false;
  }

  stop() {
    this.isRecording = false;
    this.isPause = false;
    this.processsing = true;
    this.stream.getTracks().forEach(track => track.stop());
    this.input.disconnect();
    this.processor.disconnect();
    this.context.close();

    // if(this.postProcess){
    //   this.recording = this.lameEncoder.finishPostProcess()
    // } else {
    //   this.recording = this.lameEncoder.finish()
    // }

    // // post processing attempt
    // console.log(this.soundChunks.length)
    // console.log(this.soundChunks)
    // for(let i = 0; i < this.soundChunks.length; i++){
    //   console.log(this.soundChunks[i])
    //   this.lameEncoder.encode(this.soundChunks[i]);
    // }
    // const record = this.lameEncoder.finish()
    // this.lameEncoder = new Encoder({})

    // const record = this.lameEncoder.encodeStep2()
    // this.soundChunks = []

    // original for streamed processing:
    // const record = this.lameEncoder.finish()

    this.recording.duration = convertTimeMMSS(this.duration);

    // this.records.push(record)
    // this.recording = record
    const record = "";

    this._duration = 0;
    this.duration = 0;
    this.afterRecording && this.afterRecording(record);
    this.processsing = false;
    return this.returnBuffer;
  }

  pause() {
    this.stream.getTracks().forEach(track => track.stop());
    this.input.disconnect();
    this.processor.disconnect();
    this.context.close();

    this._duration = this.duration;
    this.isPause = true;

    this.pauseRecording && this.pauseRecording("pause recording");
  }

  recordList() {
    return this.records;
  }

  lastRecord() {
    return this.records.slice(-1);
  }

  _micCaptured(stream) {
    this.context = new (window.AudioContext || window.webkitAudioContext)({
      sampleRate: 48000
    });
    this.duration = this._duration;
    this.input = this.context.createMediaStreamSource(stream);
    this.processor = this.context.createScriptProcessor(this.bufferSize, 1, 1);
    this.stream = stream;
    this.analyzer = this.context.createAnalyser();

    this.isRecording = true;
    this.processor.onaudioprocess = ev => {
      const sample = ev.inputBuffer.getChannelData(0);
      let sum = 0.0;

      const sampleBuffer = new Float32Array(sample);
      // this.returnBuffer.push(data)
      worker.postMessage({ calltype: "encodeChunk", rawData: sampleBuffer });
      // if(this.postProcess){
      //   this.lameEncoder.encodeStep1(sample)
      //   console.log(sample);
      // } else {
      //   this.lameEncoder.encode(sample)
      // }

      for (let i = 0; i < sample.length; ++i) {
        sum += sample[i] * sample[i];
      }

      this.duration =
        parseFloat(this._duration) +
        parseFloat(this.context.currentTime.toFixed(2));
      // this.volume = Math.sqrt(sum / sample.length).toFixed(2)
      this.volume = Math.sqrt(sum / sample.length).toFixed(2);
      this.waveArray.push(this.volume * 500);
    };

    this.input.connect(this.processor);
    this.processor.connect(this.context.destination);
  }

  _micError(error) {
    this.micFailed && this.micFailed(error);
  }
}
