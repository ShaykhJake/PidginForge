import { Mp3Encoder } from "lamejs";

export default class {
  constructor(config) {
    this.postProcess = config.postProcess || false;
    this.bitRate = config.bitRate || 128;
    this.sampleRate = config.sampleRate || 48000;
    // this.sampleRate = config.sampleRate || 44100
    this.dataBuffer = [];
    this.sampleChunks = [];
    // this.postProcessProgress = 0
    this.encoder = new Mp3Encoder(1, this.sampleRate, this.bitRate);
  }

  // readBlobAsync(file) {
  //   return new Promise((resolve, reject) => {
  //     let reader = new FileReader();

  //     reader.onload = () => {
  //       resolve(reader.result);
  //     };

  //     reader.onerror = reject;

  //     reader.readAsArrayBuffer(file);
  //   })
  // }

  encodeStep1(arrayBuffer) {
    const samples = this._convertBuffer(arrayBuffer);
    this.sampleChunks.push(samples);
    // return samples
  }
  finishPostProcess() {
    for (let a = 0; a < this.sampleChunks.length; a++) {
      const maxSamples = 1152;
      let remaining = this.sampleChunks[a].length;

      for (let i = 0; remaining >= 0; i += maxSamples) {
        const left = this.sampleChunks[a].subarray(i, i + maxSamples);
        const buffer = this.encoder.encodeBuffer(left);
        this.dataBuffer.push(new Int8Array(buffer));
        remaining -= maxSamples;
      }
    }
    this.dataBuffer.push(this.encoder.flush());
    const blob = new Blob(this.dataBuffer, { type: "audio/mp3" });
    this.dataBuffer = [];

    return {
      id: Date.now(),
      blob: blob,
      url: URL.createObjectURL(blob)
    };
  }

  encode(arrayBuffer) {
    const maxSamples = 576;
    const samples = this._convertBuffer(arrayBuffer);
    let remaining = samples.length;

    for (let i = 0; remaining >= 0; i += maxSamples) {
      const left = samples.subarray(i, i + maxSamples);
      const buffer = this.encoder.encodeBuffer(left);
      this.dataBuffer.push(new Int8Array(buffer));
      remaining -= maxSamples;
    }
  }

  finish() {
    this.dataBuffer.push(this.encoder.flush());
    const blob = new Blob(this.dataBuffer, { type: "audio/mp3" });
    this.dataBuffer = [];

    return {
      id: Date.now(),
      blob: blob,
      url: URL.createObjectURL(blob)
    };
  }

  _floatTo16BitPCM(input, output) {
    for (let i = 0; i < input.length; i++) {
      const s = Math.max(-1, Math.min(1, input[i]));
      output[i] = s < 0 ? s * 0x8000 : s * 0x7fff;
    }
  }

  _convertBuffer(arrayBuffer) {
    const data = new Float32Array(arrayBuffer);
    const out = new Int16Array(arrayBuffer.length);
    this._floatTo16BitPCM(data, out);
    return out;
  }
}
