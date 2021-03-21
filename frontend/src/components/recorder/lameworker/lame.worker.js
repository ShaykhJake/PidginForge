import Encoder from "./encoder.js";

const encoder = new Encoder({});

self.addEventListener("message", ({ data }) => {
  if (data.calltype === "liveProcess") {
    const rawData = data.rawData;
    encoder.encode(rawData);
  } else if (data.calltype === "postProcess") {
    // console.log("hello")
    // const result = encoder.finish()
    const rawData = data.rawData;
    const frameCount = rawData.length;
    // console.log("hello")
    for (let i = 0; i < frameCount; i++) {
      const progress = (100 / (frameCount + 1)) * i;
      const response = {
        restype: "progress",
        processPercent: progress
      };
      // console.log(progress)
      self.postMessage(response);
      const newChunk = new Float32Array(rawData[i]);
      encoder.encode(newChunk);
    }
    const result = encoder.finish();
    const response = {
      restype: "finished",
      message: "Finished processing MP3",
      result: result
    };
    self.postMessage(response);
  } else if (data.calltype === "finishLive") {
    // encoder.encode(data)
    // console.log("finishing")
    const result = encoder.finish();
    // console.log(result)
    const response = {
      restype: "finished",
      message: "Finished processing MP3",
      result: result
    };
    self.postMessage(response);

    // self.postMessage({result});
  } else {
    self.postMessage({ message: "error" });
  }
});
